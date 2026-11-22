# Diccionario de datos – Base de datos `biblioteca`

Motor: MySQL. Fuente: `database/db.sql`.

## bibliotecarios
Personal que usa el sistema (login y roles).

| Columna | Tipo | Nulo | Clave / Restricción | Descripción |
|---|---|---|---|---|
| id_bibliotecario | INT AUTO_INCREMENT | No | PK | Identificador del bibliotecario |
| nombre_completo | VARCHAR(100) | No | | Nombre completo |
| usuario | VARCHAR(50) | No | UNIQUE | Nombre de usuario para iniciar sesión |
| password_hash | VARCHAR(255) | No | | Contraseña almacenada como hash (nunca en texto plano) |
| rol | ENUM('administrador','operador','consulta') | No | | Rol que define los permisos |
| estado | ENUM('activo','inactivo') | No | Default `activo` | Si puede entrar al sistema |

## alumnos
Lectores que piden libros prestados.

| Columna | Tipo | Nulo | Clave / Restricción | Descripción |
|---|---|---|---|---|
| id_alumno | INT AUTO_INCREMENT | No | PK | Identificador del alumno |
| nombre_completo | VARCHAR(100) | No | | Nombre completo |
| matricula | VARCHAR(30) | No | UNIQUE | Matrícula escolar |
| estado | ENUM('activo','suspendido') | No | Default `activo` | Un alumno suspendido no debería recibir préstamos |

## libros
Datos bibliográficos de la obra.

| Columna | Tipo | Nulo | Clave / Restricción | Descripción |
|---|---|---|---|---|
| id_libro | INT AUTO_INCREMENT | No | PK | Identificador del libro |
| titulo | VARCHAR(200) | No | | Título de la obra |
| autor | VARCHAR(100) | No | | Autor |
| categoria | VARCHAR(60) | No | | Categoría o género |

## ejemplares
Copia física de un libro, con etiqueta de código de barras.

| Columna | Tipo | Nulo | Clave / Restricción | Descripción |
|---|---|---|---|---|
| id_ejemplar | INT AUTO_INCREMENT | No | PK | Identificador del ejemplar |
| codigo_barras | VARCHAR(50) | No | UNIQUE | Código leído por el escáner |
| id_libro | INT | No | FK → libros.id_libro | Libro al que pertenece la copia |
| estado | ENUM('disponible','prestado') | No | Default `disponible` | Situación actual de la copia |

## prestamos
Un préstamo = un ejemplar prestado a un alumno, atendido por un bibliotecario.

| Columna | Tipo | Nulo | Clave / Restricción | Descripción |
|---|---|---|---|---|
| id_prestamo | INT AUTO_INCREMENT | No | PK | Identificador del préstamo |
| id_alumno | INT | No | FK → alumnos.id_alumno | Quién lo pidió |
| id_ejemplar | INT | No | FK → ejemplares.id_ejemplar | Copia prestada |
| id_bibliotecario | INT | No | FK → bibliotecarios.id_bibliotecario | Quién registró el préstamo |
| fecha_prestamo | DATETIME | No | Default `CURRENT_TIMESTAMP` | Momento del préstamo |
| fecha_limite | DATE | No | | Fecha máxima de devolución |
| fecha_devolucion | DATETIME | Sí | | `NULL` = aún no devuelto |

## auditoria
Se llena automáticamente con los triggers de auditoría.

| Columna | Tipo | Nulo | Clave / Restricción | Descripción |
|---|---|---|---|---|
| id_auditoria | INT AUTO_INCREMENT | No | PK | Identificador del registro |
| tabla | VARCHAR(64) | No | | Tabla afectada |
| operacion | VARCHAR(10) | No | | INSERT, UPDATE o DELETE |
| fecha_hora | DATETIME | No | Default `CURRENT_TIMESTAMP` | Cuándo ocurrió |
| usuario | VARCHAR(100) | No | | Usuario que hizo la operación |
| datos_anteriores | TEXT | Sí | | Valores antes del cambio (NULL en INSERT) |
| datos_nuevos | TEXT | Sí | | Valores después del cambio (NULL en DELETE) |

## Relaciones

- `libros` 1 — N `ejemplares`
- `alumnos` 1 — N `prestamos`
- `ejemplares` 1 — N `prestamos`
- `bibliotecarios` 1 — N `prestamos`
- `auditoria` no tiene llaves foráneas (es un registro independiente).
