
-- sample
SELECT
tipo_rebanho,
CASE
  WHEN ano BETWEEN 2016 AND 2019 THEN '2016_2019'
  WHEN ano BETWEEN 2020 AND 2024 THEN '2020_2024'
END AS periodo,
SUM(quantidade) AS agg_quantidade,
FROM `basedosdados.br_ibge_ppm.efetivo_rebanhos`
WHERE ano BETWEEN 2016 AND 2024
AND sigla_uf IN ('AP','DF','GO','MA','MT','MS','PA','PI','RO','TO') #delete line to get national
GROUP BY tipo_rebanho, periodo
ORDER BY tipo_rebanho, periodo;


-- national
SELECT
tipo_rebanho,
CASE
  WHEN ano BETWEEN 2016 AND 2019 THEN '2016_2019'
  WHEN ano BETWEEN 2020 AND 2024 THEN '2020_2024'
END AS periodo,
SUM(quantidade) AS agg_quantidade,
FROM `basedosdados.br_ibge_ppm.efetivo_rebanhos`
WHERE ano BETWEEN 2016 AND 2024
GROUP BY tipo_rebanho, periodo
ORDER BY tipo_rebanho, periodo;