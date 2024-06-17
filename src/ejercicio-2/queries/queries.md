**10.** Cuáles son las 10 aeronaves más utilizadas entre el 01/01/2021 y el 30/06/2022 que despegaron desde la Ciudad Autónoma de Buenos Aires o desde Buenos Aires, exceptuando aquellas aeronaves que no cuentan con nombre. Mostrar consulta y visualización.

**Resolución:** 

```
SELECT DISTINCT
    v.aeronave,
    COUNT(v.aeronave) OVER(PARTITION BY aeronave) aeronave_sum
FROM
    vuelos v
LEFT JOIN
    aeropuertos_detalles ad
ON ad.aeropuerto = v.aeropuerto
WHERE 
    tipo_de_movimiento = 'Despegue'
AND
    fecha BETWEEN "2021-01-01" AND "2022-06-30"
AND 
    ad.provincia LIKE '%BUENOS AIRES' 
AND
    v.aeronave != '0'
ORDER BY 
    aeronave_sum DESC
LIMIT 10;
```

![img/ejercicio-1/10_aeronaves.png](img/ejercicio-1/10_aeronaves.png)
