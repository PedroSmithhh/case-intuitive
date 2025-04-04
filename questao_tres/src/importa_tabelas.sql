-- NOTA: Este script usa caminhos absolutos no diretório secure_file_priv do MySQL.
-- Certifique-se de que os arquivos CSVs estão no diretório especificado por secure_file_priv.

-- Ativar mensagens de log
SET @log_message = '';

-- Importando os dados de demonstrações contábeis (2023)
SELECT 'Importando 1T2023.csv...' AS 'Status';
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/demonstracoes_contabeis/2023/1T2023.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(DATA, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_INICIAL, VL_SALDO_FINAL);
SET @log_message = CONCAT('Linhas importadas de 1T2023.csv: ', ROW_COUNT());
SELECT @log_message AS 'Resultado';

SELECT 'Importando 2T2023.csv...' AS 'Status';
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/demonstracoes_contabeis/2023/2t2023.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(DATA, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_INICIAL, VL_SALDO_FINAL);
SET @log_message = CONCAT('Linhas importadas de 2T2023.csv: ', ROW_COUNT());
SELECT @log_message AS 'Resultado';

SELECT 'Importando 3T2023.csv...' AS 'Status';
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/demonstracoes_contabeis/2023/3T2023.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(DATA, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_INICIAL, VL_SALDO_FINAL);
SET @log_message = CONCAT('Linhas importadas de 3T2023.csv: ', ROW_COUNT());
SELECT @log_message AS 'Resultado';

SELECT 'Importando 4T2023.csv...' AS 'Status';
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/demonstracoes_contabeis/2023/4T2023.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@data, @reg_ans, @cd_conta_contabil, @descricao, @vl_saldo_inicial, @vl_saldo_final)
SET DATA = STR_TO_DATE(@data, '%d/%m/%Y'),
    REG_ANS = @reg_ans,
    CD_CONTA_CONTABIL = @cd_conta_contabil,
    DESCRICAO = @descricao,
    VL_SALDO_INICIAL = REPLACE(@vl_saldo_inicial, ',', '.'),
    VL_SALDO_FINAL = REPLACE(@vl_saldo_final, ',', '.');
SET @log_message = CONCAT('Linhas importadas de 4T2023.csv: ', ROW_COUNT());
SELECT @log_message AS 'Resultado';

-- Importando os dados de demonstrações contábeis (2024)
SELECT 'Importando 1T2024.csv...' AS 'Status';
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/demonstracoes_contabeis/2024/1T2024.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(DATA, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_INICIAL, VL_SALDO_FINAL);
SET @log_message = CONCAT('Linhas importadas de 1T2024.csv: ', ROW_COUNT());
SELECT @log_message AS 'Resultado';

SELECT 'Importando 2T2024.csv...' AS 'Status';
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/demonstracoes_contabeis/2024/2T2024.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(DATA, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_INICIAL, VL_SALDO_FINAL);
SET @log_message = CONCAT('Linhas importadas de 2T2024.csv: ', ROW_COUNT());
SELECT @log_message AS 'Resultado';

SELECT 'Importando 3T2024.csv...' AS 'Status';
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/demonstracoes_contabeis/2024/3T2024.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(DATA, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_INICIAL, VL_SALDO_FINAL);
SET @log_message = CONCAT('Linhas importadas de 3T2024.csv: ', ROW_COUNT());
SELECT @log_message AS 'Resultado';

SELECT 'Importando 4T2024.csv...' AS 'Status';
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/demonstracoes_contabeis/2024/4T2024.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(DATA, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_INICIAL, VL_SALDO_FINAL);
SET @log_message = CONCAT('Linhas importadas de 4T2024.csv: ', ROW_COUNT());
SELECT @log_message AS 'Resultado';

-- Importando os dados de operadoras ativas
SELECT 'Importando Relatorio_cadop.csv...' AS 'Status';
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv'
INTO TABLE operadoras_ativas
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@registro_ans, @cnpj, @razao_social, @nome_fantasia, @modalidade, @logradouro, @numero, @complemento, @bairro, @cidade, @uf, @cep, @ddd, @telefone, @fax, @endereco_eletronico, @representante, @cargo_representante, @regiao_de_comercializacao, @data_registro_ans)
SET Registro_ANS = @registro_ans,
    CNPJ = @cnpj,
    Razao_Social = @razao_social,
    Nome_Fantasia = @nome_fantasia,
    Modalidade = @modalidade,
    Logradouro = @logradouro,
    Numero = @numero,
    Complemento = @complemento,
    Bairro = @bairro,
    Cidade = @cidade,
    UF = @uf,
    CEP = @cep,
    DDD = @ddd,
    Telefone = IF(@telefone = '', NULL, SUBSTRING(@telefone, 1, 20)),   -- Truncar para 20 caracteres
    Fax = @fax,
    Endereco_eletronico = @endereco_eletronico,
    Representante = @representante,
    Cargo_Representante = @cargo_representante,
    Regiao_de_Comercializacao = IF(@regiao_de_comercializacao = '', NULL, @regiao_de_comercializacao),
    Data_Registro_ANS = STR_TO_DATE(@data_registro_ans, '%Y-%m-%d');
SET @log_message = CONCAT('Linhas importadas de Relatorio_cadop.csv: ', ROW_COUNT());
SELECT @log_message AS 'Resultado';