-- Criação do Banco de Dados
CREATE DATABASE IF NOT EXISTS `caobalhota`;
USE `caobalhota`;

-- Configurações de Sistema
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- ------------------------------------------------------
-- Estrutura da tabela `cliente`
-- ------------------------------------------------------
DROP TABLE IF EXISTS `cliente`;
CREATE TABLE `cliente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `cpf` varchar(20) DEFAULT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `endereco` varchar(255) DEFAULT NULL,
  `admin` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `cliente` VALUES 
(4,'Consumidor Final','000.000.000-00','00000','vendas@caobalhota.com','Loja',NULL),
(5,'João Mendes','111.111.111-11','11955554444','joao@email.com','Rua das Flores, 123',NULL),
(6,'Maria Clara','222.222.222-22','11933332222','maria@email.com','Av. Brasil, 456',NULL),
(7,'Pedro Gomes','333.333.333-33','11911110000','pedro@email.com','Rua do Sol, 789',NULL);

-- ------------------------------------------------------
-- Estrutura da tabela `pet`
-- ------------------------------------------------------
DROP TABLE IF EXISTS `pet`;
CREATE TABLE `pet` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int DEFAULT NULL,
  `nome` varchar(100) NOT NULL,
  `especie` varchar(50) DEFAULT NULL,
  `raca` varchar(50) DEFAULT NULL,
  `idade` varchar(20) DEFAULT NULL,
  `porte` enum('pequeno','médio','grande') DEFAULT NULL,
  `cuidados_especiais` text,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_pet_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `pet` VALUES 
(4,4,'Totó','Gato','SRD','2 anos','pequeno','Nenhum'),
(5,5,'Rex','Cão','Golden Retriever','3 anos','grande','Nenhum'),
(6,5,'Mimi','Gato','Siamês','1 ano','pequeno','Não gosta de água'),
(7,6,'Max','Cão','Pug','2 anos','pequeno','Problemas respiratórios'),
(8,7,'Piu','Pássaro','Calopsita','6 meses','pequeno','Gaiola limpa');

-- ------------------------------------------------------
-- Estrutura da tabela `funcionario`
-- ------------------------------------------------------
DROP TABLE IF EXISTS `funcionario`;
CREATE TABLE `funcionario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `cargo` varchar(50) DEFAULT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `login` varchar(50) DEFAULT NULL,
  `senha` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `funcionario` VALUES 
(1,'João Silva','Veterinário','11999999999','joao@caobalhota.com','joao.silva','123456'),
(2,'Maria Oliveira','Recepcionista','11988888888','maria@caobalhota.com','maria.oliveira','senha123'),
(3,'Admin','Administrador','11000000000','admin@caobalhota.com','admin','admin');

-- ------------------------------------------------------
-- Estrutura da tabela `servico`
-- ------------------------------------------------------
DROP TABLE IF EXISTS `servico`;
CREATE TABLE `servico` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `valor_base` double NOT NULL,
  `descricao` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `servico` VALUES 
(1,'Tosa Básica',50,'Tosa higiênica'),
(2,'Banho Completo',40,'Banho e secagem'),
(5,'Consulta Veterinária',120,'Avaliação geral');

-- ------------------------------------------------------
-- Estrutura da tabela `agendamento`
-- ------------------------------------------------------
DROP TABLE IF EXISTS `agendamento`;
CREATE TABLE `agendamento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int DEFAULT NULL,
  `id_pet` int DEFAULT NULL,
  `id_servico` int DEFAULT NULL,
  `id_funcionario` int DEFAULT NULL,
  `data` date DEFAULT NULL,
  `hora` time DEFAULT NULL,
  `status` enum('agendado','iniciado','concluído','cancelado','pago') DEFAULT NULL,
  `cor_tintura` varchar(30) DEFAULT NULL,
  `observacoes` text,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_age_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`),
  CONSTRAINT `fk_age_pet` FOREIGN KEY (`id_pet`) REFERENCES `pet` (`id`),
  CONSTRAINT `fk_age_servico` FOREIGN KEY (`id_servico`) REFERENCES `servico` (`id`),
  CONSTRAINT `fk_age_func` FOREIGN KEY (`id_funcionario`) REFERENCES `funcionario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `agendamento` VALUES (1,5,5,2,1,'2026-03-15','10:00:00','agendado',NULL,'Cão dócil');

-- ------------------------------------------------------
-- Estrutura da tabela `produto`
-- ------------------------------------------------------
DROP TABLE IF EXISTS `produto`;
CREATE TABLE `produto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `codigo` varchar(50) DEFAULT NULL,
  `nome` varchar(100) NOT NULL,
  `descricao` text,
  `preco` double NOT NULL,
  `estoque` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `produto` VALUES (3,'PRD-001','Ração Golden','Premium',150,10),(4,'PRD-002','Shampoo','Neutro',25.5,50);

-- ------------------------------------------------------
-- Estrutura da tabela `venda`
-- ------------------------------------------------------
DROP TABLE IF EXISTS `venda`;
CREATE TABLE `venda` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int DEFAULT NULL,
  `data_venda` date DEFAULT NULL,
  `valor_total` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ------------------------------------------------------
-- Estrutura da tabela `item_venda`
-- ------------------------------------------------------
DROP TABLE IF EXISTS `item_venda`;
CREATE TABLE `item_venda` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_venda` int DEFAULT NULL,
  `id_produto` int DEFAULT NULL,
  `id_servico` int DEFAULT NULL,
  `quantidade` int DEFAULT NULL,
  `valor_unitario` double DEFAULT NULL,
  `tipo_item` enum('produto','servico') DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_item_venda` FOREIGN KEY (`id_venda`) REFERENCES `venda` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Restaurar configurações
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;