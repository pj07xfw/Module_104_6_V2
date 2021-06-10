--

-- Database: NOM_PRENOM_INFO1X_SUJET_BD_104
-- Détection si une autre base de donnée du même nom existe

DROP DATABASE IF EXISTS Rapin_Mathieu_INFO1d_Drones_104_2021;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS Rapin_Mathieu_INFO1d_Drones_104_2021;

-- Utilisation de cette base de donnée

USE Rapin_Mathieu_INFO1d_Drones_104_2021;

-- phpMyAdmin SQL Dump
-- version 4.5.4.1
-- http://www.phpmyadmin.net
--
-- Client :  localhost
-- Généré le :  Mar 25 Mai 2021 à 09:53
-- Version du serveur :  5.7.11
-- Version de PHP :  5.6.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `drones_math`
--

-- --------------------------------------------------------

--
-- Structure de la table `t_drone`
--

CREATE TABLE `t_drone` (
  `id_drone` int(11) NOT NULL,
  `nom_drone` varchar(100) NOT NULL,
  `affiche_drone` varchar(150) DEFAULT NULL,
  `FK_Marque` int(11) DEFAULT NULL,
  `FK_gamme` int(11) DEFAULT NULL,
  `FK_type_drone` int(11) DEFAULT NULL,
  `FK_magasin` int(11) DEFAULT NULL,
  `FK_fonctionalite` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_drone`
--

INSERT INTO `t_drone` (`id_drone`, `nom_drone`, `affiche_drone`, `FK_Marque`, `FK_gamme`, `FK_type_drone`, `FK_magasin`, `FK_fonctionalite`) VALUES
(1, 'Mavic pro', 'https://images-na.ssl-images-amazon.com/images/I/61qc5w63VdL._AC_SL1400_.jpg', 1, 1, 1, 0, 0),
(2, 'Mavic air 2', 'https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/HP3D2?wid=4218&hei=2182&fmt=jpeg&qlt=95&.v=1588367929110', 1, 2, 1, 0, 0),
(3, 'Mavic mini 2', 'https://media.ldlc.com/r1600/ld/products/00/05/75/34/LD0005753464_1.jpg', 1, 3, 3, 0, 0),
(4, 'Mavic mini', 'https://i0.wp.com/lmddrone.com/wp-content/uploads/2019/10/dji_mavic_mini.jpg?fit=960%2C480&ssl=1', 1, 3, 3, 0, 0),
(5, 'DJI Spark', 'https://www.helicomicro.com/wp-content/uploads/2017/05/DJI-Spark-Lava-Red-Front-34-1200-spk.jpg', NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `t_drone_images`
--

CREATE TABLE `t_drone_images` (
  `id_drone_images` int(11) NOT NULL,
  `FK_drone` int(11) NOT NULL,
  `FK_images` int(11) NOT NULL,
  `Date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_drone_images`
--

INSERT INTO `t_drone_images` (`id_drone_images`, `FK_drone`, `FK_images`, `Date`) VALUES
(2, 3, 15, NULL),
(14, 2, 20, NULL),
(15, 4, 14, NULL),
(18, 1, 18, NULL),
(19, 5, 15, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `t_drone_lieu_decollage`
--

CREATE TABLE `t_drone_lieu_decollage` (
  `id_drone_lieu_decollage` int(11) NOT NULL,
  `FK_drone` int(11) NOT NULL,
  `FK_lieu` int(11) NOT NULL,
  `Date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `t_fonctionalite`
--

CREATE TABLE `t_fonctionalite` (
  `id_fonctionalite` int(11) NOT NULL,
  `autonomie` int(11) NOT NULL,
  `portee_drone` int(11) NOT NULL,
  `poids` int(11) NOT NULL,
  `taille_diagonale` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `t_gamme`
--

CREATE TABLE `t_gamme` (
  `id_gamme` int(11) NOT NULL,
  `nom_gamme` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_gamme`
--

INSERT INTO `t_gamme` (`id_gamme`, `nom_gamme`) VALUES
(1, 'Mavic'),
(2, 'Mavic Air'),
(3, 'Mavic Mini\r\n');

-- --------------------------------------------------------

--
-- Structure de la table `t_images`
--

CREATE TABLE `t_images` (
  `id_images` int(11) NOT NULL,
  `chemin_images` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_images`
--

INSERT INTO `t_images` (`id_images`, `chemin_images`) VALUES
(14, 'maccaud'),
(15, 'sql'),
(18, 'lol'),
(20, 'salut');

-- --------------------------------------------------------

--
-- Structure de la table `t_lieu_decollage`
--

CREATE TABLE `t_lieu_decollage` (
  `id_lieu_decollage` int(11) NOT NULL,
  `lieu` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `t_magasin`
--

CREATE TABLE `t_magasin` (
  `id_magasin` int(11) NOT NULL,
  `nom_magasin` varchar(30) NOT NULL,
  `prix` int(30) NOT NULL,
  `reduction` int(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `t_marque`
--

CREATE TABLE `t_marque` (
  `id_marque` int(11) NOT NULL,
  `marque` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_marque`
--

INSERT INTO `t_marque` (`id_marque`, `marque`) VALUES
(1, 'DJI'),
(2, 'Parrot'),
(3, 'Hubsan');

-- --------------------------------------------------------

--
-- Structure de la table `t_type_drone`
--

CREATE TABLE `t_type_drone` (
  `id_type_drone` int(11) NOT NULL,
  `type_drone` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_type_drone`
--

INSERT INTO `t_type_drone` (`id_type_drone`, `type_drone`) VALUES
(1, 'Grand Public'),
(2, 'Professionnel'),
(3, 'Débutant\r\n');

--
-- Index pour les tables exportées
--

--
-- Index pour la table `t_drone`
--
ALTER TABLE `t_drone`
  ADD PRIMARY KEY (`id_drone`),
  ADD KEY `FK_Marque` (`FK_Marque`),
  ADD KEY `FK_gamme` (`FK_gamme`),
  ADD KEY `FK_type_drone` (`FK_type_drone`),
  ADD KEY `FK_fonctionalite` (`FK_fonctionalite`),
  ADD KEY `FK_magasin` (`FK_magasin`);

--
-- Index pour la table `t_drone_images`
--
ALTER TABLE `t_drone_images`
  ADD PRIMARY KEY (`id_drone_images`),
  ADD KEY `FK_drone` (`FK_drone`),
  ADD KEY `FK_images` (`FK_images`);

--
-- Index pour la table `t_drone_lieu_decollage`
--
ALTER TABLE `t_drone_lieu_decollage`
  ADD PRIMARY KEY (`id_drone_lieu_decollage`),
  ADD KEY `FK_lieu` (`FK_lieu`),
  ADD KEY `FK_drone` (`FK_drone`);

--
-- Index pour la table `t_fonctionalite`
--
ALTER TABLE `t_fonctionalite`
  ADD PRIMARY KEY (`id_fonctionalite`);

--
-- Index pour la table `t_gamme`
--
ALTER TABLE `t_gamme`
  ADD PRIMARY KEY (`id_gamme`);

--
-- Index pour la table `t_images`
--
ALTER TABLE `t_images`
  ADD PRIMARY KEY (`id_images`);

--
-- Index pour la table `t_lieu_decollage`
--
ALTER TABLE `t_lieu_decollage`
  ADD PRIMARY KEY (`id_lieu_decollage`);

--
-- Index pour la table `t_magasin`
--
ALTER TABLE `t_magasin`
  ADD PRIMARY KEY (`id_magasin`);

--
-- Index pour la table `t_marque`
--
ALTER TABLE `t_marque`
  ADD PRIMARY KEY (`id_marque`);

--
-- Index pour la table `t_type_drone`
--
ALTER TABLE `t_type_drone`
  ADD PRIMARY KEY (`id_type_drone`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `t_drone`
--
ALTER TABLE `t_drone`
  MODIFY `id_drone` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
--
-- AUTO_INCREMENT pour la table `t_drone_images`
--
ALTER TABLE `t_drone_images`
  MODIFY `id_drone_images` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
--
-- AUTO_INCREMENT pour la table `t_drone_lieu_decollage`
--
ALTER TABLE `t_drone_lieu_decollage`
  MODIFY `id_drone_lieu_decollage` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `t_fonctionalite`
--
ALTER TABLE `t_fonctionalite`
  MODIFY `id_fonctionalite` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `t_gamme`
--
ALTER TABLE `t_gamme`
  MODIFY `id_gamme` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT pour la table `t_images`
--
ALTER TABLE `t_images`
  MODIFY `id_images` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
--
-- AUTO_INCREMENT pour la table `t_lieu_decollage`
--
ALTER TABLE `t_lieu_decollage`
  MODIFY `id_lieu_decollage` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `t_marque`
--
ALTER TABLE `t_marque`
  MODIFY `id_marque` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT pour la table `t_type_drone`
--
ALTER TABLE `t_type_drone`
  MODIFY `id_type_drone` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `t_drone`
--
ALTER TABLE `t_drone`
  ADD CONSTRAINT `t_drone_ibfk_1` FOREIGN KEY (`FK_Marque`) REFERENCES `t_marque` (`id_marque`),
  ADD CONSTRAINT `t_drone_ibfk_3` FOREIGN KEY (`FK_type_drone`) REFERENCES `t_type_drone` (`id_type_drone`),
  ADD CONSTRAINT `t_drone_ibfk_5` FOREIGN KEY (`FK_gamme`) REFERENCES `t_gamme` (`id_gamme`);

--
-- Contraintes pour la table `t_drone_images`
--
ALTER TABLE `t_drone_images`
  ADD CONSTRAINT `t_drone_images_ibfk_1` FOREIGN KEY (`FK_drone`) REFERENCES `t_drone` (`id_drone`),
  ADD CONSTRAINT `t_drone_images_ibfk_2` FOREIGN KEY (`FK_images`) REFERENCES `t_images` (`id_images`);

--
-- Contraintes pour la table `t_drone_lieu_decollage`
--
ALTER TABLE `t_drone_lieu_decollage`
  ADD CONSTRAINT `t_drone_lieu_decollage_ibfk_1` FOREIGN KEY (`FK_lieu`) REFERENCES `t_lieu_decollage` (`id_lieu_decollage`),
  ADD CONSTRAINT `t_drone_lieu_decollage_ibfk_2` FOREIGN KEY (`FK_drone`) REFERENCES `t_drone` (`id_drone`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
