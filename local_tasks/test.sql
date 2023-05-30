-- a count query for all rows in vaccines table where the ESTIAP column is equal to either "IL-CITY OF CHICAGO" or "NY-CITY OF NEW YORK" group by ESTIAP and year
SELECT "ESTIAP", year, count(*) as count
FROM vaccines
WHERE "ESTIAP" IN ('IL-CITY OF CHICAGO', 'NY-CITY OF NEW YORK')
GROUP BY "ESTIAP", year
ORDER BY "ESTIAP", year;
```