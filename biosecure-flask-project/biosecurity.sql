CREATE DATABASE  IF NOT EXISTS `biosecurity` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `biosecurity`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: biosecurity
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `mariner_profiles`
--

DROP TABLE IF EXISTS `mariner_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mariner_profiles` (
  `mariner_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `mariner_id_number` varchar(20) NOT NULL,
  `address` text NOT NULL,
  PRIMARY KEY (`mariner_id`),
  UNIQUE KEY `mariner_id_number` (`mariner_id_number`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `mariner_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mariner_profiles`
--

LOCK TABLES `mariner_profiles` WRITE;
/*!40000 ALTER TABLE `mariner_profiles` DISABLE KEYS */;
INSERT INTO `mariner_profiles` VALUES (6,1,'John','Sailor','M001','123 Ocean View, Seaport'),(7,2,'Emily','Waves','M002','456 Sea Breeze Ave, Baytown'),(8,3,'Alex','Deck','M003','789 Marina Blvd, Dockside'),(9,4,'Sarah','Sails','M004','321 Coral Lane, Starfish Bay'),(10,5,'Dave','Anchor','M005','654 Nautical Mile, Sailorville');
/*!40000 ALTER TABLE `mariner_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ocean_guide`
--

DROP TABLE IF EXISTS `ocean_guide`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ocean_guide` (
  `ocean_id` int NOT NULL AUTO_INCREMENT,
  `ocean_item_type` enum('pest','disease') NOT NULL,
  `present_in_NZ` tinyint(1) NOT NULL,
  `common_name` varchar(255) NOT NULL,
  `scientific_name` varchar(255) DEFAULT NULL,
  `key_characteristics` text,
  `biology_description` text,
  `threats` text,
  `location` text,
  `primary_image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ocean_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocean_guide`
--

LOCK TABLES `ocean_guide` WRITE;
/*!40000 ALTER TABLE `ocean_guide` DISABLE KEYS */;
INSERT INTO `ocean_guide` VALUES (1,'pest',0,'Asian Clam','Corbicula fluminea','Small, triangular shell with distinct concentric ridges.','Native to Asia, it has been introduced to various freshwater and brackish habitats worldwide.','Competes with native species, alters habitats, impacts water quality.','Freshwater and brackish habitats globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\1Asian_clam.png'),(2,'pest',0,'Chinese Mitten Crab','Eriocheir sinensis','Hairy claws, brownish-green carapace with a distinct notch.','Native to East Asia, it has been introduced to other regions through ballast water and aquaculture.','Disrupts ecosystems, damages infrastructure, competes with native species.','Freshwater and estuarine habitats globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\2Chinese_mitten_crab.png'),(3,'pest',0,'European Shore Crab','Carcinus maenas','Greenish-brown carapace with five spines on each side, often found in intertidal zones.','Native to Europe, it has been introduced to various regions globally, often through ballast water.','Competes with native crabs, preys on native species, disrupts ecosystems.','Intertidal zones globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\3European_shore_crab.png'),(4,'pest',0,'Northern Pacific Seastar','Asterias amurensis','Five arms with distinct spines, coloration varies from orange to brownish-red.','Native to the northern Pacific, it has become invasive in parts of Australia and New Zealand, preying on native species.','Predation on native species, alters ecosystems.','Coastal waters of the northern Pacific and invasive in Australia and New Zealand.','D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\4Northern_Pacific_Seastar.png'),(5,'pest',0,'Asian Green Mussel','Perna viridis','Green shell with greenish-yellow lips, often forming dense aggregations.','Native to the Indo-Pacific, it has been introduced to other regions through shipping and aquaculture.','Competes with native species, alters habitats, impacts aquaculture.','Coastal waters globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\5Asian_green mussel.jpg'),(6,'pest',0,'Lionfish','Pterois volitans','Striking red and white stripes, fan-like pectoral fins, and venomous spines.','Native to the Indo-Pacific, they have become invasive in the western Atlantic, Caribbean, and Gulf of Mexico.','Predation on native species, disrupts ecosystems.','Invasive in the western Atlantic, Caribbean, and Gulf of Mexico.','D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\6Lionfish.jpg'),(7,'disease',0,'White Plague','Vibrio spp.','Infectious coral disease causing tissue loss and skeletal damage.','White Plague is a coral disease affecting various species worldwide, leading to significant coral mortality.','Coral reef degradation, loss of biodiversity.','Coral reef ecosystems globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\7White_plague.jpg'),(8,'disease',0,'Stony Coral Tissue Disease','Various bacteria','Infectious coral disease causing rapid tissue loss and mortality.','Stony Coral Tissue Disease is a significant threat to coral reefs, affecting various species globally.','Coral reef degradation, loss of biodiversity.','Coral reef ecosystems globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\8Stony_coral_tissue.jpg'),(9,'pest',1,'Aquarium Caulerpa','Caulerpa taxifolia','Invasive green algae with distinct fronds resembling ferns.','Native to the Indian Ocean, it was introduced to aquariums and has spread to various marine environments, forming dense mats that outcompete native species.','Displacement of native species, alteration of habitats.','Various marine environments globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\1Aquarium_Caulerpa.png'),(10,'pest',1,'Asian Date Mussel','Musculista senhousia','Small bivalve mollusk with a dark brown shell, often forming dense aggregations.','Native to the western Pacific, it has been introduced to many areas worldwide, often as a fouling organism on ships.','Competes with native species, alters habitats, impacts aquaculture.','Coastal waters globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\2Asian_date_mussel.jpg'),(11,'pest',1,'Asian Paddle Crab','Charybdis japonica','Distinctive paddle-shaped rear legs, brown carapace with lighter markings.','Native to the western Pacific, it has spread to other regions through ballast water and aquaculture.','Competes with native crabs, preys on native species, disrupts ecosystems.','Coastal waters of the Pacific, Indian Ocean, and parts of the Atlantic.','D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\3Asian_paddle_crab.jpg'),(12,'pest',1,'Australian Droplet Tunicate','Eudistoma elongatum','Gelatinous, translucent body with droplet-like structures.','Native to Australia, it has spread to other regions through shipping and aquaculture.','Fouling of structures, displacement of native species.','Coastal waters globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\4Australian_droplet_tunicate.jpg'),(13,'pest',1,'Clubbed Tunicate','Styela clava','Thick, club-shaped body with a tough, wrinkled texture.','Native to the northwest Pacific, it has spread widely as a fouling organism.','Fouling of structures, displacement of native species.','Coastal waters globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\5Clubbed_Tunicate.jpg'),(14,'pest',1,'Mediterranean Fanworm','Sabella spallanzanii','Feathery fan-like feeding tentacles, segmented body with a tube-like structure.','Native to the Mediterranean, it has spread globally through ship fouling.','Competes with native species, alters habitats, impacts aquaculture.','Coastal waters globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\6Mediterranean_fanworm.jpg'),(15,'pest',1,'Wakame Asian Kelp','Undaria pinnatifida','Brown algae with long, strap-like fronds and a central rib.','Native to East Asia, it has been introduced to other regions as a fouling organism and through aquaculture.','Displaces native species, alters habitats, impacts aquaculture.','Coastal waters globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\7Wakame_Asian_Kelp.jpg'),(16,'pest',1,'Black-spined Sea Urchin','Centrostephanus rodgersii','Black spines covering the test (shell), usually found in aggregations.','Native to Australia, it has become invasive in some regions, impacting kelp forests and other marine ecosystems.','Overgrazing of kelp, habitat alteration.','Coastal waters of Australia and some parts of New Zealand.','D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\8Black-spined_sea_urchin.jpg'),(17,'disease',1,'Bonamia Ostreae','Bonamia ostreae','Parasitic protist affecting oysters, leading to reduced reproductive success and increased mortality.','Infects native oysters, impacting wild and farmed populations.','Declines in oyster populations, economic losses for shellfish industries.','Found in various oyster habitats globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\9Bonamia_ostreae.jpg'),(18,'pest',1,'Green-lipped Mussel Pest','Perna viridis','Green shell with distinctive green lips, often forming dense aggregations.','Native to the Indo-Pacific, it has been introduced to other regions through shipping and aquaculture.','Competes with native species, alters habitats, impacts aquaculture.','Coastal waters globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\10Green-lipped_mussel_pest.jpg'),(19,'pest',1,'Mediterranean Mussel','Mytilus galloprovincialis','Blue-black shell, often forming dense colonies on hard surfaces.','Native to the Mediterranean, it has been introduced to many regions worldwide as a fouling organism.','Displaces native species, alters habitats, impacts aquaculture.','Coastal waters globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\11Mediterranean_mussel.jpg'),(20,'pest',1,'Undaria Seaweed','Undaria pinnatifida','Large brown algae with a distinct midrib and branching fronds.','Native to East Asia, it has spread globally as a fouling organism and through aquaculture.','Displaces native species, alters habitats, impacts aquaculture.','Coastal waters globally.','D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\12Undaria_Seaweed.jpg');
/*!40000 ALTER TABLE `ocean_guide` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ocean_images`
--

DROP TABLE IF EXISTS `ocean_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ocean_images` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `ocean_id` int NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `is_primary` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`image_id`),
  KEY `ocean_id` (`ocean_id`),
  CONSTRAINT `ocean_images_ibfk_1` FOREIGN KEY (`ocean_id`) REFERENCES `ocean_guide` (`ocean_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocean_images`
--

LOCK TABLES `ocean_images` WRITE;
/*!40000 ALTER TABLE `ocean_images` DISABLE KEYS */;
INSERT INTO `ocean_images` VALUES (1,1,'D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\1Asian_clam.png',1),(2,2,'D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\2Chinese_mitten_crab.png',1),(3,3,'D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\3European_shore_crab.png',1),(4,4,'D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\4Northern_Pacific_Seastar.png',1),(5,5,'D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\5Asian_green mussel.jpg',1),(6,6,'D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\6Lionfish.jpg',1),(7,7,'D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\7White_plague.jpg',1),(8,8,'D:\\Biosecurity\\biosecure-flask-project\\static\\non_nz_pest\\8Stony_coral_tissue.jpg',1),(9,9,'D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\1Aquarium_Caulerpa.png',1),(10,10,'D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\2Asian_date_mussel.jpg',1),(11,11,'D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\3Asian_paddle_crab.jpg',1),(12,12,'D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\4Australian_droplet_tunicate.jpg',1),(13,13,'D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\5Clubbed_Tunicate.jpg',1),(14,14,'D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\6Mediterranean_fanworm.jpg',1),(15,15,'D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\7Wakame_Asian_Kelp.jpg',1),(16,16,'D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\8Black-spined_sea_urchin.jpg',1),(17,17,'D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\9Bonamia_ostreae.jpg',1),(18,18,'D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\10Green-lipped_mussel_pest.jpg',1),(19,19,'D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\11Mediterranean_mussel.jpg',1),(20,20,'D:\\Biosecurity\\biosecure-flask-project\\static\\nz_pest\\12Undaria_Seaweed.jpg',1);
/*!40000 ALTER TABLE `ocean_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role_name` enum('mariner','staff','admin') NOT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'mariner'),(2,'staff'),(3,'admin');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff_admin_profiles`
--

DROP TABLE IF EXISTS `staff_admin_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff_admin_profiles` (
  `staff_admin_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `staff_number` varchar(20) NOT NULL,
  `work_phone` varchar(20) DEFAULT NULL,
  `hire_date` date NOT NULL,
  `position` varchar(255) DEFAULT NULL,
  `department` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`staff_admin_id`),
  UNIQUE KEY `staff_number` (`staff_number`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `staff_admin_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_admin_profiles`
--

LOCK TABLES `staff_admin_profiles` WRITE;
/*!40000 ALTER TABLE `staff_admin_profiles` DISABLE KEYS */;
INSERT INTO `staff_admin_profiles` VALUES (1,7,'Laura','Anchor','S001','123-456-7897','2023-07-10','Researcher','Marine Biology'),(2,8,'Tom','Fisher','S002','123-456-7898','2023-08-15','Coordinator','Marine Conservation'),(3,9,'Boss','Admin','A001','987-654-3333','2023-01-01','Administrator','Management'),(8,6,'Eric','Marine','S004','123-456-7896','2023-01-05','Marine Specialist','Research and Development');
/*!40000 ALTER TABLE `staff_admin_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role_id` int NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `status` enum('active','inactive') NOT NULL,
  `date_joined` date NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'johnsailor','hashed_password',1,'john.sailor@example.com','123-456-7890','active','2024-03-01'),(2,'emilywaves','hashed_password',1,'emily.waves@example.com','123-456-7891','active','2024-03-02'),(3,'alexdeck','hashed_password',1,'alex.deck@example.com','123-456-7892','active','2024-03-03'),(4,'sarahsails','hashed_password',1,'sarah.sails@example.com','123-456-7893','active','2024-03-04'),(5,'daveanchor','hashed_password',1,'dave.anchor@example.com','123-456-7894','active','2024-03-05'),(6,'ericmarine','hashed_password',2,'eric.marine@example.com','123-456-7896','active','2024-03-07'),(7,'lauraanchor','hashed_password',2,'laura.anchor@example.com','123-456-7897','active','2024-03-08'),(8,'tomfisher','hashed_password',2,'tom.fisher@example.com','123-456-7898','active','2024-03-09'),(9,'adminboss','hashed_password',3,'boss.admin@example.com','987-654-3333','active','2024-02-03');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-13  1:01:43
