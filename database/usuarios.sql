-- Usuarios y roles
use biblioteca;

-- Roles
create role 'rol_administrador', 'rol_operador', 'rol_consulta';

-- el admin maneja usuarios, alumnos, libros y puede ver la auditoria
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
grant execute on function biblioteca.ejemplares_disponibles to 'rol_administrador';
grant execute on function biblioteca.dias_retraso to 'rol_administrador';

-- el operador hace prestamos y devoluciones (solo con los procedimientos)
grant select on biblioteca.alumnos to 'rol_operador';
grant select on biblioteca.libros to 'rol_operador';
grant select on biblioteca.ejemplares to 'rol_operador';
grant select on biblioteca.prestamos to 'rol_operador';
grant execute on procedure biblioteca.registrar_prestamo to 'rol_operador';
grant execute on procedure biblioteca.registrar_devolucion to 'rol_operador';
grant execute on procedure biblioteca.consultar_alumno to 'rol_operador';
grant execute on function biblioteca.ejemplares_disponibles to 'rol_operador';
grant execute on function biblioteca.dias_retraso to 'rol_operador';

-- consulta nada mas ve libros y si hay disponibles
grant select on biblioteca.libros to 'rol_consulta';
grant select on biblioteca.ejemplares to 'rol_consulta';
grant execute on function biblioteca.ejemplares_disponibles to 'rol_consulta';

-- Usuarios
create user 'bib_admin'@'localhost' identified by 'Admin123!';
create user 'bib_operador'@'localhost' identified by 'Operador123!';
create user 'bib_consulta'@'localhost' identified by 'Consulta123!';
-- este usuario es solo para el login de la app
-- esta pensado para cuando aun no ha hecho login ningun usuario y se quiere verificar que el usuario y contraseña son correctos cuando se hace login en la app
create user 'bib_login'@'localhost' identified by 'Login123!';
grant execute on procedure biblioteca.iniciar_sesion to 'bib_login'@'localhost';

-- Asignar los roles
grant 'rol_administrador' to 'bib_admin'@'localhost';
grant 'rol_operador' to 'bib_operador'@'localhost';
grant 'rol_consulta' to 'bib_consulta'@'localhost';

-- si no se pone esto el rol no se activa al entrar
set default role 'rol_administrador' to 'bib_admin'@'localhost';
set default role 'rol_operador' to 'bib_operador'@'localhost';
set default role 'rol_consulta' to 'bib_consulta'@'localhost';
