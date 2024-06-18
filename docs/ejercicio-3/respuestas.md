# Ejercicio 3: Google Skills Boost - Dataprep

![dataprep.png](img/dataprep.png)

**1.** ¿Para qué se utiliza Dataprep?

Data Prep es una herramienta que se puede utilizar en GCP y se utiliza para explorar, limpiar y transformar conjuntos de datos para su análIsis, estos datos pueden ser estructurados y no estructurados.

Data Prep facilita la transformación de datos sin tener que escribir código, utilizando una interfaz visual y automatizaciones.

**2.** ¿Qué cosas se pueden realizar con Dataprep?

Es posible conectarse a diversas fuentes de datos como: Cloud Storage, BigQuery, bases de datos SQL, archivos locales, entre otras.

Explorar datos: Obtener información sobre los datos, como tipos de datos, valores únicos, distribuciones, relaciones, máximos, mínimos, etc.

Limpiar datos: Eliminar valores duplicados, corregir errores ortográficos, formatear datos inconsistentes y más.

Transformar datos: Filtrar, agregar, eliminar, ordenar, unir y agregar campos a los datos.

Enriquecer datos: Combinar tus datos con otras fuentes, o crear otras columnas mediante cálculos para obtener información adicional.

Validar datos: Asegurar que los datos cumplan con las reglas de calidad definidas.

Visualizar datos: Crear gráficos y tablas para comprender mejor tus datos.

Automatizar tareas: Crear flujos de trabajo para ejecutar transformaciones de datos de forma repetitiva.

Exportar los datos: Exportar datos a BigQuery, Cloud SQL y otras herramientas de análisis.

**3.** ¿Por qué otra/s herramientas lo podrías reemplazar? ¿Por qué?

**Dataflow:** Es ideal para procesamientos de datos a gran escala y en tiempo real, con alta escalabilidad y rendimiento. Además posee templates para acceder rápidamente a pipelines ya diseñados, que pueden ser personalizados y automatizarse para su ejecución recurrente. La diferencia con Dataprep, es que Dataflow no ofrece la misma interfaz intuitiva y las capacidades de preparación de datos interactivos.

**Data Fusion:** Permite la creación de flujos de trabajo de datos visualmente, utilizando una interfaz gráfica. Es utilizado para la integración de datos, orquestación de flujos de trabajo de datos y automatización de tareas de preparación de datos. La diferencia con Dataprep es que Data Fusion se enfoca en la orquestación de flujos de trabajo, mientras que Dataprep ofrece una gama más amplia de herramientas para la limpieza y transformación de datos.

**4.** ¿Cuáles son los casos de uso comunes de Data Prep de GCP?

**Preparación de datos para análisis:** Limpiar, transformar y enriquecer datos para su uso en herramientas de análisis como BigQuery y Tableau, y para herramientas de ML e IA.

**Integración de datos:** Combinar datos de diferentes fuentes para obtener una vista completa de tu negocio.

**Crear flujos de trabajo reutilizables:** Dataprep permite crear flujos de trabajo de preparación de datos reutilizables que pueden aplicarse a nuevos conjuntos de datos con similar estructura. 

**Cumplimiento normativo:** Dataprep permite establecer reglas de negocio personalizadas para validar los datos y garantizar que cumplan con los requisitos específicos de la organización.

**5.** ¿Cómo se cargan los datos en Data Prep de GCP?

Se cargan creando un nuevo flujo de datos como se ve en la siguiente imagen, o desde la sección "Import Data" en la plataforma. 

Es posible cargar datos de Cloud Storage, BigQuery, Google Sheets (CSV, JSON, Parquet, etc.), bases de datos (Cloud SQL, MySQL, PostgreSQL y SQL Server), aplicaciones (Salesforce y Marketo) y archivos locales.

**6.** ¿Qué tipos de datos se pueden preparar en Data Prep de GCP?

Datos estructurados (csv, parquet, avro, etc.), datos semi estructurados (JSON, XSML, etc.) y datos no estructurados (audio, imágenes), aunque en este último tipo, tiene funciones limitadas. 

**7.** ¿Qué pasos se pueden seguir para limpiar y transformar datos en Data Prep de GCP?

![import](img/import.png)

1. Conectar a tus datos: Seleccionar la fuente de datos y cargar los datos en Dataprep.
2. Explorar los datos: Analizar la información sobre los datos, como tipos de datos, valores únicos, distribuciones y relaciones.

![import](img/prep.png)
![import](img/prep2.png)

3. Limpiar los datos: Eliminar valores duplicados, corregir errores ortográficos, formatear fechas y horas, estandarizar valores de texto.
4. Transformar los datos: Filtrar, agregar, eliminar, ordenar, unir y agregar campos a tus datos.
5. Guardar conjuntos de datos: Guarde los datos transformados en Cloud Storage o BigQuery para su acceso posterior.