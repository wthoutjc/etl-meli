SET FOREIGN_KEY_CHECKS=0
;

DROP TABLE IF EXISTS `Categories` CASCADE
;

DROP TABLE IF EXISTS `Locations` CASCADE
;

DROP TABLE IF EXISTS `Products` CASCADE
;

DROP TABLE IF EXISTS `Sales` CASCADE
;

DROP TABLE IF EXISTS `Sellers` CASCADE
;

DROP TABLE IF EXISTS `Text_analysis` CASCADE
;

CREATE TABLE `Categories`
(
	`k_categories` BIGINT NOT NULL,
	`name` VARCHAR(50) NOT NULL,
	`k_products` BIGINT NULL,
	CONSTRAINT `PK_Categories` PRIMARY KEY (`k_categories` ASC)
)

;

CREATE TABLE `Locations`
(
	`k_locations` BIGINT NOT NULL,
	`city` VARCHAR(50) NOT NULL,
	`department` VARCHAR(50) NOT NULL,
	CONSTRAINT `PK_Locations` PRIMARY KEY (`k_locations` ASC)
)

;

CREATE TABLE `Products`
(
	`k_products` BIGINT NOT NULL,
	`name` VARCHAR(50) NOT NULL,
	`description` VARCHAR(250) NOT NULL,
	`price` BIGINT NOT NULL,
	`condition` VARCHAR(50) NOT NULL,
	`k_categories` BIGINT NULL,
	CONSTRAINT `PK_Products` PRIMARY KEY (`k_products` ASC)
)

;

CREATE TABLE `Sales`
(
	`k_sales` BIGINT NOT NULL,
	`date` DATETIME NOT NULL,
	`amount_sold` BIGINT NOT NULL,
	`k_locations` BIGINT NULL,
	`k_products` BIGINT NULL,
	`k_sellers` BIGINT NULL,
	CONSTRAINT `PK_Sales` PRIMARY KEY (`k_sales` ASC)
)

;

CREATE TABLE `Sellers`
(
	`k_sellers` BIGINT NOT NULL,
	`name` VARCHAR(50) NOT NULL,
	`rating` BIGINT NOT NULL,
	`k_locations` BIGINT NULL,
	CONSTRAINT `PK_Sellers` PRIMARY KEY (`k_sellers` ASC)
)

;

CREATE TABLE `Text_analysis`
(
	`k_text_analysis` BIGINT NOT NULL,
	`analysis` BIGINT NOT NULL,
	`k_products` BIGINT NULL,
	CONSTRAINT `PK_Text_analysis` PRIMARY KEY (`k_text_analysis` ASC)
)

;

ALTER TABLE `Products` 
 ADD INDEX `IXFK_Products_Categories` (`k_categories` ASC)
;

ALTER TABLE `Sales` 
 ADD INDEX `IXFK_Sales_Products` (`k_products` ASC)
;

ALTER TABLE `Sales` 
 ADD INDEX `IXFK_Sales_Sellers` (`k_sellers` ASC)
;

ALTER TABLE `Sellers` 
 ADD INDEX `IXFK_Sellers_Locations` (`k_locations` ASC)
;

ALTER TABLE `Text_analysis` 
 ADD INDEX `IXFK_Text_analysis_Products` (`k_products` ASC)
;

ALTER TABLE `Products` 
 ADD CONSTRAINT `FK_Products_Categories`
	FOREIGN KEY (`k_categories`) REFERENCES `Categories` (`k_categories`) ON DELETE Restrict ON UPDATE Restrict
;

ALTER TABLE `Sales` 
 ADD CONSTRAINT `FK_Sales_Products`
	FOREIGN KEY (`k_products`) REFERENCES `Products` (`k_products`) ON DELETE Restrict ON UPDATE Restrict
;

ALTER TABLE `Sales` 
 ADD CONSTRAINT `FK_Sales_Sellers`
	FOREIGN KEY (`k_sellers`) REFERENCES `Sellers` (`k_sellers`) ON DELETE Restrict ON UPDATE Restrict
;

ALTER TABLE `Sellers` 
 ADD CONSTRAINT `FK_Sellers_Locations`
	FOREIGN KEY (`k_locations`) REFERENCES `Locations` (`k_locations`) ON DELETE Restrict ON UPDATE Restrict
;

ALTER TABLE `Text_analysis` 
 ADD CONSTRAINT `FK_Text_analysis_Products`
	FOREIGN KEY (`k_products`) REFERENCES `Products` (`k_products`) ON DELETE Restrict ON UPDATE Restrict
;

SET FOREIGN_KEY_CHECKS=1
;

