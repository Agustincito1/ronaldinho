-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 29-10-2025 a las 22:07:17
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `mensaje`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mensaje`
--

CREATE TABLE `mensaje` (
  `Id` int(5) NOT NULL,
  `pregunta` varchar(1000) NOT NULL,
  `opciones` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`opciones`)),
  `respuesta` varchar(1000) NOT NULL,
  `usuario` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mensaje`
--

INSERT INTO `mensaje` (`Id`, `pregunta`, `opciones`, `respuesta`, `usuario`) VALUES
(256, '¿Cuál es una de las principales causas del cambio climático?', '[\"Deforestaci\\u00f3n\", \"Aumento de la biodiversidad\", \"Reducci\\u00f3n de residuos\"]', 'Aumento de la biodiversidad', 'lazaro'),
(257, '¿Cuál es una de las principales causas del cambio climático?', '[\"Deforestaci\\u00f3n\", \"Aumento de la biodiversidad\", \"Reciclaje de materiales\"]', 'Reciclaje de materiales', 'lazaro'),
(258, '¿Cuál de las siguientes prácticas ayuda a reducir la contaminación del aire?', '[\"Usar transporte p\\u00fablico\", \"Aumentar el uso de pl\\u00e1sticos\", \"Quemar basura en espacios abiertos\"]', 'Quemar basura en espacios abiertos', 'lazaro'),
(259, '¿Cuál es una de las principales causas del cambio climático?', '[\"Deforestaci\\u00f3n\", \"Reciclaje\", \"Energ\\u00eda solar\"]', 'Reciclaje', 'lazaro'),
(260, '¿Cuál es una de las principales causas de la deforestación en el mundo?', '[\"La urbanizaci\\u00f3n\", \"La producci\\u00f3n de energ\\u00eda solar\", \"La conservaci\\u00f3n de espacios verdes\"]', 'La urbanización', 'lazarito          '),
(261, '¿Cuál es la principal causa del cambio climático?', '[\"Deforestaci\\u00f3n\", \"Emisiones de gases de efecto invernadero\", \"Contaminaci\\u00f3n del agua\"]', 'Emisiones de gases de efecto invernadero', 'lazarito          '),
(262, '¿Cuál es uno de los principales objetivos de la educación ambiental?', '[\"Fomentar el consumo excesivo de recursos\", \"Crear conciencia sobre la protecci\\u00f3n del medio ambiente\", \"Promover la contaminaci\\u00f3n del aire\"]', 'Promover la contaminación del aire', 'lazarito          ');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `mensaje`
--
ALTER TABLE `mensaje`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `mensaje`
--
ALTER TABLE `mensaje`
  MODIFY `Id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=263;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
