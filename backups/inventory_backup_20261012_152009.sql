-- MySQL dump 10.13  Distrib 8.4.11, for Win64 (x86_64)
--
-- Host: localhost    Database: stock_management
-- ------------------------------------------------------
-- Server version	8.4.11

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'pbkdf2_sha256$1500000$1eAFYdRlcpZEuJEBnZqzKo$A/cWApf2QSD61yO16r4HJDryXeBt1YxqE0F5mYNFLck=','2026-10-12 10:02:59.575712',1,'admin','','','admin@gmail.com',1,1,'2026-08-26 08:52:23.000000','ADMIN'),(2,'pbkdf2_sha256$1500000$UtYKiHdi0oKzRQxJkW5vCw$UD8maRYr++FmFSOCs7IgMuJ4zhaykTZySp4jSUiLQxI=','2026-10-08 16:29:32.322442',0,'manager','','','',0,1,'2026-08-26 08:55:04.000000','MANAGER'),(3,'pbkdf2_sha256$1500000$Kgrw5Z90gIQSQXOW32A9bP$pWBogWEcJMxV9Xb1OkZDqcZd3ME0gAO4ix4FPzllmc8=','2026-10-08 16:13:38.336115',0,'Ali','','','',0,1,'2026-08-26 16:52:27.000000','SALESMAN'),(5,'pbkdf2_sha256$1500000$mgySj2lO2if0ROB54hptD7$iuxuA0Wr9rTxHxubKrM9B4yV+h4oisaFkd3tBAicOZ0=','2026-09-09 04:43:28.680669',0,'zulki','','','zulki@gmail.com',0,1,'2026-09-09 04:43:10.339731','MANAGER');
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activity_log`
--

DROP TABLE IF EXISTS `activity_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_log` (
  `LogId` int NOT NULL AUTO_INCREMENT,
  `Action` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Module` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Description` longtext COLLATE utf8mb4_unicode_ci,
  `IPAddress` char(39) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `CreatedAt` datetime(6) NOT NULL,
  `User_id` bigint DEFAULT NULL,
  PRIMARY KEY (`LogId`),
  KEY `activity_log_User_id_cfc9668c_fk_accounts_user_id` (`User_id`),
  CONSTRAINT `activity_log_User_id_cfc9668c_fk_accounts_user_id` FOREIGN KEY (`User_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_log`
--

LOCK TABLES `activity_log` WRITE;
/*!40000 ALTER TABLE `activity_log` DISABLE KEYS */;
INSERT INTO `activity_log` VALUES (1,'Product Added','Inventory','Product \"chocolate\" was added.','127.0.0.1','2026-10-08 13:25:23.334407',1),(2,'Sale Created','Sales','Sale #9 was created. Total amount: 270000.00.','127.0.0.1','2026-10-10 14:31:58.635801',1);
/*!40000 ALTER TABLE `activity_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_user'),(22,'Can change user',6,'change_user'),(23,'Can delete user',6,'delete_user'),(24,'Can view user',6,'view_user'),(25,'Can add product',8,'add_product'),(26,'Can change product',8,'change_product'),(27,'Can delete product',8,'delete_product'),(28,'Can view product',8,'view_product'),(29,'Can add category',7,'add_category'),(30,'Can change category',7,'change_category'),(31,'Can delete category',7,'delete_category'),(32,'Can view category',7,'view_category'),(33,'Can add supplier',11,'add_supplier'),(34,'Can change supplier',11,'change_supplier'),(35,'Can delete supplier',11,'delete_supplier'),(36,'Can view supplier',11,'view_supplier'),(37,'Can add stock entry detail',10,'add_stockentrydetail'),(38,'Can change stock entry detail',10,'change_stockentrydetail'),(39,'Can delete stock entry detail',10,'delete_stockentrydetail'),(40,'Can view stock entry detail',10,'view_stockentrydetail'),(41,'Can add stock entry',9,'add_stockentry'),(42,'Can change stock entry',9,'change_stockentry'),(43,'Can delete stock entry',9,'delete_stockentry'),(44,'Can view stock entry',9,'view_stockentry'),(45,'Can add customer',12,'add_customer'),(46,'Can change customer',12,'change_customer'),(47,'Can delete customer',12,'delete_customer'),(48,'Can view customer',12,'view_customer'),(49,'Can add sale detail',14,'add_saledetail'),(50,'Can change sale detail',14,'change_saledetail'),(51,'Can delete sale detail',14,'delete_saledetail'),(52,'Can view sale detail',14,'view_saledetail'),(53,'Can add sale',13,'add_sale'),(54,'Can change sale',13,'change_sale'),(55,'Can delete sale',13,'delete_sale'),(56,'Can view sale',13,'view_sale'),(57,'Can add sale return detail',16,'add_salereturndetail'),(58,'Can change sale return detail',16,'change_salereturndetail'),(59,'Can delete sale return detail',16,'delete_salereturndetail'),(60,'Can view sale return detail',16,'view_salereturndetail'),(61,'Can add sale return',15,'add_salereturn'),(62,'Can change sale return',15,'change_salereturn'),(63,'Can delete sale return',15,'delete_salereturn'),(64,'Can view sale return',15,'view_salereturn'),(65,'Can add activity log',17,'add_activitylog'),(66,'Can change activity log',17,'change_activitylog'),(67,'Can delete activity log',17,'delete_activitylog'),(68,'Can view activity log',17,'view_activitylog');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `CT_Id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Description` longtext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`CT_Id`),
  UNIQUE KEY `category_Name_ffffe424_uniq` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Electronics','Electronic products'),(2,'Stationery','Stationery products'),(3,'Food','Food products'),(4,'Clothing','Clothing products'),(6,'Grocery','Grocery products'),(9,'Furniture','Furniture products');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `CustomerId` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Phone` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Email` varchar(254) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Address` longtext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`CustomerId`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (2,'huk','45','zainadris4724@gmail.com','Katchery Road\r\nNear Anarkali Bazar'),(4,'sameer zaviyar','9238786996','sameer@gmail.com','gujranwala');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-08-26 08:55:05.005192','2','zain',1,'[{\"added\": {}}]',6,1),(2,'2026-08-26 09:00:31.943499','1','admin',2,'[{\"changed\": {\"fields\": [\"Username\"]}}]',6,1),(3,'2026-08-26 09:00:55.731821','1','admin',2,'[{\"changed\": {\"fields\": [\"Email address\", \"Role\"]}}]',6,1),(4,'2026-08-26 16:52:27.647468','3','ali',1,'[{\"added\": {}}]',6,1),(5,'2026-08-31 17:18:09.675242','3','ali',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',6,1),(6,'2026-08-31 17:22:00.054453','2','zain',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',6,1),(7,'2026-08-31 17:22:20.021436','2','manager',2,'[{\"changed\": {\"fields\": [\"Username\"]}}]',6,1),(8,'2026-08-31 17:22:58.991964','3','Ali',2,'[{\"changed\": {\"fields\": [\"Username\"]}}]',6,1),(9,'2026-09-09 04:42:15.515162','4','sameer',3,'',6,1),(10,'2026-10-08 14:56:20.345191','3','Ali',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',6,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (6,'accounts','user'),(1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'contenttypes','contenttype'),(17,'inventory','activitylog'),(7,'inventory','category'),(12,'inventory','customer'),(8,'inventory','product'),(13,'inventory','sale'),(14,'inventory','saledetail'),(15,'inventory','salereturn'),(16,'inventory','salereturndetail'),(9,'inventory','stockentry'),(10,'inventory','stockentrydetail'),(11,'inventory','supplier'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-08-26 08:40:33.082133'),(2,'contenttypes','0002_remove_content_type_name','2026-08-26 08:40:33.151483'),(3,'auth','0001_initial','2026-08-26 08:40:33.404681'),(4,'auth','0002_alter_permission_name_max_length','2026-08-26 08:40:33.450380'),(5,'auth','0003_alter_user_email_max_length','2026-08-26 08:40:33.458134'),(6,'auth','0004_alter_user_username_opts','2026-08-26 08:40:33.463839'),(7,'auth','0005_alter_user_last_login_null','2026-08-26 08:40:33.470770'),(8,'auth','0006_require_contenttypes_0002','2026-08-26 08:40:33.473457'),(9,'auth','0007_alter_validators_add_error_messages','2026-08-26 08:40:33.481824'),(10,'auth','0008_alter_user_username_max_length','2026-08-26 08:40:33.489083'),(11,'auth','0009_alter_user_last_name_max_length','2026-08-26 08:40:33.496469'),(12,'auth','0010_alter_group_name_max_length','2026-08-26 08:40:33.512452'),(13,'auth','0011_update_proxy_permissions','2026-08-26 08:40:33.520529'),(14,'auth','0012_alter_user_first_name_max_length','2026-08-26 08:40:33.526589'),(15,'accounts','0001_initial','2026-08-26 08:40:33.755592'),(16,'admin','0001_initial','2026-08-26 08:40:33.862826'),(17,'admin','0002_logentry_remove_auto_add','2026-08-26 08:40:33.871671'),(18,'admin','0003_logentry_add_action_flag_choices','2026-08-26 08:40:33.882018'),(19,'sessions','0001_initial','2026-08-26 08:40:33.913763'),(20,'inventory','0001_initial','2026-08-26 09:31:40.113941'),(21,'inventory','0002_stockentry_supplier_stockentrydetail_and_more','2026-08-27 19:05:55.714401'),(22,'inventory','0003_customer_sale_saledetail','2026-08-28 16:52:30.259464'),(23,'inventory','0004_alter_category_options_alter_customer_options_and_more','2026-08-31 17:04:10.667753'),(24,'inventory','0005_salereturn_salereturndetail','2026-10-03 12:38:56.513605'),(25,'inventory','0006_activitylog','2026-10-08 12:52:09.504978');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('3ec1hll1ba7utmbo891wysmrlqrn2p0q','.eJxVjMsOgjAQAP9lz6ZpF_ri6N1vaLbdrqAGEgon478bEg56nZnMGxLt25j2Vtc0MQxg4PLLMpVnnQ_BD5rviyrLvK1TVkeiTtvUbeH6up7t32CkNsIAnSAJsrG6GO9zYRZbbY8ozmH0obIPSF1nhWIfq7Au4iiKOAw6hwKfL_MaOHc:1x4AYE:_3lW4-0-j304SoZhOipbaFxKSYU_VnshxT-xQtAUxZo','2026-09-23 05:08:50.101342'),('ji2dm3mzstubckv2z7wxcxmmnl20nsxs','.eJxVjDEKwzAMAP-iuRjLTmyRsXvfECRbrtOWBOJkKv17CWRo17vj3jDyvtVxb7qOU4YBHFx-mXB66nyI_OD5vpi0zNs6iTkSc9pmbkvW1_Vs_waVW4UBCocSOieWkDoU8UFDIVWfHPc9dYQxO-uZLKp49CUSBoq2kHBBQvh8AdarN0E:1x0MCv:fkscGMVMe8OToGrFcmqKMHcEN6IBmOqmkd7VTJ1Xy9E','2026-09-12 16:47:05.869710'),('ogsrb114w2uyh5uchyu4ajjnbie0g53p','.eJxVjMsOgjAQAP9lz6ZpF_ri6N1vaLbdrqAGEgon478bEg56nZnMGxLt25j2Vtc0MQxg4PLLMpVnnQ_BD5rviyrLvK1TVkeiTtvUbeH6up7t32CkNsIAnSAJsrG6GO9zYRZbbY8ozmH0obIPSF1nhWIfq7Au4iiKOAw6hwKfL_MaOHc:1xGCrz:fsLz_2cwntfCB7sP3O361hNdOjTYnd9NYSpEqe-tALA','2026-10-26 10:02:59.586471'),('t4819aio2ofta8j5u6hj9cm33uuxccmn','.eJxVjMsOgjAQAP9lz6ZpF_ri6N1vaLbdrqAGEgon478bEg56nZnMGxLt25j2Vtc0MQxg4PLLMpVnnQ_BD5rviyrLvK1TVkeiTtvUbeH6up7t32CkNsIAnSAJsrG6GO9zYRZbbY8ozmH0obIPSF1nhWIfq7Au4iiKOAw6hwKfL_MaOHc:1x4CKx:QOqg-3w0SJArmcgyG6KHJbVDqaaLMweLXgnW3GIa-Gk','2026-09-23 07:03:15.222718');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `ProductId` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Barcode` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `CostPrice` decimal(12,2) NOT NULL,
  `UnitPrice` decimal(12,2) NOT NULL,
  `CurrentStock` int unsigned NOT NULL,
  `Status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Category_id` int NOT NULL,
  PRIMARY KEY (`ProductId`),
  UNIQUE KEY `Barcode` (`Barcode`),
  KEY `product_Category_id_bd3e5246_fk_category_CT_Id` (`Category_id`),
  CONSTRAINT `product_Category_id_bd3e5246_fk_category_CT_Id` FOREIGN KEY (`Category_id`) REFERENCES `category` (`CT_Id`),
  CONSTRAINT `product_chk_1` CHECK ((`CurrentStock` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (4,'bulb','76756',98.00,120.00,15,'Active',1),(5,'bulb','87867',453.00,80.00,10,'Inactive',9),(6,'fridge','234354',60000.00,90000.00,15,'Active',1),(7,'herbal','87654',700.00,789.00,0,'Active',3),(8,'coca cola','899778',70.00,85.00,3,'Active',3),(9,'glass','876765',45.00,90.00,90,'Active',6),(10,'switch','345456565',70.00,90.00,100,'Active',1),(11,'nimko','988787',50.00,60.00,13,'Inactive',3),(12,'chocolate','7658665',20.00,40.00,60,'Active',3);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sale`
--

DROP TABLE IF EXISTS `sale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sale` (
  `SaleId` int NOT NULL AUTO_INCREMENT,
  `SaleDate` datetime(6) NOT NULL,
  `TotalAmount` decimal(12,2) NOT NULL,
  `Remarks` longtext COLLATE utf8mb4_unicode_ci,
  `Customer_id` int NOT NULL,
  PRIMARY KEY (`SaleId`),
  KEY `sale_Customer_id_203b9e92_fk_customer_CustomerId` (`Customer_id`),
  CONSTRAINT `sale_Customer_id_203b9e92_fk_customer_CustomerId` FOREIGN KEY (`Customer_id`) REFERENCES `customer` (`CustomerId`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale`
--

LOCK TABLES `sale` WRITE;
/*!40000 ALTER TABLE `sale` DISABLE KEYS */;
INSERT INTO `sale` VALUES (1,'2026-08-29 13:27:48.044923',435.00,'asasa',2),(2,'2026-08-29 18:27:01.384757',18000.00,'jh',2),(3,'2026-08-29 18:53:24.776484',2268.00,'',2),(4,'2026-08-29 18:57:46.642114',2080000.00,'ss',2),(5,'2026-08-30 16:31:08.052277',63932.00,'zxzxzx',2),(6,'2026-08-30 16:39:04.981534',640360.00,'zzx',2),(7,'2026-08-31 13:18:51.795739',9070.00,'jhg',2),(8,'2026-10-04 14:50:52.374817',420.00,'hhwl',4),(9,'2026-10-10 14:31:58.618449',270000.00,'',2);
/*!40000 ALTER TABLE `sale` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sale_detail`
--

DROP TABLE IF EXISTS `sale_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sale_detail` (
  `SaleDetailId` int NOT NULL AUTO_INCREMENT,
  `Quantity` int unsigned NOT NULL,
  `SellingPrice` decimal(12,2) NOT NULL,
  `Total` decimal(12,2) NOT NULL,
  `Product_id` int NOT NULL,
  `Sale_id` int NOT NULL,
  PRIMARY KEY (`SaleDetailId`),
  KEY `sale_detail_Product_id_0f0d8bb1_fk_product_ProductId` (`Product_id`),
  KEY `sale_detail_Sale_id_19c37f71_fk_sale_SaleId` (`Sale_id`),
  CONSTRAINT `sale_detail_Product_id_0f0d8bb1_fk_product_ProductId` FOREIGN KEY (`Product_id`) REFERENCES `product` (`ProductId`),
  CONSTRAINT `sale_detail_Sale_id_19c37f71_fk_sale_SaleId` FOREIGN KEY (`Sale_id`) REFERENCES `sale` (`SaleId`),
  CONSTRAINT `sale_detail_chk_1` CHECK ((`Quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale_detail`
--

LOCK TABLES `sale_detail` WRITE;
/*!40000 ALTER TABLE `sale_detail` DISABLE KEYS */;
INSERT INTO `sale_detail` VALUES (1,5,87.00,435.00,4,1),(2,2,9000.00,18000.00,7,2),(3,4,567.00,2268.00,8,3),(4,20,9000.00,180000.00,6,4),(5,20,95000.00,1900000.00,7,4),(6,1,890.00,890.00,8,5),(7,7,9006.00,63042.00,7,5),(8,4,90.00,360.00,5,6),(9,8,80000.00,640000.00,6,6),(10,1,9070.00,9070.00,7,7),(11,6,70.00,420.00,9,8),(12,3,90000.00,270000.00,6,9);
/*!40000 ALTER TABLE `sale_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sale_return`
--

DROP TABLE IF EXISTS `sale_return`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sale_return` (
  `ReturnId` int NOT NULL AUTO_INCREMENT,
  `ReturnDate` datetime(6) NOT NULL,
  `TotalAmount` decimal(12,2) NOT NULL,
  `Remarks` longtext COLLATE utf8mb4_unicode_ci,
  `Sale_id` int NOT NULL,
  PRIMARY KEY (`ReturnId`),
  KEY `sale_return_Sale_id_64fdeca3_fk_sale_SaleId` (`Sale_id`),
  CONSTRAINT `sale_return_Sale_id_64fdeca3_fk_sale_SaleId` FOREIGN KEY (`Sale_id`) REFERENCES `sale` (`SaleId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale_return`
--

LOCK TABLES `sale_return` WRITE;
/*!40000 ALTER TABLE `sale_return` DISABLE KEYS */;
INSERT INTO `sale_return` VALUES (1,'2026-10-04 14:52:53.154238',210.00,'fracture glass',8),(2,'2026-10-04 14:54:17.540868',140.00,'low quality glass',8),(3,'2026-10-04 14:57:14.855015',70.00,'',8);
/*!40000 ALTER TABLE `sale_return` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sale_return_detail`
--

DROP TABLE IF EXISTS `sale_return_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sale_return_detail` (
  `ReturnDetailId` int NOT NULL AUTO_INCREMENT,
  `Quantity` int unsigned NOT NULL,
  `RefundAmount` decimal(12,2) NOT NULL,
  `SaleDetail_id` int NOT NULL,
  `SaleReturn_id` int NOT NULL,
  PRIMARY KEY (`ReturnDetailId`),
  KEY `sale_return_detail_SaleDetail_id_d630b75c_fk_sale_deta` (`SaleDetail_id`),
  KEY `sale_return_detail_SaleReturn_id_29369f94_fk_sale_retu` (`SaleReturn_id`),
  CONSTRAINT `sale_return_detail_SaleDetail_id_d630b75c_fk_sale_deta` FOREIGN KEY (`SaleDetail_id`) REFERENCES `sale_detail` (`SaleDetailId`),
  CONSTRAINT `sale_return_detail_SaleReturn_id_29369f94_fk_sale_retu` FOREIGN KEY (`SaleReturn_id`) REFERENCES `sale_return` (`ReturnId`),
  CONSTRAINT `sale_return_detail_chk_1` CHECK ((`Quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale_return_detail`
--

LOCK TABLES `sale_return_detail` WRITE;
/*!40000 ALTER TABLE `sale_return_detail` DISABLE KEYS */;
INSERT INTO `sale_return_detail` VALUES (1,3,210.00,11,1),(2,2,140.00,11,2),(3,1,70.00,11,3);
/*!40000 ALTER TABLE `sale_return_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_entry`
--

DROP TABLE IF EXISTS `stock_entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_entry` (
  `SE_Id` int NOT NULL AUTO_INCREMENT,
  `EntryDate` datetime(6) NOT NULL,
  `Cost` decimal(12,2) NOT NULL,
  `Remarks` longtext COLLATE utf8mb4_unicode_ci,
  `Supplier_id` int NOT NULL,
  PRIMARY KEY (`SE_Id`),
  KEY `stock_entry_Supplier_id_42168f45_fk_supplier_SupplierId` (`Supplier_id`),
  CONSTRAINT `stock_entry_Supplier_id_42168f45_fk_supplier_SupplierId` FOREIGN KEY (`Supplier_id`) REFERENCES `supplier` (`SupplierId`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_entry`
--

LOCK TABLES `stock_entry` WRITE;
/*!40000 ALTER TABLE `stock_entry` DISABLE KEYS */;
INSERT INTO `stock_entry` VALUES (1,'2026-08-28 15:53:09.343001',1812.00,'sdsdsdff',1),(2,'2026-08-28 15:58:30.941741',980.00,'added stock',1),(3,'2026-08-28 16:05:33.300305',109300.00,'sfdfd',1),(4,'2026-08-29 16:54:07.967609',456.00,'',1),(5,'2026-08-29 18:22:50.763746',48000.00,'',2);
/*!40000 ALTER TABLE `stock_entry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_entry_detail`
--

DROP TABLE IF EXISTS `stock_entry_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_entry_detail` (
  `SED_Id` int NOT NULL AUTO_INCREMENT,
  `Quantity` int unsigned NOT NULL,
  `PurchasePrice` decimal(12,2) NOT NULL,
  `Product_id` int NOT NULL,
  `StockEntry_id` int NOT NULL,
  PRIMARY KEY (`SED_Id`),
  KEY `stock_entry_detail_Product_id_d4a1f88e_fk_product_ProductId` (`Product_id`),
  KEY `stock_entry_detail_StockEntry_id_1ebc5bf8_fk_stock_entry_SE_Id` (`StockEntry_id`),
  CONSTRAINT `stock_entry_detail_Product_id_d4a1f88e_fk_product_ProductId` FOREIGN KEY (`Product_id`) REFERENCES `product` (`ProductId`),
  CONSTRAINT `stock_entry_detail_StockEntry_id_1ebc5bf8_fk_stock_entry_SE_Id` FOREIGN KEY (`StockEntry_id`) REFERENCES `stock_entry` (`SE_Id`),
  CONSTRAINT `stock_entry_detail_chk_1` CHECK ((`Quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_entry_detail`
--

LOCK TABLES `stock_entry_detail` WRITE;
/*!40000 ALTER TABLE `stock_entry_detail` DISABLE KEYS */;
INSERT INTO `stock_entry_detail` VALUES (1,4,453.00,5,1),(2,10,98.00,4,2),(3,20,5465.00,6,3),(4,6,76.00,6,4),(5,6,8000.00,7,5);
/*!40000 ALTER TABLE `stock_entry_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supplier`
--

DROP TABLE IF EXISTS `supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supplier` (
  `SupplierId` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Phone` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Email` varchar(254) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Address` longtext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`SupplierId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supplier`
--

LOCK TABLES `supplier` WRITE;
/*!40000 ALTER TABLE `supplier` DISABLE KEYS */;
INSERT INTO `supplier` VALUES (1,'ABC Traders','03001234567','abc@gmail.com','Lahore'),(2,'hadi','728394958','hadi@gmail.com','karachi'),(3,'Five star','9267765888','fivestar@gmail.com','lahore');
/*!40000 ALTER TABLE `supplier` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-12 15:20:10
