-- sample
SELECT
produto,
CASE
 WHEN ano BETWEEN 2016 AND 2019 THEN '2016_2019'
 WHEN ano BETWEEN 2020 AND 2024 THEN '2020_2024'
END AS periodo,
 ANY_VALUE(unidade) AS unidade,
 SUM(quantidade) AS agg_quantidade,
 SUM(valor) AS agg_valor
FROM `basedosdados.br_ibge_ppm.producao_origem_animal`
WHERE ano BETWEEN 2016 AND 2024
AND sigla_uf IN ('AP','DF','GO','MA','MT','MS','PA','PI','RO','TO') #delete line to get national
GROUP BY produto, periodo
ORDER BY produto, periodo;


-- national
SELECT
produto,
CASE
 WHEN ano BETWEEN 2016 AND 2019 THEN '2016_2019'
 WHEN ano BETWEEN 2020 AND 2024 THEN '2020_2024'
END AS periodo,
 ANY_VALUE(unidade) AS unidade,
 SUM(quantidade) AS agg_quantidade,
 SUM(valor) AS agg_valor
FROM `basedosdados.br_ibge_ppm.producao_origem_animal`
WHERE ano BETWEEN 2016 AND 2024
AND sigla_uf IN ('AP','DF','GO','MA','MT','MS','PA','PI','RO','TO')
GROUP BY produto, periodo
ORDER BY produto, periodo;
