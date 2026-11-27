# Proyecto Final – Taller de Bases de Datos

## Repositorio

[https://github.com/ismparra/Biblioteca](https://github.com/ismparra/Biblioteca.git)

## Resumen

- Sistema de información con BD relacional (MySQL) + aplicación conectada + **lector de código de barras físico** que funcione en la presentación.
- Equipo de 3 integrantes. **Prohibido: POS / sistema de ventas y cobro.**
- Todo debe ser creado y explicado por nosotros. Se evalúa en el equipo donde se presente.

## Decisiones del equipo

- Sistema elegido: **Biblioteca**
- Lenguaje / tecnología de la app: **(Back Python → TBA) + (MySQL) + (FrontEnd → TBA)**
- Lector de código de barras (modelo): *(pendiente)*
- Repositorio GitHub: *(pendiente, debe mostrar el trabajo de cada integrante) @ISMAEL PARRA CALDERON*

## Integrantes y responsabilidades

- Integrante 1: LUIS ANGEL VILLANUEVA TENORIO
    - TBA
- Integrante 2: ISMAEL PARRA CALDERON
    - TBA
- Integrante 3: CHRISTIAN ESCUTIA DURAN
    - TBA

## Checklist de requisitos técnicos (mínimos)

- [ ]  Diagrama entidad-relación + modelo relacional + diccionario de datos
- [ ]  Script SQL de creación y datos de prueba (PK, FK, restricciones de integridad)
- [ ]  Código de barras en columna con restricción UNIQUE
- [ ]  Tabla de usuarios (id, nombre completo, usuario, contraseña con hash, rol, estado)
- [ ]  Login + roles (ej. administrador / operador / consulta) con permisos reales
- [ ]  Al menos 1 transacción explícita (START TRANSACTION / COMMIT / ROLLBACK) con varias modificaciones relacionadas
- [ ]  3 stored procedures (uno con parámetros de entrada, uno con OUT, uno que modifique datos) usados desde la app
- [ ]  2 funciones almacenadas usadas en consultas u otros objetos
- [ ]  2 triggers de validación
- [ ]  2 triggers de auditoría + tabla de auditoría (tabla, operación, fecha/hora, usuario, datos anteriores y nuevos)
- [ ]  1–2 reportes con 3+ características (JOIN de 3+ tablas, subconsultas, agregación, GROUP BY, HAVING, EXISTS, ventanas, CTE) mostrados en la app
- [ ]  App: login, menú, módulos de registros, búsqueda por código de barras, mensajes de error/confirmación, restricciones por rol
- [ ]  Lector físico funcionando en la demo

## Entregables

- [ ]  1. Descripción del problema y justificación
- [ ]  2. Requerimientos funcionales y no funcionales
- [ ]  3. Modelo relacional y diccionario de datos
- [ ]  4. Script SQL de creación (tablas, funciones, procedimientos, triggers)
- [ ]  5. Script de procedimientos, funciones y triggers
- [ ]  6. Script de usuarios, roles y permisos
- [ ]  7. Código fuente completo en GitHub (con aportes de cada alumno)
- [ ]  8. Evidencias del lector de código de barras
