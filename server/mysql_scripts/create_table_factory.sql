
CREATE TABLE `bonus_koeficient` (
  `percentage_of_profits` decimal(5,2) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `posts` (
  `id_post` int NOT NULL AUTO_INCREMENT,
  `label_post` varchar(45) NOT NULL,
  PRIMARY KEY (`id_post`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `department` (
  `id_department` int NOT NULL AUTO_INCREMENT,
  `title` varchar(45) NOT NULL,
  PRIMARY KEY (`id_department`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `conf_criterion` (
  `id_criterion` int NOT NULL AUTO_INCREMENT,
  `title_criterion` varchar(45) DEFAULT NULL,
  `max_coef` int unsigned NOT NULL,
  `w_coef` decimal(5,2) unsigned NOT NULL,
  PRIMARY KEY (`id_criterion`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `status` (
  `id_status` int NOT NULL AUTO_INCREMENT,
  `status` varchar(45) NOT NULL,
  PRIMARY KEY (`id_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `client` (
  `id_client` int NOT NULL AUTO_INCREMENT,
  `title_client` varchar(45) NOT NULL,
  PRIMARY KEY (`id_client`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


CREATE TABLE `project` (
  `id_project` int NOT NULL AUTO_INCREMENT,
  `title_project` varchar(45) NOT NULL,
  `id_client` int NOT NULL,
  `begin_date` date DEFAULT NULL,
  `finish_date` date DEFAULT NULL,
  `id_status` int DEFAULT NULL,
  `price_project` int unsigned NOT NULL,
  PRIMARY KEY (`id_project`),
  KEY `fk_id_client_idx` (`id_client`),
  KEY `fk_id_status_idx` (`id_status`),
  CONSTRAINT `fk_id_client` FOREIGN KEY (`id_client`) REFERENCES `client` (`id_client`),
  CONSTRAINT `fk_id_status` FOREIGN KEY (`id_status`) REFERENCES `status` (`id_status`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


CREATE TABLE `data_personal` (
  `id_personal` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `education` varchar(45) DEFAULT NULL,
  `number` varchar(45) NOT NULL,
  `certification` int unsigned DEFAULT NULL,
  `id_post` int NOT NULL,
  `id_department` int DEFAULT NULL,
  `salaryl` int unsigned NOT NULL,
  `bonus` int unsigned NOT NULL,
  PRIMARY KEY (`id_personal`),
  KEY `fk_id_post_idx` (`id_post`),
  KEY `fk_id_department` (`id_department`),
  CONSTRAINT `fk_id_department` FOREIGN KEY (`id_department`) REFERENCES `department` (`id_department`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `fk_id_post` FOREIGN KEY (`id_post`) REFERENCES `posts` (`id_post`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `progress_now` (
  `id_progress` int NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `id_name_personal` int NOT NULL,
  `id_title_project` int NOT NULL,
  `task` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_progress`),
  KEY `fk_id_project_idx` (`id_title_project`,`id_name_personal`),
  KEY `fk_id_name_idx` (`id_name_personal`),
  CONSTRAINT `fk_id_name` FOREIGN KEY (`id_name_personal`) REFERENCES `data_personal` (`id_personal`),
  CONSTRAINT `fk_id_project` FOREIGN KEY (`id_title_project`) REFERENCES `project` (`id_project`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `progress_mean` (
  `id_progress` int NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `id_name_personal` int NOT NULL,
  `id_title_project` int NOT NULL,
  `task` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_progress`),
  KEY `fk_id_name_idx` (`id_name_personal`),
  KEY `fk_id_project_idx` (`id_title_project`),
  CONSTRAINT `fi_is_name` FOREIGN KEY (`id_name_personal`) REFERENCES `data_personal` (`id_personal`),
  CONSTRAINT `fk_project` FOREIGN KEY (`id_title_project`) REFERENCES `project` (`id_project`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;






