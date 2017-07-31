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
-- Table structure for table `pitchersdaily`
--

DROP TABLE IF EXISTS `pitchersdaily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pitchersdaily` (
  `idpitchersdaily` int(11) NOT NULL AUTO_INCREMENT,
  `pitcherID` int(11) DEFAULT NULL,
  `pgameID` int(11) DEFAULT NULL,
  `walks` int(11) DEFAULT NULL,
  `earnedRuns` int(11) DEFAULT NULL,
  `era` decimal(8,4) DEFAULT NULL,
  `hits` int(11) DEFAULT NULL,
  `hbp` int(11) DEFAULT NULL,
  `homerunsAllowed` int(11) DEFAULT NULL,
  `ip` decimal(4,2) DEFAULT NULL,
  `strikeouts` int(11) DEFAULT NULL,
  `numberPitches` int(11) DEFAULT NULL,
  `runs` int(11) DEFAULT NULL,
  `strikes` int(11) DEFAULT NULL,
  `win` int(11) DEFAULT NULL,
  `shutout` int(11) DEFAULT NULL,
  `completegame` int(11) DEFAULT NULL,
  `nohitter` int(11) DEFAULT NULL,
  `save` int(11) DEFAULT NULL,
  `whip` decimal(8,4) DEFAULT NULL,
  `dkpoints` decimal(7,3) DEFAULT '0.000',
  `team` varchar(45) DEFAULT NULL,
  `oppTeam` varchar(45) DEFAULT NULL,
  `dkPointsPred` float DEFAULT NULL,
  `rotogrindersPoints` float DEFAULT NULL,
  `saberSimPoints` float DEFAULT NULL,
  `rotowirePoints` float DEFAULT NULL,
  `dkSalary` int(11) DEFAULT NULL,
  `variance` float DEFAULT '0',
  `pOWN` float DEFAULT '0.001',
  `contR` float DEFAULT '0',
  PRIMARY KEY (`idpitchersdaily`),
  KEY `pgameID_idx` (`pgameID`),
  KEY `pitcherID_idx` (`pitcherID`),
  CONSTRAINT `pgameID` FOREIGN KEY (`pgameID`) REFERENCES `dates` (`iddates`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `pitcherID` FOREIGN KEY (`pitcherID`) REFERENCES `pitchers` (`idpitchers`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=13064 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-07-28 15:39:28
