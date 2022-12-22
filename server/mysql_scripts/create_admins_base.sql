CREATE TABLE `access_factory` (
  `id_access_factory` int NOT NULL AUTO_INCREMENT,
  `id_user` int NOT NULL,
  `id_factory` int NOT NULL,
  PRIMARY KEY (`id_access_factory`),
  KEY `fk_user_idx` (`id_user`),
  KEY `fk_factory_idx` (`id_factory`),
  CONSTRAINT `fk_factory` FOREIGN KEY (`id_factory`) REFERENCES `factory` (`id_factory`),
  CONSTRAINT `fk_user` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_users`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `admin` (
  `id_admin` int NOT NULL AUTO_INCREMENT,
  `admin_name` varchar(45) NOT NULL,
  `number_factory` int NOT NULL,
  `password` varchar(70) NOT NULL,
  `salt_user` varchar(70) NOT NULL,
  `salt_server` varchar(70) NOT NULL,
  PRIMARY KEY (`id_admin`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory` (
  `id_factory` int NOT NULL AUTO_INCREMENT,
  `name_factory` varchar(45) DEFAULT NULL,
  `id_admin` int NOT NULL,
  PRIMARY KEY (`id_factory`),
  KEY `fk_admin_idx` (`id_admin`),
  CONSTRAINT `fk_admin` FOREIGN KEY (`id_admin`) REFERENCES `admin` (`id_admin`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `user_keys` (
  `id_keys` int NOT NULL AUTO_INCREMENT,
  `name_keys` varchar(45) NOT NULL,
  PRIMARY KEY (`id_keys`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `users` (
  `id_users` int NOT NULL AUTO_INCREMENT,
  `nickname` varchar(45) NOT NULL,
  `password` varchar(70) NOT NULL,
  `salt_server` varchar(70) NOT NULL,
  `salt_user` varchar(70) NOT NULL,
  `id_admin` int NOT NULL,
  PRIMARY KEY (`id_users`),
  KEY `fk_admin_idx` (`id_admin`),
  CONSTRAINT `fk_admins` FOREIGN KEY (`id_admin`) REFERENCES `admin` (`id_admin`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
