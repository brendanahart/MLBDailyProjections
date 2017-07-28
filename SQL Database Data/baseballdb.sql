-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema baseball
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema baseball
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `baseball` DEFAULT CHARACTER SET utf8 ;
USE `baseball` ;

-- -----------------------------------------------------
-- Table `baseball`.`batters`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `baseball`.`batters` (
  `idbatters` INT NOT NULL,
  `mlbID` INT NULL,
  `playerName` VARCHAR(100) NULL,
  `team` VARCHAR(45) NULL,
  `hand` VARCHAR(45) NULL,
  `pos1` VARCHAR(45) NULL,
  `pos2` VARCHAR(45) NULL,
  `pos3` VARCHAR(45) NULL,
  PRIMARY KEY (`idbatters`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `baseball`.`pitchers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `baseball`.`pitchers` (
  `idpitchers` INT NOT NULL,
  `mlbID` INT NULL,
  `playerName` VARCHAR(100) NULL,
  `team` VARCHAR(45) NULL,
  `throws` VARCHAR(45) NULL,
  PRIMARY KEY (`idpitchers`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `baseball`.`games`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `baseball`.`games` (
  `idgames` INT NOT NULL,
  `date` DATETIME NULL,
  PRIMARY KEY (`idgames`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `baseball`.`battersdaily`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `baseball`.`battersdaily` (
  `idbattersdaily` INT NOT NULL,
  `ab` INT NULL,
  `hits` INT NULL,
  `singles` INT NULL,
  `doubles` INT NULL,
  `triples` INT NULL,
  `homeruns` INT NULL,
  `average` DECIMAL(6,4) NULL,
  `slugging` DECIMAL(6,4) NULL,
  `onbase` DECIMAL(6,4) NULL,
  `ops` DECIMAL(6,4) NULL,
  `stolenbases` INT NULL,
  `caughtstealing` INT NULL,
  `runs` INT NULL,
  `rbi` INT NULL,
  `walks` INT NULL,
  `errors` INT NULL,
  `hbp` INT NULL,
  `ibb` INT NULL,
  `pa` INT NULL,
  `strikeouts` INT NULL,
  `batterID` INT NULL,
  `bgameID` INT NULL,
  PRIMARY KEY (`idbattersdaily`),
  INDEX `batterID_idx` (`batterID` ASC),
  INDEX `gameID_idx` (`bgameID` ASC),
  CONSTRAINT `batterID`
    FOREIGN KEY (`batterID`)
    REFERENCES `baseball`.`batters` (`idbatters`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `bgameID`
    FOREIGN KEY (`bgameID`)
    REFERENCES `baseball`.`games` (`idgames`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `baseball`.`pitchersdaily`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `baseball`.`pitchersdaily` (
  `idpitcherdaily` INT NOT NULL,
  `pitcherID` INT NULL,
  `pgameID` INT NULL,
  `walks` INT NULL,
  `earnedRuns` INT NULL,
  `era` DECIMAL(8,4) NULL,
  `hits` INT NULL,
  `hbp` INT NULL,
  `homerunsAllowed` INT NULL,
  `ip` DECIMAL(4,2) NULL,
  `strikeouts` INT NULL,
  `numberPitches` INT NULL,
  `runs` INT NULL,
  `strikes` INT NULL,
  `win` INT NULL,
  `shutout` INT NULL,
  `completegame` INT NULL,
  `nohitter` INT NULL,
  `save` INT NULL,
  `whip` DECIMAL(8,4) NULL,
  INDEX `pitcherID_idx` (`pitcherID` ASC),
  INDEX `gameID_idx` (`pgameID` ASC),
  PRIMARY KEY (`idpitcherdaily`),
  CONSTRAINT `pitcherID`
    FOREIGN KEY (`pitcherID`)
    REFERENCES `baseball`.`pitchers` (`idpitchers`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `pgameID`
    FOREIGN KEY (`pgameID`)
    REFERENCES `baseball`.`games` (`idgames`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
