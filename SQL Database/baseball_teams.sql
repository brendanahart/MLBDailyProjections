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
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teams` (
  `teamid` int(11) NOT NULL AUTO_INCREMENT,
  `teamName` varchar(100) DEFAULT NULL,
  `teamAbbrv` varchar(45) DEFAULT NULL,
  `BBP` decimal(6,4) DEFAULT NULL,
  `KP` decimal(6,4) DEFAULT NULL,
  `ISO` decimal(6,4) DEFAULT NULL,
  `BABIP` decimal(6,4) DEFAULT NULL,
  `AVG` decimal(6,4) DEFAULT NULL,
  `OBP` decimal(6,4) DEFAULT NULL,
  `SLG` decimal(6,4) DEFAULT NULL,
  `wOBA` decimal(6,4) DEFAULT NULL,
  `oppPitcherT` int(11) DEFAULT NULL,
  `startPitcherT` int(11) DEFAULT NULL,
  `oppPitcher` int(11) DEFAULT NULL,
  `startPitcher` int(11) DEFAULT NULL,
  PRIMARY KEY (`teamid`),
  UNIQUE KEY `teamAbbrv_UNIQUE` (`teamAbbrv`),
  UNIQUE KEY `teamName_UNIQUE` (`teamName`),
  KEY `oppPitcher_idx` (`oppPitcher`),
  KEY `startPitcher_idx` (`startPitcher`),
  KEY `oppPitcherT_idx` (`oppPitcherT`),
  KEY `startPitcherT_idx` (`startPitcherT`),
  CONSTRAINT `oppPitcherT` FOREIGN KEY (`oppPitcherT`) REFERENCES `pitchers` (`idpitchers`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `startPitcherT` FOREIGN KEY (`startPitcherT`) REFERENCES `pitchers` (`idpitchers`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=541 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-07-28 15:39:40
