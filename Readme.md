# Proyecto: Topicos de Telemática ST0263
## Estudiantes
- **Nombre:** Juan Pablo Ramirez, Luis Felipe Urquijo Vargas, David Sanchez Arboleda
- **Correo Electrónico:** jurami35@eafit.edu.co, lfurquijov@eafit.edu.co, dasancheza@eafit.edu.co

## Profesor
- **Nombre:** Alvaro Enrique Ospina Sanjuan
- **Correo Electrónico:** aeospinas@eafit.edu.co

## Introducción
En el contexto de la creciente necesidad de manejar grandes volúmenes de datos de manera eficiente y escalable, los sistemas de archivos distribuidos han emergido como una solución fundamental. Estos sistemas permiten compartir y acceder a archivos almacenados en diferentes nodos de manera concurrente, lo que resulta especialmente relevante para entornos donde la cantidad de datos supera la capacidad de almacenamiento de un solo servidor.
El presente trabajo tiene como objetivo diseñar e implementar un sistema de archivos distribuidos minimalista, que combine las características de los enfoques basados en bloques y objetos para ofrecer una solución eficaz y versátil. En particular, nos centraremos en un diseño que incorpore la escalabilidad y la tolerancia a fallos de los sistemas de archivos basados en bloques, con la simplicidad y la eficiencia en el almacenamiento de objetos.
Para comprender mejor el contexto y los principios fundamentales que guiarán nuestro trabajo, es necesario revisar los antecedentes de investigación en el área de sistemas de archivos distribuidos, así como los conceptos clave presentados en los papers fundacionales de sistemas como el Google File System (GFS) y el Hadoop Distributed File System (HDFS).
Estos sistemas representan hitos importantes en el desarrollo de tecnologías de almacenamiento distribuido y proporcionarán una base sólida para nuestro proyecto.
A lo largo de este trabajo, se describirá la arquitectura propuesta para el sistema de archivos distribuidos minimalista, detallando los protocolos de comunicación entre sus componentes, el proceso de escritura y lectura de archivos. Además, se presentarán los entregables planificados y los plazos de ejecución para cada etapa del proyecto.

## Descripción
El proyecto implica el desarrollo de una plataforma de almacenamiento distribuido con dos tipos de comunicaciones entre procesos: un Canal de Control y un Canal de Datos. Se establece un algoritmo para la distribución de bloques y su replicación, donde cada archivo se divide en bloques y se replica en al menos dos DataNodes para tolerancia a fallos. La transferencia de archivos se realiza desde los DataNodes que contienen los bloques principales o replicas, y el NameNode coordina la selección óptima de DataNodes para la escritura de archivos. Además, se introduce el concepto de Leader y Follower para la replicación de bloques entre DataNodes, asegurando así la tolerancia a fallos en el sistema.

## Fundamentos Teóricos
Presentación de las teorías, conceptos y modelos relevantes para el estudio.
Se evidencia el manejo de dos arquitecturas, por un lado, GFS y por el otro HFS:
-	Arquitectura GFS: opera en una arquitectura maestro/esclavo con un maestro central controlando los metadatos y numerosos servidores de fragmentos que almacenan bloques de datos reales. El sistema emplea un mecanismo de almacenamiento basado en fragmentos, donde los archivos se dividen en fragmentos de tamaño fijo, optimizando significativamente la gestión y el acceso a los datos. Como no todos los archivos tienen un tamaño fijo, existen métodos para que el sistema continue funcionando, como lo es llenar el espacio restante con 0’s, manteniendo el sistema con bloques de tamaño fijo.
-	Arquitectura HDFS: reconocido por su capacidad para gestionar conjuntos de datos extremadamente grandes con un alto grado de eficiencia. Su arquitectura se compone principalmente de dos componentes principales: el NameNode y los DataNodes. El NameNode orquesta los metadatos del sistema de archivos y la ubicación de los bloques de datos, mientras que los DataNodes almacenan los datos reales. Uno de los aspectos críticos de HDFS es su tolerancia a fallos, lograda mediante la replicación de bloques, con una configuración predeterminada de tres copias. Esta replicación garantiza que los datos no se pierdan incluso si un nodo falla. La arquitectura de HDFS permite interacciones directas del cliente con los DataNodes para transferencias de datos, evitando la creación de un cuello de botella en el NameNode.
Para cada arquitectura, existen distintos componentes que permiten su implementación:
-	Componentes GFS:
o	Maestro: también se conoce como servidor maestro, es el componente central de la arquitectura. Coordina todas las operaciones del sistema de archivos, incluyendo la gestión de metadatos, el control de acceso, la información sobre la estructura del sistema de archivos, como la ubicación de los fragmentos de datos y las réplicas.
o	Chunk servers o servidores de fragmentos: estos actúan como los nodos de almacenamiento que contienen los bloques de datos reales, que también se conocen como chunks. También, son los responsables de almacenar, recuperar y servir los fragmentos de datos apetición del maestro o los clientes.
o	Cliente: responsables de acceder al sistema de archivos de GFS para leer, escribir o modificar datos. Interactúan directamente con el maestro para obtener información sobre la ubicación de los datos y luego acceden a los fragmentos directamente con los chunks.
-	Componentes HDFS:
o	NameNode: El Servidor Maestro actúa como el "cerebro" del sistema de archivos. Almacena todos los detalles sobre cómo se organizan los archivos y directorios, así como la ubicación de los bloques de datos en el clúster. Utiliza la información proporcionada por los servidores de datos para mantener esta estructura actualizada en su memoria RAM.
o	DataNode: Los Servidores de Datos (DataNodes) son como los "guardaespaldas" del sistema. Su principal función es almacenar los bloques de datos que componen los archivos y proporcionarlos al Servidor Maestro (NameNode) o a los clientes que los solicitan.
-	Procesos de escritura y lectura GFS:
 
o	El proceso de escritura en GFS inicia cuando un cliente envía una solicitud al maestro, esta solicitud incluye el nombre del archivo y los datos. El nodo maestro consulta el catálogo para determinar la ubicación de los fragmentos de cada archivo. Una vez el maestro localiza los fragmentos, determina el Chunkserver en los que están, normalmente, cada fragmento se replica en múltiples Chunkservers para la tolerancia a fallos. El cliente envía los datos a escribir y cada chunk almacena los datos y actualiza su estado. El cliente recibe una confirmación del nodo maestro, confirmando el proceso de forma exitosa.
o	El proceso de lectura inicia cuando el cliente desea leer datos de un archivo enviando una solicitud al maestro. Nuevamente, esta solicitud incluye el nombre del archivo y la posición de inicio de lectura. El maestro consulta el catálogo para determinar la ubicación de los fragmentos de cada archivo. Una vez localizado el Chunkserver que alberga el archivo o los archivos a leer, el cliente solicita los datos al servidor correspondiente y este se encarga de enviárselos. El cliente recibirá los datos y los procesa según sea necesario.
-	Procesos de escritura y lectura HDFS
o	El proceso de escritura en HDFS inicia con la solicitud del cliente al namenode para escribir un archivo, tras lo cual el namenode realiza comprobaciones previas y otorga el permiso correspondiente. Posteriormente, el cliente particiona el archivo en bloques y para cada bloque, el cliente recibe una lista de datanodes donde escribirlo. Acto seguido, el cliente envía cada bloque secuencialmente a los datanodes correspondientes, y cada datanode confirma la escritura del bloque. Una vez que todos los bloques han sido escritos, el cliente informa al namenode de la finalización del proceso.
o	El Proceso de lectura, este se inicia con la solicitud del cliente al namenode para la recuperación de un archivo. El namenode busca en sus metadatos los bloques que componen el archivo y sus ubicaciones, y proporciona al cliente una lista de datanodes donde encontrar los bloques. Luego, el cliente contacta a cada datanode para obtener los bloques necesarios, y con los bloques obtenidos, reconstruye el archivo original.

## Antecedentes de la Investigación
Antes de la introducción del Google File System (GFS), varios sistemas de archivos se utilizaron ampliamente en entornos distribuidos y de almacenamiento de datos a gran escala. Algunos de los sistemas de archivos más comunes que precedieron a GFS incluyen:
•	NFS (Network File System): NFS es un protocolo estándar de la industria que permite a los usuarios acceder y compartir archivos a través de una red. Fue desarrollado por Sun Microsystems en la década de 1980 y se convirtió en uno de los primeros sistemas de archivos distribuidos ampliamente utilizados. NFS sigue siendo utilizado en muchos entornos, especialmente en redes Unix y Linux.
 
•	AFS (Andrew File System): AFS es un sistema de archivos distribuidos desarrollado en la Universidad Carnegie Mellon en la década de 1980. Fue uno de los primeros sistemas de archivos distribuidos comerciales y se utilizó ampliamente en entornos académicos y de investigación.
•	Coda File System: Coda es otro sistema de archivos distribuidos desarrollado en la Universidad Carnegie Mellon como un sucesor del AFS. Se diseñó para ser altamente escalable y tolerante a fallos, lo que lo hace adecuado para entornos distribuidos a gran escala.
•	Lustre File System: Lustre es un sistema de archivos paralelo distribuido de alto rendimiento diseñado para aplicaciones de computación de alto rendimiento (HPC) y grandes volúmenes de datos. Se utiliza en muchos supercomputadores y centros de datos de alto rendimiento en todo el mundo.

## Retos
Consistencia de datos: Mantener la consistencia de los datos distribuidos en múltiples nodos es fundamental para evitar inconsistencias y corrupción de datos. Esto implica implementar algoritmos de consenso y mecanismos de sincronización robustos.
Tolerancia a fallos: Un sistema de archivos distribuido debe ser capaz de tolerar fallos en los nodos individuales sin comprometer la integridad de los datos. Esto implica diseñar estrategias de replicación y recuperación ante fallos.
Rendimiento: Mantener un buen rendimiento en operaciones de lectura y escritura es crucial para garantizar una experiencia de usuario fluida. Esto implica optimizar la distribución de datos y minimizar la latencia de red.
Escalabilidad: El sistema debe escalar eficientemente según se agregan más nodos al clúster. Esto implica minimizar los cuellos de botella y diseñar algoritmos de distribución de carga eficientes.

## Protocolos y/o APIs entre los diferentes componentes del sistema
-	Para la comunicación entre cliente y el NameNode, utilizaremos interfaces rest en el canal de control para los procesos de lectura.
-	Para la comunicación entre el cliente y los DataNode usaremos interfaces gRPC para los procesos de escritura por medio del canal de datos.
-	Para la comunicación entre DataNode’s, por medio de un canal de datos se harán las respectivas replicaciones de los bloques en cada DataNode según sea especificado.

Estas comunicaciones serian de la forma representrada en la arquitectura a continuación: 
# Arquitectura
[![imagen-2024-04-07-230939054.png](https://i.postimg.cc/6pdXwdNV/imagen-2024-04-07-230939054.png)](https://postimg.cc/Js4g5H0t)

## Entorno de Desarrollo y Configuraciones

## Lenguaje de Programación

## Librerías Utilizadas
- **grpcio** v1.62.0
- **grpcio-tools** v1.62.0
- **Flask** v3.0.0
- **requests** v2.31.0

## Instalación de Librerías
Para instalar las librerías necesarias, ejecuta el siguiente comando en una terminal:

pip install grpcio grpcio-tools Flask requests
