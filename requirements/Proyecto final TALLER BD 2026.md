## Proyecto final:

## Desarrollo de un sistema de información con base de datos relacional

Materia: Taller de Bases de Datos

Equipos de 3 integrantes

Proyecto práctico

Objetivo: Analizar, diseñar e implementar un sistema de información que utilice una base de datos relacional, incorporando mecanismos de seguridad, integridad, automatización, auditoría y generación de reportes.

## 1. Descripción general

Cada equipo deberá seleccionar una problemática real o simulada y desarrollar un sistema de información que permita administrar sus procesos mediante una aplicación conectada a una base de datos.

El sistema deberá utilizar un lector de código de barras para realizar al menos una operación importante. El lector no deberá utilizarse únicamente como elemento decorativo: su lectura tendrá que provocar una consulta, registro, actualización o proceso dentro del sistema.

Restricción importante: No se permite desarrollar un sistema de punto de venta (POS), ni un sistema cuya función principal sea registrar ventas y cobrar productos.

## 2. Propuestas de sistemas de información

Los equipos podrán seleccionar una de las siguientes propuestas o plantear otra, siempre que sea autorizada por el docente.

## 1. Sistema de gestión de biblioteca

- Registrar libros mediante código de barras.

- Realizar préstamos y devoluciones.

- Consultar disponibilidad de ejemplares.

- Identificar libros con retraso en devolución.

## 2. Sistema de control de inventario de equipo de cómputo

- Registrar equipos mediante código de barras.

- Asignar equipos a alumnos, docentes o departamentos.

- Registrar préstamos y devoluciones.

- Consultar historial de asignaciones y estado de los equipos.


## 3. Sistema de administración de laboratorio

- Registrar reactivos y materiales con código de barras.

- Registrar entradas y salidas de materiales.

- Controlar existencias y fechas de caducidad.

- Registrar responsables de los movimientos.

## 4. Sistema de gestión documental

- Identificar expedientes mediante código de barras.

- Registrar préstamos y devoluciones de expedientes.

- Consultar su ubicación física.

- Mantener un historial de consultas y movimientos.

## 5. Sistema de control de material médico

- Identificar materiales mediante código de barras.

- Registrar entradas y salidas.

- Controlar lotes y caducidades.

- Consultar materiales próximos a agotarse.

## 3. Requerimientos funcionales y técnicos obligatorios

Todos los proyectos deberán cumplir con los siguientes requisitos.

## A. Diseño y construcción de la base de datos

## El equipo deberá:

- 1. 2. 3. 4. 5. 6. 7. Definir llaves primarias y foráneas.

- Elaborar un diagrama entidad-relación.

- Diseñar las tablas y establecer sus relaciones.

- Establecer restricciones de integridad.

- Implementar la base de datos mediante sentencias SQL.

- Incluir datos de prueba suficientes para demostrar el funcionamiento del sistema.

- Identificar las entidades necesarias para el funcionamiento del sistema.


Entregable: Diagrama entidad-relación, modelo relacional y script SQL de creación y población de la base de datos.

## B. Uso del lector de código de barras

El sistema deberá utilizar un lector físico de código de barras.

El lector deberá permitir realizar al menos una de las siguientes operaciones:

- Buscar un registro mediante su código.

- Registrar la entrada de un artículo o equipo.

- Registrar la salida de un artículo o equipo.

- Realizar un préstamo o devolución.

- Identificar un activo o expediente.

- Consultar información asociada al código leído.

El código de barras deberá estar almacenado en una columna de la base de datos y contar con una restricción que evite duplicados.

Importante: Se deberá demostrar el funcionamiento del lector físico durante la presentación del proyecto.

## C. Tabla de usuarios y seguridad

La base de datos deberá incluir una tabla para administrar los usuarios del sistema.

Como mínimo, deberá almacenar:

- Identificador del usuario.

- Nombre completo.

- Nombre de usuario.

- Contraseña almacenada como hash.

- Rol o tipo de usuario.

- Estado de la cuenta.

Requisitos de seguridad:

- 1. 2. 3. 4. 5. 6. Utilizar un algoritmo adecuado para almacenamiento de contraseñas, como sha2, Argon2id o bcrypt.

- No almacenar contraseñas en texto plano.

- Implementar diferentes roles de usuario.

- Restringir las operaciones de acuerdo con los permisos de cada rol.

- Evitar que los usuarios puedan ejecutar operaciones para las cuales no tienen autorización.

Por ejemplo, el sistema podría tener los roles de administrador, operador y consulta.

- Implementar inicio de sesión.


## D. Transacciones

El sistema deberá implementar al menos una operación que utilice una transacción explícita.

Se deberán utilizar las instrucciones:

## START TRANSACTION;

- - Operaciones de modificación

COMMIT;

También deberá contemplarse el uso de:

ROLLBACK;

La transacción deberá resolver una operación que involucre varias modificaciones relacionadas.

## Ejemplos:

- Registrar un préstamo y actualizar la disponibilidad del equipo.

- Registrar una devolución y actualizar el estado del ejemplar.

- Registrar una salida de material y actualizar las existencias.

- Registrar una asignación de equipo y actualizar su ubicación.

No se aceptará una transacción que solamente ejecute una inserción aislada. Debe existir una situación en

la que sea necesario confirmar o cancelar varias operaciones para mantener la integridad de los datos.

## E. Stored Procedures (procedimientos almacenados)

El proyecto deberá incluir al menos 3 procedimientos almacenados.

## Requisitos:

- Al menos uno deberá recibir parámetros de entrada.

- Al menos uno deberá utilizar parámetros de salida (OUT).

- Al menos uno deberá realizar operaciones de inserción, actualización o eliminación.

- Deberán utilizarse desde la aplicación.

## Ejemplos:

- Registrar un préstamo.

- Consultar información de un artículo por código de barras.

- Registrar una devolución.

- Obtener la cantidad de materiales disponibles.

- Consultar el historial de movimientos de un equipo.


## F. Functions (funciones)

Se deberán desarrollar al menos 2 funciones almacenadas.

Las funciones deberán resolver operaciones útiles para el sistema.

Ejemplos:

- Calcular los días de retraso de un préstamo.

- Obtener la cantidad de artículos disponibles.

- Calcular el total de materiales asignados a un departamento.

- Determinar si un artículo se encuentra disponible.

- Calcular el porcentaje de disponibilidad de equipos.

Las funciones deberán utilizarse en consultas SQL o en otros objetos de la base de datos.

## G. Triggers de validación

Se deberán desarrollar al menos 2 triggers de validación.

Su propósito será impedir operaciones que puedan generar inconsistencias.

Ejemplos:

- Impedir que se registre una salida cuando no existen existencias suficientes.

- Impedir que se preste un equipo que ya se encuentra asignado.

- Impedir que se registre una devolución de un préstamo inexistente.

- Evitar que se establezca una cantidad negativa.

- Impedir que se registre un código de barras vacío.

Los triggers deberán ejecutarse automáticamente ante las operaciones correspondientes.

## H. Triggers de auditoría

Se deberán desarrollar al menos 2 triggers de auditoría.

Se deberá crear una tabla de auditoría que permita registrar cambios realizados en la base de datos. Como mínimo, deberá almacenar:

- Identificador del movimiento.

- Tabla afectada.

- Tipo de operación (INSERT, UPDATE o DELETE).

- Fecha y hora.

- Usuario responsable.

- Información anterior, cuando corresponda.

- Información nueva, cuando corresponda.

Se deberán registrar automáticamente operaciones de modificación realizadas sobre alguna tabla importante del sistema.

Ejemplo: Si un usuario modifica la ubicación de un equipo, el trigger deberá registrar la ubicación anterior y la nueva.


## I. Reportes y consultas avanzadas

El sistema deberá incluir uno o dos reportes que permitan obtener información relevante para la toma de decisiones.

Los reportes deberán utilizar consultas SQL de complejidad intermedia o avanzada.

Se deberán demostrar al menos tres de las siguientes características:

- JOIN entre tres o más tablas.

- Subconsultas.

- Funciones de agregación (COUNT, SUM, AVG, etc.).

- Agrupaciones con GROUP BY.

- Condiciones sobre agrupaciones con HAVING.

- Consultas con EXISTS o NOT EXISTS.

- Funciones de ventana, cuando el gestor las soporte.

- CTE, cuando el gestor las soporte.

Ejemplos de reportes:

## Sistema Reporte propuesto

Biblioteca

Laboratorio

Equipo cómputo

Gestión documental

Expedientes más consultados y expedientes que no han sido devueltos.

Material médico Materiales con mayor salida y productos próximos a agotarse.

Los reportes deberán presentarse en la aplicación, no únicamente ejecutarse desde el gestor de base de datos.

Libros más solicitados y alumnos con préstamos vencidos.

Materiales con mayor consumo y reactivos próximos a caducar.

de Equipos con más asignaciones y departamentos con mayor cantidad de equipos.

## 4. Desarrollo de la aplicación

El equipo deberá construir una aplicación que permita interactuar con la base de datos.

La aplicación deberá incluir, como mínimo:

- Inicio de sesión.

- Menú principal.

- Módulos para administrar los registros principales del sistema.

- Búsquedas mediante código de barras.

- Operaciones que utilicen procedimientos almacenados.

- Visualización de los reportes.

- Manejo de mensajes de error y confirmación.

- Restricciones de acceso según el rol del usuario.

La interfaz puede desarrollarse con las tecnologías vistas durante el curso o las autorizadas por el docente.


La aplicación deberá conectarse a la base de datos y ejecutar operaciones reales. No se aceptarán prototipos que solamente simulen el funcionamiento.

## 5. Entregables del proyecto

Cada equipo deberá entregar los siguientes elementos:

## No. Entregable

- 1 Documento con la descripción del problema y justificación del sistema.

- 2 Lista de requerimientos funcionales y no funcionales.

- 4 Modelo relacional y diccionario de datos.

- 5 Script SQL para crear la base de datos y sus tablas. Incluir funciones, proc, triggers.

- 6 Script de procedimientos almacenados, funciones y triggers.

- 7 Script de usuarios, roles y permisos de seguridad.

- 8 Código fuente completo de la aplicación en GITHUB donde se muestre el trabajo de cada alumno.

- 9 Evidencias de funcionamiento del lector de código de barras.

## 9. Condiciones importantes

- Los equipos estarán integrados por tres alumnos, en condiciones especiales podrían ser 2.

- No se permitirá entregar una base de datos descargada o un sistema previamente desarrollado.

- Todos los objetos de base de datos deberán ser creados y explicados por los integrantes.

- El lector de código de barras deberá ser físico y funcionar durante la presentación.

- No se aceptará que los procedimientos, funciones o triggers sean solamente scripts sin relación con el funcionamiento real del sistema.

- Los integrantes deberán responder preguntas sobre el diseño y la implementación.

- El proyecto deberá ejecutarse correctamente en el equipo donde se realice la evaluación.
