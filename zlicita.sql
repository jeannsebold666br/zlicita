-- MySQL dump 10.15  Distrib 10.0.17-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: zlicita
-- ------------------------------------------------------
-- Server version	10.0.17-MariaDB-0ubuntu1

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
-- Table structure for table `coleta`
--

DROP TABLE IF EXISTS `coleta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coleta` (
  `id_coleta` int(11) NOT NULL,
  `data` date DEFAULT NULL,
  `qtd_registro` int(11) DEFAULT NULL,
  `qtd_coletado` int(11) DEFAULT NULL,
  `data_ini_coleta` datetime DEFAULT NULL,
  `data_fim_coleta` datetime DEFAULT NULL,
  `html` text,
  `finalizado` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id_coleta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coleta`
--

LOCK TABLES `coleta` WRITE;
/*!40000 ALTER TABLE `coleta` DISABLE KEYS */;
INSERT INTO `coleta` VALUES (1,'2015-01-01',0,0,'2015-06-27 00:00:00','2015-06-27 00:00:00',NULL,1),(2,'2015-01-02',50,49,NULL,NULL,NULL,0),(3,'2015-01-03',NULL,NULL,NULL,NULL,NULL,0),(4,'2015-01-04',NULL,NULL,NULL,NULL,NULL,0),(5,'2015-01-05',NULL,NULL,NULL,NULL,NULL,0),(6,'2015-01-06',NULL,NULL,NULL,NULL,NULL,0),(7,'2015-01-07',NULL,NULL,NULL,NULL,NULL,0),(8,'2015-01-08',NULL,NULL,NULL,NULL,NULL,0),(9,'2015-01-09',NULL,NULL,NULL,NULL,NULL,0),(10,'2015-01-10',NULL,NULL,NULL,NULL,NULL,0);
/*!40000 ALTER TABLE `coleta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registro`
--

DROP TABLE IF EXISTS `registro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registro` (
  `id_registro` int(11) NOT NULL AUTO_INCREMENT,
  `id_coleta` int(11) DEFAULT NULL,
  `numero_registro` int(11) DEFAULT NULL,
  `cidade` varchar(255) DEFAULT NULL,
  `estado` char(2) DEFAULT NULL,
  `uasg` varchar(255) DEFAULT NULL,
  `orgao1` varchar(255) DEFAULT NULL,
  `orgao2` varchar(255) DEFAULT NULL,
  `orgao3` varchar(255) DEFAULT NULL,
  `pregao` varchar(255) DEFAULT NULL,
  `objeto` text,
  `edital` varchar(255) DEFAULT NULL,
  `endereco` varchar(255) DEFAULT NULL,
  `telefone` varchar(45) DEFAULT NULL,
  `fax` varchar(45) DEFAULT NULL,
  `proposta` varchar(255) DEFAULT NULL,
  `item_material` mediumtext,
  `item_servico` mediumtext,
  `html` mediumtext,
  `link_download` varchar(512) DEFAULT NULL,
  `url` varchar(1024) DEFAULT NULL,
  `data_inicio_coleta` datetime DEFAULT NULL,
  `data_fim_coleta` datetime DEFAULT NULL,
  PRIMARY KEY (`id_registro`),
  KEY `fk_registro_1_idx` (`id_coleta`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registro`
--

LOCK TABLES `registro` WRITE;
/*!40000 ALTER TABLE `registro` DISABLE KEYS */;
/*!40000 ALTER TABLE `registro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(200) NOT NULL,
  `password` varchar(250) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `valid` tinyint(4) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','698dc19d489c4e4db73e28a713eab07b','Admin',1,'admin');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-06-27  3:22:29
