# Ejercicio 1: Aviación Civil

La Administración Nacional de Aviación Civil necesita una serie de informes para elevar al Ministerio de Transporte acerca de los aterrizajes y despegues en todo el territorio argentino, como por ejemplo: cuáles aviones son los que más volaron, cuántos pasajeros volaron, ciudades de partidas y aterrizajes entre fechas determinadas, etc. Usted, como data engineer, deberá realizar un pipeline con esta información, automatizarlo y realizar los análisis de datos solicitados que permitan responder las preguntas de negocio y hacer sus recomendaciones con respecto al estado actual.

![img/readme/AVION.jpg](img/readme/AVION.jpg)

## Tareas 

### **1.** Hacer ingest de los siguientes archivos relacionados con el transporte aéreo de Argentina.

**Resolución:** Los archivos de la ingesta son: 

[ingest-vuelos-2021.sh](src/ejercicio-1/ingest/ingest-vuelos-2021.sh)

[ingest-vuelos-2022.sh](src/ejercicio-1/ingest/ingest-vuelos-2022.sh)

[ingest-aeropuertos-details.sh](src/ejercicio-1/ingest/ingest-aeropuertos-details.sh)

### **2.** Crear 2 tablas en el datawarehouse, una para los vuelos realizados en 2021 y 2022 (2021-informe-ministerio.csv y 202206-informe-ministerio):  

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

### **3.** Realizar un proceso automático orquestado por Airflow que ingeste los archivos previamente mencionados entre las fechas 01/01/2021 y 30/06/2022 en las dos tablas creadas.

Los archivos 202206-informe-ministerio.csv y 202206-informe-ministerio.csv → en la tabla aeropuerto_tabla

El archivo aeropuertos_detalle.csv → en la tabla aeropuerto_detalles_tabla

**Resolución:** El DAG de Airflow se puede ver en el archivo [ejercicio_final_1.py](src/ejercicio-1/dag/ejercicio_final_1.py).

![img/ejercicio-1/3_dag.png](img/ejercicio-1/3_dag.png)
![img/ejercicio-1/3_dagg.png](img/ejercicio-1/3_dagg.png)

### **4.** Realizar las siguientes transformaciones en los pipelines de datos:
- Eliminar la columna inhab ya que no se utilizará para el análisis.
- Eliminar la columna fir ya que no se utilizará para el análisis.
- Eliminar la columna “calidad del dato” ya que no se utilizará para el análisis.
- Filtrar los vuelos internacionales ya que solamente se analizarán los vuelos domésticos.
- En el campo pasajeros, si se encuentran valores nulos, convertirlos en 0 (cero).
- En el campo distancia_ref, si se encuentran valores nulos, convertirlos en 0 (cero).

**Resolución:** Las transformaciones solicitadas se realizaron en Spark y están en los archivos: 

[etl_vuelos.py](src/ejercicio-1/etl/etl_vuelos.py)

[etl_detalles.py](src/ejercicio-1/etl/etl_detalles.py)

### **5.** Mostrar mediante una impresión de pantalla que los tipos de campos de las tablas sean los solicitados en el datawarehouse (ej: fecha date, aeronave string, pasajeros integer, etc.).

**Resolución:** 

![img/ejercicio-1/5_vuelos.png](img/ejercicio-1/5_vuelos.png)
![img/ejercicio-1/5_aeropuertos_detalles.png](img/ejercicio-1/5_aeropuertos_detalles.png)

## Arquitectura

La implementación del proyecto puede verse de manera gráfica a continuación: 

![img/readme/arq.png](img/readme/arq.png)

### Por medio de consultas SQL al data warehouse, mostrar consulta y resultado de la query:

**6.** Determinar la cantidad de vuelos entre las fechas 01/12/2021 y 31/01/2022. 

**7.** Cantidad de pasajeros que viajaron en Aerolíneas Argentinas entre el 01/01/2021 y el 30/06/2022. 

**8.** Mostrar fecha, hora, código aeropuerto de salida, ciudad de salida, código de aeropuerto de arribo, ciudad de arribo y cantidad de pasajeros de cada vuelo, entre el 01/01/2022 y el 30/06/2022, ordenados por fecha de manera descendente. 

**9.** Cuáles son las 10 aerolíneas que más pasajeros llevaron entre el 01/01/2021 y el 30/06/2022, exceptuando aquellas aerolíneas que no tengan nombre. 

**10.** Cuáles son las 10 aeronaves más utilizadas entre el 01/01/2021 y el 30/06/2022 que despegaron desde la Ciudad Autónoma de Buenos Aires o desde Buenos Aires, exceptuando aquellas aeronaves que no cuentan con nombre. 

**Resolución 6, 7, 8, 9 y 10:** 
[Queries](src/ejercicio-1/queries/queries-1.md)

### **11.** Qué datos externos agregarías a este dataset que mejorarían el análisis de los datos.

El objetivo del proyecto es realizar informes acerca de los aterrizajes y despegues en todo el territorio argentino, con lo que creo que se podrían enriquecer estos informes agregando información sobre:

**Información meteorológica:** Permitiría correlacionar cómo las condiciones climáticas afectan a retrasos, cancelaciones y seguridad de los vuelos, con la finalidad de mejorar la planificación ante estos eventos climáticos. Sería útil contar con datos de temperatura, visibilidad, viento y precipitaciones en los aeropuertos de salida y arribo.

**Combustible y emisiones:** Permitiría analizar el impacto ambiental según cada vuelo o según cada grupo de vuelos. Los datos deberían ser de combustible y emisión de CO2.

**Identificador de vuelo:** La información en la tabla de vuelos no cuenta con un identificador para cada vuelo. Este identificador permitiría poder cruzar la información del vuelo con tablas con datos demográficos de los tripulantes, con datos de los pilotos y personal de servicio, y con datos de precios de boletos en caso de vuelos civiles.

**Datos de costos:** KPIs estándares en términos de vuelos como el costo por milla de asiento disponible (CASM), costo por pasajero embarcado (CPE), costo operativo directo por hora bloque (DOC) y el costo de mantenimiento por hora de vuelo, serían posibles si se tuvieran datos de los costos operativos totales, costos de mantenimiento totales y el número de asientos que una compañía aérea pone a disposición por cada milla que un avión de esta recorre.

### **12.** Elabora tus conclusiones y recomendaciones sobre este proyecto.



### **13.** Proponer una arquitectura alternativa para este proceso, ya sea con herramientas on-premise o en la nube (si aplica).

**Resolución:** Se puede replicar la arquitectura del proyecto en la nube a través de Google Cloud Platform, integrando las herramientas Google Cloud Storage: 

*Google Cloud Storage:* Para el almacenamiento de objetos en la nube, similar a HDFS pero con mayor escalabilidad y disponibilidad.

*Dataproc:* Permite ejecutar aplicaciones de Hadoop y Spark en clústeres de máquinas virtuales. 

*Composer:* Servicio de orquestación de flujos de trabajo en la nube, permite crear, programar y monitorear flujos de trabajo de Apache Airflow. 

*BigQuery:* Datawarehouse en la nube que te permite almacenar, consultar y analizar datos de forma rápida y eficiente. Es una alternativa a Hive.

![img/ejercicio-1/13_gcp.png](img/ejercicio-1/13_gcp.png)

Para realizar el ETL también es posible hacer el proceso ETL con Apache Beam, y utilizar Postgres como data warehouse. 

![img/ejercicio-1/13_beam.png](img/ejercicio-1/13_beam.png)

En contraste, también es posible utilizar Beam en GCP, mediante Dataflow. 

![img/ejercicio-1/13_dflow.png](img/ejercicio-1/13_dflow.png)


# Ejercicio 2: Alquiler de automóviles

Una de las empresas líderes en alquileres de automóviles solicita una serie de dashboards y reportes para poder basar sus decisiones en datos. Entre los indicadores mencionados se encuentran total de alquileres, segmentación por tipo de combustible, lugar, marca y modelo de automóvil, valoración de cada alquiler, etc.

Como Data Engineer debe crear y automatizar el pipeline para tener como resultado los datos listos para ser visualizados y responder las preguntas de negocio.

### 1. Crear en Hive una database `car_rental_db` y dentro una tabla llamada `car_rental_analytics`, con estos campos:

| campos           | tipo    |
|------------------|---------|
| fuelType         | string  |
| rating           | integer |
| renterTripsTaken | integer |
| reviewCount      | integer |
| city             | string  |
| state_name       | string  |
| owner_id         | integer |
| rate_daily       | integer |
| make             | string  |
| model            | string  |
| year             | integer |

**Resolución:** En el archivo [tables.txt](src/ejercicio-2/tables.txt) se puede ver el código para crear la base de datos y la tabla solicitadas en Hive. 

![img/ejercicio-2/1.png](img/ejercicio-2/1.png)

### 2. Crear script para el ingest de estos dos files

- [https://edvaibucket.blob.core.windows.net/data-engineer-edvai/CarRentalData.csv?sp=r&st=2023-11-06T12:52:39Z&se=2025-11-06T20:52:39Z&sv=2022-11-02&sr=c&sig=J4Ddi2c7Ep23OhQLPisbYaerlH472iigPwc1%2FkG80EM%3D](https://edvaibucket.blob.core.windows.net/data-engineer-edvai/CarRentalData.csv?sp=r&st=2023-11-06T12:52:39Z&se=2025-11-06T20:52:39Z&sv=2022-11-02&sr=c&sig=J4Ddi2c7Ep23OhQLPisbYaerlH472iigPwc1%2FkG80EM%3D)
- [https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-united-states-of-america-state/exports/csv?lang=en&timezone=America%2FArgentina%2FBuenos_Aires&use_labels=true&delimiter=%3B](https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-united-states-of-america-state/exports/csv?lang=en&timezone=America%2FArgentina%2FBuenos_Aires&use_labels=true&delimiter=%3B)

**Sugerencia:** descargar el segundo archivo con un comando similar al abajo mencionado, ya que al tener caracteres como ‘&’ falla si no se le asignan comillas. Adicionalmente, el parámetro `-O` permite asignarle un nombre más legible al archivo descargado.

```bash
wget -P ruta_destino -O ruta_destino/nombre_archivo.csv ruta_al_archivo
```

**Resolución:** El archivo de la ingesta es: 
[ingest-car_rental_data.sh](src/ejercicio-2/ingest/ingest-car_rental_data.sh)

### 3. Crear un script para tomar el archivo desde HDFS y hacer las siguientes transformaciones:

- En donde sea necesario, modificar los nombres de las columnas. Evitar espacios y puntos (reemplazar por `_`). Evitar nombres de columna largos.
- Redondear los float de `rating` y castear a int.
- Joinear ambos files.
- Eliminar los registros con `rating` nulo.
- Cambiar mayúsculas por minúsculas en `fuelType`.
- Excluir el estado Texas.

Finalmente insertar en Hive el resultado.

**Resolución:** El archivo donde se realizan las transformaciones es: 
[etl_car_rental_data.py](src/ejercicio-2/etl/etl_car_rental_data.py)

### 4. Realizar un proceso automático en Airflow que orqueste los pipelines creados en los puntos anteriores. Crear dos tareas:

a. Un DAG padre que ingeste los archivos y luego llame al DAG hijo.
b. Un DAG hijo que procese la información y la cargue en Hive.

**Resolución:** Los archivos con los dag son: 

[ejercicio_final_2_dag_padre.py](src/ejercicio-2/dag/ejercicio_final_2_dag_padre.py)

[ejercicio_final_2_dag_hijo.py](src/ejercicio-2/dag/ejercicio_final_2_dag_hijo.py)

![img/ejercicio-2/4_padre.png](img/ejercicio-2/4_padre.png)
![img/ejercicio-2/4_hijo.png](img/ejercicio-2/4_hijo.png)

### 5. Por medio de consultas SQL al data warehouse, mostrar:

a. Cantidad de alquileres de autos, teniendo en cuenta sólo los vehículos ecológicos (fuelType híbrido o eléctrico) y con un rating de al menos 4.

b. Los 5 estados con menor cantidad de alquileres (crear visualización).

c. Los 10 modelos (junto con su marca) de autos más rentados (crear visualización).

d. Mostrar por año, cuántos alquileres se hicieron, teniendo en cuenta automóviles fabricados desde 2010 a 2015.

e. Las 5 ciudades con más alquileres de vehículos ecológicos (fuelType híbrido o eléctrico).

f. El promedio de reviews, segmentando por tipo de combustible.

**Resolución:** [Queries](src/ejercicio-2/queries/queries-2.md)

### 6. Elabore sus conclusiones y recomendaciones sobre este proyecto.

### 7. Proponer una arquitectura alternativa para este proceso ya sea con herramientas on premise o cloud (si aplica).

**Resolución:** Una arquitectura alternativa puede ser como cualquiera de las que plantee en el punto anterior. 

En ambos casos, en la parte de la ingesta desde la web, y puesta en HDFS, también se puede utilizar Apache Nifi. 


# Ejercicio 3: Google Skills Boost

Realizar el siguiente LAB, al finalizar pegar un print screen donde se ve su perfil y el progreso
final verificado: 

https://www.cloudskillsboost.google/focuses/4415?catalog_rank=%7B%22rank%22%3A1%2C%22num_filters%22%3A0%2C%22has_search%22%3Atrue%7D&parent=catalog&search_id=32278924

**Resolución:** 

![GoogleSkillsBoost.png](img/ejercicio-3/GoogleSkillsBoost.png)

### Contestar las siguientes preguntas: 

1. ¿Para qué se utiliza Dataprep?
2. ¿Qué cosas se pueden realizar con Dataprep?
3. ¿Por qué otra/s herramientas lo podrías reemplazar? ¿Por qué?
4. ¿Cuáles son los casos de uso comunes de Dataprep de GCP?
5. ¿Cómo se cargan los datos en Dataprep de GCP?
6. ¿Qué tipos de datos se pueden preparar en Dataprep de GCP?
7. ¿Qué pasos se pueden seguir para limpiar y transformar datos en Dataprep de GCP?
8. ¿Cómo se pueden automatizar tareas de preparación de datos en Dataprep de GCP?
9. ¿Qué tipos de visualizaciones se pueden crear en Dataprep de GCP?
10. ¿Cómo se puede garantizar la calidad de los datos en Dataprep de GCP?

**Resolución:** [Respuestas Google Skills Boost](src/ejercicio-3/respuestas.md)


# Ejercicio 4: Arquitectura 

El gerente de Analítica te pide realizar una arquitectura hecha en GCP que contemple el uso de esta herramienta, ya que le parece muy fácil de usar y tiene una interfaz visual que ayuda a sus desarrolladores, ya que no necesitan conocer ningún lenguaje de desarrollo.

Esta arquitectura debería contemplar las siguientes etapas:

**1. Ingesta**: datos parquet almacenados en un bucket de S3 y datos de una aplicación que guarda sus datos en Cloud SQL.
**2. Procesamiento**: filtrar, limpiar y procesar datos provenientes de estas fuentes.
**3. Almacenamiento**: almacenar los datos procesados en BigQuery.
**4. BI**: herramientas para visualizar la información almacenada en el Data Warehouse.
**5. ML**: herramienta para construir un modelo de regresión lineal con la información almacenada en el Data Warehouse.
