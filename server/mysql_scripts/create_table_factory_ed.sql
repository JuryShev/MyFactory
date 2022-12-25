CREATE TABLE `department` (
  `id_department` int NOT NULL AUTO_INCREMENT,
  `title` varchar(45) NOT NULL,
  PRIMARY KEY (`id_department`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `bonus_koeficient` (
  `id_bonus_koeficient` int NOT NULL AUTO_INCREMENT,
  `percentage_of_profits` decimal(5,2) unsigned NOT NULL,
  PRIMARY KEY (`id_bonus_koeficient`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
CREATE TABLE `drop_criterion` (
  `id_drop_criterion` int NOT NULL,
  `title_drop_criterion` varchar(100) DEFAULT NULL,
  `max_coef` int DEFAULT NULL,
  `w_coef` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_drop_criterion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `conf_criterion` (
  `id_conf_criterion` int NOT NULL AUTO_INCREMENT,
  `title_criterion` varchar(45) DEFAULT NULL,
  `max_coef` int unsigned NOT NULL,
  `w_coef` decimal(5,2) unsigned NOT NULL,
  PRIMARY KEY (`id_conf_criterion`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
CREATE TABLE `posts` (
  `id_posts` int NOT NULL AUTO_INCREMENT,
  `label_post` varchar(45) NOT NULL,
  PRIMARY KEY (`id_posts`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `personal` (
  `id_personal` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `education` varchar(45) DEFAULT NULL,
  `number` varchar(45) NOT NULL,
  `certification` int unsigned DEFAULT NULL,
  `id_posts` int NOT NULL,
  `id_department` int DEFAULT NULL,
  `salaryl` int unsigned NOT NULL,
  `bonus` int unsigned NOT NULL,
  `dir_avatar` varchar(100) DEFAULT NULL,
  `birthday` varchar(45) DEFAULT NULL,
  `created_pers` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `personal_arch` int DEFAULT '0',
  PRIMARY KEY (`id_personal`),
  KEY `fk_id_post_idx` (`id_posts`),
  KEY `fk_id_department` (`id_department`),
  CONSTRAINT `fk_id_department` FOREIGN KEY (`id_department`) REFERENCES `department` (`id_department`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `fk_id_post` FOREIGN KEY (`id_posts`) REFERENCES `posts` (`id_posts`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `rules` (
  `id_rules` int NOT NULL AUTO_INCREMENT,
  `title_rule` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_rules`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `users` (
  `id_users` int NOT NULL AUTO_INCREMENT,
  `id_personal` int NOT NULL,
  `nickname` varchar(45) NOT NULL,
  `password` varchar(70) NOT NULL,
  `salt_user` varchar(70) NOT NULL,
  `salt_server` varchar(70) NOT NULL,
  `right_user` varchar(45) NOT NULL,
  PRIMARY KEY (`id_users`),
  KEY `fk_id_personal_idx` (`id_personal`),
  CONSTRAINT `fk_id_personal` FOREIGN KEY (`id_personal`) REFERENCES `personal` (`id_personal`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `access_rule` (

  `id_access_rule` int NOT NULL AUTO_INCREMENT,
  `id_users` int NOT NULL,
  `id_rule` int NOT NULL,
  PRIMARY KEY (`id_access_rule`),
  KEY `key_rule_idx` (`id_rule`),
  KEY `key_nickname_idx` (`id_users`),
  CONSTRAINT `key_nickname` FOREIGN KEY (`id_users`) REFERENCES `users` (`id_users`) ON DELETE CASCADE,
  CONSTRAINT `key_rule` FOREIGN KEY (`id_rule`) REFERENCES `rules` (`id_rules`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `client` (
  `id_client` int NOT NULL AUTO_INCREMENT,
  `title_client` varchar(45) NOT NULL,
  PRIMARY KEY (`id_client`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `status` (
  `id_status` int NOT NULL AUTO_INCREMENT,
  `status` varchar(45) NOT NULL,
  PRIMARY KEY (`id_status`)
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


CREATE TABLE `personal_assessment` (
  `id_assessment` int NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `id_name_personal` int NOT NULL,
  `id_title_project` int DEFAULT NULL,
  `comments` varchar(100) DEFAULT NULL,
  `id_criterion` int NOT NULL,
  `id_drop_criterion` int DEFAULT NULL,
  `id_person_add` int DEFAULT NULL,
  `id_person_edit` int DEFAULT NULL,
  `assessment` int DEFAULT NULL,
  PRIMARY KEY (`id_assessment`),
  KEY `fk_id_project_idx` (`id_title_project`,`id_name_personal`),
  KEY `fk_id_name_idx` (`id_name_personal`),
  KEY `fk_id_criterion_idx` (`id_criterion`),
  KEY `fk_id_drop_criterion_idx` (`id_drop_criterion`),
  KEY `fk_person_add_idx` (`id_person_add`),
  KEY `fk_person_edit_idx` (`id_person_edit`,`id_person_add`),
  KEY `fk_person_add` (`id_person_add`),
  CONSTRAINT `fk_id_crit` FOREIGN KEY (`id_criterion`) REFERENCES `conf_criterion` (`id_conf_criterion`),
  CONSTRAINT `fk_id_drop_criterion` FOREIGN KEY (`id_drop_criterion`) REFERENCES `drop_criterion` (`id_drop_criterion`) ON DELETE SET NULL,
  CONSTRAINT `fk_id_name_person` FOREIGN KEY (`id_name_personal`) REFERENCES `personal` (`id_personal`) ON DELETE CASCADE,
  CONSTRAINT `fk_id_project` FOREIGN KEY (`id_title_project`) REFERENCES `project` (`id_project`),
  CONSTRAINT `fk_person_add` FOREIGN KEY (`id_person_add`) REFERENCES `personal` (`id_personal`) ON DELETE SET NULL,
  CONSTRAINT `fk_person_edit` FOREIGN KEY (`id_person_edit`) REFERENCES `personal` (`id_personal`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb3;



CREATE TABLE `progress_mean` (
  `id_progress_mean` int NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `id_name_personal` int NOT NULL,
  `id_title_project` int NOT NULL,
  `task` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_progress_mean`),
  KEY `fk_id_name_idx` (`id_name_personal`),
  KEY `fk_id_project_idx` (`id_title_project`),
  CONSTRAINT `fi_is_name` FOREIGN KEY (`id_name_personal`) REFERENCES `personal` (`id_personal`),
  CONSTRAINT `fk_project` FOREIGN KEY (`id_title_project`) REFERENCES `project` (`id_project`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;