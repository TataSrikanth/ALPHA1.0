-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 19, 2025 at 06:18 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `chatbot_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `username`, `password`) VALUES
(6, 'admin', 'admin123');

-- --------------------------------------------------------

--
-- Table structure for table `chat_history`
--

CREATE TABLE `chat_history` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `question` text DEFAULT NULL,
  `answer` text DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `chat_history`
--

INSERT INTO `chat_history` (`id`, `user_id`, `question`, `answer`, `timestamp`) VALUES
(1, 1, 'can you explain incomplete right bundle branch block?', 'Echo: can you explain incomplete right bundle branch block?', '2025-06-16 05:09:18'),
(2, 1, 'dry skin', 'Echo: dry skin', '2025-06-16 05:09:26'),
(3, 1, 'dry skin', 'Echo: dry skin', '2025-06-16 05:09:29'),
(4, 1, 'dry skin', 'Echo: dry skin', '2025-06-16 05:11:14'),
(5, 1, 'dry skin', 'Echo: dry skin', '2025-06-16 05:14:16'),
(6, 1, 'dry skin', 'Echo: dry skin', '2025-06-16 05:14:16'),
(7, 1, 'dry skin', 'Echo: dry skin', '2025-06-18 06:24:08'),
(8, 1, 'dry skin', 'Moisturizing regularly and using gentle, hydrating cleansers can help treat dry skin.', '2025-06-18 06:31:41'),
(9, 1, 'dry skin', 'Moisturizing regularly and using gentle, hydrating cleansers can help treat dry skin.', '2025-06-18 06:31:57'),
(10, 2, 'dry skin', 'Moisturizing regularly and using gentle, hydrating cleansers can help treat dry skin.', '2025-06-18 06:32:13'),
(11, 2, 'dry skin', 'Moisturizing regularly and using gentle, hydrating cleansers can help treat dry skin.', '2025-06-19 01:57:19'),
(12, 2, 'oily skin', 'Using oil-free cleansers and blotting papers can help manage oily skin.', '2025-06-19 02:05:46'),
(13, 2, 'oily skin', 'Using oil-free cleansers and blotting papers can help manage oily skin.', '2025-06-19 02:06:01'),
(14, 2, 'oily skin', 'Using oil-free cleansers and blotting papers can help manage oily skin.', '2025-06-19 02:09:37'),
(15, 2, 'How can I treat dry skin?', 'Moisturizing regularly and using gentle, hydrating cleansers can help treat dry skin.', '2025-06-19 02:09:39'),
(16, 2, 'Can coconut oil help with dry skin?', 'Coconut oil helps moisturize dry skin and reduce inflammation.', '2025-06-19 02:09:41'),
(17, 2, 'How can I reduce oily skin?', 'Using oil-free cleansers and blotting papers can help manage oily skin.', '2025-06-19 02:09:44'),
(18, 2, 'oily skin', 'Using oil-free cleansers and blotting papers can help manage oily skin.', '2025-06-19 02:11:01'),
(19, 2, 'What is the best body lotion for dry skin?', 'For dry skin, use lotions with shea butter, ceramides, and glycerin.', '2025-06-19 02:11:05'),
(20, 2, 'How can I treat dry skin?', 'Moisturizing regularly and using gentle, hydrating cleansers can help treat dry skin.', '2025-06-19 02:11:13'),
(21, 2, 'What is the best body lotion for dry skin?', 'For dry skin, use lotions with shea butter, ceramides, and glycerin.', '2025-06-19 02:11:20'),
(22, 2, 'Can coconut oil help with dry skin?', 'Coconut oil helps moisturize dry skin and reduce inflammation.', '2025-06-19 02:11:26'),
(23, 2, 'What is the best body lotion for dry skin?', 'For dry skin, use lotions with shea butter, ceramides, and glycerin.', '2025-06-19 02:11:27'),
(24, 2, 'How can I treat dry skin?', 'Moisturizing regularly and using gentle, hydrating cleansers can help treat dry skin.', '2025-06-19 02:11:29'),
(25, 2, 'oily skin', 'Using oil-free cleansers and blotting papers can help manage oily skin.', '2025-06-19 02:12:51'),
(26, 2, 'What is the best body lotion for dry skin?', 'For dry skin, use lotions with shea butter, ceramides, and glycerin.', '2025-06-19 02:12:54'),
(27, 2, 'How can I treat dry skin?', 'Moisturizing regularly and using gentle, hydrating cleansers can help treat dry skin.', '2025-06-19 02:12:56'),
(28, 3, 'dry skin', 'Moisturizing regularly and using gentle, hydrating cleansers can help treat dry skin.', '2025-06-19 03:09:47'),
(29, 4, 'Yeast infection with open sores and swelling—why isn’t my medication working?', 'Fungal skin infections can be treated with antifungal creams and keeping the skin dry.', '2025-06-19 03:10:20'),
(30, 6, 'what is ai?', 'I\'m not sure about that. Could you provide more details or consult a dermatologist?', '2025-06-19 03:11:15'),
(31, 6, 'acne', 'Acne is caused by clogged pores due to excess oil, bacteria, and dead skin cells.', '2025-06-19 03:30:18'),
(32, 6, 'Can dairy cause acne?', 'Dairy may contribute to acne due to hormonal effects in milk.', '2025-06-19 03:30:23'),
(33, 6, 'What causes acne?', 'Acne is caused by clogged pores due to excess oil, bacteria, and dead skin cells.', '2025-06-19 03:30:25'),
(34, 6, 'Why do I get pimples on my back?', 'Back acne can be treated with exfoliation and anti-acne body washes.', '2025-06-19 03:30:30'),
(35, 6, 'acne', 'Acne is caused by clogged pores due to excess oil, bacteria, and dead skin cells.', '2025-06-19 03:36:40'),
(36, 6, 'What is the best skincare routine for acne?', 'Acne skincare should include gentle cleansers, exfoliation, and non-comedogenic products.', '2025-06-19 03:36:43'),
(37, 6, 'What is the best skincare routine for acne?', 'Acne skincare should include gentle cleansers, exfoliation, and non-comedogenic products.', '2025-06-19 03:36:43'),
(38, 6, 'What is the best way to treat acne scars?', 'Acne scars can be treated with microneedling, laser therapy, or retinol.', '2025-06-19 03:36:46'),
(39, 6, 'How can I remove acne scars?', 'Acne scars can be reduced with treatments like retinoids, chemical peels, and laser therapy.', '2025-06-19 03:36:47'),
(40, 6, 'How do I fade scars naturally?', 'Natural scar fading remedies include aloe vera, honey, and lemon juice.', '2025-06-19 03:36:48'),
(41, 6, 'How can I make my skin glow naturally?', 'For naturally glowing skin, eat a healthy diet and stay hydrated.', '2025-06-19 03:36:49');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_blocked` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `is_blocked`) VALUES
(1, 'jitesh', 'santosh@gmail.com', 'scrypt:32768:8:1$lLL7DRn9VWr2gkJe$4d837d5a2d7bd351b336e798c80761072885c10690d43ef6595291be5b9331bb0ac8be09827882f2e23b77c55ac83e1e87ab49c0c1b572e19571b7014b5005b0', 0),
(2, 'yanhavi', 'shelkevishal9920@gmail.com', 'scrypt:32768:8:1$UwKTBlreCte32hip$81cf1fa30e8eb7069cc5e1ed688bb7bc1542c57e2350143714e1b1343bee4b9366bb54ea242b45f1fac4d32dc019fae7235e4aa9ab70ae8e626dfabc190525f9', 0),
(3, 'sam', 'sam@gmail.com', 'scrypt:32768:8:1$zNS9PubzvBBg5j8f$9d49f712c29cf907d626ed98e4b6a07dd40fe836281e5e284b5effc7eddec6b4e026a3e551cc83b4e1b17163f1928bb4cb6c2c29d38829f6470f36d6c6a806a7', 0),
(4, 'ram', 'ram@gmail.com', 'scrypt:32768:8:1$FvQLLpNN32sANABJ$44148bc50584084d8731449e307766ab5be547f0978fea2306b0797e40ec1d343482f2024f0287a818905e283af339b03a882635a6c5ff4bc10a0db04927eb12', 0),
(5, 'sham', 'sham@gmail.com', 'scrypt:32768:8:1$E7jFL7f1KNDSx1qE$d005517bfc6bbcff9bff4b2d2616141814939b02da9a00b8ecfde089a4a5e94405be8e17594613c7c71e678b6f752e18a8c7222eb321403564800efaf6b6b9e6', 0),
(6, 'sima', 'sima@gmail.com', 'scrypt:32768:8:1$Lfm12ghrZllBsutT$23a948c274e02d88c2cb3b640095a2a0e32e304e1fabf8920f9fed4c2524d92f6e8f374a4499a63ebbbfeb35c1631df9fd0470dbe3057e1797803b56fb87d514', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `chat_history`
--
ALTER TABLE `chat_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `chat_history`
--
ALTER TABLE `chat_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `chat_history`
--
ALTER TABLE `chat_history`
  ADD CONSTRAINT `chat_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
