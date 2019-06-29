# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.22)
# Database: autohome
# Generation Time: 2019-06-29 11:10:11 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table af_ymp_autobrand
# ------------------------------------------------------------

DROP TABLE IF EXISTS `af_ymp_autobrand`;

CREATE TABLE `af_ymp_autobrand` (
  `autobrand_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL DEFAULT '0',
  `logo` varchar(255) DEFAULT NULL,
  `sort_order` int(11) NOT NULL,
  `status` int(1) NOT NULL,
  `date_added` datetime NOT NULL,
  `date_modified` datetime NOT NULL,
  PRIMARY KEY (`autobrand_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;



# Dump of table af_ymp_autobrand_description
# ------------------------------------------------------------

DROP TABLE IF EXISTS `af_ymp_autobrand_description`;

CREATE TABLE `af_ymp_autobrand_description` (
  `autobrand_id` int(11) NOT NULL,
  `language_id` int(11) NOT NULL,
  `name` varchar(64) NOT NULL,
  `initial` char(1) DEFAULT '',
  PRIMARY KEY (`autobrand_id`,`language_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;



# Dump of table af_ymp_automodel
# ------------------------------------------------------------

DROP TABLE IF EXISTS `af_ymp_automodel`;

CREATE TABLE `af_ymp_automodel` (
  `automodel_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `autobrand_id` int(11) NOT NULL,
  `sort_order` int(11) NOT NULL,
  `status` int(1) NOT NULL,
  `date_added` datetime NOT NULL,
  `date_modified` datetime NOT NULL,
  PRIMARY KEY (`automodel_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;



# Dump of table af_ymp_automodel_description
# ------------------------------------------------------------

DROP TABLE IF EXISTS `af_ymp_automodel_description`;

CREATE TABLE `af_ymp_automodel_description` (
  `automodel_id` int(11) NOT NULL,
  `language_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`automodel_id`,`language_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
