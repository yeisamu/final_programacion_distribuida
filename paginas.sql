-- phpMyAdmin SQL Dump
-- version 3.2.4
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 06-06-2017 a las 19:08:29
-- Versión del servidor: 5.1.41
-- Versión de PHP: 5.3.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `paginas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paginas`
--

CREATE TABLE IF NOT EXISTS `paginas` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `url` longtext NOT NULL,
  `pclave` longtext NOT NULL,
  `puntos` int(3) DEFAULT NULL,
  `penalizado` enum('si','no') NOT NULL DEFAULT 'no',
  `dudoso` enum('si','no') NOT NULL DEFAULT 'no',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

--
-- Volcar la base de datos para la tabla `paginas`
--

INSERT INTO `paginas` (`id`, `url`, `pclave`, `puntos`, `penalizado`, `dudoso`) VALUES
(3, 'http://www.espn.com.co', 'Deportes, ciclismo, fÃºtbol, champions League', NULL, 'si', 'si'),
(5, 'http://www.cotecnova.edu.co', '', NULL, 'no', 'no'),
(6, 'http://mysexualidad.weebly.com ', '', NULL, 'no', 'no'),
(7, 'http://ipornogratisx.xxx', '', NULL, 'no', 'no');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
