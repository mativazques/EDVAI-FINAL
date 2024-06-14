# Aviación Civil

La Administración Nacional de Aviación Civil necesita una serie de informes para elevar al Ministerio de Transporte acerca de los aterrizajes y despegues en todo el territorio argentino, como por ejemplo: cuáles aviones son los que más volaron, cuántos pasajeros volaron, ciudades de partidas y aterrizajes entre fechas determinadas, etc. Usted, como data engineer, deberá realizar un pipeline con esta información, automatizarlo y realizar los análisis de datos solicitados que permitan responder las preguntas de negocio y hacer sus recomendaciones con respecto al estado actual.

![img/readme/AVION.jpg](img/readme/AVION.jpg)

## Tareas 
**1.** Hacer ingest de los siguientes archivos relacionados con el transporte aéreo de Argentina.

**Resolución:** Los archivos de la ingesta son: 

[ingest-vuelos-2021.sh](src/ejercicio-1/ingest/ingest-vuelos-2021.sh)

[ingest-vuelos-2022.sh](src/ejercicio-1/ingest/ingest-vuelos-2022.sh)

[ingest-aeropuertos-details.sh](src/ejercicio-1/ingest/ingest-aeropuertos-details.sh)

**2.** Crear 2 tablas en el datawarehouse, una para los vuelos realizados en 2021 y 2022 (2021-informe-ministerio.csv y 202206-informe-ministerio):  

|         Campos         |   Tipo  |
|:----------------------:|:-------:|
| fecha                  | date    |
| horaUTC                | string  |
| clase_de_vuelo         | string  |
| clasificacion_de_vuelo | string  |
| tipo_de_movimiento     | string  |
| aeropuerto             | string  |
| origen_destino         | string  |
| aerolinea_nombre       | string  |
| aeronave               | string  |
| pasajeros              | integer |

Y otra tabla para el detalle de los aeropuertos (aeropuertos_detalle.csv):

|     Campos    |  Tipo  |
|---------------|--------|
| aeropuerto    | string |
| oac           | string |
| iata          | string |
| tipo          | string |
| denominacion  | string |
| coordenadas   | string |
| latitud       | string |
| longitud      | string |
| elev          | float  |
| uom_elev      | string |
| ref           | string |
| distancia_ref | float  |
| direccion_ref | string |
| condicion     | string |
| control       | string |
| region        | string |
| uso           | string |
| trafico       | string |
| sna           | string |
| concesionado  | string |
| provincia     | string |
 
**Resolución:** En el archivo [tables.txt](src/ejercicio-1/tables.txt) se puede ver el código para crear la base de datos y las tablas solicitadas en Hive. 

**3.** Realizar un proceso automático orquestado por Airflow que ingeste los archivos previamente mencionados entre las fechas 01/01/2021 y 30/06/2022 en las dos tablas creadas.

Los archivos 202206-informe-ministerio.csv y 202206-informe-ministerio.csv → en la tabla aeropuerto_tabla

El archivo aeropuertos_detalle.csv → en la tabla aeropuerto_detalles_tabla

**Resolución:** El DAG de Airflow se puede ver en el archivo [ejercicio_final_1.py](src/ejercicio-1/dag/ejercicio_final_1.py).

![img/ejercicio-1/3_dag.png](img/ejercicio-1/3_dag.png)
![img/ejercicio-1/3_dagg.png](img/ejercicio-1/3_dagg.png)

**4.** Realizar las siguientes transformaciones en los pipelines de datos:
- Eliminar la columna inhab ya que no se utilizará para el análisis.
- Eliminar la columna fir ya que no se utilizará para el análisis.
- Eliminar la columna “calidad del dato” ya que no se utilizará para el análisis.
- Filtrar los vuelos internacionales ya que solamente se analizarán los vuelos domésticos.
- En el campo pasajeros, si se encuentran valores nulos, convertirlos en 0 (cero).
- En el campo distancia_ref, si se encuentran valores nulos, convertirlos en 0 (cero).

**Resolución:** Las transformaciones solicitadas se realizaron en Spark y están en los archivos: 

[etl_vuelos.py](src/ejercicio-1/etl/etl_vuelos.py)

[etl_detalles.py](src/ejercicio-1/etl/etl_detalles.py)

**5.** Mostrar mediante una impresión de pantalla que los tipos de campos de las tablas sean los solicitados en el datawarehouse (ej: fecha date, aeronave string, pasajeros integer, etc.).

**Resolución:** 

![img/ejercicio-1/5_vuelos.png](img/ejercicio-1/5_vuelos.png)
![img/ejercicio-1/5_aeropuertos_detalles.png](img/ejercicio-1/5_aeropuertos_detalles.png)

**6.** Determinar la cantidad de vuelos entre las fechas 01/12/2021 y 31/01/2022. Mostrar consulta y resultado de la query.

**Resolución:** 

```sql
SELECT 
    COUNT(*)
FROM
    vuelos
WHERE
    fecha BETWEEN "2021-12-01" AND "2022-01-31";
```

**7.** Cantidad de pasajeros que viajaron en Aerolíneas Argentinas entre el 01/01/2021 y el 30/06/2022. Mostrar consulta y resultado de la query.

**Resolución:** 

```
SELECT 
    SUM(pasajeros)
FROM 
    vuelos
WHERE 
    aerolinea_nombre="AEROLINEAS ARGENTINAS SA"
AND
    fecha BETWEEN "2021-01-01" AND "2022-06-30";
```

![img/ejercicio-1/7_pasajeros.png](img/ejercicio-1/7_pasajeros.png)

**8.** Mostrar fecha, hora, código aeropuerto de salida, ciudad de salida, código de aeropuerto de arribo, ciudad de arribo y cantidad de pasajeros de cada vuelo, entre el 01/01/2022 y el 30/06/2022, ordenados por fecha de manera descendente. Mostrar consulta y resultado de la query.

**Resolución:** 

```
SELECT DISTINCT
    v.fecha,
    v.horautc,
    CASE 
        WHEN v.tipo_de_movimiento = 'Despegue' THEN v.aeropuerto 
        ELSE v.origen_destino 
    END AS codigo_aeropuerto_salida,
    ad_salida.ref AS ciudad_salida,
    CASE 
        WHEN v.tipo_de_movimiento = 'Aterrizaje' THEN v.aeropuerto 
        ELSE v.origen_destino 
    END AS codigo_aeropuerto_arribo,
    ad_arribo.ref AS ciudad_arribo,
    v.pasajeros
FROM
    vuelos v

LEFT JOIN 
    aeropuertos_detalles ad_salida 
ON 
    ad_salida.aeropuerto = CASE 
                            WHEN v.tipo_de_movimiento = 'Despegue' THEN v.aeropuerto 
                            ELSE v.origen_destino 
                            END
LEFT JOIN 
    aeropuertos_detalles ad_arribo 
ON ad_arribo.aeropuerto = CASE 
                            WHEN v.tipo_de_movimiento = 'Aterrizaje' THEN v.aeropuerto 
                            ELSE v.origen_destino 
                            END
WHERE
    fecha BETWEEN "2022-01-01" AND "2022-06-30"
ORDER BY
    v.fecha DESC;
```
![img/ejercicio-1/8_origen_destino.png](img/ejercicio-1/8_origen_destino.png)

**9.** Cuáles son las 10 aerolíneas que más pasajeros llevaron entre el 01/01/2021 y el 30/06/2022, exceptuando aquellas aerolíneas que no tengan nombre. Mostrar consulta y visualización.

**Resolución:** 

```
SELECT DISTINCT 
    aerolinea_nombre,
    SUM(pasajeros) OVER(PARTITION BY aerolinea_nombre) pasajeros_sum
FROM 
    vuelos
WHERE 
    aerolinea_nombre IS NOT NULL
AND
    aerolinea_nombre != '0'
AND
    fecha BETWEEN "2021-01-01" AND "2022-06-30"
ORDER BY 
    pasajeros_sum DESC
LIMIT 10;
```

![img/ejercicio-1/9_top_sum_pasajeros.png](img/ejercicio-1/9_top_sum_pasajeros.png)

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

**11.** Qué datos externos agregarías a este dataset que mejorarían el análisis de los datos.

El objetivo del proyecto es realizar informes acerca de los aterrizajes y despegues en todo el territorio argentino, con lo que creo que se podrían enriquecer estos informes agregando información sobre: 

**Información meteorológica:** Permitiría correlacionar con las condiciones climáticas afectan a retrasos, cancelaciones y seguridad de los vuelos, con la finalidad de mejor la planificación ante estos eventos climáticos. Sería utilidad contar con datos de temperatura, vsibilidad, viento y precipitaciones en los aeropuertos de salida y arribo. 

****

**12.** Elabora tus conclusiones y recomendaciones sobre este proyecto.

**13.** Proponer una arquitectura alternativa para este proceso, ya sea con herramientas on-premise o en la nube (si aplica).