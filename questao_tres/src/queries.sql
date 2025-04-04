-- 10 operadoras com maiores despesas no último trimestre
SELECT 
    o.Nome_Fantasia, 
    SUM(d.VL_SALDO_INICIAL - d.VL_SALDO_FINAL) AS total_despesa
FROM intuitivecare.demonstracoes_contabeis AS d
JOIN operadoras_ativas o ON d.REG_ANS = o.Registro_ANS
WHERE 
    d.DATA = '2024-10-01'
    AND d.DESCRICAO = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
GROUP BY o.Nome_Fantasia
ORDER BY total_despesa DESC
LIMIT 10;

-- 10 operadoras com maiores despesas no último ano
SELECT o.Nome_Fantasia, 
       SUM(d.VL_SALDO_INICIAL - d.VL_SALDO_FINAL) AS total_despesa
FROM demonstracoes_contabeis d
JOIN operadoras_ativas o ON d.REG_ANS = o.Registro_ANS
WHERE YEAR(d.DATA) = 2024
AND d.DESCRICAO = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
GROUP BY o.Nome_Fantasia
ORDER BY total_despesa DESC
LIMIT 10;