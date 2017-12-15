-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: 192.168.56.101    Database: beetcount
-- ------------------------------------------------------
-- Server version	5.7.20-0ubuntu0.16.04.1

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
-- Dumping data for table `drivers`
--

LOCK TABLES `drivers` WRITE;
/*!40000 ALTER TABLE `drivers` DISABLE KEYS */;
INSERT INTO `drivers` VALUES (1,'Гребенщиков Федот Потапович',89903456787,'greben1976@mail.ru',NULL,NULL,1,1,12234),(2,'Нагиев Никита Михаилович',88045863449,'nagiev49380@yandex.ru',NULL,NULL,2,2,45567),(3,'Рогозин Леондий Моисеевич',NULL,NULL,NULL,NULL,3,3,89900);
/*!40000 ALTER TABLE `drivers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `loadpoints`
--

LOCK TABLES `loadpoints` WRITE;
/*!40000 ALTER TABLE `loadpoints` DISABLE KEYS */;
INSERT INTO `loadpoints` VALUES (1,'Поле №1','д. Екатериновка',NULL,1),(2,'СЕК.067/234-12','Березовка',NULL,2),(3,'ТЦ-390','Боевка',NULL,3);
/*!40000 ALTER TABLE `loadpoints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `photos`
--

LOCK TABLES `photos` WRITE;
/*!40000 ALTER TABLE `photos` DISABLE KEYS */;
/*!40000 ALTER TABLE `photos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `regions`
--

LOCK TABLES `regions` WRITE;
/*!40000 ALTER TABLE `regions` DISABLE KEYS */;
INSERT INTO `regions` VALUES (1,'Елецкий'),(2,'Становлянский'),(3,'Тербунский');
/*!40000 ALTER TABLE `regions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `samples`
--

LOCK TABLES `samples` WRITE;
/*!40000 ALTER TABLE `samples` DISABLE KEYS */;
/*!40000 ALTER TABLE `samples` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
INSERT INTO `suppliers` VALUES (1,'ПРИМА','ООО \"Прима\"',1,'sekretar@prima.com',88799094531,'ИНН, кор.счет. расч. счет и т.п.',0),(2,'СЕКУНДА','ООО \"Секунда\"',2,'buhgalter@sekunda.to',89203560933,'ИНН, кор.счет. расч. счет и т.п.',0),(3,'ТЕРЦИЯ','ООО \"Терция\"',3,NULL,NULL,'ИНН, кор.счет. расч. счет и т.п.',0),(4,'ИВАНОВ','ИП Иванов П.Г.',1,NULL,NULL,'ИНН, кор.счет. расч. счет и т.п.',1);
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `transport`
--

LOCK TABLES `transport` WRITE;
/*!40000 ALTER TABLE `transport` DISABLE KEYS */;
INSERT INTO `transport` VALUES (1,1,'А123АА48','АА1234',40.5,19.8,1),(2,2,'В456ВВ48','ВВ4567',50.1,20,2),(3,3,'С789СС199',NULL,30.3,17.6,3);
/*!40000 ALTER TABLE `transport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `transport_models`
--

LOCK TABLES `transport_models` WRITE;
/*!40000 ALTER TABLE `transport_models` DISABLE KEYS */;
INSERT INTO `transport_models` VALUES (1,'КАМАЗ',1),(2,'МАЗ',1),(3,'FOTON',3),(4,'MAN',4);
/*!40000 ALTER TABLE `transport_models` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `transport_types`
--

LOCK TABLES `transport_types` WRITE;
/*!40000 ALTER TABLE `transport_types` DISABLE KEYS */;
INSERT INTO `transport_types` VALUES (1,'Самосвал'),(2,'Бортовой'),(3,'Ленточный');
/*!40000 ALTER TABLE `transport_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `trips`
--

LOCK TABLES `trips` WRITE;
/*!40000 ALTER TABLE `trips` DISABLE KEYS */;
INSERT INTO `trips` VALUES 
(1,101,1,1,1,1,'2017-10-24 00:05:44.000000','2017-10-24 00:25:03.000000',NULL,1,1,'2017-10-24 00:41:44.000000',1,33.6,'2017-10-24 00:40:13.000000',NULL,16.9,'2017-10-24 00:50:56.000000',NULL,16.7,NULL,16.1),
(2,201,2,2,2,2,'2017-10-24 01:05:44.000000','2017-10-24 01:25:03.000000',NULL,2,2,'2017-10-24 01:41:44.000000',2,23,'2017-10-24 01:40:13.000000',NULL,10.2,'2017-10-24 01:50:56.000000',NULL,12.8,NULL,11.9),
(3,301,3,3,3,3,'2017-10-24 01:15:44.000000','2017-10-24 01:35:03.000000',NULL,3,3,'2017-10-24 01:51:44.000000',3,45.7,'2017-10-24 01:50:13.000000',NULL,20.3,'2017-10-24 02:00:56.000000',NULL,25.4,NULL,24.6);
/*!40000 ALTER TABLE `trips` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `unloaders`
--

LOCK TABLES `unloaders` WRITE;
/*!40000 ALTER TABLE `unloaders` DISABLE KEYS */;
INSERT INTO `unloaders` VALUES (1,'Семенов Дмитрий Яковович','Булдаков Егор Елисеевич','Тарасов Казимир Дмитриевич','Казанцев Ипполит Прохорович',1,1223),(2,'Комолов Павел Маркович','Галыгин Ерофей Демьянович',NULL,NULL,2,4556),(3,'Митин Евгений Яковович',NULL,NULL,NULL,3,7889);
/*!40000 ALTER TABLE `unloaders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `unloadpoints`
--

LOCK TABLES `unloadpoints` WRITE;
/*!40000 ALTER TABLE `unloadpoints` DISABLE KEYS */;
INSERT INTO `unloadpoints` VALUES (1,'Бурачная','1',NULL),(2,'Кагат 1','2',1),(3,'Кагат 2','2',1);
/*!40000 ALTER TABLE `unloadpoints` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-26 21:05:16
