-- MySQL dump 1.13  Distrib 8..32, for Win64 (86_64)
--
-- Host: localhost    Database: recipes
-- ------------------------------------------------------
-- Server version	8..32

/*!411 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!411 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!411 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!553 SET NAMES utf8mb4 */;
/*!413 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!413 SET TIME_ZONE='+:' */;
/*!414 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS= */;
/*!414 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS= */;
/*!411 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!4111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES= */;

--
-- Table structure for table `recipe_details`
--

DROP TABLE IF EXISTS `recipe_details`;
/*!411 SET @saved_cs_client     = @@character_set_client */;
/*!553 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipe_details` (
  `NAME` char(1) DEFAULT NULL,
  `ID` int DEFAULT NULL,
  `MINUTES` int DEFAULT NULL,
  `CONTRIBUTOR_ID` int DEFAULT NULL,
  `SUBMITTED` date DEFAULT NULL,
  `TAGS` tet,
  `NUTRITION` tet,
  `N_STEPS` int DEFAULT NULL,
  `STEPS` tet,
  `DESCRIPTION` tet,
  `INGREDIENTS` tet,
  `N_INGREDIENTS` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!411 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipe_details`
--

LOCK TABLES `recipe_details` WRITE;
/*!4 ALTER TABLE `recipe_details` DISABLE KEYS */;
INSERT INTO 'recipe_details' VALUE('Apple Pot Pie', 1, 60, "Apples, Salt" );
-- /*!4 ALTER TABLE `recipe_details` ENABLE KEYS */;
-- UNLOCK TABLES;

