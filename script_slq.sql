CREATE DATABASE IF NOT EXISTS aps_gestao_ambiental;

USE aps_gestao_ambiental;

CREATE TABLE IF NOT EXISTS indicadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa VARCHAR(255) NOT NULL,
    ano INT NOT NULL,
    consumo_agua_m3 FLOAT NOT NULL,
    residuos_ton FLOAT NOT NULL,
    emissoes_co2_ton FLOAT NOT NULL
);

INSERT INTO indicadores (empresa, ano, consumo_agua_m3, residuos_ton, emissoes_co2_ton)
VALUES 
('ABC Indústria de Alimentos', 2023, 1500, 75, 320),
('Transportadora XYZ', 2023, 400, 15, 950);