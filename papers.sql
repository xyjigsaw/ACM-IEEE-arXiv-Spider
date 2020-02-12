/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80017
 Source Host           : localhost:3306
 Source Schema         : papers

 Target Server Type    : MySQL
 Target Server Version : 80017
 File Encoding         : 65001

 Date: 12/02/2020 10:48:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ACM_Data
-- ----------------------------
DROP TABLE IF EXISTS `ACM_Data`;
CREATE TABLE `ACM_Data` (
  `p_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(511) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `authors` varchar(511) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `year` varchar(511) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `type` varchar(2047) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `subjects` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `abstract` varchar(4095) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `citation` int(10) DEFAULT NULL,
  PRIMARY KEY (`p_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4376 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
