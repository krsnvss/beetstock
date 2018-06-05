-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: beetstock
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu18.04.1

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
-- Table structure for table `drivers`
--

DROP TABLE IF EXISTS `drivers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drivers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(150) COLLATE utf8_unicode_ci NOT NULL,
  `phone` char(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` char(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `comment` text COLLATE utf8_unicode_ci,
  `photo` int(11) DEFAULT NULL,
  `transport` int(11) NOT NULL,
  `employer` int(11) NOT NULL,
  `rfid` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `drivers_fk0` (`photo`),
  KEY `drivers_fk1` (`transport`),
  KEY `drivers_fk2` (`employer`),
  CONSTRAINT `drivers_fk1` FOREIGN KEY (`transport`) REFERENCES `transport` (`id`),
  CONSTRAINT `drivers_fk2` FOREIGN KEY (`employer`) REFERENCES `suppliers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `loadpoints`
--

DROP TABLE IF EXISTS `loadpoints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `loadpoints` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(50) COLLATE utf8_unicode_ci NOT NULL,
  `location` char(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `coordinates` char(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `supplier` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `loadpoints_fk0` (`supplier`),
  CONSTRAINT `loadpoints_fk0` FOREIGN KEY (`supplier`) REFERENCES `suppliers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `photos`
--

DROP TABLE IF EXISTS `photos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `photos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `photo` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `regions`
--

DROP TABLE IF EXISTS `regions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(150) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `samples`
--

DROP TABLE IF EXISTS `samples`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `samples` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `refuse` float DEFAULT NULL,
  `polarisation` float DEFAULT NULL,
  `k` float DEFAULT NULL,
  `n` float DEFAULT NULL,
  `an` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `suppliers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(100) COLLATE utf8_unicode_ci NOT NULL,
  `full_name` char(255) COLLATE utf8_unicode_ci NOT NULL,
  `region` int(11) NOT NULL,
  `email` char(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  `requisites` text COLLATE utf8_unicode_ci,
  `transporter_only` tinyint(1) NOT NULL DEFAULT '0',
  `default_load` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `suppliers_fk0` (`region`),
  KEY `default_load_idx` (`default_load`),
  CONSTRAINT `default_load` FOREIGN KEY (`default_load`) REFERENCES `loadpoints` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `suppliers_fk0` FOREIGN KEY (`region`) REFERENCES `regions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transport`
--

DROP TABLE IF EXISTS `transport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transport` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model` int(11) NOT NULL,
  `plate` char(10) COLLATE utf8_unicode_ci NOT NULL,
  `trailer` char(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `avg_gross` float DEFAULT NULL,
  `avg_tare` float DEFAULT NULL,
  `owner` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `transport_fk0` (`model`),
  KEY `transport_fk1` (`owner`),
  CONSTRAINT `transport_fk0` FOREIGN KEY (`model`) REFERENCES `transport_models` (`id`),
  CONSTRAINT `transport_fk1` FOREIGN KEY (`owner`) REFERENCES `suppliers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transport_models`
--

DROP TABLE IF EXISTS `transport_models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transport_models` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_name` char(255) COLLATE utf8_unicode_ci NOT NULL,
  `type` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `transport_models_fk0` (`type`),
  CONSTRAINT `transport_models_fk0` FOREIGN KEY (`type`) REFERENCES `transport_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transport_types`
--

DROP TABLE IF EXISTS `transport_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transport_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` char(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trips`
--

DROP TABLE IF EXISTS `trips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trips` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `trip` int(11) NOT NULL,
  `driver` int(11) NOT NULL,
  `transport` int(11) NOT NULL,
  `supplier` int(11) NOT NULL,
  `loadpoint` int(11) NOT NULL,
  `load_dt` datetime(6) DEFAULT NULL,
  `arrival_dt` datetime(6) DEFAULT NULL,
  `arrival_photo` int(11) DEFAULT NULL,
  `unload_send` int(11) DEFAULT NULL,
  `unload_fact` int(11) DEFAULT NULL,
  `unload_dt` datetime(6) DEFAULT NULL,
  `unloaders` int(11) DEFAULT NULL,
  `gross_weight` float DEFAULT NULL,
  `gross_dt` datetime(6) DEFAULT NULL,
  `gross_photo` int(11) DEFAULT NULL,
  `tare_weight` float DEFAULT NULL,
  `tare_dt` datetime(6) DEFAULT NULL,
  `tare_photo` int(11) DEFAULT NULL,
  `net_weight` float DEFAULT NULL,
  `sample` int(11) DEFAULT NULL,
  `clear_weight` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `trips_fk0` (`driver`),
  KEY `trips_fk1` (`transport`),
  KEY `trips_fk2` (`supplier`),
  KEY `trips_fk3` (`loadpoint`),
  KEY `trips_fk4` (`arrival_photo`),
  KEY `trips_fk5` (`unload_send`),
  KEY `trips_fk6` (`unload_fact`),
  KEY `trips_fk7` (`unloaders`),
  KEY `trips_fk8` (`gross_photo`),
  KEY `trips_fk9` (`tare_photo`),
  KEY `trips_fk10` (`sample`),
  CONSTRAINT `trips_fk0` FOREIGN KEY (`driver`) REFERENCES `drivers` (`id`),
  CONSTRAINT `trips_fk1` FOREIGN KEY (`transport`) REFERENCES `transport` (`id`),
  CONSTRAINT `trips_fk10` FOREIGN KEY (`sample`) REFERENCES `samples` (`id`),
  CONSTRAINT `trips_fk2` FOREIGN KEY (`supplier`) REFERENCES `suppliers` (`id`),
  CONSTRAINT `trips_fk3` FOREIGN KEY (`loadpoint`) REFERENCES `loadpoints` (`id`),
  CONSTRAINT `trips_fk4` FOREIGN KEY (`arrival_photo`) REFERENCES `photos` (`id`),
  CONSTRAINT `trips_fk5` FOREIGN KEY (`unload_send`) REFERENCES `unloadpoints` (`id`),
  CONSTRAINT `trips_fk6` FOREIGN KEY (`unload_fact`) REFERENCES `unloadpoints` (`id`),
  CONSTRAINT `trips_fk7` FOREIGN KEY (`unloaders`) REFERENCES `unloaders` (`id`),
  CONSTRAINT `trips_fk8` FOREIGN KEY (`gross_photo`) REFERENCES `photos` (`id`),
  CONSTRAINT `trips_fk9` FOREIGN KEY (`tare_photo`) REFERENCES `photos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1492 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `unloaders`
--

DROP TABLE IF EXISTS `unloaders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unloaders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(150) COLLATE utf8_unicode_ci NOT NULL,
  `assistant1` char(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `assistant2` char(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `assistant3` char(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `unload_point` int(11) DEFAULT NULL,
  `rfid` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `unloaders_fk0` (`unload_point`),
  CONSTRAINT `unloaders_fk0` FOREIGN KEY (`unload_point`) REFERENCES `unloadpoints` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `unloadpoints`
--

DROP TABLE IF EXISTS `unloadpoints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unloadpoints` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(250) COLLATE utf8_unicode_ci NOT NULL,
  `type` char(100) COLLATE utf8_unicode_ci NOT NULL,
  `preffered_truck_type` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `unloadpoints_fk0` (`preffered_truck_type`),
  CONSTRAINT `unloadpoints_fk0` FOREIGN KEY (`preffered_truck_type`) REFERENCES `transport_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-04 22:53:40
