# Biblioteca CriCri: Requerimientos del sistema

## Requerimientos funcionales

| ID | Requerimiento | Prioridad | Rol |
|---|---|---|---|
| RF-01 | El sistema permite iniciar sesión con usuario y contraseña, validando las credenciales contra la base de datos y verificando que el usuario esté activo. | Alta | Todos |
| RF-02 | El sistema busca e identifica un ejemplar y su obra asociada al leer su código de barras con el lector óptico. | Alta | Administrador, Operador |
| RF-03 | El sistema muestra el catálogo de libros en una galería interactiva 3D y permite filtrar obras por título o autor. | Alta | Todos |
| RF-04 | El sistema muestra la ficha detallada de un libro, incluyendo la cantidad de ejemplares disponibles calculada dinámicamente. | Alta | Todos |
| RF-05 | El sistema permite registrar, editar y eliminar libros, impidiendo eliminar obras que cuenten con historial de préstamos. | Alta | Administrador |
| RF-06 | El sistema permite dar de alta ejemplares físicos asociados a un libro, asignándoles un código de barras único y estado inicial disponible. | Alta | Administrador |
| RF-07 | El sistema permite registrar préstamos de uno o varios ejemplares escaneados a un alumno activo, actualizando atómicamente el estado del ejemplar a prestado. | Alta | Administrador, Operador |
| RF-08 | El sistema permite registrar la devolución de un ejemplar mediante su código de barras, cerrando el préstamo con la fecha y hora actual y liberando el ejemplar. | Alta | Administrador, Operador |
| RF-09 | El sistema permite consultar el historial de préstamos activos y devueltos, mostrando alumno, libro, bibliotecario, fechas y días de atraso. | Alta | Administrador, Operador |
| RF-10 | El sistema permite consultar el resumen de un alumno por matrícula, indicando su nombre, préstamos activos y préstamos vencidos. | Media | Administrador, Operador |
| RF-11 | El sistema permite gestionar alumnos: alta, consulta, edición, suspensión (baja lógica), reactivación y eliminación controlada. | Alta | Administrador |
| RF-12 | El sistema permite gestionar usuarios bibliotecarios: registro con contraseña hasheada, consulta, edición, baja lógica, reactivación y eliminación (impidiendo auto-eliminarse). | Alta | Administrador |
| RF-13 | El sistema genera reportes de libros más solicitados (2 o más préstamos) y de alumnos con préstamos vencidos ordenados por días de atraso. | Alta | Administrador, Operador |
| RF-14 | El sistema registra automáticamente en una tabla de auditoría cada préstamo y cada devolución, permitiendo su consulta desde el panel administrativo. | Alta | Administrador |
| RF-15 | El sistema permite cerrar sesión, limpiando las variables de sesión del navegador y retornando al catálogo público. | Media | Todos |

## Requerimientos no funcionales

| ID | Requerimiento | Categoría |
|---|---|---|
| RNF-01 | Las contraseñas de los usuarios se almacenan como hash SHA-256 con sal por usuario, nunca en texto plano. | Seguridad |
| RNF-02 | El sistema utiliza MySQL 8.0 como gestor de base de datos relacional con motor InnoDB. | Compatibilidad |
| RNF-03 | Las operaciones críticas (préstamos, devoluciones y borrado de libros) se ejecutan bajo transacciones ACID con bloqueo pesimista `FOR UPDATE` y `ROLLBACK` automático ante fallos. | Integridad / Confiabilidad |
| RNF-04 | El acceso a la base de datos implementa el principio de mínimo privilegio mediante roles nativos de MySQL y un usuario aislado exclusivo para el login. | Seguridad |
| RNF-05 | La interfaz web ofrece navegación responsiva en tema oscuro de alto contraste, retroalimentación inmediata mediante alertas y compatibilidad con navegadores modernos. | Usabilidad |
| RNF-06 | La lectura de códigos de barras opera con cualquier escáner USB estándar en modo emulación de teclado (HID), sin requerir controladores propietarios. | Interoperabilidad |
| RNF-07 | Cada inserción o devolución en la tabla de préstamos queda registrada automáticamente en la tabla de auditoría con fecha, hora, usuario y estado anterior y nuevo. | Auditabilidad |
| RNF-08 | El código fuente del proyecto (backend, vistas y scripts SQL) se mantiene bajo control de versiones en Git y GitHub. | Mantenibilidad |
