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
-- Table structure for table `zipsbatters`
--

DROP TABLE IF EXISTS `zipsbatters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zipsbatters` (
  `Player` text,
  `Tm` text,
  `B` text,
  `PO` text,
  `Age` int(11) DEFAULT NULL,
  `RC/27` double DEFAULT NULL,
  `BA` double DEFAULT NULL,
  `OBP` double DEFAULT NULL,
  `SLG` double DEFAULT NULL,
  `G` int(11) DEFAULT NULL,
  `AB` int(11) DEFAULT NULL,
  `R` int(11) DEFAULT NULL,
  `H` int(11) DEFAULT NULL,
  `2B` int(11) DEFAULT NULL,
  `3B` int(11) DEFAULT NULL,
  `HR` int(11) DEFAULT NULL,
  `RBI` int(11) DEFAULT NULL,
  `BB` int(11) DEFAULT NULL,
  `SO` int(11) DEFAULT NULL,
  `HP` int(11) DEFAULT NULL,
  `SB` int(11) DEFAULT NULL,
  `CS` int(11) DEFAULT NULL,
  `SH` int(11) DEFAULT NULL,
  `SF` int(11) DEFAULT NULL,
  `IBB` int(11) DEFAULT NULL,
  `GDP` int(11) DEFAULT NULL,
  `OPS+` int(11) DEFAULT NULL,
  `DR` int(11) DEFAULT NULL,
  `WAR` double DEFAULT NULL,
  `SLG>.500` text,
  `SLG>.450` text,
  `SLG>.400` text,
  `200+ H` text,
  `150+ H` text,
  `45+ 2B` text,
  `30+ 2B` text,
  `10+ 3B` text,
  `5+ 3B` text,
  `50+ HR` text,
  `40+ HR` text,
  `30+ HR` text,
  `20+ HR` text,
  `10+ HR` text,
  `BA>.350` text,
  `BA>.325` text,
  `BA>.300` text,
  `BA>.275` text,
  `BA>.250` text,
  `OB?>.400` text,
  `OBP>.375` text,
  `OBP>.350` text,
  `OBP>.325` text,
  `OBP>.300` text,
  `140+ OPS+` text,
  `130+ OPS+` text,
  `120+ OPS+` text,
  `110+ OPS+` text,
  `100+ OPS+` text,
  `90+ OPS+` text,
  `80+ OPS+` text,
  `TOP` text,
  `2nd` text,
  `MID` text,
  `4th` text,
  `LOW` text,
  `Offensive Comp 1` text
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

-- Dump completed on 2017-07-28 15:39:34
