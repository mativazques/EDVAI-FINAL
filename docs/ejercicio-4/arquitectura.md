# Ejercicio 4: Arquitectura 

El gerente de Analítica te pide realizar una arquitectura hecha en GCP que contemple el uso de Dataprep, ya que le parece muy fácil de usar y tiene una interfaz visual que ayuda a sus desarrolladores, ya que no necesitan conocer ningún lenguaje de desarrollo.

Esta arquitectura debería contemplar las siguientes etapas:

**1. Ingesta**: datos parquet almacenados en un bucket de S3 y datos de una aplicación que guarda sus datos en Cloud SQL.

**2. Procesamiento**: filtrar, limpiar y procesar datos provenientes de estas fuentes.

**3. Almacenamiento**: almacenar los datos procesados en BigQuery.

**4. BI**: herramientas para visualizar la información almacenada en el Data Warehouse.

**5. ML**: herramienta para construir un modelo de regresión lineal con la información almacenada en el Data Warehouse.
 
## Desarrollo 

### 1. Ingesta

**Datos Parquet en S3:** se va a utilizar Google Cloud Composer para orquestar la transferencia de archivos Parquet desde el bucket de Amazon S3 a un bucket en Google Cloud Storage (GCS). Esto se puede lograr utilizando operadores de Airflow como S3ToGCSOperator.

**Datos de Cloud SQL:** también con Cloud Composer se va a automatizar la exportación de datos desde Cloud SQL a GCS. Esto se puede realizar mediante operadores de Airflow como MySqlToGCSOperator o PostgresToGCSOperator.

**Google Cloud Storage (GCS):** como destino de los datos exportados desde Cloud SQL como los datos transferidos desde S3, se utilizará un bucket de GCS que actúa como una área de staging.

### 2. Procesamiento

**Google Cloud Dataprep:** luego de la configuración de la ingesta hay que configurar flujos de trabajo (recipes) en Dataprep para automatizar los procesos de transformación.

Primero hay que conectar Dataprep a los datos almacenados en GCS. Luego, diseñar las tareas de limpieza, filtrado y procesamiento de datos. 

Finalmente hay que configurar Dataprep para exportar los datos procesados a BigQuery.

Para la orquestación de la ejecución de las tareas de Dataprep, se utilizará Composer.

### 3. Almacenamiento

**Google BigQuery:** es necesario crear datasets y tablas en BigQuery para organizar los datos transformados.

### 4. BI 

**Looker:** se utilizará Looker como herramienta de visualización. Es necesario conectar Looker a BigQuery para crear dashboards interactivos y reportes.

### 5. ML

**Vertex AI:** se utilizará Vertex AI para construir, entrenar y desplegar un modelo de regresión lineal.

Aunque también se puede utilizar BigQuery ML como una alternativa rápida y simple para entrenar modelos de ML directamente en BigQuery, si los requerimientos son básicos. 

# Modelado 

La arquitectura planteada se puede observar a continuación. 

![arq.png](img/arq.png)