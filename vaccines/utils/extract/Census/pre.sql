SELECT "ESTIAP", year, count(*) as count
FROM vaccines
WHERE "ESTIAP" IN ('IL-CITY OF CHICAGO', 'NY-CITY OF NEW YORK')
GROUP BY "ESTIAP", year
ORDER BY "ESTIAP", year;