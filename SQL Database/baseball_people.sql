CREATE DATABASE  IF NOT EXISTS `baseball` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `baseball`;
-- MySQL dump 10.13  Distrib 5.7.12, for osx10.9 (x86_64)
--
-- Host: 127.0.0.1    Database: baseball
-- ------------------------------------------------------
-- Server version	5.7.10

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `people`
--

DROP TABLE IF EXISTS `people`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people` (
  `key_person` varchar(50) NOT NULL,
  `key_uuid` text,
  `key_mlbam` text,
  `key_retro` text,
  `key_bbref` text,
  `key_bbref_minors` text,
  `key_fangraphs` int(11) DEFAULT NULL,
  `key_npb` text,
  `key_sr_nfl` text,
  `key_sr_nba` text,
  `key_sr_nhl` text,
  `key_findagrave` text,
  `name_last` text,
  `name_first` text,
  `name_given` text,
  `name_suffix` text,
  `name_matrilineal` text,
  `name_nick` text,
  `birth_year` text,
  `birth_month` text,
  `birth_day` text,
  `death_year` text,
  `death_month` text,
  `death_day` text,
  `pro_played_first` text,
  `pro_played_last` text,
  `mlb_played_first` text,
  `mlb_played_last` text,
  `col_played_first` text,
  `col_played_last` text,
  `pro_managed_first` text,
  `pro_managed_last` text,
  `mlb_managed_first` text,
  `mlb_managed_last` text,
  `col_managed_first` text,
  `col_managed_last` text,
  `pro_umpired_first` text,
  `pro_umpired_last` text,
  `mlb_umpired_first` text,
  `mlb_umpired_last` text,
  `rotowireID` text,
  `rotogrindersID` text,
  PRIMARY KEY (`key_person`),
  UNIQUE KEY `key_person_UNIQUE` (`key_person`),
  UNIQUE KEY `key_fangraphs_UNIQUE` (`key_fangraphs`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-07-28 15:39:27
