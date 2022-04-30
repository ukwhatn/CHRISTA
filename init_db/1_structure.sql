# CONFIG
SET @OLD_CHARACTER_SET_CLIENT = @@CHARACTER_SET_CLIENT;
SET NAMES utf8;
SET NAMES utf8mb4;
SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0;
SET @OLD_SQL_MODE = @@SQL_MODE, SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';
SET @OLD_SQL_NOTES = @@SQL_NOTES, SQL_NOTES = 0;

# PERMISSION
# ACCOUNT CREATE -> docker-compose.yml
GRANT SELECT, INSERT, UPDATE, DELETE ON Master.* TO application;

# CREATE DATABASE "Master"
CREATE DATABASE IF NOT EXISTS `Master` DEFAULT CHARACTER SET utf8mb4;
USE `Master`;

DROP TABLE IF EXISTS `config`;
CREATE TABLE `config`
(
    `id`    int(11)      NOT NULL AUTO_INCREMENT,
    `name`  varchar(50)  NOT NULL,
    `value` varchar(200) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS `drafts`;
CREATE TABLE `drafts`
(
    `id`             int(11) unsigned NOT NULL AUTO_INCREMENT,
    `fullname`       varchar(50)      NOT NULL,
    `title`          varchar(200)     NOT NULL,
    `author_id`      int(10) unsigned NOT NULL,
    `author_name`    varchar(50)      NOT NULL,
    `category`       varchar(10)      NOT NULL,
    `notified`       tinyint(1)       NOT NULL DEFAULT '0',
    `latest_updated` datetime         NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

SET SQL_MODE = IFNULL(@OLD_SQL_MODE, '');
SET FOREIGN_KEY_CHECKS = IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1);
SET CHARACTER_SET_CLIENT = @OLD_CHARACTER_SET_CLIENT;
SET SQL_NOTES = IFNULL(@OLD_SQL_NOTES, 1);
