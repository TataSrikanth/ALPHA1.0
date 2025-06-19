from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import nltk
import spacy
import string
from nltk.corpus import wordnet
from sentence_transformers import SentenceTransformer, util
from werkzeug.security import generate_password_hash
print(generate_password_hash("admin123"))


# ---------------- Flask App Setup ----------------
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# ---------------- Database Connection ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chatbot_db"
)
cursor = db.cursor(dictionary=True)

# ---------------- NLP & Dataset Setup ----------------
nltk.download("punkt")
nltk.download("wordnet")
nlp = spacy.load("en_core_web_sm")

df = pd.read_csv("skin_problems_QA.csv")
df.columns = ["question", "answer", "cleaned_question"]
df.dropna(inplace=True)
df["cleaned_question"] = df["question"].apply(lambda text: text.lower().strip().translate(str.maketrans("", "", string.punctuation)))

model = SentenceTransformer("all-MiniLM-L6-v2")
question_embeddings = model.encode(df["cleaned_question"].tolist(), convert_to_tensor=True)

def extract_skin_terms(text):
    doc = nlp(text)
    return [ent.text.lower() for ent in doc.ents]

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower().replace("_", " "))
    return list(synonyms)

def get_answer(user_question):
    user_question = user_question.lower().strip().translate(str.maketrans("", "", string.punctuation))
    extracted_terms = extract_skin_terms(user_question)
    expanded_question = user_question
    if extracted_terms:
        for term in extracted_terms:
            synonyms = get_synonyms(term)
            if synonyms:
                expanded_question += " " + " ".join(synonyms)

    user_embedding = model.encode(expanded_question, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(user_embedding, question_embeddings)[0]
    best_match_index = similarities.argmax().item()
    confidence_score = similarities[best_match_index].item()

    if confidence_score < 0.5:
        return {
            "answer": "I'm not sure about that. Could you provide more details or consult a dermatologist?",
            "related_questions": []
        }

    best_answer = df.iloc[best_match_index]["answer"]
    related_indices = similarities.argsort(descending=True)[1:4].tolist()
    related_questions = [
        df.iloc[int(i)]["question"] for i in related_indices if similarities[i] > 0.5
    ]
    return {
        "answer": best_answer,
        "related_questions": related_questions
    }

# ---------------- Routes ----------------

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            db.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], password_input):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('user_dashboard'))
        else:
            flash("Invalid username or password.")
    return render_template('login.html')

@app.route('/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/ask', methods=['GET'])
def ask():
    if 'user_id' not in session:
        return jsonify({"answer": "Please log in first!", "related_questions": []})

    user_question = request.args.get("question", "")
    if not user_question:
        return jsonify({"answer": "Please enter a valid question!", "related_questions": []})

    result = get_answer(user_question)

    cursor.execute("INSERT INTO chat_history (user_id, question, answer) VALUES (%s, %s, %s)",
                   (session['user_id'], user_question, result['answer']))
    db.commit()
    return jsonify(result)

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cursor.execute("SELECT question, answer, timestamp FROM chat_history WHERE user_id=%s ORDER BY timestamp DESC", (session['user_id'],))
    chats = cursor.fetchall()
    return render_template('history.html', chats=chats)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

# ---------------- Admin Routes ----------------

# ---------------- Admin Routes ----------------

from flask import send_file
import io
import csv

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        cursor.execute("SELECT * FROM admins WHERE username=%s", (username,))
        admin = cursor.fetchone()

        if admin and admin['password'] == password_input:
            session['admin'] = admin['id']
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid admin credentials.")
    return render_template('admin_login.html')


@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    # Pagination
    per_page = 5
    current_page = int(request.args.get("page", 1))
    offset = (current_page - 1) * per_page

    cursor.execute("SELECT COUNT(*) AS total FROM users")
    total_users = cursor.fetchone()['total']
    total_pages = (total_users + per_page - 1) // per_page

    cursor.execute("SELECT id, username, email, is_blocked FROM users LIMIT %s OFFSET %s", (per_page, offset))
    users_to_display = cursor.fetchall()

    cursor.execute("SELECT * FROM chat_history ORDER BY timestamp DESC LIMIT 10")
    chats = cursor.fetchall()

    return render_template(
        'admin_dashboard.html',
        users=users_to_display,
        chats=chats,
        total_pages=total_pages,
        current_page=current_page
    )


@app.route('/admin/block_user/<int:user_id>', methods=['POST'])
def block_user(user_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    cursor.execute("UPDATE users SET is_blocked = 1 WHERE id = %s", (user_id,))
    db.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/unblock_user/<int:user_id>', methods=['POST'])
def unblock_user(user_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    cursor.execute("UPDATE users SET is_blocked = 0 WHERE id = %s", (user_id,))
    db.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_password = request.form['new_password']

        if new_password:
            hashed_password = generate_password_hash(new_password)
            cursor.execute("UPDATE users SET username=%s, email=%s, password=%s WHERE id=%s",
                           (username, email, hashed_password, user_id))
        else:
            cursor.execute("UPDATE users SET username=%s, email=%s WHERE id=%s",
                           (username, email, user_id))
        db.commit()
        flash('User updated successfully.')
        return redirect(url_for('admin_dashboard'))

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    return render_template('edit_user.html', user=user)




@app.route('/admin/qa', methods=['GET', 'POST'])
def manage_qa():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        cleaned_q = question.lower().translate(str.maketrans("", "", string.punctuation))
        df.loc[len(df)] = [question, answer, cleaned_q]
        df.to_csv("skin_problems_QA.csv", index=False)
        flash("New Q&A added successfully.")

    qa_records = df[["question", "answer"]].copy()
    qa_records["row_index"] = df.index  # ✅ Include the real index
    return render_template("admin_qa.html", qa_list=qa_records.to_dict(orient="records"))



@app.route('/admin/delete_qa/<int:index>', methods=['POST'])
def delete_qa(index):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    df.drop(index, inplace=True)
    df.to_csv("skin_problems_QA.csv", index=False)
    flash("Q&A deleted.")
    return redirect(url_for('manage_qa'))



@app.route('/admin/export_chats')
def export_chats():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cursor.execute("SELECT * FROM chat_history ORDER BY timestamp DESC")
    chats = cursor.fetchall()

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=chats[0].keys())
    writer.writeheader()
    writer.writerows(chats)

    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype="text/csv", as_attachment=True, download_name="chat_logs.csv")

@app.route('/admin/stats')
def admin_stats():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    # Total users
    cursor.execute("SELECT COUNT(*) AS user_count FROM users")
    user_count = cursor.fetchone()["user_count"]

    # Total chats
    cursor.execute("SELECT COUNT(*) AS chat_count FROM chat_history")
    chat_count = cursor.fetchone()["chat_count"]

    # Last chat timestamp
    cursor.execute("SELECT MAX(timestamp) AS last_chat FROM chat_history")
    last_chat = cursor.fetchone()["last_chat"]

    # Line chart: Chats per day
    cursor.execute("""
        SELECT DATE(timestamp) as date, COUNT(*) as count
        FROM chat_history
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp)
    """)
    daily_data = cursor.fetchall()
    chat_dates = [row["date"].strftime('%Y-%m-%d') for row in daily_data]
    chat_counts = [row["count"] for row in daily_data]

    # Pie chart: Top 5 most active users
    cursor.execute("""
        SELECT u.username, COUNT(c.id) AS total
        FROM users u
        JOIN chat_history c ON u.id = c.user_id
        GROUP BY u.username
        ORDER BY total DESC
        LIMIT 5
    """)
    active_users = cursor.fetchall()
    user_labels = [row["username"] for row in active_users]
    user_chat_counts = [row["total"] for row in active_users]

    return render_template(
        "admin_stats.html",
        user_count=user_count,
        chat_count=chat_count,
        last_chat=last_chat,
        chat_dates=chat_dates,
        chat_counts=chat_counts,
        user_labels=user_labels,
        user_chat_counts=user_chat_counts
    )




@app.route('/admin/user/<int:user_id>/history')
def admin_user_history(user_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cursor.execute("SELECT username FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    cursor.execute("SELECT question, answer, timestamp FROM chat_history WHERE user_id=%s ORDER BY timestamp DESC", (user_id,))
    chats = cursor.fetchall()

    return render_template("admin_user_history.html", username=user['username'], chats=chats)


@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cursor.execute("DELETE FROM chat_history WHERE user_id=%s", (user_id,))
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.commit()

    flash("User and their history deleted successfully.")
    return redirect(url_for('admin_dashboard'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()

    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        new_password = request.form['new_password']

        if new_password:
            hashed_password = generate_password_hash(new_password)
            cursor.execute("UPDATE users SET username=%s, email=%s, password=%s WHERE id=%s",
                           (new_username, new_email, hashed_password, session['user_id']))
        else:
            cursor.execute("UPDATE users SET username=%s, email=%s WHERE id=%s",
                           (new_username, new_email, session['user_id']))
        db.commit()
        flash('Profile updated successfully.')
        session['username'] = new_username
        return redirect(url_for('profile'))

    return render_template("profile.html", user=user)


# ----------------- Manage User Routes (Separate for Clarity) -----------------

@app.route('/admin/users')
def user_management():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cursor.execute("SELECT id, username, email, is_blocked FROM users")
    users = cursor.fetchall()
    return render_template("user.html", users=users)


@app.route('/admin/users/edit/<int:user_id>', methods=['POST'])
def user_edit(user_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    username = request.form['username']
    email = request.form['email']
    new_password = request.form['new_password']

    if new_password:
        hashed_password = generate_password_hash(new_password)
        cursor.execute("UPDATE users SET username=%s, email=%s, password=%s WHERE id=%s",
                       (username, email, hashed_password, user_id))
    else:
        cursor.execute("UPDATE users SET username=%s, email=%s WHERE id=%s",
                       (username, email, user_id))
    db.commit()
    flash("User updated successfully.")
    return redirect(url_for('user_management'))


@app.route('/admin/users/block/<int:user_id>', methods=['POST'])
def user_block(user_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    cursor.execute("UPDATE users SET is_blocked = 1 WHERE id=%s", (user_id,))
    db.commit()
    flash("User blocked.")
    return redirect(url_for('user_management'))


@app.route('/admin/users/unblock/<int:user_id>', methods=['POST'])
def user_unblock(user_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    cursor.execute("UPDATE users SET is_blocked = 0 WHERE id=%s", (user_id,))
    db.commit()
    flash("User unblocked.")
    return redirect(url_for('user_management'))


@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
def user_delete(user_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cursor.execute("DELETE FROM chat_history WHERE user_id=%s", (user_id,))
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.commit()
    flash("User and history deleted.")
    return redirect(url_for('user_management'))





# ---------------- Run App ----------------

if __name__ == "__main__":
    app.run(debug=True)
