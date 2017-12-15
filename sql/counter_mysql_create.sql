CREATE TABLE `drivers` (
	`id` int NOT NULL AUTO_INCREMENT UNIQUE,
	`name` char(150) NOT NULL UNIQUE,
	`phone` bigint,
	`email` char(100),
	`comment` TEXT(250),
	`photo` int,
	`transport` int NOT NULL,
	`employer` int NOT NULL,
	`rfid` bigint,
	PRIMARY KEY (`id`)
);

CREATE TABLE `transport` (
	`id` int NOT NULL AUTO_INCREMENT UNIQUE,
	`model` int NOT NULL,
	`plate` char(10) NOT NULL,
	`trailer` char(10),
	`avg_gross` FLOAT,
	`avg_tare` FLOAT,
	`owner` int NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `trips` (
	`id` int NOT NULL AUTO_INCREMENT,
	`trip` int NOT NULL,
	`driver` int NOT NULL,
	`transport` int NOT NULL,
	`supplier` int NOT NULL,
	`loadpoint` int NOT NULL,
	`load_dt` DATETIME(6),
	`arrival_dt` DATETIME(6),
	`arrival_photo` int,
	`unload_send` int,
	`unload_fact` int,
	`unload_dt` DATETIME(6),
	`unloaders` int,
	`gross_weight` FLOAT,
	`gross_dt` DATETIME(6),
	`gross_photo` int,
	`tare_weight` FLOAT,
	`tare_dt` DATETIME(6),
	`tare_photo` int,
	`net_weight` FLOAT,
	`sample` int,
	`clear_weight` FLOAT,
	PRIMARY KEY (`id`)
);

CREATE TABLE `loadpoints` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` char(50) NOT NULL,
	`location` char(150),
	`coordinates` char(100),
	`supplier` int NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `unloadpoints` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` char(250) NOT NULL,
	`type` char(100) NOT NULL,
	`preffered_truck_type` int,
	PRIMARY KEY (`id`)
);

CREATE TABLE `samples` (
	`id` int NOT NULL AUTO_INCREMENT,
	`refuse` FLOAT,
	`polarisation` FLOAT,
	`k` FLOAT,
	`n` FLOAT,
	`an` FLOAT,
	PRIMARY KEY (`id`)
);

CREATE TABLE `unloaders` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` char(150) NOT NULL,
	`assistant1` char(150),
	`assistant2` char(150),
	`assistant3` char(150),
	`unload_point` int,
	`rfid` bigint,
	PRIMARY KEY (`id`)
);

CREATE TABLE `photos` (
	`id` int NOT NULL AUTO_INCREMENT,
	`photo` TEXT(1000),
	PRIMARY KEY (`id`)
);

CREATE TABLE `suppliers` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` char(100) NOT NULL UNIQUE,
	`full_name` char(255) NOT NULL,
	`region` int NOT NULL,
	`email` char(150),
	`phone` bigint,
	`requisites` TEXT(1000),
	`transporter_only` bool NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`)
);

CREATE TABLE `regions` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` char(150) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `transport_models` (
	`id` int NOT NULL AUTO_INCREMENT,
	`model_name` char(255) NOT NULL,
	`type` int,
	PRIMARY KEY (`id`)
);

CREATE TABLE `transport_types` (
	`id` int NOT NULL AUTO_INCREMENT,
	`type_name` char(255),
	PRIMARY KEY (`id`)
);

ALTER TABLE `drivers` ADD CONSTRAINT `drivers_fk0` FOREIGN KEY (`photo`) REFERENCES `photos`(`id`);

ALTER TABLE `drivers` ADD CONSTRAINT `drivers_fk1` FOREIGN KEY (`transport`) REFERENCES `transport`(`id`);

ALTER TABLE `drivers` ADD CONSTRAINT `drivers_fk2` FOREIGN KEY (`employer`) REFERENCES `suppliers`(`id`);

ALTER TABLE `transport` ADD CONSTRAINT `transport_fk0` FOREIGN KEY (`model`) REFERENCES `transport_models`(`id`);

ALTER TABLE `transport` ADD CONSTRAINT `transport_fk1` FOREIGN KEY (`owner`) REFERENCES `suppliers`(`id`);

ALTER TABLE `trips` ADD CONSTRAINT `trips_fk0` FOREIGN KEY (`driver`) REFERENCES `drivers`(`id`);

ALTER TABLE `trips` ADD CONSTRAINT `trips_fk1` FOREIGN KEY (`transport`) REFERENCES `transport`(`id`);

ALTER TABLE `trips` ADD CONSTRAINT `trips_fk2` FOREIGN KEY (`supplier`) REFERENCES `suppliers`(`id`);

ALTER TABLE `trips` ADD CONSTRAINT `trips_fk3` FOREIGN KEY (`loadpoint`) REFERENCES `loadpoints`(`id`);

ALTER TABLE `trips` ADD CONSTRAINT `trips_fk4` FOREIGN KEY (`arrival_photo`) REFERENCES `photos`(`id`);

ALTER TABLE `trips` ADD CONSTRAINT `trips_fk5` FOREIGN KEY (`unload_send`) REFERENCES `unloadpoints`(`id`);

ALTER TABLE `trips` ADD CONSTRAINT `trips_fk6` FOREIGN KEY (`unload_fact`) REFERENCES `unloadpoints`(`id`);

ALTER TABLE `trips` ADD CONSTRAINT `trips_fk7` FOREIGN KEY (`unloaders`) REFERENCES `unloaders`(`id`);

ALTER TABLE `trips` ADD CONSTRAINT `trips_fk8` FOREIGN KEY (`gross_photo`) REFERENCES `photos`(`id`);

ALTER TABLE `trips` ADD CONSTRAINT `trips_fk9` FOREIGN KEY (`tare_photo`) REFERENCES `photos`(`id`);

ALTER TABLE `trips` ADD CONSTRAINT `trips_fk10` FOREIGN KEY (`sample`) REFERENCES `samples`(`id`);

ALTER TABLE `loadpoints` ADD CONSTRAINT `loadpoints_fk0` FOREIGN KEY (`supplier`) REFERENCES `suppliers`(`id`);

ALTER TABLE `unloadpoints` ADD CONSTRAINT `unloadpoints_fk0` FOREIGN KEY (`preffered_truck_type`) REFERENCES `transport_types`(`id`);

ALTER TABLE `unloaders` ADD CONSTRAINT `unloaders_fk0` FOREIGN KEY (`unload_point`) REFERENCES `unloadpoints`(`id`);

ALTER TABLE `suppliers` ADD CONSTRAINT `suppliers_fk0` FOREIGN KEY (`region`) REFERENCES `regions`(`id`);

ALTER TABLE `transport_models` ADD CONSTRAINT `transport_models_fk0` FOREIGN KEY (`type`) REFERENCES `transport_types`(`id`);
