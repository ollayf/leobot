-- MySQL dump 10.13  Distrib 8.0.22, for Linux (x86_64)
--
-- Host: localhost    Database: leobot_2
-- ------------------------------------------------------
-- Server version	8.0.22-0ubuntu0.20.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `parent_id` int DEFAULT NULL,
  `name` text,
  `description` longtext,
  `tag` bit(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_id_parent` (`parent_id`),
  CONSTRAINT `fk_id_parent` FOREIGN KEY (`parent_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,NULL,NULL,NULL,NULL),(2,NULL,'Testimony','Heartfelt personal sharing',_binary '\0'),(3,NULL,'potato',NULL,_binary ''),(4,NULL,'beans',NULL,_binary ''),(5,NULL,'scrabble',NULL,_binary ''),(6,NULL,'egg',NULL,_binary ''),(7,NULL,'another_egg',NULL,_binary ''),(8,NULL,'Tag1',NULL,_binary ''),(9,NULL,'Tag2',NULL,_binary ''),(10,NULL,'Eggs',NULL,_binary '');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `msg_id` int DEFAULT NULL,
  `thread_id` int DEFAULT NULL,
  `author_id` int DEFAULT NULL,
  `msg` longtext,
  `post_dt` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_comment_threads` (`thread_id`),
  KEY `fk_comment_users` (`author_id`),
  CONSTRAINT `fk_comment_threads` FOREIGN KEY (`thread_id`) REFERENCES `threads` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_comment_users` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `id` int NOT NULL AUTO_INCREMENT,
  `author_id` int DEFAULT NULL,
  `msg` longtext,
  `reply` longtext,
  `resolved_dt` datetime DEFAULT NULL,
  `title` text,
  `file_id` varchar(2000) DEFAULT NULL,
  `file_type` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_feedback_users` (`author_id`),
  CONSTRAINT `fk_feedback_users` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (1,1,'Beans',NULL,NULL,'Potato',NULL,NULL),(3,1,'Beans',NULL,NULL,'Title','AgACAgUAAxkBAAIGtV-f2jezkDBU0CXRNY6IX7mFlzxTAALsqjEbuM7AVBzQdw7-C2djc3nra3QAAwEAAwIAA3kAAzXGBQABHgQ','<class \'telegram.files.photosize.PhotoSize\'>'),(4,1,'Blah ndkwkw\nShown\nWhuwnwnww',NULL,NULL,'Cars 2','AgACAgUAAxkBAAIHLF-gD4R0Fs9wgjVSVMEuzSMz2rtoAALsqjEbuM7AVBzQdw7-C2djc3nra3QAAwEAAwIAA3kAAzXGBQABHgQ','<class \'telegram.files.photosize.PhotoSize\'>');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `functions`
--

DROP TABLE IF EXISTS `functions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `functions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(2000) DEFAULT NULL,
  `description` longtext,
  `permissions_id` int DEFAULT NULL,
  `sleep_menu` bit(1) DEFAULT b'0',
  `start_menu` bit(1) DEFAULT b'0',
  `admin_menu` bit(1) DEFAULT b'0',
  `backend` bit(1) DEFAULT b'0',
  `all_menu` bit(1) DEFAULT b'0',
  `in_action` bit(1) DEFAULT b'0',
  PRIMARY KEY (`id`),
  KEY `fk_functions_permissions` (`permissions_id`),
  CONSTRAINT `fk_functions_permissions` FOREIGN KEY (`permissions_id`) REFERENCES `permissions` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `functions`
--

LOCK TABLES `functions` WRITE;
/*!40000 ALTER TABLE `functions` DISABLE KEYS */;
INSERT INTO `functions` VALUES (7,'help','find out what are the functions you can access now',1,_binary '\0',_binary '\0',_binary '\0',_binary '\0',_binary '',_binary '\0'),(8,'start','starts a conversation with the bot',1,_binary '',_binary '\0',_binary '\0',_binary '\0',_binary '\0',_binary '\0'),(9,'cancel','cancels currently using job or function',1,_binary '\0',_binary '\0',_binary '\0',_binary '\0',_binary '\0',_binary ''),(10,'end','ends the conversation menu',1,_binary '\0',_binary '',_binary '',_binary '',_binary '\0',_binary ''),(11,'quit','quits all menus and returns to start menu',1,_binary '\0',_binary '\0',_binary '',_binary '',_binary '\0',_binary ''),(12,'admin_menu','enters the admin menu (only for people with admin perms)',3,_binary '\0',_binary '',_binary '\0',_binary '\0',_binary '\0',_binary '\0'),(13,'new_thread','write a new thread to be posted in the group!',1,_binary '\0',_binary '',_binary '\0',_binary '\0',_binary '\0',_binary '\0'),(14,'feedback','write a feedback to the admins',1,_binary '\0',_binary '',_binary '\0',_binary '\0',_binary '\0',_binary '\0'),(15,'sview_fb','Feedback Summary View',1,_binary '\0',_binary '\0',_binary '',_binary '\0',_binary '\0',_binary '\0'),(16,'dview_fb','<feedback id> Feedback Detailed View',1,_binary '\0',_binary '\0',_binary '',_binary '\0',_binary '\0',_binary '\0'),(17,'ch_perm','/ch_perm <user> <perms> to change the permissions of another user',3,_binary '\0',_binary '\0',_binary '',_binary '\0',_binary '\0',_binary '\0'),(18,'del_threads','/del_threads <thread number> for any number of values to delete the threads. There is no confirmation messgae so please by sure before deleting',3,_binary '\0',_binary '\0',_binary '',_binary '\0',_binary '\0',_binary '\0');
/*!40000 ALTER TABLE `functions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permissions`
--

DROP TABLE IF EXISTS `permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` longtext NOT NULL,
  `power` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissions`
--

LOCK TABLES `permissions` WRITE;
/*!40000 ALTER TABLE `permissions` DISABLE KEYS */;
INSERT INTO `permissions` VALUES (1,'member',0),(2,'mod',9),(3,'admin',10),(4,'dev',100);
/*!40000 ALTER TABLE `permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `threads`
--

DROP TABLE IF EXISTS `threads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `threads` (
  `id` int NOT NULL AUTO_INCREMENT,
  `msg_id` int DEFAULT NULL,
  `parent_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  `msg` longtext,
  `post_dt` datetime DEFAULT NULL,
  `title` text,
  `author_id` int DEFAULT NULL,
  `file_id` varchar(2000) DEFAULT NULL,
  `likes` int DEFAULT '0',
  `deleted` bit(1) DEFAULT b'0',
  PRIMARY KEY (`id`),
  KEY `fk_threads_categories` (`category_id`),
  KEY `fk_threads_users` (`author_id`),
  KEY `fk_threads_parent` (`parent_id`),
  CONSTRAINT `fk_threads_categories` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_threads_parent` FOREIGN KEY (`parent_id`) REFERENCES `threads` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_threads_users` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `threads`
--

LOCK TABLES `threads` WRITE;
/*!40000 ALTER TABLE `threads` DISABLE KEYS */;
INSERT INTO `threads` VALUES (17,1381,NULL,2,'Content','2020-11-02 08:05:19','Title',1,NULL,0,_binary '\0'),(18,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,_binary '\0'),(19,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,_binary '\0'),(20,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,_binary '\0'),(21,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,_binary '\0'),(22,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,_binary '\0'),(23,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,_binary '\0'),(25,1631,NULL,2,'Content','2020-11-02 08:52:57','Title2',1,NULL,0,_binary '\0'),(31,23,NULL,2,'Content','2021-01-03 10:00:23','Yeet',1,NULL,0,_binary '');
/*!40000 ALTER TABLE `threads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permissions_id` int DEFAULT NULL,
  `username` text NOT NULL,
  `firstname` text,
  `lastname` text,
  PRIMARY KEY (`id`),
  KEY `fk_users_permissions` (`permissions_id`),
  CONSTRAINT `fk_users_permissions` FOREIGN KEY (`permissions_id`) REFERENCES `permissions` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,333647246,4,'ollayf','Hosea',NULL),(2,678686611,3,'ollayff','Yu Fei','Ng');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-03 18:59:21
