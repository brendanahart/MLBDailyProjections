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
-- Table structure for table `batters`
--

DROP TABLE IF EXISTS `batters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `batters` (
  `idbatters` int(11) NOT NULL AUTO_INCREMENT,
  `mlbID` int(11) DEFAULT NULL,
  `playerName` varchar(100) DEFAULT NULL,
  `wOBAL` double DEFAULT '0',
  `wOBAR` double DEFAULT '0',
  `ISOL` double DEFAULT '0',
  `ISOR` double DEFAULT '0',
  `OBPL` double DEFAULT '0',
  `OBPR` double DEFAULT '0',
  `OPSL` double DEFAULT '0',
  `OPSR` double DEFAULT '0',
  `SLGL` double DEFAULT '0',
  `SLGR` double DEFAULT '0',
  `KPL` double DEFAULT '1',
  `KPR` double DEFAULT '1',
  `BABIPL` double DEFAULT '0',
  `BABIPR` double DEFAULT '0',
  `ABL` int(11) DEFAULT '0',
  `ABR` int(11) DEFAULT '0',
  `BBL` double DEFAULT '0',
  `BBR` double DEFAULT '0',
  `paL` int(11) DEFAULT '0',
  `paR` int(11) DEFAULT '0',
  `start` int(11) DEFAULT '0',
  `battingOrder` int(11) DEFAULT '0',
  `hand` varchar(45) DEFAULT NULL,
  `pos` varchar(45) DEFAULT NULL,
  `pos1` varchar(45) DEFAULT NULL,
  `team` varchar(45) DEFAULT NULL,
  `lastOpp` varchar(45) DEFAULT NULL,
  `wOBA` double DEFAULT '0',
  `ISO` double DEFAULT '0',
  `OBP` double DEFAULT '0',
  `SLG` double DEFAULT '0',
  `OPS` double DEFAULT '0',
  `KP` double DEFAULT '0',
  `BB` double DEFAULT '0',
  `BABIP` double DEFAULT '0',
  `wSB` double DEFAULT '0',
  PRIMARY KEY (`idbatters`),
  UNIQUE KEY `mlbID` (`mlbID`)
) ENGINE=InnoDB AUTO_INCREMENT=184892 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-07-28 15:39:26
