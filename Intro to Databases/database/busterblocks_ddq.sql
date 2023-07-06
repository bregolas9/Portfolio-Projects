-- MySQL dump 10.16  Distrib 10.1.37-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: bsg
-- ------------------------------------------------------
-- Server version	10.1.37-MariaDB

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

DROP TABLE IF EXISTS `movies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movies` (
    `itemID` int(11) AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `release_year` int(11) NOT NULL,
    `in_stock` TINYINT NOT NULL,
    `qty` int(11) NOT NULL,
    `rental_price` DECIMAL(6,2) NOT NULL UNIQUE,
    PRIMARY KEY (`itemID`)
) ENGINE=InnoDB;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `movies` WRITE;
/*!40000 ALTER TABLE `movies` DISABLE KEYS */;
INSERT INTO `movies` VALUES (1, 'Fellowship of the ring', 2001, true, 2, 3);
INSERT INTO `movies` VALUES (2, 'Trainspotting', 1996, false, 1, 4);
/*!40000 ALTER TABLE `movies` ENABLE KEYS */;
UNLOCK TABLES;

DROP TABLE IF EXISTS `members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `members` (
    `memberID` int(11) AUTO_INCREMENT,
    `member_name` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`memberID`)
)ENGINE=InnoDB;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `members` WRITE;
/*!40000 ALTER TABLE `members` DISABLE KEYS */;
INSERT INTO `members` VALUES (1, 'John Smith', 'js@aol.com');
INSERT INTO `members` VALUES (2, 'Abe Lincoln','penny@netscape.org');
/*!40000 ALTER TABLE `members` ENABLE KEYS */;
UNLOCK TABLES;

DROP TABLE IF EXISTS `movies_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movies_members` (
    `itemID` int(11) NOT NULL,
    `memberID` int(11) NOT NULL,
    PRIMARY KEY (`itemID`, `memberID`),
    CONSTRAINT `movies_members_fk` FOREIGN KEY (`itemID`) REFERENCES `movies`(`itemID`),
    CONSTRAINT `movies_members_fk_two` FOREIGN KEY (`memberID`) REFERENCES `members`(`memberID`)
) ENGINE=InnoDB;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transactions` (
    `transactionID` int(11) AUTO_INCREMENT,
    `itemID` int(11) NOT NULL,
    `memberID` int(11),
    `rental_price` DECIMAL(6,2) NOT NULL,
    PRIMARY KEY (`transactionID`),
    CONSTRAINT `transactions_fk` FOREIGN KEY (`itemID`) REFERENCES `movies`(`itemID`),
    CONSTRAINT `transactions_fk_two` FOREIGN KEY (`memberID`) REFERENCES `members`(`memberID`),
    CONSTRAINT `transactions_fk_three` FOREIGN KEY (`rental_price`) REFERENCES `movies`(`rental_price`)
)ENGINE=InnoDB;
/*!40101 SET character_set_client = @saved_cs_client */;


LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1, 2, 1, 3);
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

DROP TABLE IF EXISTS `rentals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rentals` (
    `memberID` int(11),
    `itemID` int(11) NOT NULL,
    `transactionID` int(11) NOT NULL,
    PRIMARY KEY (`memberID`, `itemID`, `transactionID`),
    CONSTRAINT `rentals_fk` FOREIGN KEY (`itemID`) REFERENCES `movies`(`itemID`),
    CONSTRAINT `rentals_fk_two` FOREIGN KEY (`memberID`) REFERENCES `members`(`memberID`),
    CONSTRAINT `rentals_fk_three` FOREIGN KEY (`transactionID`) REFERENCES `transactions`(`transactionID`)
)ENGINE=InnoDB;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-03  0:38:33