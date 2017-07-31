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
-- Table structure for table `zipspitchers`
--

DROP TABLE IF EXISTS `zipspitchers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zipspitchers` (
  `Player` text,
  `Tm` text,
  `T` text,
  `Age` int(11) DEFAULT NULL,
  `W` int(11) DEFAULT NULL,
  `L` int(11) DEFAULT NULL,
  `ERA` double DEFAULT NULL,
  `G` int(11) DEFAULT NULL,
  `GS` int(11) DEFAULT NULL,
  `IP` double DEFAULT NULL,
  `H` int(11) DEFAULT NULL,
  `R` int(11) DEFAULT NULL,
  `ER` int(11) DEFAULT NULL,
  `HR` int(11) DEFAULT NULL,
  `BB` int(11) DEFAULT NULL,
  `SO` int(11) DEFAULT NULL,
  `WP` int(11) DEFAULT NULL,
  `G/GF` text,
  `HBP` int(11) DEFAULT NULL,
  `GDP` int(11) DEFAULT NULL,
  `IBB` int(11) DEFAULT NULL,
  `BK` int(11) DEFAULT NULL,
  `ERA+` int(11) DEFAULT NULL,
  `WAR` double DEFAULT NULL,
  `WP*` int(11) DEFAULT NULL,
  `HOLD*` text,
  `Comp1` text,
  `ST*` text,
  `REL*` text,
  `ERA+>140` text,
  `ERA+>130` text,
  `ERA+>120` text,
  `ERA+>110` text,
  `ERA+>100` text,
  `ERA+>90` text,
  `ERA+>80` text,
  `K/9 >9` text,
  `K/9 >8` text,
  `K/9 >7` text,
  `K/9 >6` text,
  `BB/9 <1.5` text,
  `BB/9 <2` text,
  `BB/9 <2.5` text,
  `BB/9 <3` text,
  `BB/9 <3.5` text,
  `BB/9 <4` text,
  `HR/9 <0.7` text,
  `HR/9 <1` text,
  `HR/9 <1.3` text,
  `HR/9 <1.6` text
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

-- Dump completed on 2017-07-28 15:39:31
