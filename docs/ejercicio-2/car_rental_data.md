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

**Resolución:** En el archivo [tables.txt](../../src/ejercicio-2/tables.txt) se puede ver el código para crear la base de datos y la tabla solicitadas en Hive. 

![img/1.png](img/1.png)

### 2. Crear script para el ingest de estos dos files

- [https://edvaibucket.blob.core.windows.net/data-engineer-edvai/CarRentalData.csv?sp=r&st=2023-11-06T12:52:39Z&se=2025-11-06T20:52:39Z&sv=2022-11-02&sr=c&sig=J4Ddi2c7Ep23OhQLPisbYaerlH472iigPwc1%2FkG80EM%3D](https://edvaibucket.blob.core.windows.net/data-engineer-edvai/CarRentalData.csv?sp=r&st=2023-11-06T12:52:39Z&se=2025-11-06T20:52:39Z&sv=2022-11-02&sr=c&sig=J4Ddi2c7Ep23OhQLPisbYaerlH472iigPwc1%2FkG80EM%3D)
- [https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-united-states-of-america-state/exports/csv?lang=en&timezone=America%2FArgentina%2FBuenos_Aires&use_labels=true&delimiter=%3B](https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-united-states-of-america-state/exports/csv?lang=en&timezone=America%2FArgentina%2FBuenos_Aires&use_labels=true&delimiter=%3B)

**Sugerencia:** descargar el segundo archivo con un comando similar al abajo mencionado, ya que al tener caracteres como ‘&’ falla si no se le asignan comillas. Adicionalmente, el parámetro `-O` permite asignarle un nombre más legible al archivo descargado.

```bash
wget -P ruta_destino -O ruta_destino/nombre_archivo.csv ruta_al_archivo
```

**Resolución:** El archivo de la ingesta es: 
[ingest-car_rental_data.sh](../../src/ejercicio-2/ingest/ingest-car_rental_data.sh)


### 3. Crear un script para tomar el archivo desde HDFS y hacer las siguientes transformaciones:

- En donde sea necesario, modificar los nombres de las columnas. Evitar espacios y puntos (reemplazar por `_`). Evitar nombres de columna largos.
- Redondear los float de `rating` y castear a int.
- Joinear ambos files.
- Eliminar los registros con `rating` nulo.
- Cambiar mayúsculas por minúsculas en `fuelType`.
- Excluir el estado Texas.

Finalmente insertar en Hive el resultado.

**Resolución:** El archivo donde se realizan las transformaciones es: 
[etl_car_rental_data.py](../../src/ejercicio-2/etl/etl_car_rental_data.py)

### 4. Realizar un proceso automático en Airflow que orqueste los pipelines creados en los puntos anteriores. Crear dos tareas:

a. Un DAG padre que ingeste los archivos y luego llame al DAG hijo.
b. Un DAG hijo que procese la información y la cargue en Hive.

**Resolución:** Los archivos con los dag son: 

[ejercicio_final_2_dag_padre.py](../../src/ejercicio-2/dag/ejercicio_final_2_dag_padre.py)

[ejercicio_final_2_dag_hijo.py](../../src/ejercicio-2/dag/ejercicio_final_2_dag_hijo.py)

![img/4_padre.png](img/4_padre.png)
![img/4_hijo.png](img/4_hijo.png)

### 5. Por medio de consultas SQL al data warehouse, mostrar:

a. Cantidad de alquileres de autos, teniendo en cuenta sólo los vehículos ecológicos (fuelType híbrido o eléctrico) y con un rating de al menos 4.

b. Los 5 estados con menor cantidad de alquileres (crear visualización).

c. Los 10 modelos (junto con su marca) de autos más rentados (crear visualización).

d. Mostrar por año, cuántos alquileres se hicieron, teniendo en cuenta automóviles fabricados desde 2010 a 2015.

e. Las 5 ciudades con más alquileres de vehículos ecológicos (fuelType híbrido o eléctrico).

f. El promedio de reviews, segmentando por tipo de combustible.

**Resolución:** [Queries](queries/queries-2.md)

**Visualización:** Para la visualización se exportó un .csv ([car_rental.csv](docs/ejercicio-2/car_rental.csv)) desde Spark después de las transformaciones pedidas para poder hacer las visualizaciones en Power BI. 

El archivo de la visualización en Power BI: [Alquiler de automóviles](docs/ejercicio-2/Alquiler_de_automoviles.pbix)

![pbi](img/pbi.png)

### 6. Elabore sus conclusiones y recomendaciones sobre este proyecto.

#### Alquileres de automóviles ecológicos:

El alquiler en modelos ecológicos (híbridos y eléctricos) que representan un 15% de la demanda total con un rating entre 4 y 5. 

**Recomendación:** si se quiere aumentar la demanda de autos ecológicos para que reprensente mayor parte de la demanda se debe fortalecer la flota de vehículos. 

#### Segmentación por lugar:

San Diego, Las Vegas, Los Angeles, San Francisco y Portland son las ciudades con más alquileres de vehículos ecológicos. Estados como Montana y Arkansas tienen la menor cantidad de alquileres.

**Recomendación:** la compañía se debe enfocar en estrategias de marketing y promociones en las ciudades con más demanda para maximizar ingresos. Analizar las razones de baja demanda en ciertos estados y ajustar la oferta o estrategias de mercado en consecuencia.

#### Segmentación por marca y modelo de automóvil:

Modelos como Tesla Model 3 y Ford Mustang son los más rentados, lo que indica la popularidad de ciertas marcas y modelos entre los clientes.

**Recomendación:** hay que mantener una flota bien abastecida de los modelos más populares y evaluar la incorporación de nuevos modelos de estas marcas para satisfacer la demanda y atraer nuevos clientes.

### 7. Proponer una arquitectura alternativa para este proceso ya sea con herramientas on premise o cloud (si aplica).

**Resolución:** Por la similitud en los pipelines, una arquitectura alternativa puede ser como cualquiera de las que se plantearon en el ejercicio 1. 

Como alternativa extra, en ambos ejercicios: en la parte de la ingesta desde otro proveedor cloud, y puesta en HDFS, también se puede utilizar Apache Nifi. 
