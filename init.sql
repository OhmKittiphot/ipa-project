CREATE DATABASE IF NOT EXISTS ipa2025;
USE ipa2025;

CREATE TABLE routers (
  ip VARCHAR(50) PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(50) NOT NULL
);

CREATE TABLE interface_status (
  id INT AUTO_INCREMENT PRIMARY KEY,
  router_ip VARCHAR(50) NOT NULL,
  interface_name VARCHAR(50) NOT NULL,
  ip_address VARCHAR(50),
  status VARCHAR(50),
  proto VARCHAR(50),
  is_monitored BOOLEAN DEFAULT FALSE,
  last_checked DATETIME DEFAULT CURRENT_TIMESTAMP 
               ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY unique_iface (router_ip, interface_name)
);