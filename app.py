from flask import Flask, request, jsonify, render_template
import pandas as pd
import nltk
import spacy
import string
from nltk.corpus import wordnet
from sentence_transformers import SentenceTransformer, util

# Initialize Flask app
app = Flask(__name__)

# Download necessary resources
nltk.download("punkt")
nltk.download("wordnet")
nlp = spacy.load("en_core_web_sm")  # Load spaCy's English model

# Load dataset
file_path = "skin_problems_QA.csv"
df = pd.read_csv(file_path)
df.columns = ["question", "answer"]
df.dropna(inplace=True)  # Remove null values

# Load BERT-based Sentence Transformer for Semantic Similarity
model = SentenceTransformer("all-MiniLM-L6-v2")

# Text Preprocessing Function
def preprocess_text(text):
    text = text.lower().strip()  # Convert to lowercase
    text = text.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation
    return text

# Apply preprocessing
df["cleaned_question"] = df["question"].apply(preprocess_text)

# Generate BERT embeddings for all questions
question_embeddings = model.encode(df["cleaned_question"].tolist(), convert_to_tensor=True)

# Named Entity Recognition (NER) for extracting skin-related terms
def extract_skin_terms(text):
    doc = nlp(text)
    extracted_terms = [ent.text.lower() for ent in doc.ents]  # Extract entities
    return extracted_terms

# Generate synonyms using WordNet
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower().replace("_", " "))  # Replace underscores
    return list(synonyms)

# Function to find the best matching answer + related questions
def get_answer(user_question):
    user_question = preprocess_text(user_question)

    # Extract key terms using NER
    extracted_terms = extract_skin_terms(user_question)

    # Expand question with synonyms (if available)
    expanded_question = user_question
    if extracted_terms:
        for term in extracted_terms:
            synonyms = get_synonyms(term)
            if synonyms:
                expanded_question += " " + " ".join(synonyms)

    # Convert user question to BERT embedding
    user_embedding = model.encode(expanded_question, convert_to_tensor=True)

    # Compute cosine similarity with stored questions
    similarities = util.pytorch_cos_sim(user_embedding, question_embeddings)[0]

    # Get the best match index
    best_match_index = similarities.argmax().item()
    confidence_score = similarities[best_match_index].item()

    # If confidence is too low, return a fallback response
    if confidence_score < 0.5:
        return {
            "answer": "I'm not sure about that. Could you provide more details or consult a dermatologist?",
            "related_questions": []
        }

    # Get the best-matching answer
    best_answer = df.iloc[best_match_index]["answer"]

    # Get top 3 most similar questions (excluding the top match)
    related_indices = similarities.argsort(descending=True)[1:4].tolist()  # Convert to list
    related_questions = [
        df.iloc[int(i)]["question"] for i in related_indices if similarities[i] > 0.5
    ]  # Only include related questions with a similarity score > 0.5

    return {
        "answer": best_answer,
        "related_questions": related_questions
    }

# Route to serve frontend
@app.route("/")
def home():
    return render_template("index.html")  # Ensure index.html is inside the "templates" folder

# API route to handle user queries
@app.route("/ask", methods=["GET"])
def ask():
    user_question = request.args.get("question", "")
    if not user_question:
        return jsonify({"answer": "Please enter a valid question!", "related_questions": []})

    response = get_answer(user_question)
    return jsonify(response)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
