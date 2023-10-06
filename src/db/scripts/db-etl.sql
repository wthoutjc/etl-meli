USE etl_meli
;

SET FOREIGN_KEY_CHECKS=0
;

DROP TABLE IF EXISTS `Categories` CASCADE
;

DROP TABLE IF EXISTS `Locations` CASCADE
;

DROP TABLE IF EXISTS `Product_Details` CASCADE
;

DROP TABLE IF EXISTS `Products` CASCADE
;

DROP TABLE IF EXISTS `Sellers` CASCADE
;

DROP TABLE IF EXISTS `Text_analysis` CASCADE
;

CREATE TABLE `Categories`
(
	`k_categories` VARCHAR(50) NOT NULL,
	`name` VARCHAR(50) NOT NULL,
	CONSTRAINT `PK_Categories` PRIMARY KEY (`k_categories` ASC)
)

;

CREATE TABLE `Locations`
(
	`city` VARCHAR(50) NOT NULL,
	`department` VARCHAR(50) NOT NULL,
	`country` VARCHAR(50) NOT NULL,
	CONSTRAINT `PK_Locations` PRIMARY KEY (`city` ASC)
)

;

CREATE TABLE `Product_Details`
(
	`k_product_details` BIGINT NOT NULL AUTO_INCREMENT,
	`date` DATETIME NOT NULL,
	`amount_sold` BIGINT NOT NULL,
	`available_quantity` BIGINT NOT NULL,
	`k_products` VARCHAR(50) NOT NULL,
	`k_sellers` BIGINT NOT NULL,
	CONSTRAINT `PK_Product_Details` PRIMARY KEY (`k_product_details` ASC)
)

;

CREATE TABLE `Products`
(
	`k_products` VARCHAR(50) NOT NULL,
	`name` VARCHAR(50) NOT NULL,
	`price` BIGINT NOT NULL,
	`condition` VARCHAR(50) NOT NULL,
	`k_categories` VARCHAR(50) NOT NULL,
	CONSTRAINT `PK_Products` PRIMARY KEY (`k_products` ASC)
)

;

CREATE TABLE `Sellers`
(
	`k_sellers` BIGINT NOT NULL,
	`name` VARCHAR(50) NOT NULL,
	`rating` DECIMAL(2,2) NOT NULL,
	`city` VARCHAR(50) NULL,
	CONSTRAINT `PK_Sellers` PRIMARY KEY (`k_sellers` ASC)
)

;

CREATE TABLE `Text_analysis`
(
	`k_text_analysis` BIGINT NOT NULL,
	`analysis` BIGINT NOT NULL,
	`k_products` VARCHAR(50) NULL,
	CONSTRAINT `PK_Text_analysis` PRIMARY KEY (`k_text_analysis` ASC)
)

;

ALTER TABLE `Product_Details` 
 ADD INDEX `IXFK_Product_Details_Products` (`k_products` ASC)
;

ALTER TABLE `Product_Details` 
 ADD INDEX `IXFK_Product_Details_Sellers` (`k_sellers` ASC)
;

ALTER TABLE `Products` 
 ADD INDEX `IXFK_Products_Categories` (`k_categories` ASC)
;

ALTER TABLE `Sellers` 
 ADD INDEX `IXFK_Sellers_Locations` (`city` ASC)
;

ALTER TABLE `Text_analysis` 
 ADD INDEX `IXFK_Text_analysis_Products` (`k_products` ASC)
;

ALTER TABLE `Product_Details` 
 ADD CONSTRAINT `FK_Product_Details_Products`
	FOREIGN KEY (`k_products`) REFERENCES `Products` (`k_products`) ON DELETE Restrict ON UPDATE Restrict
;

ALTER TABLE `Product_Details` 
 ADD CONSTRAINT `FK_Product_Details_Sellers`
	FOREIGN KEY (`k_sellers`) REFERENCES `Sellers` (`k_sellers`) ON DELETE Restrict ON UPDATE Restrict
;

ALTER TABLE `Products` 
 ADD CONSTRAINT `FK_Products_Categories`
	FOREIGN KEY (`k_categories`) REFERENCES `Categories` (`k_categories`) ON DELETE Restrict ON UPDATE Restrict
;

ALTER TABLE `Sellers` 
 ADD CONSTRAINT `FK_Sellers_Locations`
	FOREIGN KEY (`city`) REFERENCES `Locations` (`city`) ON DELETE Restrict ON UPDATE Restrict
;

ALTER TABLE `Text_analysis` 
 ADD CONSTRAINT `FK_Text_analysis_Products`
	FOREIGN KEY (`k_products`) REFERENCES `Products` (`k_products`) ON DELETE Restrict ON UPDATE Restrict
;

SET FOREIGN_KEY_CHECKS=1
;

