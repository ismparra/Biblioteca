### **INSTITUTO TECNOLÓGICO SUPERIOR DEL SUR DE GUANAJUATO** 

Ingeniería en Sistemas Computacionales  •  5to Semestre 

**PROYECTO FINAL  —  TALLER DE BASES DE DATOS** 

# **Biblioteca CriCri** 

Desarrollo de un Sistema de Información de Gestión Bibliotecaria 

con Base de Datos Relacional en MySQL 8.0 

|**Integrantes del equipo**|Luis Ángel Villanueva Tenorio<br>Ismael Parra Calderón<br>Christian Escutia Durán|
|---|---|
|**Docente**|Luis Germán Gutiérrez Torres|
|**Asignatura**|Taller de Bases de Datos|
|**Institución y Grupo**|Instituto Tecnológico Superior del Sur de Guanajuato<br>(ITSUR)|
||Ingeniería en Sistemas Computacionales — 5to|
||Semestre|
|**Repositorio GitHub**|https://github.com/ismparra/Biblioteca/|



**Uriangato, Guanajuato  •  Jueves, 26 de noviembre de 2026** 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

## **1. Descripción del problema y justificación** 

#### **1.1 Contexto** 

En las bibliotecas escolares y universitarias de tamaño pequeño a mediano, la administración diaria del acervo bibliográfico —que abarca el registro de obras, el control individual de ejemplares físicos, el padrón de alumnos y el seguimiento de préstamos y devoluciones— suele gestionarse de manera manual mediante libretas de registro, tarjetas de cartulina o, en el mejor de los casos, hojas de cálculo independientes en Microsoft Excel. Este esquema tradicional carece de validación automática, concurrencia segura y trazabilidad histórica, lo que dificulta la operación cotidiana tanto del personal bibliotecario como de los estudiantes que desean consultar la disponibilidad real de un título. 

#### **1.2 Problemática** 

La ausencia de un sistema centralizado respaldado por una base de datos relacional genera las siguientes fallas operativas críticas: 

- **Pérdida de control de existencias físicas:** Al existir múltiples copias físicas de un mismo título sin un identificador único por ejemplar, resulta frecuente desconocer cuántos ejemplares se encuentran disponibles en estantería y cuántos están prestados. 

- **Préstamos sin validación ni seguimiento de atrasos:** Los registros manuales permiten que se autoricen préstamos a alumnos con historial suspendido o que se asignen fechas límite inválidas, además de complicar la detección oportuna de devoluciones vencidas. 

- **Búsquedas ineficientes en el catálogo:** Consultar el catálogo por título o autor y confirmar disponibilidad exige revisiones físicas en estantes o búsquedas manuales lentas. 

- **Errores de captura en mostrador:** La transcripción manual de códigos o títulos en mostrador introduce errores de captura y ralentiza la atención durante picos de demanda escolar. 

- **Falta de seguridad y trazabilidad:** Al no existir cuentas diferenciadas ni bitácoras automáticas, no es posible restringir operaciones administrativas sensibles ni auditar qué usuario registró un préstamo o devolución. 

#### **1.3 Objetivo general** 

Desarrollar el sistema de información web «Biblioteca CriCri», respaldado por una base de datos relacional en MySQL 8.0, que automatice el control del acervo bibliográfico, ejemplares con código de barras, préstamos, devoluciones, reportes de seguimiento y auditoría, garantizando la integridad transaccional y la seguridad por roles. 

#### **1.4 Objetivos específicos** 

- Diseñar e implementar un modelo relacional normalizado en MySQL 8.0 que separe las obras bibliográficas de sus copias físicas (ejemplares), vinculándolas con alumnos, bibliotecarios, préstamos y bitácora de auditoría. 

- Programar lógica de negocio directamente en el gestor de base de datos mediante procedimientos almacenados transaccionales (START TRANSACTION, COMMIT, ROLLBACK y bloqueos FOR UPDATE), funciones almacenadas y triggers de validación y auditoría. 

- Implementar un esquema de seguridad de mínimo privilegio mediante roles y usuarios dedicados en MySQL, junto con el almacenamiento seguro de contraseñas utilizando hash SHA-256 con sal por usuario. 

- Integrar un lector de código de barras USB en modo emulación de teclado (HID) para agilizar el escaneo de ejemplares durante el registro de préstamos y su consulta inmediata. 

- Desarrollar una aplicación web en Python (Flask) con un catálogo interactivo 3D para consulta pública y un panel administrativo completo con reportes avanzados de demanda y morosidad. 

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 2 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

#### **1.5 Justificación** 

La implementación de «Biblioteca CriCri» sustituye los controles informales por una arquitectura confiable donde las reglas de negocio críticas se garantizan desde la propia base de datos. Al concentrar validaciones en transacciones atómicas y triggers, se impide el préstamo simultáneo del mismo ejemplar físico, se bloquea la eliminación accidental de libros con historial de préstamos y se preserva un registro automático e inalterable de cada movimiento en la tabla de auditoría. Adicionalmente, la incorporación del lector de código de barras reduce drásticamente el tiempo de atención en mostrador y elimina errores tipográficos, mientras que los reportes SQL avanzados ofrecen información accionable sobre los títulos más solicitados y los alumnos con préstamos vencidos. 

#### **1.6 Alcance y limitaciones** 

El alcance del sistema cubre el ciclo operativo completo de circulación bibliotecaria: 

- **Qué SÍ hace el sistema:** Catálogo web público con búsqueda por título o autor, navegación visual en carrusel 3D y consulta en tiempo real de ejemplares disponibles. 

- Gestión integral (alta, consulta, edición y baja controlada) de libros, ejemplares con código de barras único, alumnos y bibliotecarios. 

- Registro transaccional de préstamos (con vencimiento automático a 8 días) y devoluciones mediante escaneo de código de barras, cálculo automático de días de retraso, reportes analíticos y bitácora de auditoría. 

- **Qué NO hace el sistema (Limitaciones):** El sistema no es un punto de venta (POS) ni un módulo financiero; no realiza ventas de libros, no calcula ni cobra multas monetarias, no procesa pagos electrónicos ni emite facturas o comprobantes fiscales. Asimismo, no gestiona reservaciones anticipadas en línea ni envíos automáticos de correo electrónico o notificaciones SMS, operando dentro de un entorno de red local institucional. 

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 3 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

## **2. Requerimientos del sistema** 

#### **2.1 Requerimientos funcionales** 

|**ID**<br>**RF-01**|**Requerimiento**<br>El sistema permite iniciar sesión<br>con usuario y contraseña<br>validando credenciales contra la<br>base de datos y verificando<br>estado activo.|**Prioridad**<br>Alta|**Rol**<br>Todos|
|---|---|---|---|
|**RF-02**|El sistema busca e identifica un<br>ejemplar y su obra asociada al<br>leer su código de barras con el<br>lector óptico.|Alta|Administrador, Operador|
|**RF-03**|El sistema muestra el catálogo<br>de libros en una galería<br>interactiva 3D y permite filtrar<br>obras por título o autor.|Alta|Todos|
|**RF-04**|El sistema muestra la ficha<br>detallada de un libro incluyendo<br>la cantidad exacta de ejemplares<br>disponibles calculada<br>dinámicamente.|Alta|Todos|
|**RF-05**|El sistema permite registrar,<br>editar y eliminar libros,<br>impidiendo eliminar obras que<br>cuenten con historial de<br>préstamos.|Alta|Administrador|
|**RF-06**|El sistema permite dar de alta<br>ejemplares físicos asociados a<br>un libro asignándoles un código<br>de barras único y estado inicial<br>disponible.|Alta|Administrador|
|**RF-07**|El sistema permite registrar<br>préstamos de uno o varios<br>ejemplares escaneados a un<br>alumno activo, actualizando<br>atómicamente el estado del<br>ejemplar a prestado.|Alta|Administrador, Operador|
|**RF-08**|El sistema permite registrar la<br>devolución de un ejemplar<br>mediante su código de barras,<br>cerrando el préstamo con fecha/<br>hora actual y liberando el<br>ejemplar.|Alta|Administrador, Operador|
|**RF-09**|El sistema permite consultar el<br>historial de préstamos activos y<br>devueltos mostrando alumno,<br>libro, bibliotecario, fechas y días<br>de atraso.|Alta|Administrador, Operador|



Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 4 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

|**ID**|**Requerimiento**|**Prioridad**|**Rol**|
|---|---|---|---|
|**RF-10**|El sistema permite consultar el<br>resumen de un alumno por<br>matrícula indicando su nombre,<br>préstamos activos y préstamos<br>vencidos.|Media|Administrador, Operador|
|**RF-11**|El sistema permite gestionar<br>alumnos: alta, consulta, edición,<br>suspensión (baja lógica),<br>reactivación y eliminación<br>controlada.|Alta|Administrador|
|**RF-12**|El sistema permite gestionar<br>usuarios bibliotecarios: registro<br>con contraseña hasheada,<br>consulta, edición, baja lógica,<br>reactivación y eliminación<br>(impidiendo auto-eliminarse).|Alta|Administrador|
|**RF-13**|El sistema genera reportes<br>avanzados de libros más<br>solicitados (2 o más préstamos)<br>y alumnos con préstamos<br>vencidos ordenados por días de<br>atraso.|Alta|Administrador, Operador|
|**RF-14**|El sistema registra<br>automáticamente en una tabla<br>de auditoría cada préstamo y<br>cada devolución, permitiendo su<br>consulta desde el panel<br>administrativo.|Alta|Administrador|
|**RF-15**|El sistema permite cerrar sesión<br>limpiando las variables de sesión<br>del navegador y retornando al<br>catálogo público.|Media|Todos|



#### **2.2 Requerimientos no funcionales** 

|**ID**|**Requerimiento**|**Categoría**|
|---|---|---|
|**RNF-01**|Las contraseñas de los usuarios se<br>almacenan como hash SHA-256 con sal por<br>usuario (nunca en texto plano).|Seguridad|
|**RNF-02**|El sistema utiliza MySQL 8.0 como sistema<br>gestor de base de datos relacional con<br>motor InnoDB.|Compatibilidad|
|**RNF-03**|Las operaciones críticas (préstamos,<br>devoluciones y borrado de libros) se<br>ejecutan bajo transacciones ACID con<br>bloqueo pesimista FOR UPDATE y ROLLBACK<br>automático ante fallos.|Integridad / Confiabilidad|



Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 5 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

|**ID**|**Requerimiento**|**Categoría**|
|---|---|---|
|**RNF-04**|El acceso a la base de datos implementa el<br>principio de mínimo privilegio mediante<br>roles nativos de MySQL y un usuario aislado<br>exclusivo para el login.|Seguridad|
|**RNF-05**|La interfaz web ofrece navegación<br>responsiva en tema oscuro de alto contraste,<br>retroalimentación inmediata mediante<br>alertas y compatibilidad con navegadores<br>modernos.|Usabilidad|
|**RNF-06**|La lectura de códigos de barras opera con<br>cualquier escáner USB estándar en modo<br>emulación de teclado (HID) sin requerir<br>controladores propietarios.|Interoperabilidad|
|**RNF-07**|Cada inserción o devolución en la tabla de<br>préstamos queda trazada automáticamente<br>en la tabla de auditoría con fecha, hora,<br>usuario y estado anterior/nuevo.|Auditabilidad|
|**RNF-08**|El código fuente del proyecto (backend,<br>vistas y scripts SQL) se mantiene bajo<br>control de versiones distribuido en Git y<br>GitHub.|Mantenibilidad|



#### **2.3 Roles de usuario** 

|**Rol**|**Descripción**|**Permisos principales**|
|---|---|---|
|**Administrador**|Responsable total de la gestión del sistema,<br>del catálogo bibliográfico, del padrón de<br>usuarios/alumnos y de la supervisión de<br>auditoría.|Acceso completo al panel administrativo;<br>alta, edición y eliminación controlada de<br>libros y ejemplares; alta, edición,<br>suspensión/reactivación y borrado de<br>alumnos y bibliotecarios; registro de<br>préstamos y devoluciones; consulta de<br>reportes avanzados y bitácora de auditoría.|
|**Operador**|Personal de mostrador encargado de la<br>operación diaria de circulación de<br>ejemplares y atención a estudiantes.|Inicio de sesión en el panel operativo;<br>registro de préstamos y devoluciones<br>mediante lector de código de barras;<br>consulta de alumnos, catálogo de libros,<br>préstamos activos/históricos y reportes de<br>seguimiento. No puede modificar el catálogo<br>ni administrar cuentas.|
||Usuario lector o terminal de consulta de solo|Navegación en el catálogo público 3D,<br>búsqueda de libros por título o autor y<br>visualización de ficha técnica con|
|**Consulta**|lectura orientado a verificar existencias del<br>acervo.|disponibilidad real de ejemplares mediante<br>la función ejemplares_disponibles(). Sin<br>acceso al panel administrativo ni<br>modificación de datos.|



Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 6 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

## **3. Diseño de la base de datos** 

#### **3.1 Entidades identificadas** 

|**Entidad**|**Descripción**|
|---|---|
|**bibliotecarios**|Almacena al personal autorizado del sistema con sus<br>credenciales hasheadas, rol asignado (administrador, operador o<br>consulta) y estado de actividad.|
|**alumnos**|Registra a los estudiantes lectores habilitados para solicitar<br>libros, identificados mediante su matrícula institucional única y<br>su estado (activo o suspendido).|
|**libros**|Contiene los metadatos bibliográficos generales de cada obra<br>del acervo: título, autor y categoría temática.|
|**ejemplares**|Representa cada copia física individual perteneciente a un libro,<br>etiquetada con un código de barras único y su estado de<br>circulación (disponible o prestado).|
|**prestamos**|Registra cada evento de préstamo vinculando un alumno, un<br>ejemplar físico y el bibliotecario responsable, junto con las<br>fechas de emisión, límite y devolución.|
|**auditoria**|Bitácora de trazabilidad alimentada automáticamente por<br>triggers para registrar operaciones INSERT y UPDATE relevantes<br>sobre la tabla de préstamos.|



#### **3.2 Diagrama entidad-relación** 

La Figura 1 presenta el diagrama entidad-relación del sistema «Biblioteca CriCri», evidenciando la separación conceptual entre libros y ejemplares físicos (1:N), la relación de circulación hacia préstamos desde alumnos (1:N), ejemplares (1:N) y bibliotecarios (1:N), así como la alimentación automática de la bitácora de auditoría mediante triggers. 

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 7 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 



<!-- Start of picture text -->
DIAGRAMA ENTIDAD-RELACION — BIBLIOTECA CRICRI<br>Bros EJEMPLARE:<br>d<br>ator estos sepa 1 vere '<br>reategoria ‘datos.|1 seat -ootoeenterioreseves t 1<br>H i<br>N va<br>ALUMNOS PRESTAM 7 ‘4 BIBLIOTECARIOS<br>-liso 1 >] id_prestame en eee<br>sestadatuact) | nnee IN<> snomére_comele>-pasnorsro eadash<br><!-- End of picture text -->

_Figura 1. Diagrama Entidad-Relación del sistema Biblioteca CriCri con cardinalidades visibles._ 

#### **3.3 Modelo relacional** 

La Figura 2 muestra el modelo relacional implementado en MySQL 8.0, detallando los nombres exactos de tablas y columnas, tipos de datos, llaves primarias (PK), llaves foráneas (FK), índices únicos (UQ) y valores por defecto. 

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 8 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 



<!-- Start of picture text -->
MODELO RELACIONAL — BASE DE DATOS "biblioteca" (MySQL 8.0)<br><!-- End of picture text -->

_Figura 2. Modelo relacional de la base de datos «biblioteca» en MySQL 8.0._ 

#### **3.4 Diccionario de datos** 

A continuación se detalla la estructura completa de cada una de las seis tablas definidas en el script db.sql: 

##### **Tabla: bibliotecarios** 

|**Campo**|**Tipo**|**Llave**|**Nulo**|**Restricciones**|**Descripción**|
|---|---|---|---|---|---|
|**id_bibliotecario**|INT|PK|NO|AUTO_INCREMENT|Identificador único<br>del bibliotecario.|
|**nombre_completo**|VARCHAR(100)|—|NO|NOT NULL|Nombre completo del<br>personal.|
|**usuario**|VARCHAR(50)|UQ|NO|NOT NULL, UNIQUE|Nombre de usuario<br>único para iniciar<br>sesión.|
|**password_hash**|VARCHAR(255)|—|NO|NOT NULL|Hash SHA-256 con sal<br>de la contraseña.|
|**rol**|ENUM('administrador'<br>,'operador','consulta')|—|NO|NOT NULL|Rol operativo<br>asignado al usuario.|
|**estado**|ENUM('activo','inactiv<br>o')|—|NO|NOT NULL, DEFAULT<br>'activo'|Estatus de vigencia de<br>la cuenta.|



Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 9 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

**Tabla: alumnos** 

|**Campo**|**Tipo**|**Llave**|**Nulo**|**Restricciones**|**Descripción**|
|---|---|---|---|---|---|
|**id_alumno**|INT|PK|NO|AUTO_INCREMENT|Identificador único<br>del alumno.|
|**nombre_completo**|VARCHAR(100)|—|NO|NOT NULL|Nombre completo del<br>estudiante.|
|**matricula**|VARCHAR(30)|UQ|NO|NOT NULL, UNIQUE|Matrícula escolar<br>única del alumno.|
|**estado**|ENUM('activo','suspe<br>ndido')|—|NO|NOT NULL, DEFAULT<br>'activo'|Indica si el alumno<br>está habilitado para<br>préstamos.|



**Tabla: libros** 

|**Campo**|**Tipo**|**Llave**|**Nulo**|**Restricciones**|**Descripción**|
|---|---|---|---|---|---|
|**id_libro**|INT|PK|NO|AUTO_INCREMENT|Identificador único de<br>la obra bibliográfica.|
|**titulo**|VARCHAR(200)|—|NO|NOT NULL|Título oficial del libro.|
|**autor**|VARCHAR(100)|—|NO|NOT NULL|Nombre del autor o<br>autores de la obra.|
|**categoria**|VARCHAR(60)|—|NO|NOT NULL|Categoría o género<br>bibliográfico.|



**Tabla: ejemplares** 

|**Campo**|**Tipo**|**Llave**|**Nulo**|**Restricciones**|**Descripción**|
|---|---|---|---|---|---|
|**id_ejemplar**|INT|PK|NO|AUTO_INCREMENT|Identificador único de<br>la copia física.|
|**codigo_barras**|VARCHAR(50)|UQ|NO|NOT NULL, UNIQUE|Código de barras<br>único impreso en el<br>ejemplar.|
|**id_libro**|INT|FK|NO|NOT NULL,<br>REFERENCES<br>libros(id_libro)|Obra bibliográfica a la<br>que pertenece la<br>copia.|
|**estado**|ENUM('disponible','pr<br>estado')|—|NO|NOT NULL, DEFAULT<br>'disponible'|Disponibilidad física<br>actual del ejemplar.|



**Tabla: prestamos** 

|**Campo**|**Tipo**|**Llave**|**Nulo**|**Restricciones**|**Descripción**|
|---|---|---|---|---|---|
|**id_prestamo**|INT|PK|NO|AUTO_INCREMENT|Identificador único<br>del préstamo.|
|**id_alumno**|INT|FK|NO|NOT NULL,<br>REFERENCES<br>alumnos(id_alumno)|Alumno que solicita el<br>ejemplar.|



Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 10 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

|**Campo**|**Tipo**|**Llave**|**Nulo**|**Restricciones**|**Descripción**|
|---|---|---|---|---|---|
|**id_ejemplar**|INT|FK|NO|NOT NULL,<br>REFERENCES<br>ejemplares(id_ejempl<br>ar)|Copia física específica<br>prestada.|
|**id_bibliotecario**|INT|FK|NO|NOT NULL,<br>REFERENCES<br>bibliotecarios(id_bibli<br>otecario)|Personal que autorizó<br>y registró el préstamo.|
|**fecha_prestamo**|DATETIME|—|NO|NOT NULL, DEFAULT<br>CURRENT_TIMESTAM<br>P|Fecha y hora exacta<br>en que se emitió el<br>préstamo.|
|**fecha_limite**|DATE|—|NO|NOT NULL|Fecha compromiso<br>para devolver el<br>ejemplar.|
|**fecha_devolucion**|DATETIME|—|SÍ|NULL por defecto|Fecha y hora real de<br>devolución (NULL si<br>sigue activo).|



**Tabla: auditoria** 

|**Campo**|**Tipo**|**Llave**|**Nulo**|**Restricciones**|**Descripción**|
|---|---|---|---|---|---|
|**id_auditoria**|INT|PK|NO|AUTO_INCREMENT|Identificador<br>consecutivo del<br>evento auditado.|
|**tabla**|VARCHAR(64)|—|NO|NOT NULL|Nombre de la tabla<br>afectada por la<br>operación.|
|**operacion**|VARCHAR(10)|—|NO|NOT NULL|Tipo de sentencia<br>ejecutada (INSERT,<br>UPDATE).|
|**fecha_hora**|DATETIME|—|NO|NOT NULL, DEFAULT<br>CURRENT_TIMESTAM<br>P|Marca temporal<br>exacta del<br>movimiento.|
|**usuario**|VARCHAR(100)|—|NO|NOT NULL|Usuario de MySQL<br>que originó el cambio<br>(user()).|
|**datos_anteriores**|TEXT|—|SÍ|NULL permitido|Resumen del estado<br>previo (NULL en<br>inserciones).|
|**datos_nuevos**|TEXT|—|SÍ|NULL permitido|Resumen de los<br>valores nuevos<br>registrados.|



#### **3.5 Restricciones de integridad** 

La consistencia de los datos se protege mediante múltiples capas de restricciones declarativas y procedimentales en MySQL 8.0: 

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 11 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

- **Integridad de entidad (PRIMARY KEY):** Todas las tablas cuentan con llaves primarias sustitutas de tipo INT con AUTO_INCREMENT (id_bibliotecario, id_alumno, id_libro, id_ejemplar, id_prestamo, id_auditoria), garantizando unicidad absoluta de filas. 

- **Integridad referencial (FOREIGN KEY):** Se definieron cuatro llaves foráneas explícitas: ejemplares.id_libro -> libros(id_libro), prestamos.id_alumno -> alumnos(id_alumno), prestamos.id_ejemplar -> ejemplares(id_ejemplar) y prestamos.id_bibliotecario -> bibliotecarios(id_bibliotecario), impidiendo registros huérfanos. 

- **Unicidad (UNIQUE):** Se impusieron restricciones UNIQUE en ejemplares.codigo_barras (evitando etiquetas duplicadas en el inventario), alumnos.matricula (evitando duplicidad en el padrón estudiantil) y bibliotecarios.usuario (asegurando inicios de sesión inequívocos). 

- **Obligatoriedad (NOT NULL):** Todos los campos obligatorios están declarados como NOT NULL, dejando únicamente como opcionales prestamos.fecha_devolucion (NULL mientras el libro no ha sido devuelto) y auditoria.datos_anteriores / datos_nuevos. 

- **Valores por defecto (DEFAULT):** Se asignaron valores predeterminados coherentes con la operación: estado = 'activo' en bibliotecarios y alumnos, estado = 'disponible' en ejemplares y DEFAULT CURRENT_TIMESTAMP en prestamos.fecha_prestamo y auditoria.fecha_hora. 

- **Integridad de dominio y validaciones de negocio (ENUM + Triggers):** En lugar de cláusulas CHECK aisladas, los dominios cerrados se controlan estrictamente con tipos ENUM ('administrador'/'operador'/'consulta', 'activo'/'inactivo', 'activo'/'suspendido', 'disponible'/'prestado') y las reglas de negocio cruzadas (código de barras no vacío tras TRIM, ejemplar nuevo obligatorio en estado 'disponible', alumno activo y fecha límite mayor o igual a la fecha del préstamo) se refuerzan mediante los triggers BEFORE INSERT validar_prestamo y validar_ejemplar con SIGNAL SQLSTATE '45000'. 

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 12 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

## **4. Objetos de la base de datos** 

#### **4.1 Transacciones** 

Las operaciones críticas del sistema están encapsuladas en tres procedimientos almacenados que implementan control transaccional explícito con START TRANSACTION, COMMIT y un manejador global DECLARE EXIT HANDLER FOR SQLEXCEPTION que ejecuta ROLLBACK y propaga la excepción original a la aplicación mediante RESIGNAL. Adicionalmente, las lecturas previas emplean bloqueo pesimista (SELECT ... FOR UPDATE) para prevenir condiciones de carrera cuando dos operadores intentan prestar o modificar el mismo registro simultáneamente. 

|**Transacción**|**Modificaciones que agrupa**|**Condiciones de cancelación (ROLLBACK)**|
|---|---|---|
|**registrar_prestamo**|1) Bloquea fila del alumno y del ejemplar<br>(FOR UPDATE).<br>2) Inserta el registro en prestamos.<br>3) Actualiza ejemplares.estado = 'prestado'.|Se cancela (ROLLBACK) si el alumno no<br>existe o está suspendido, si el código de<br>barras no existe, si el ejemplar no está<br>disponible, si el bibliotecario no tiene rol<br>administrador/operador activo, si la fecha<br>límite es nula o anterior a CURDATE(), o ante<br>cualquier error SQL.|
|**registrar_devolucion**|1) Bloquea el ejemplar por código de barras<br>y su préstamo abierto (fecha_devolucion IS<br>NULL) con FOR UPDATE.<br>2) Actualiza prestamos.fecha_devolucion =<br>NOW().<br>3) Restaura ejemplares.estado = 'disponible'.|Se cancela (ROLLBACK) si el código de barras<br>no corresponde a ningún ejemplar<br>registrado, si el ejemplar no tiene un<br>préstamo activo pendiente de devolución o<br>si ocurre un fallo durante cualquiera de las<br>dos actualizaciones.|
|**eliminar_libro**|1) Bloquea la fila del libro (FOR UPDATE).<br>2) Verifica ausencia de préstamos históricos<br>en sus ejemplares.<br>3) Elimina los registros asociados en<br>ejemplares.<br>4) Elimina el registro en libros.|Se cancela (ROLLBACK) si el libro no existe o<br>si al menos uno de sus ejemplares tiene<br>préstamos registrados en el historial,<br>preservando así la integridad histórica de la<br>biblioteca.|



#### **4.2 Procedimientos almacenados** 

|**Nombre**|**Parámetros (IN / OUT)**|**Qué hace**|**Pantalla de la app donde se usa**|
|---|---|---|---|
|**registrar_prestamo**|IN p_matricula VARCHAR(30)<br>IN p_codigo VARCHAR(50)<br>IN p_bibliotecario INT<br>IN p_fecha_limite DATE|Valida alumno activo, ejemplar<br>disponible, rol autorizado y fecha<br>límite; inserta el préstamo y<br>cambia el estado del ejemplar a<br>'prestado' dentro de una<br>transacción atómica.|Registrar Préstamo (/admin/<br>panel/registrar -> POST /<br>prestamo/registrar)|
|**registrar_devolucion**|IN p_codigo VARCHAR(50)|Localiza el ejemplar y su préstamo<br>abierto, registra NOW() como<br>fecha de devolución y marca el<br>ejemplar nuevamente como<br>'disponible' de forma<br>transaccional.|Panel de Préstamos (/admin/<br>panel/prestamos -> POST /admin/<br>panel/prestamos/devolver)|
|**eliminar_libro**|IN p_libro INT|Verifica que el libro exista y no<br>tenga préstamos históricos;<br>elimina sus ejemplares y la obra<br>en una sola transacción.|Información del Libro (/libro/info<br>-> POST /libros/eliminar)|



Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 13 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

|**Nombre**|**Parámetros (IN / OUT)**|**Qué hace**|**Pantalla de la app donde se usa**|
|---|---|---|---|
|**consultar_alumno**|IN p_matricula VARCHAR(30)<br>OUT p_nombre VARCHAR(100)<br>OUT p_activos INT<br>OUT p_vencidos INT|Devuelve mediante parámetros<br>OUT el nombre completo del<br>alumno, total de préstamos<br>activos y total de préstamos<br>vencidos (usando dias_retraso); si<br>no existe retorna 'Alumno no<br>encontrado' y ceros.|Consultas de verificación en BD /<br>módulo de alumnos y pruebas de<br>validación|
|**iniciar_sesion**|IN p_usuario VARCHAR(50)<br>IN p_password VARCHAR(100)|Calcula SHA2(CONCAT(usuario,<br>p_password), 256) y retorna<br>id_bibliotecario,<br>nombre_completo, usuario, rol y<br>estado si las credenciales<br>coinciden.|Modal de Acceso Administrativo<br>(index.html -> POST /admin/login)|
|**registrar_usuario**|IN p_nombre VARCHAR(100)<br>IN p_usuario VARCHAR(50)<br>IN p_password VARCHAR(100)<br>IN p_rol VARCHAR(20)|Inserta un nuevo bibliotecario con<br>estado 'activo' almacenando su<br>contraseña directamente como<br>hash SHA-256 con sal de usuario.|Panel Administrativo — Pestaña<br>Crear Usuario (POST /admin/<br>panel/crearUsuario)|



**Nota técnica de extensión en backend:** Adicionalmente a los seis procedimientos centrales documentados en procedimientos.sql, las rutas administrativas de mantenimiento en BD/users.py y BD/alumnos.py contemplan las invocaciones a actualizar_usuario, eliminar_usuario y eliminar_alumno para soportar la edición y borrado seguro desde las vistas de gestión de usuarios (/admin/panel/usuarios) y alumnos (/admin/panel/alumnos). 

#### **4.3 Funciones almacenadas** 

|**Nombre**|**Parámetros**|**Devuelve**|**Dónde se usa**|
|---|---|---|---|
|**ejemplares_disponibles**|p_libro INT|INT — Cantidad de copias físicas<br>del libro cuyo estado es<br>'disponible'.|Ficha de detalle del libro (BD/<br>libros.py -> buscar_libro en /<br>libro/info) y consultas del<br>catálogo.|
|**dias_retraso**|p_prestamo INT|INT — Días transcurridos desde<br>fecha_limite hasta<br>fecha_devolucion (o CURDATE()<br>si aún no se devuelve). Retorna<br>0 si está a tiempo y -1 si el<br>préstamo no existe.|Panel de préstamos (BD/<br>prestamos.py -><br>obtenerPrestamos), Reporte 2<br>de morosidad (/admin/panel/<br>reportes) y procedimiento<br>consultar_alumno.|



#### **4.4 Triggers de validación** 

|**Nombre**|**Tabla / Evento**|**Qué valida o impide**|
|---|---|---|
|**validar_prestamo**|prestamos /<br>BEFORE INSERT|Impide insertar un préstamo (SIGNAL<br>SQLSTATE '45000') si: (1) el alumno no existe<br>o está suspendido, (2) el ejemplar no existe<br>o no está en estado 'disponible', o (3)<br>fecha_limite es anterior a<br>DATE(fecha_prestamo). Actúa como barrera<br>defensiva incluso ante inserciones directas<br>fuera de los procedimientos.|



Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 14 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

|**Nombre**|**Tabla / Evento**|**Qué valida o impide**|
|---|---|---|
|**validar_ejemplar**|ejemplares /<br>BEFORE INSERT|Impide registrar un ejemplar si<br>codigo_barras es NULL o está vacío/solo<br>espacios (TRIM), o si se intenta insertar un<br>ejemplar nuevo con estado distinto a<br>'disponible'.|



#### **4.5 Triggers de auditoría** 

|**Nombre**|**Tabla / Evento**|**Qué registra**|
|---|---|---|
|**auditar_prestamo**|prestamos /<br>AFTER INSERT|Inserta un registro en auditoria con tabla =<br>'prestamos', operacion = 'INSERT',<br>fecha_hora = NOW(), usuario = USER(),<br>datos_anteriores = NULL y datos_nuevos<br>con el detalle concatenado de id_prestamo,<br>id_alumno, id_ejemplar, id_bibliotecario y<br>fecha_limite.|
|**auditar_devolucion**|prestamos /<br>AFTER UPDATE|Evalúa si cambió fecha_devolucion mediante<br>el operador null-safe NOT<br>(NEW.fecha_devolucion <=><br>OLD.fecha_devolucion). En caso afirmativo,<br>registra en auditoria la operación 'UPDATE'<br>con el estado previo ('sin devolver' o fecha<br>previa) y el nuevo valor de fecha_devolucion<br>junto con USER().|



Se utilizó la función USER() en lugar de CURRENT_USER() dentro de los triggers de auditoría debido a que CURRENT_USER() reporta el definidor del trigger, mientras que USER() captura con precisión la cuenta de MySQL que ejecutó la transacción en tiempo real. 

##### **Estructura de la tabla de auditoría (auditoria)** 

|**Campo**|**Tipo**|**Descripción**|
|---|---|---|
|**id_auditoria**|INT (PK, AI)|Identificador autoincremental único del<br>movimiento auditado.|
|**tabla**|VARCHAR(64)|Nombre de la tabla afectada (por ejemplo,<br>'prestamos').|
|**operacion**|VARCHAR(10)|Tipo de operación registrada: INSERT o<br>UPDATE.|
|**fecha_hora**|DATETIME|Fecha y hora exacta en que se generó el<br>registro (DEFAULT CURRENT_TIMESTAMP).|
|**usuario**|VARCHAR(100)|Usuario de base de datos responsable de la<br>operación (capturado vía USER()).|
|**datos_anteriores**|TEXT|Estado previo del registro antes de la<br>modificación (NULL en operaciones INSERT).|
|**datos_nuevos**|TEXT|Estado resultante después de ejecutarse el<br>préstamo o la devolución.|



Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 15 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 16 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

## **5. Seguridad** 

#### **5.1 Tabla de usuarios y almacenamiento de contraseñas** 

Las cuentas del personal se almacenan en la tabla bibliotecarios (campos: id_bibliotecario, nombre_completo, usuario, password_hash, rol y estado). Ninguna contraseña se guarda en texto plano: tanto en el procedimiento registrar_usuario como en la carga inicial de pruebas.sql, se aplica el algoritmo criptográfico SHA-256 (función nativa SHA2(..., 256) de MySQL 8.0) concatenando el nombre de usuario como sal única por registro: 

**Fórmula de hash y verificación en MySQL (procedimientos.sql)** 

```
-- Al registrar usuario:
INSERT INTO bibliotecarios
VALUES (DEFAULT, p_nombre, p_usuario, SHA2(CONCAT(p_usuario, p_password), 256), p_rol, 'activo');
-- Al iniciar sesión (procedimiento iniciar_sesion):
SELECT id_bibliotecario, nombre_completo, usuario, rol, estado
FROM bibliotecarios
WHERE usuario = p_usuario
  AND password_hash = SHA2(CONCAT(usuario, p_password), 256);
```

El uso del nombre de usuario como sal garantiza que dos cuentas con la misma contraseña produzcan resúmenes criptográficos completamente distintos y mitiga ataques basados en diccionarios precomputados (tablas arcoíris). En la capa de aplicación (app.py), al recibir la respuesta de iniciar_sesion, el servidor Flask valida además que el rol pertenezca al conjunto administrativo/operativo permitido y que el estado sea distinto de 'inactivo'; si las credenciales son válidas, almacena id, nombre, user, rol y estado en la sesión firmada del servidor mediante app.secret_key. 

#### **5.2 Roles y permisos** 

En MySQL 8.0 se crearon tres roles de negocio (rol_administrador, rol_operador y rol_consulta) activados automáticamente mediante SET DEFAULT ROLE para sus respectivos usuarios locales, más una cuenta dedicada pre-autenticación (bib_login) siguiendo el principio de mínimo privilegio: 

|**Rol**|**Usuario de MySQL**|**Privilegios otorgados**|**Operaciones permitidas en la app**|
|---|---|---|---|
|**Administrador**<br>**(rol_administrador)**|bib_admin@localhost|SELECT, INSERT, UPDATE en<br>bibliotecarios, alumnos, libros y<br>ejemplares; SELECT en prestamos<br>y auditoria; EXECUTE en todos los<br>procedimientos<br>(registrar_prestamo,<br>registrar_devolucion,<br>eliminar_libro, registrar_usuario,<br>consultar_alumno, iniciar_sesion)<br>y funciones.|Control total en el panel: gestionar<br>libros y ejemplares, dar de alta/<br>baja/editar alumnos y<br>bibliotecarios, registrar préstamos<br>y devoluciones, consultar reportes<br>avanzados y revisar la bitácora de<br>auditoría.|
|**Operador**<br>**(rol_operador)**|bib_operador@localhost|SELECT en alumnos, libros,<br>ejemplares y prestamos; EXECUTE<br>únicamente en<br>registrar_prestamo,<br>registrar_devolucion,<br>consultar_alumno,<br>ejemplares_disponibles y<br>dias_retraso.|Operación diaria de mostrador:<br>escanear ejemplares para registrar<br>préstamos, registrar devoluciones,<br>consultar préstamos activos/<br>vencidos, consultar alumnos y<br>visualizar reportes. Sin permiso<br>directo INSERT/UPDATE/DELETE en<br>tablas.|



Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 17 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

|**Rol**|**Usuario de MySQL**|**Privilegios otorgados**|**Operaciones permitidas en la app**|
|---|---|---|---|
|**Consulta**<br>**(rol_consulta)**|bib_consulta@localhost|SELECT en libros y ejemplares;<br>EXECUTE únicamente en<br>ejemplares_disponibles.|Acceso de solo lectura al catálogo<br>público 3D, búsqueda por título/<br>autor y consulta de disponibilidad<br>real de copias físicas.|
|||EXECUTE exclusivamente sobre el|Validación segura de credenciales<br>antes de autenticar la sesión,|
|**Pre-autenticación**<br>**(Sin rol asignado)**|bib_login@localhost|procedimiento<br>biblioteca.iniciar_sesion. Sin<br>acceso directo a ninguna tabla.|impidiendo que un atacante no<br>autenticado lea la tabla<br>bibliotecarios u otros datos del<br>esquema.|



**Aclaración sobre la conexión en entorno de desarrollo:** El módulo BD/connection.py expone la función parametrizable get_connection(usuario, password) con 'bib_admin' como perfil predeterminado para las pruebas integradas en localhost, permitiendo escalar fácilmente a conexiones dinámicas por rol de sesión aprovechando los cuatro usuarios ya aprovisionados en usuarios.sql. 

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 18 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

## **6. Lector de código de barras** 

#### **6.1 Equipo utilizado** 

|**Especificación**|**Detalle del dispositivo**|
|---|---|
|**Modelo del lector**|Honeywell Voyager 1250g (Lector láser lineal 1D de mano con<br>soporte)|
|**Tipo de conexión**|USB cableado con emulación de teclado estándar HID (Plug &<br>Play, sin drivers adicionales)|
|**Simbología soportada**|EAN-13 (utilizada en las etiquetas del acervo, p. ej.<br>7501000000011), UPC-A, Code 128 y Code 39|
|**Configuración de sufijo**|Sufijo automático Carriage Return (tecla Enter) al finalizar cada<br>lectura exitosa|



#### **6.2 Operación realizada con el lector** 

Al operar como dispositivo HID (Human Interface Device), el lector inyecta los dígitos del código de barras directamente en el campo de texto activo y envía la pulsación de la tecla Enter. El sistema aprovecha este comportamiento en tres flujos operativos clave: 

- **1. Búsqueda e incorporación de ejemplares al préstamo:** En la pantalla /admin/panel/registrar (controlada por static/js/registrarForm.js), el operador captura la matrícula del alumno y enfoca el campo de escaneo (#codigo). Al leer la etiqueta de un ejemplar, el evento keydown detecta la tecla Enter, detiene el envío convencional del formulario (e.preventDefault()) y dispara una petición asíncrona fetch POST a /api/libro/codigo. 

- **2. Validación en tiempo real y encolado múltiple:** El endpoint en app.py invoca buscar_libro_cod(codigo) (SELECT * FROM libros NATURAL JOIN ejemplares WHERE codigo_barras = %s) y devuelve en formato JSON el título, autor y código del ejemplar. Si existe, se agrega dinámicamente a la lista de préstamo en pantalla y se limpia el input para escanear inmediatamente el siguiente libro; si no existe, despliega una alerta de libro no encontrado. 

- **3. Confirmación transaccional, alta de ejemplares y devoluciones:** Al presionar «Registrar préstamo», el frontend envía la matrícula del alumno y el arreglo de códigos de barras escaneados a POST /prestamo/registrar. El backend calcula automáticamente la fecha límite a 8 días (date.today() + timedelta(days=8)) y ejecuta CALL registrar_prestamo(...) por cada ejemplar, actualizando su estado a 'prestado' y redirigiendo al listado de préstamos. De forma análoga, el lector agiliza la captura de códigos al dar de alta nuevos ejemplares (/libros/ejemplar) y al registrar devoluciones (/admin/panel/prestamos/devolver). 

## **7. Reportes y consultas avanzadas** 

El sistema implementa consultas SQL avanzadas tanto en reportes.sql como integradas directamente en el módulo de reportes y en el panel de préstamos de la aplicación web, demostrando cinco características avanzadas de SQL: JOIN de 3, 4 y 5 tablas, funciones de agregación (COUNT, MAX, GROUP_CONCAT), agrupamiento con GROUP BY, filtrado de grupos con HAVING e invocación de funciones almacenadas personalizadas dentro de consultas analíticas. 

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 19 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

|**Reporte**|**Propósito**|**Características SQL usadas**|**Pantalla**|
|---|---|---|---|
|**Reporte 1: Libros más solicitados**|Identificar las obras con mayor<br>demanda histórica (prestadas 2 o<br>más veces) para orientar la<br>adquisición de nuevos ejemplares.|JOIN de 3 tablas (libros,<br>ejemplares, prestamos), función<br>de agregación COUNT(*), GROUP<br>BY, HAVING COUNT(*) >= 2,<br>ORDER BY DESC.|Reportes (/admin/panel/reportes)|
|**Reporte 2: Alumnos con**<br>**préstamos vencidos**|Detectar estudiantes con entregas<br>vencidas sin devolver,<br>cuantificando total de préstamos<br>atrasados, máximo de días de<br>retraso y lista consolidada de<br>títulos adeudados.|JOIN de 4 tablas (alumnos,<br>prestamos, ejemplares, libros),<br>agregación COUNT(*), MAX() y<br>GROUP_CONCAT(... SEPARATOR ',<br>'), función almacenada<br>dias_retraso(), filtrado WHERE,<br>GROUP BY y ORDER BY DESC.|Reportes (/admin/panel/reportes)|
|**Consulta 3: Panel consolidado de**<br>**préstamos**|Mostrar el historial integral de<br>préstamos activos y cerrados con<br>información legible del alumno,<br>obra, bibliotecario, código de<br>barras y cálculo en vivo de días de<br>atraso.|JOIN de 5 tablas (prestamos,<br>ejemplares, libros, alumnos,<br>bibliotecarios) e invocación de la<br>función almacenada<br>dias_retraso(p.id_prestamo).|Panel de Préstamos (/admin/<br>panel/prestamos)|



**Consultas SQL implementadas en reportes.sql y app.py (/admin/panel/reportes)** 

|`-- Reporte 1: Libros más solicitados (2 o más préstamos)`<br>`SELECT l.titulo, l.autor, COUNT(*) AS veces_prestado`<br>`FROM libros l`|
|---|
|`JOIN ejemplares e ON e.id_libro = l.id_libro`<br>`JOIN prestamos p ON p.id_ejemplar = e.id_ejemplar`<br>`GROUP BY l.id_libro, l.titulo, l.autor`<br>`HAVING COUNT(*) >= 2`<br>`ORDER BY veces_prestado DESC;`|
|`-- Reporte 2: Alumnos con préstamos vencidos y días de atraso`<br>`SELECT a.matricula,`<br>`a.nombre_completo,`<br>`COUNT(*) AS prestamos_vencidos,`<br>`MAX(dias_retraso(p.id_prestamo)) AS dias_atraso,`<br>`GROUP_CONCAT(l.titulo SEPARATOR ', ') AS libros`<br>`FROM alumnos a`|
|`JOIN prestamos p ON p.id_alumno = a.id_alumno`<br>`JOIN ejemplares e ON e.id_ejemplar = p.id_ejemplar`<br>`JOIN libros l ON l.id_libro = e.id_libro`<br>`WHERE p.fecha_devolucion IS NULL`<br>`AND dias_retraso(p.id_prestamo) > 0`|
|`GROUP BY a.id_alumno, a.matricula, a.nombre_completo`<br>`ORDER BY dias_atraso DESC;`|



Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 20 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

## **8. Aplicación** 

#### **8.1 Tecnologías utilizadas** 

|**Componente**|**Tecnología**|
|---|---|
|**Lenguaje / framework**|Python 3 con microframework web Flask (rutas REST/HTML,<br>sesiones y motor de plantillas Jinja2)|
|**Conexión a MySQL**|Driver oficial mysql-connector-python (capa modular de acceso<br>a datos en paquete BD/)|
|**Gestor de base de datos**|MySQL 8.0 (motor InnoDB con soporte completo para roles,<br>triggers, procedimientos y funciones)|
|**Interfaz (Frontend)**|HTML5, CSS3 modular (tema oscuro, animaciones y diseño<br>responsivo), JavaScript Vanilla (ES6+ Fetch API, carrusel 3D<br>coverflow) y portadas SVG dinámicas (/cover/<id>.svg)|
|**Control de versiones**|Git / GitHub (repositorio colaborativo público en ismparra/<br>Biblioteca)|



#### **8.2 Módulos y pantallas** 

|**Módulo / pantalla**|**Función**|**Roles con acceso**|
|---|---|---|
|**Catálogo Principal 3D (/)**|Exhibe las obras en un carrusel 3D interactivo<br>navegable con teclado, rueda del ratón o<br>arrastre, con barra de búsqueda por título/<br>autor y portadas SVG generadas<br>dinámicamente.|Todos (Público, Consulta, Operador,<br>Administrador)|
|**Ficha de Libro (/libro/info)**|Muestra título, autor, categoría y cantidad de<br>ejemplares disponibles en tiempo real; habilita<br>botones de editar, eliminar o agregar ejemplar<br>para administradores.|Todos (acciones de edición solo Administrador)|
|**Modal de Inicio de Sesión (/admin/login)**|Formulario emergente superpuesto al catálogo<br>que autentica al personal mediante<br>iniciar_sesion y abre sesión en Flask.|Operador, Administrador|
|**Panel Administrativo (/admin/panel)**|Centro de mando con barra lateral de<br>navegación, accesos rápidos a módulos y<br>formularios con pestañas para alta rápida de<br>usuarios y alumnos.|Administrador, Operador|
|**Registrar Préstamo (/admin/panel/registrar)**|Interfaz optimizada para escaneo consecutivo<br>con lector de código de barras, acumulación de<br>múltiples ejemplares por alumno y registro<br>transaccional con fecha límite automática (+8<br>días).|Administrador, Operador|
|**Gestión de Préstamos (/admin/panel/**<br>**prestamos)**|Listado tabular de préstamos activos e<br>históricos con indicador de días de atraso y<br>acción directa para registrar devolución<br>mediante registrar_devolucion.|Administrador, Operador|
|**Gestión de Libros y Ejemplares (/addBook, /**<br>**libros/editar, /libros/ejemplar)**|Formularios para dar de alta nuevas obras,<br>actualizar sus datos bibliográficos, eliminar<br>obras sin préstamos y registrar copias físicas<br>con código de barras único.|Administrador|



Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 21 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

|**Módulo / pantalla**|**Función**|**Roles con acceso**|
|---|---|---|
|**Gestión de Alumnos (/admin/panel/alumnos)**|Consulta del padrón estudiantil, alta, edición de<br>datos, suspensión/reactivación (alta/baja<br>lógica) y eliminación controlada.|Administrador (consulta habilitada a Operador)|
|**Gestión de Usuarios (/admin/panel/usuarios)**|Administración de bibliotecarios: listado, alta<br>con contraseña hasheada, edición de perfil/rol,<br>baja/alta lógica y eliminación protegida.|Administrador (consulta habilitada a Operador)|
||Presenta los cuadros analíticos de libros más||
|**Reportes Avanzados (/admin/panel/reportes)**|solicitados y alumnos con préstamos vencidos<br>con sus títulos y días de atraso.|Administrador, Operador|
|**Bitácora de Auditoría (/admin/panel/**<br>**auditorias)**|Muestra el historial cronológico de registros<br>capturados por los triggers sobre la tabla<br>auditoria (operación, fecha, usuario, datos<br>anteriores y nuevos).|Administrador|



#### **8.3 Manejo de errores y confirmaciones** 

El sistema combina validaciones en base de datos con mecanismos claros de retroalimentación hacia el usuario: 

- **Propagación de errores de base de datos:** Las excepciones lanzadas desde los procedimientos y triggers de MySQL mediante SIGNAL SQLSTATE '45000' (por ejemplo, alumno suspendido, ejemplar ya prestado o código inexistente) son capturadas en Python con mysql.connector.Error o Exception. En el flujo AJAX de préstamos (/prestamo/ registrar), el servidor devuelve código HTTP 500 con un objeto JSON {ok: false, error: mensaje}, el cual registrarForm.js despliega inmediatamente al operador. 

- **Alertas visuales en interfaz:** En las vistas tradicionales servidas por Flask, los fallos de inicio de sesión, errores SQL en edición/eliminación de usuarios o alumnos y operaciones con cero filas afectadas se comunican mediante el banner animado .alert-message en la parte superior de la pantalla. 

- **Validaciones preventivas y de sesión:** Se bloquean accesos sin sesión activa o sin rol autorizado redirigiendo a la página principal (/), y se impide explícitamente que un administrador elimine su propia cuenta activa ('No puedes eliminar tu propio usuario'). 

- **Consultas parametrizadas:** Todas las consultas y llamadas a procedimientos utilizan marcadores parametrizados (%s) mediante mysql-connector-python, evitando inyección SQL y asegurando cierres ordenados de cursores y conexiones tras confirmar (commit) cada transacción. 

#### **8.4 Repositorio** 

**Enlace al repositorio oficial en GitHub:** https://github.com/ismparra/Biblioteca/  — Contiene el código fuente completo de la aplicación Flask (app.py, paquete BD/, Extra/, plantillas HTML, hojas CSS, scripts JS) y la suite integral de scripts SQL de MySQL 8.0. 

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 22 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

## **9. Pruebas** 

Se ejecutó una batería integral de 16 casos de prueba basados en pruebas.sql y en los flujos reales de la aplicación web, abarcando pruebas positivas, pruebas negativas (manejo de excepciones y rollbacks), triggers de validación/ auditoría y reportes avanzados: 

|**No.**<br>**CP-01**|**Caso de prueba**<br>Invocar función<br>ejemplares_disponibles(id_li<br>bro) sobre el catálogo<br>cargado.|**Resultado esperado**<br>Retorna conteo exacto de<br>ejemplares con estado<br>'disponible' por libro.|**Resultado obtenido**<br>Se devolvieron las<br>existencias disponibles<br>exactas para los 5 libros de<br>prueba.|**Estado**<br>**APROBADO**|
|---|---|---|---|---|
|**CP-02**|Invocar<br>dias_retraso(id_prestamo)<br>con préstamo a tiempo,<br>préstamo vencido y<br>préstamo inexistente<br>(100000000).|Retorna 0 si está a tiempo,<br>entero positivo para<br>vencidos y -1 si no existe.|Retornó 0, los días exactos<br>de atraso y -1 para el ID<br>inexistente.|**APROBADO**|
|**CP-03**|Inicio de sesión válido<br>mediante CALL<br>iniciar_sesion('admin',<br>'admin123').|Retorna registro del<br>bibliotecario con rol<br>'administrador' y estado<br>'activo'.|Autenticación exitosa y<br>creación de sesión en Flask<br>con acceso al panel.|**APROBADO**|
|**CP-04**|Inicio de sesión con<br>contraseña incorrecta<br>('admin', '1234') o usuario<br>inexistente ('IPC').|Conjunto vacío sin acceso al<br>panel; mensaje de error en<br>pantalla.|La consulta devolvió 0 filas y<br>la app mostró 'Usuario o<br>contraseña incorrecto(s)'.|**APROBADO**|
|**CP-05**|Registrar nuevo usuario<br>mediante CALL<br>registrar_usuario('Rosa<br>Diaz','rosa','rosa123','operad<br>or') e iniciar sesión.|Inserta usuario con hash<br>SHA-256 con sal y permite<br>login posterior.|Usuario creado<br>correctamente y autenticado<br>con éxito en iniciar_sesion.|**APROBADO**|
|**CP-06**|Intentar registrar un usuario<br>duplicado ('admin').|Error de restricción UNIQUE<br>impidiendo duplicar el<br>nombre de usuario.|MySQL rechazó el registro<br>por clave duplicada en<br>bibliotecarios.usuario.|**APROBADO**|
|**CP-07**|Registrar préstamo válido<br>CALL<br>registrar_prestamo('A002',<br>'7501000000011', 2, +7 días)<br>vía escáner/app.|Inserta fila en prestamos,<br>actualiza ejemplar a<br>'prestado' y registra INSERT<br>en auditoria.|Transacción confirmada<br>(COMMIT), ejemplar<br>marcado 'prestado' y evento<br>auditado.|**APROBADO**|
|**CP-08**|Intentar prestar a un alumno<br>suspendido ('A004').|Lanza SQLSTATE '45000' y<br>ejecuta ROLLBACK sin<br>modificar tablas.|Error: 'El alumno no existe o<br>esta suspendido'; tablas<br>intactas.|**APROBADO**|
|**CP-09**|Intentar prestar código de<br>barras inexistente<br>('0000000000000') o<br>ejemplar ya prestado<br>('7501000000042').|Cancela transacción con<br>mensaje descriptivo para<br>cada caso.|Se devolvieron exactamente<br>los mensajes de error<br>configurados y ROLLBACK.|**APROBADO**|
|**CP-10**|Intentar registrar préstamo<br>con usuario rol 'consulta' (ID<br>3) o con fecha límite pasada<br>('2000-01-01').|Impide la operación por falta<br>de permisos o fecha límite<br>inválida.|Se bloquearon ambos<br>intentos devolviendo los<br>mensajes de validación.|**APROBADO**|
|**CP-11**|Registrar devolución válida<br>CALL<br>registrar_devolucion('75010<br>00000011').|Asigna fecha_devolucion =<br>NOW(), cambia ejemplar a<br>'disponible' y audita UPDATE.|Préstamo cerrado, ejemplar<br>liberado y registro UPDATE<br>guardado en auditoria.|**APROBADO**|



Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 23 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

|**No.**|**Caso de prueba**|**Resultado esperado**|**Resultado obtenido**|**Estado**|
|---|---|---|---|---|
|**CP-12**|Intentar devolver ejemplar<br>sin préstamo activo<br>('7501000000028') o código<br>inexistente.|Lanza SQLSTATE '45000' y<br>ejecuta ROLLBACK.|Error controlado sin alterar<br>registros existentes.|**APROBADO**|
|**CP-13**|Eliminar libro sin préstamos<br>(ID 5) vs. intentar eliminar<br>libro con historial (ID 1).|Borra libro 5 y sus<br>ejemplares; bloquea borrado<br>del libro 1.|Libro 5 eliminado<br>exitosamente; libro 1<br>protegido con mensaje de<br>historial.|**APROBADO**|
|**CP-14**|Inserciones directas inválidas<br>sobre prestamos (alumno<br>suspendido, ejemplar<br>prestado, fecha pasada).|Trigger validar_prestamo<br>intercepta y cancela las<br>inserciones.|El trigger BEFORE INSERT<br>bloqueó los tres casos con<br>SQLSTATE '45000'.|**APROBADO**|
|**CP-15**|Inserciones directas inválidas<br>sobre ejemplares (código<br>vacío '  ' o estado inicial<br>'prestado').|Trigger validar_ejemplar<br>impide ambos registros.|El trigger rechazó ambos<br>INSERT con sus respectivos<br>mensajes de error.|**APROBADO**|
|**CP-16**|Ejecutar Reporte 1 (libros<br>más solicitados) y Reporte 2<br>(alumnos con vencidos) en /<br>admin/panel/reportes.|Despliega libros con >= 2<br>préstamos y alumnos<br>morosos con títulos<br>concatenados y atraso.|Ambos reportes mostraron<br>resultados exactos y<br>ordenados<br>descendentemente.|**APROBADO**|



Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 24 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

## **10. Distribución del trabajo** 

|**Integrante**|**Actividades realizadas**|**Objetos de BD / módulos a su cargo**|
|---|---|---|
|**Luis Ángel Villanueva Tenorio**<br>**(Product Owner)**|Definición de la visión del producto,<br>levantamiento y priorización de<br>requerimientos funcionales/no funcionales,<br>delimitación del alcance, validación de<br>reglas de negocio frente a los criterios<br>académicos, coordinación del equipo,<br>diseño de pruebas de aceptación y<br>elaboración de la documentación técnica<br>final.|Requerimientos y arquitectura general del<br>sistema; revisión del modelo ER/Relacional,<br>validación de reglas de integridad, seguridad<br>por roles, matriz de pruebas (pruebas.sql) y<br>entregable documental completo.|
|**Christian Escutia Durán**<br>**(Desarrollador)**|Implementación principal de la base de<br>datos relacional en MySQL 8.0, codificación<br>de la lógica de backend en Python/Flask,<br>capa de acceso a datos y construcción de las<br>vistas funcionales del catálogo y panel<br>administrativo.|Scripts SQL (db.sql, procedimientos.sql,<br>funciones.sql, triggers.sql, usuarios.sql,<br>reportes.sql), servidor Flask (app.py),<br>módulos BD/*.py, formularios CRUD y lógica<br>de interacción del lector (registrarForm.js).|
|**Ismael Parra Calderón**<br>**(Desarrollador Colaborativo y QA de App)**|Desarrollo colaborativo en módulos de la<br>aplicación web, administración del<br>repositorio GitHub, integración continua<br>entre frontend y backend, revisión constante<br>del comportamiento de la aplicación,<br>pruebas funcionales de pantallas y<br>refinamiento visual.|Administración del repositorio (github.com/<br>ismparra/Biblioteca), apoyo en rutas y vistas<br>HTML/CSS/JS (carrusel 3D, estilos del panel y<br>flujos de usuario), pruebas de integración y<br>verificación de fallos en la aplicación.|



## **11. Conclusiones** 

**Luis Ángel Villanueva Tenorio:** Liderar este proyecto desde el rol de Product Owner me permitió confirmar que el éxito de un sistema de información no depende únicamente de escribir código que funcione, sino de alinear las reglas de negocio reales con un diseño de base de datos sólido desde el inicio. Separar la obra bibliográfica de cada ejemplar físico, definir roles claros con mínimo privilegio y asegurar la consistencia mediante transacciones y triggers nos permitió entregar una aplicación coherente, auditable y útil para el control bibliotecario. Además, coordinar las entregas y validar cada módulo contra casos de prueba concretos fortaleció nuestra disciplina de ingeniería de software en equipo. 

**Ismael Parra Calderón:** Participar en el desarrollo colaborativo y en la verificación continua de la aplicación me dejó un aprendizaje práctico muy valioso sobre cómo se integra un repositorio real con una base de datos relacional en MySQL 8.0. Revisar el flujo completo de las pantallas —desde el carrusel 3D y el inicio de sesión hasta los préstamos con lector de código de barras y los reportes— evidenció la importancia de manejar adecuadamente los errores provenientes del gestor de base de datos y de mantener organizado el código en GitHub para trabajar de forma ordenada y sin conflictos. 

**Christian Escutia Durán:** El desarrollo de «Biblioteca CriCri» consolidó mis conocimientos en programación avanzada de bases de datos y desarrollo web con Flask. Implementar procedimientos almacenados con START TRANSACTION, bloqueos FOR UPDATE y ROLLBACK automático, junto con triggers de validación y auditoría, demostró que delegar las reglas críticas de integridad al propio motor de MySQL hace que la aplicación sea mucho 

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 25 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

más segura y robusta frente a inconsistencias. Integrar estos objetos con el escáner de códigos de barras y consultas SQL de múltiples tablas representó un reto técnico completo y enriquecedor. 

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 26 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

## **12. Anexos** 

**Anexo A. Script SQL de creación de la base de datos y tablas (db.sql)** 

|`create database biblioteca;`<br>`use biblioteca;`|
|---|
|`-- Personal que usa el sistema (login y roles)`<br>`create table bibliotecarios (`<br>`id_bibliotecario int primary key auto_increment,`<br>`nombre_completo varchar(100) not null,`<br>`usuario varchar(50) not null unique,`<br>`password_hash varchar(255) not null,`<br>`rol enum('administrador','operador','consulta') not null,`<br>`estado enum('activo','inactivo') not null default 'activo'`<br>`);`|
|`-- Lectores que piden prestado`<br>`create table alumnos (`<br>`id_alumno int primary key auto_increment,`<br>`nombre_completo varchar(100) not null,`<br>`matricula varchar(30) not null unique,`<br>`estado enum('activo','suspendido') not null default 'activo'`<br>`);`|
|`-- Datos bibliograficos de la obra`<br>`create table libros (`<br>`id_libro int primary key auto_increment,`<br>`titulo varchar(200) not null,`<br>`autor varchar(100) not null,`<br>`categoria varchar(60) not null`<br>`);`|
|`-- Copia fisica con etiqueta de codigo de barras`<br>`create table ejemplares (`<br>`id_ejemplar int primary key auto_increment,`<br>`codigo_barras varchar(50) not null unique,`<br>`id_libro int not null,`<br>`estado enum('disponible','prestado') not null default 'disponible',`<br>`foreign key (id_libro) references libros(id_libro)`<br>`);`|
|`-- Un prestamo = un ejemplar prestado a un alumno`<br>`create table prestamos (`|
|`id_prestamo int primary key auto_increment,`<br>`id_alumno int not null,`<br>`id_ejemplar int not null,`<br>`id_bibliotecario int not null,`<br>`fecha_prestamo datetime not null default current_timestamp,`<br>`fecha_limite date not null,`<br>`fecha_devolucion datetime,`|
|`foreign key (idalumno) references alumnos(idalumno),`|
|`_  _`<br>`foreign key (id_ejemplar) references ejemplares(id_ejemplar),`<br>`foreign key (id_bibliotecario) references bibliotecarios(id_bibliotecario)`<br>|
|`);`|
|`-- Llenada por los triggers de auditoria`<br>`create table auditoria (`|
|<br>`id_auditoria int primary key auto_increment,`<br>`tabla varchar(64) not null,`<br>`operacion varchar(10) not null,`<br>`fecha_hora datetime not null default current_timestamp,`<br>`usuario varchar(100) not null,`<br>`datos_anteriores text,`|



Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 27 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

```
    datos_nuevos text
);
```

#### **Anexo B. Script de procedimientos almacenados, funciones y triggers** 

##### **1. Funciones almacenadas (funciones.sql)** 

```
use biblioteca;
delimiter $$
create function ejemplares_disponibles(p_libro int) returns int reads sql data
begin
    declare cantidad int;
    select count(*) into cantidad from ejemplares where id_libro = p_libro and estado = 'disponible';
    return cantidad;
end $$
delimiter ;
delimiter $$
create function dias_retraso(p_prestamo int) returns int reads sql data
begin
    declare existe boolean default true;
    declare v_fecha_limite date;
    declare v_fecha_devolucion datetime;
    declare dias int;
    declare continue handler for not found set existe = false;
    select fecha_limite, fecha_devolucion into v_fecha_limite, v_fecha_devolucion
    from prestamos where id_prestamo = p_prestamo;
    if existe = false then
        return -1;
    end if;
    set dias = datediff(ifnull(v_fecha_devolucion, curdate()), v_fecha_limite);
    if dias < 0 then
        return 0;
    end if;
    return dias;
end $$
delimiter ;
```

##### **2. Procedimientos almacenados y transacciones (procedimientos.sql)** 

```
use biblioteca;
delimiter $$
create procedure registrar_prestamo(
    in p_matricula varchar(30), in p_codigo varchar(50),
    in p_bibliotecario int, in p_fecha_limite date
)
begin
    declare v_alumno int;
    declare v_ejemplar int;
    declare v_estado varchar(20);
    declare exit handler for sqlexception
    begin
        rollback;
        resignal;
    end;
    start transaction;
    select id_alumno into v_alumno from alumnos where matricula = p_matricula and estado = 'activo' for
update;
    select id_ejemplar, estado into v_ejemplar, v_estado from ejemplares where codigo_barras = p_codigo for
update;
    if v_alumno is null then
```

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 28 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

```
        signal sqlstate '45000' set message_text = 'El alumno no existe o esta suspendido';
    end if;
    if v_ejemplar is null then
        signal sqlstate '45000' set message_text = 'No existe un ejemplar con ese codigo de barras';
    end if;
    if v_estado != 'disponible' then
        signal sqlstate '45000' set message_text = 'El ejemplar ya esta prestado';
    end if;
    if not exists (select 1 from bibliotecarios where id_bibliotecario = p_bibliotecario and estado =
'activo' and rol in ('administrador','operador')) then
        signal sqlstate '45000' set message_text = 'El usuario no tiene permiso para registrar prestamos';
    end if;
    if p_fecha_limite is null or p_fecha_limite < curdate() then
        signal sqlstate '45000' set message_text = 'La fecha limite no es valida';
    end if;
    insert into prestamos(id_alumno, id_ejemplar, id_bibliotecario, fecha_limite)
    values(v_alumno, v_ejemplar, p_bibliotecario, p_fecha_limite);
    update ejemplares set estado = 'prestado' where id_ejemplar = v_ejemplar;
    commit;
end $$
delimiter ;
delimiter $$
create procedure registrar_devolucion(in p_codigo varchar(50))
begin
    declare v_ejemplar int;
    declare v_prestamo int;
    declare exit handler for sqlexception
    begin
        rollback;
        resignal;
    end;
    start transaction;
    select id_ejemplar into v_ejemplar from ejemplares where codigo_barras = p_codigo for update;
    if v_ejemplar is null then
        signal sqlstate '45000' set message_text = 'No existe un ejemplar con ese codigo de barras';
    end if;
    select id_prestamo into v_prestamo from prestamos where id_ejemplar = v_ejemplar and fecha_devolucion is
null for update;
    if v_prestamo is null then
        signal sqlstate '45000' set message_text = 'El ejemplar no tiene un prestamo activo';
    end if;
    update prestamos set fecha_devolucion = now() where id_prestamo = v_prestamo;
    update ejemplares set estado = 'disponible' where id_ejemplar = v_ejemplar;
    commit;
end $$
delimiter ;
delimiter $$
create procedure eliminar_libro(in p_libro int)
begin
    declare v_libro int;
    declare exit handler for sqlexception
    begin
        rollback;
        resignal;
    end;
    start transaction;
    select id_libro into v_libro from libros where id_libro = p_libro for update;
    if v_libro is null then
        signal sqlstate '45000' set message_text = 'El libro no existe';
    end if;
    if exists (select 1 from prestamos p join ejemplares e on e.id_ejemplar = p.id_ejemplar where e.id_libro
= p_libro) then
        signal sqlstate '45000' set message_text = 'No se puede eliminar: el libro tiene prestamos
```

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 29 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

```
registrados';
    end if;
    delete from ejemplares where id_libro = p_libro;
    delete from libros where id_libro = p_libro;
    commit;
end $$
delimiter ;
delimiter $$
create procedure consultar_alumno(
    in p_matricula varchar(30), out p_nombre varchar(100),
    out p_activos int, out p_vencidos int
)
begin
    if exists (select 1 from alumnos where matricula = p_matricula) then
        set p_nombre = (select nombre_completo from alumnos where matricula = p_matricula);
        set p_activos = (select count(*) from prestamos p join alumnos a on a.id_alumno = p.id_alumno where
a.matricula = p_matricula and p.fecha_devolucion is null);
        set p_vencidos = (select count(*) from prestamos p join alumnos a on a.id_alumno = p.id_alumno where
a.matricula = p_matricula and p.fecha_devolucion is null and dias_retraso(p.id_prestamo) > 0);
    else
        set p_nombre = 'Alumno no encontrado';
        set p_activos = 0;
        set p_vencidos = 0;
    end if;
end $$
delimiter ;
delimiter $$
create procedure iniciar_sesion(in p_usuario varchar(50), in p_password varchar(100))
begin
    select id_bibliotecario, nombre_completo, usuario, rol, estado
    from bibliotecarios
    where usuario = p_usuario and password_hash = sha2(concat(usuario, p_password), 256);
end $$
delimiter ;
delimiter $$
create procedure registrar_usuario(
    in p_nombre varchar(100), in p_usuario varchar(50),
    in p_password varchar(100), in p_rol varchar(20)
)
begin
    insert into bibliotecarios
    values(default, p_nombre, p_usuario, sha2(concat(p_usuario, p_password), 256), p_rol, 'activo');
end $$
delimiter ;
```

##### **3. Triggers de validación y auditoría (triggers.sql)** 

```
use biblioteca;
delimiter $$
create trigger validar_prestamo before insert on prestamos
for each row
begin
    if not exists (select 1 from alumnos where id_alumno = new.id_alumno and estado = 'activo') then
        signal sqlstate '45000' set message_text = 'El alumno no existe o esta suspendido';
    end if;
    if not exists (select 1 from ejemplares where id_ejemplar = new.id_ejemplar and estado = 'disponible')
then
        signal sqlstate '45000' set message_text = 'El ejemplar no esta disponible';
    end if;
    if new.fecha_limite < date(new.fecha_prestamo) then
        signal sqlstate '45000' set message_text = 'La fecha limite no puede ser anterior a la fecha del
prestamo';
```

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 30 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

```
    end if;
end $$
delimiter ;
delimiter $$
create trigger validar_ejemplar before insert on ejemplares
for each row
begin
    if new.codigo_barras is null or trim(new.codigo_barras) = '' then
        signal sqlstate '45000' set message_text = 'El codigo de barras no puede estar vacio';
    end if;
    if new.estado != 'disponible' then
        signal sqlstate '45000' set message_text = 'Un ejemplar nuevo debe estar disponible';
    end if;
end $$
delimiter ;
delimiter $$
create trigger auditar_prestamo after insert on prestamos
for each row
begin
    insert into auditoria values(default, 'prestamos', 'INSERT', now(), user(), null,
    concat('id_prestamo: ', new.id_prestamo, ', id_alumno: ', new.id_alumno,
           ', id_ejemplar: ', new.id_ejemplar, ', id_bibliotecario: ', new.id_bibliotecario,
           ', fecha_limite: ', new.fecha_limite));
end $$
delimiter ;
delimiter $$
create trigger auditar_devolucion after update on prestamos
for each row
begin
    if not (new.fecha_devolucion <=> old.fecha_devolucion) then
        insert into auditoria values(default, 'prestamos', 'UPDATE', now(), user(),
        concat('id_prestamo: ', old.id_prestamo, ', fecha_devolucion: ', ifnull(old.fecha_devolucion, 'sin
devolver')),
        concat('id_prestamo: ', new.id_prestamo, ', fecha_devolucion: ', ifnull(new.fecha_devolucion, 'sin
devolver')));
    end if;
end $$
delimiter ;
```

**Anexo C. Script de usuarios, roles y permisos (usuarios.sql)** 

```
use biblioteca;
create role 'rol_administrador', 'rol_operador', 'rol_consulta';
grant select, insert, update on biblioteca.bibliotecarios to 'rol_administrador';
grant select, insert, update on biblioteca.alumnos to 'rol_administrador';
grant select, insert, update on biblioteca.libros to 'rol_administrador';
grant select, insert, update on biblioteca.ejemplares to 'rol_administrador';
grant select on biblioteca.prestamos to 'rol_administrador';
grant select on biblioteca.auditoria to 'rol_administrador';
grant execute on procedure biblioteca.registrar_prestamo to 'rol_administrador';
grant execute on procedure biblioteca.registrar_devolucion to 'rol_administrador';
grant execute on procedure biblioteca.eliminar_libro to 'rol_administrador';
grant execute on procedure biblioteca.registrar_usuario to 'rol_administrador';
grant execute on procedure biblioteca.consultar_alumno to 'rol_administrador';
grant execute on procedure biblioteca.iniciar_sesion to 'rol_administrador';
grant execute on function biblioteca.ejemplares_disponibles to 'rol_administrador';
grant execute on function biblioteca.dias_retraso to 'rol_administrador';
grant select on biblioteca.alumnos to 'rol_operador';
```

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 31 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

```
grant select on biblioteca.libros to 'rol_operador';
grant select on biblioteca.ejemplares to 'rol_operador';
grant select on biblioteca.prestamos to 'rol_operador';
grant execute on procedure biblioteca.registrar_prestamo to 'rol_operador';
grant execute on procedure biblioteca.registrar_devolucion to 'rol_operador';
grant execute on procedure biblioteca.consultar_alumno to 'rol_operador';
grant execute on function biblioteca.ejemplares_disponibles to 'rol_operador';
grant execute on function biblioteca.dias_retraso to 'rol_operador';
grant select on biblioteca.libros to 'rol_consulta';
grant select on biblioteca.ejemplares to 'rol_consulta';
grant execute on function biblioteca.ejemplares_disponibles to 'rol_consulta';
create user 'bib_admin'@'localhost' identified by 'Admin123!';
create user 'bib_operador'@'localhost' identified by 'Operador123!';
create user 'bib_consulta'@'localhost' identified by 'Consulta123!';
create user 'bib_login'@'localhost' identified by 'Login123!';
grant execute on procedure biblioteca.iniciar_sesion to 'bib_login'@'localhost';
grant 'rol_administrador' to 'bib_admin'@'localhost';
grant 'rol_operador' to 'bib_operador'@'localhost';
grant 'rol_consulta' to 'bib_consulta'@'localhost';
set default role 'rol_administrador' to 'bib_admin'@'localhost';
set default role 'rol_operador' to 'bib_operador'@'localhost';
set default role 'rol_consulta' to 'bib_consulta'@'localhost';
```

#### **Anexo D. Script de datos de prueba y verificación (pruebas.sql)** 

```
use biblioteca;
insert into bibliotecarios values
(1,'Laura Gomez','admin',sha2('adminadmin123',256),'administrador','activo'),
(2,'Carlos Ruiz','operador',sha2('operadoroperador123',256),'operador','activo'),
(3,'Maria Lopez','consulta',sha2('consultaconsulta123',256),'consulta','activo'),
(4,'Pedro Sanchez','inactivo',sha2('inactivoinactivo123',256),'operador','inactivo');
insert into alumnos values
(1,'Ana Torres','A001','activo'),
(2,'Luis Hernandez','A002','activo'),
(3,'Sofia Martinez','A003','activo'),
(4,'Jorge Ramirez','A004','suspendido');
insert into libros values
(1,'Cien años de soledad','Gabriel Garcia Marquez','Novela'),
(2,'Fundacion','Isaac Asimov','Ciencia Ficcion'),
(3,'Sapiens','Yuval Noah Harari','Historia'),
(4,'Fundamentos de bases de datos','Abraham Silberschatz','Tecnologia'),
(5,'Pedagogia del oprimido','Paulo Freire','Educacion');
insert into ejemplares values
(1,'7501000000011',1,'disponible'),
(2,'7501000000028',1,'disponible'),
(3,'7501000000035',2,'disponible'),
(4,'7501000000042',3,'disponible'),
(5,'7501000000059',4,'disponible'),
(6,'7501000000066',4,'disponible'),
(7,'7501000000073',5,'disponible');
insert into prestamos values
(1,1,1,2, now() - interval 30 day, curdate() - interval 23 day, now() - interval 25 day),
(2,2,3,2, now() - interval 20 day, curdate() - interval 13 day, now() - interval 10 day),
(3,1,4,2, now() - interval 10 day, curdate() - interval 3 day, null),
(4,1,2,2, now() - interval 60 day, curdate() - interval 53 day, now() - interval 55 day),
```

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 32 de 33 

Taller de Bases de Datos  |  Proyecto Final: Biblioteca CriCri 

```
(5,2,2,2, now() - interval 45 day, curdate() - interval 38 day, now() - interval 36 day),
(6,3,1,2, now() - interval 50 day, curdate() - interval 43 day, now() - interval 44 day),
(7,3,3,1, now() - interval 40 day, curdate() - interval 33 day, now() - interval 34 day),
(8,1,5,2, now() - interval 55 day, curdate() - interval 48 day, now() - interval 50 day),
(9,2,5,2, now() - interval 35 day, curdate() - interval 28 day, now() - interval 27 day),
(10,3,6,1, now() - interval 42 day, curdate() - interval 35 day, now() - interval 37 day),
(11,1,6,2, now() - interval 28 day, curdate() - interval 21 day, now() - interval 18 day),
(12,3,1,2, now() - interval 20 day, curdate() - interval 13 day, now() - interval 14 day),
(13,2,5,2, now() - interval 15 day, curdate() - interval 8 day, null),
(14,3,6,2, now() - interval 14 day, curdate() - interval 7 day, null),
(15,2,3,1, now() - interval 9 day, curdate() - interval 2 day, null);
```

```
update ejemplares set estado = 'prestado' where id_ejemplar in (3,4,5,6);
-- Verificación de funciones, procedimientos, login y auditoría
select id_libro, titulo, autor, ejemplares_disponibles(id_libro) as disponibles from libros;
select id_prestamo, fecha_limite, fecha_devolucion, dias_retraso(id_prestamo) as retraso from prestamos;
call registrar_prestamo('A002','7501000000011',2, date_add(curdate(), interval 7 day));
call consultar_alumno('A001', @nombre, @activos, @vencidos);
select @nombre, @activos, @vencidos;
call registrar_devolucion('7501000000011');
call eliminar_libro(5);
call iniciar_sesion('admin','admin123');
call registrar_usuario('Rosa Diaz','rosa','rosa123','operador');
select * from auditoria;
```

#### **Anexo E. Enlace al repositorio de GitHub** 

Código fuente completo, historial de commits y scripts SQL disponibles en: 

**https://github.com/ismparra/Biblioteca/** 

Instituto Tecnológico Superior del Sur de Guanajuato (ITSUR)  —  Ing. en Sistemas Computacionales   |   Página 33 de 33 

