-- --------------------------------------------------------
-- 호스트:                          192.168.0.3
-- 서버 버전:                        10.6.18-MariaDB-0ubuntu0.22.04.1 - Ubuntu 22.04
-- 서버 OS:                        debian-linux-gnu
-- HeidiSQL 버전:                  12.7.0.6850
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- 테이블 io_ground.DEMANDS 구조 내보내기
CREATE TABLE IF NOT EXISTS `DEMANDS` (
  `DCODE` varchar(15) NOT NULL,
  `DATE` date NOT NULL,
  `PRICE` int(11) DEFAULT NULL,
  `LAST_UPDATED` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`DCODE`,`DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 io_ground.DEMAND_FOR 구조 내보내기
CREATE TABLE IF NOT EXISTS `DEMAND_FOR` (
  `UID` varchar(5) NOT NULL,
  `TID` varchar(10) NOT NULL,
  `DCODE` varchar(15) DEFAULT NULL,
  `PDATE` date NOT NULL,
  `DEMAND_FOR` int(11) NOT NULL DEFAULT 0,
  `LAST_UPDATED` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`UID`,`TID`,`PDATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 io_ground.INVENTORY 구조 내보내기
CREATE TABLE IF NOT EXISTS `INVENTORY` (
  `UID` varchar(5) NOT NULL,
  `TID` varchar(10) NOT NULL,
  `PROD_DATE` date NOT NULL,
  `QTY` int(11) DEFAULT NULL,
  `LAST_UPDATED` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`UID`,`TID`,`PROD_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 io_ground.INVENTORY_HIST 구조 내보내기
CREATE TABLE IF NOT EXISTS `INVENTORY_HIST` (
  `UID` varchar(5) NOT NULL,
  `TID` varchar(10) NOT NULL,
  `PROD_DATE` date NOT NULL,
  `SALES_DATE` date NOT NULL,
  `SALES_QTY` int(11) DEFAULT NULL,
  `LAST_UPDATED` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`UID`,`TID`,`PROD_DATE`,`SALES_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 io_ground.LEDGER 구조 내보내기
CREATE TABLE IF NOT EXISTS `LEDGER` (
  `UID` varchar(5) NOT NULL,
  `TID` varchar(10) NOT NULL,
  `DATE` date NOT NULL,
  `AMOUNT` int(11) NOT NULL DEFAULT 0,
  `ACT` varchar(10) NOT NULL COMMENT 'PROD, INVEN, BACK, SALES',
  `DES` varchar(256) DEFAULT NULL,
  `SEQ` int(1) DEFAULT NULL,
  `LAST_UPDATED` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`UID`,`TID`,`DATE`,`ACT`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 io_ground.PRODUCTIONS 구조 내보내기
CREATE TABLE IF NOT EXISTS `PRODUCTIONS` (
  `UID` varchar(5) NOT NULL,
  `TID` varchar(10) NOT NULL,
  `PDATE` date NOT NULL,
  `TYPE` varchar(5) NOT NULL DEFAULT '',
  `SCHEDULE` text DEFAULT NULL,
  `QTY` int(11) DEFAULT NULL,
  `JOBS` int(11) DEFAULT NULL,
  `LAST_UPDATED` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`UID`,`TID`,`PDATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 io_ground.SALES 구조 내보내기
CREATE TABLE IF NOT EXISTS `SALES` (
  `UID` varchar(5) NOT NULL,
  `TID` varchar(10) NOT NULL,
  `PDATE` date NOT NULL,
  `DISC_RATIO` float NOT NULL DEFAULT 0,
  `LAST_UPDATED` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`UID`,`TID`,`PDATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 io_ground.TEAMS 구조 내보내기
CREATE TABLE IF NOT EXISTS `TEAMS` (
  `UID` varchar(5) NOT NULL,
  `TID` varchar(5) NOT NULL,
  `STATUS` varchar(10) NOT NULL DEFAULT 'ACTIVE',
  `ICON_URL` varchar(255) DEFAULT NULL,
  `REG_DATE` date DEFAULT curdate(),
  `DESC` text DEFAULT NULL,
  `AUTH_KEY` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`UID`,`TID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 io_ground.Test 구조 내보내기
CREATE TABLE IF NOT EXISTS `Test` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Type` varchar(50) DEFAULT NULL,
  `Contents` text DEFAULT NULL,
  `Date` date DEFAULT current_timestamp(),
  `DateTime` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
