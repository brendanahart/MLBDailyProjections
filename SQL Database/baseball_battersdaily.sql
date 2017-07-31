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
-- Table structure for table `battersdaily`
--

DROP TABLE IF EXISTS `battersdaily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `battersdaily` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ab` int(11) DEFAULT NULL,
  `hits` int(11) DEFAULT NULL,
  `singles` int(11) DEFAULT NULL,
  `doubles` int(11) DEFAULT NULL,
  `triples` int(11) DEFAULT NULL,
  `homeruns` int(11) DEFAULT NULL,
  `average` decimal(6,4) DEFAULT NULL,
  `stolenbases` int(11) DEFAULT NULL,
  `caughtstealing` int(11) DEFAULT NULL,
  `runs` int(11) DEFAULT NULL,
  `rbi` int(11) DEFAULT NULL,
  `walks` int(11) DEFAULT NULL,
  `errors` int(11) DEFAULT NULL,
  `hbp` int(11) DEFAULT NULL,
  `strikeouts` int(11) DEFAULT NULL,
  `batterID` int(11) DEFAULT NULL,
  `bgameID` int(11) DEFAULT NULL,
  `dkpoints` float DEFAULT '0',
  `adjwOBA` float DEFAULT NULL,
  `adjKP` float DEFAULT NULL,
  `adjBBP` float DEFAULT NULL,
  `adjBABIP` float DEFAULT NULL,
  `adjISO` float DEFAULT NULL,
  `adjOBP` float DEFAULT NULL,
  `adjOPS` float DEFAULT NULL,
  `adjSLG` float DEFAULT NULL,
  `parkFactor` float DEFAULT NULL,
  `oppPitcher` int(11) DEFAULT NULL,
  `team` varchar(45) DEFAULT NULL,
  `oppTeam` varchar(45) DEFAULT NULL,
  `dkPointsPred` decimal(7,3) DEFAULT NULL,
  `dkSalary` int(11) DEFAULT NULL,
  `variance` float DEFAULT '0',
  `pOWN` float DEFAULT '0.001',
  `contR` float DEFAULT '0',
  `rotogrindersPoints` float DEFAULT NULL,
  `wOBA` float DEFAULT NULL,
  `ISO` float DEFAULT NULL,
  `OBP` float DEFAULT NULL,
  `SLG` float DEFAULT NULL,
  `OPS` float DEFAULT NULL,
  `KP` float DEFAULT NULL,
  `BB` float DEFAULT NULL,
  `BABIP` float DEFAULT NULL,
  `adjSB` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `batterID_idx` (`batterID`),
  KEY `bgameID_idx` (`bgameID`),
  KEY `oppPitcher_idx` (`oppPitcher`),
  CONSTRAINT `batterID` FOREIGN KEY (`batterID`) REFERENCES `batters` (`idbatters`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `bgameID` FOREIGN KEY (`bgameID`) REFERENCES `dates` (`iddates`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `oppPitcher` FOREIGN KEY (`oppPitcher`) REFERENCES `pitchers` (`idpitchers`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=47417 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-07-28 15:39:30
