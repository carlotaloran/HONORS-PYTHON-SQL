-- sample, temp
SELECT
produto,
CASE
  WHEN ano BETWEEN 2016 AND 2019 THEN '2016_2019'
  WHEN ano BETWEEN 2020 AND 2024 THEN '2020_2024'
END AS periodo,
SUM(valor_producao) AS agg_valor,
SUM(quantidade_produzida) AS agg_quantidade,
SUM(area_colhida) AS agg_area_colhida,
SAFE_DIVIDE(
  SUM(quantidade_produzida),
  NULLIF(SUM(area_colhida), 0)
) AS br_rendimento
FROM `basedosdados.br_ibge_pam.lavoura_temporaria` -- change temporaria to permanente to get permantent
WHERE ano BETWEEN 2016 AND 2024
 AND sigla_uf IN ('AP','DF','GO','MA','MT','MS','PA','PI','RO','TO') -- delete line to get national
GROUP BY produto, periodo
ORDER BY produto, periodo;


-- national, temp
SELECT
produto,
CASE
  WHEN ano BETWEEN 2016 AND 2019 THEN '2016_2019'
  WHEN ano BETWEEN 2020 AND 2024 THEN '2020_2024'
END AS periodo,
SUM(valor_producao) AS agg_valor,
SUM(quantidade_produzida) AS agg_quantidade,
SUM(area_colhida) AS agg_area_colhida,
SAFE_DIVIDE(
  SUM(quantidade_produzida),
  NULLIF(SUM(area_colhida), 0)
) AS br_rendimento
FROM `basedosdados.br_ibge_pam.lavoura_temporaria` -- change temporaria to permanente to get permantent
WHERE ano BETWEEN 2016 AND 2024
GROUP BY produto, periodo
ORDER BY produto, periodo;


-- sample, perm
SELECT
produto,
CASE
  WHEN ano BETWEEN 2016 AND 2019 THEN '2016_2019'
  WHEN ano BETWEEN 2020 AND 2024 THEN '2020_2024'
END AS periodo,
SUM(valor_producao) AS agg_valor,
SUM(quantidade_produzida) AS agg_quantidade,
SUM(area_colhida) AS agg_area_colhida,
SAFE_DIVIDE(
  SUM(quantidade_produzida),
  NULLIF(SUM(area_colhida), 0)
) AS br_rendimento
FROM `basedosdados.br_ibge_pam.lavoura_permanente` -- change permanente to temporaria to get seasonal
WHERE ano BETWEEN 2016 AND 2024
 AND sigla_uf IN ('AP','DF','GO','MA','MT','MS','PA','PI','RO','TO') -- delete line to get national
GROUP BY produto, periodo
ORDER BY produto, periodo;


-- national, perm
SELECT
produto,
CASE
  WHEN ano BETWEEN 2016 AND 2019 THEN '2016_2019'
  WHEN ano BETWEEN 2020 AND 2024 THEN '2020_2024'
END AS periodo,
SUM(valor_producao) AS agg_valor,
SUM(quantidade_produzida) AS agg_quantidade,
SUM(area_colhida) AS agg_area_colhida,
SAFE_DIVIDE(
  SUM(quantidade_produzida),
  NULLIF(SUM(area_colhida), 0)
) AS br_rendimento
FROM `basedosdados.br_ibge_pam.lavoura_permanente` -- change permanente to temporaria to get seasonal
WHERE ano BETWEEN 2016 AND 2024
GROUP BY produto, periodo
ORDER BY produto, periodo;