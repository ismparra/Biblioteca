-- Transaccion 1: registrar prestamo
use biblioteca;
delimiter $$
create procedure registrar_prestamo(in p_matricula varchar(30), in p_codigo varchar(50), in p_bibliotecario int, in p_fecha_limite date)
begin
	declare v_alumno int;
	declare v_ejemplar int;
	declare v_estado varchar(20);
	-- si algo truena se hace rollback y el error le llega a la app
	declare exit handler for sqlexception
	begin
		rollback;
		resignal;
	end;

start transaction;
select id_alumno into v_alumno from alumnos where matricula = p_matricula and estado = 'activo' for update;
-- el for update es para que no se preste el mismo ejemplar dos veces
select id_ejemplar, estado into v_ejemplar, v_estado from ejemplares where codigo_barras = p_codigo for update;
if v_alumno is null then
	signal sqlstate '45000' set message_text = 'El alumno no existe o esta suspendido';
end if;
if v_ejemplar is null then
	signal sqlstate '45000' set message_text = 'No existe un ejemplar con ese codigo de barras';
end if;
if v_estado != 'disponible' then
	signal sqlstate '45000' set message_text = 'El ejemplar ya esta prestado';
end if;
if not exists (select 1 from bibliotecarios where id_bibliotecario = p_bibliotecario and estado = 'activo' and rol in ('administrador','operador')) then
	signal sqlstate '45000' set message_text = 'El usuario no tiene permiso para registrar prestamos';
end if;
if p_fecha_limite is null or p_fecha_limite < curdate() then
	signal sqlstate '45000' set message_text = 'La fecha limite no es valida';
end if;
insert into prestamos(id_alumno, id_ejemplar, id_bibliotecario, fecha_limite) values(v_alumno, v_ejemplar, p_bibliotecario, p_fecha_limite);
update ejemplares set estado = 'prestado' where id_ejemplar = v_ejemplar;
commit;
end $$
delimiter ;


-- Transaccion 2: registrar devolucion
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
-- si fecha_devolucion es null es que aun no lo devuelven
select id_prestamo into v_prestamo from prestamos where id_ejemplar = v_ejemplar and fecha_devolucion is null for update;
if v_prestamo is null then
	signal sqlstate '45000' set message_text = 'El ejemplar no tiene un prestamo activo';
end if;
update prestamos set fecha_devolucion = now() where id_prestamo = v_prestamo;
update ejemplares set estado = 'disponible' where id_ejemplar = v_ejemplar;
commit;
end $$
delimiter ;


-- Transaccion 3: eliminar un libro y sus ejemplares
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
-- si ya tiene prestamos no se borra para no perder el historial
if exists (select 1 from prestamos p join ejemplares e on e.id_ejemplar = p.id_ejemplar where e.id_libro = p_libro) then
	signal sqlstate '45000' set message_text = 'No se puede eliminar: el libro tiene prestamos registrados';
end if;
delete from ejemplares where id_libro = p_libro;
delete from libros where id_libro = p_libro;
commit;
end $$
delimiter ;


-- Procedimiento 4: datos de un alumno con su matricula
delimiter $$
create procedure consultar_alumno(in p_matricula varchar(30), out p_nombre varchar(100), out p_activos int, out p_vencidos int)
begin
if exists (select 1 from alumnos where matricula = p_matricula) then
	set p_nombre = (select nombre_completo from alumnos where matricula = p_matricula);
	set p_activos = (select count(*) from prestamos p join alumnos a on a.id_alumno = p.id_alumno where a.matricula = p_matricula and p.fecha_devolucion is null);
	set p_vencidos = (select count(*) from prestamos p join alumnos a on a.id_alumno = p.id_alumno where a.matricula = p_matricula and p.fecha_devolucion is null and dias_retraso(p.id_prestamo) > 0);
else
	-- si no existe el alumno se mandan ceros
	set p_nombre = 'Alumno no encontrado';
	set p_activos = 0;
	set p_vencidos = 0;
end if;
end $$
delimiter ;


-- Procedimiento 5: iniciar sesion
delimiter $$
create procedure iniciar_sesion(in p_usuario varchar(50), in p_password varchar(100))
begin
-- se hashea lo que escribio y se compara con lo guardado, si no coincide no regresa nada
-- se esta usando una sal para que dos usuarios con la misma contraseña no tengan el mismo hash, y se evita que alguien pueda usar un diccionario de hashes para adivinar la contraseña
select id_bibliotecario, nombre_completo, usuario, rol, estado from bibliotecarios where usuario = p_usuario and password_hash = sha2(concat(usuario, p_password), 256);
end $$
delimiter ;


-- Procedimiento 6: registrar un usuario
delimiter $$
create procedure registrar_usuario(in p_nombre varchar(100), in p_usuario varchar(50), in p_password varchar(100), in p_rol varchar(20))
begin
-- la contraseña se hashea igual que en iniciar_sesion
insert into bibliotecarios values(default, p_nombre, p_usuario, sha2(concat(p_usuario, p_password), 256), p_rol, 'activo');
end $$
delimiter ;


-- Procedimiento 7: actualizar un usuario
delimiter $$
create procedure actualizar_usuario(in p_id int, in p_nombre varchar(100), in p_usuario varchar(50), in p_password varchar(100), in p_rol varchar(20))
begin
	declare v_usuario varchar(50);
	set v_usuario = (select usuario from bibliotecarios where id_bibliotecario = p_id);
	if v_usuario is null then
		signal sqlstate '45000' set message_text = 'El usuario no existe';
	end if;
	-- el hash usa el nombre de usuario como sal, si cambia hay que capturar la contraseña otra vez
	if binary v_usuario != binary p_usuario and ifnull(p_password, '') = '' then
		signal sqlstate '45000' set message_text = 'Si cambias el nombre de usuario debes escribir una contraseña';
	end if;
	-- si la contraseña viene vacia se conserva la anterior
	update bibliotecarios set nombre_completo = p_nombre, usuario = p_usuario, rol = p_rol,
		password_hash = if(ifnull(p_password, '') = '', password_hash, sha2(concat(p_usuario, p_password), 256))
	where id_bibliotecario = p_id;
end $$
delimiter ;


-- Procedimiento 8: eliminar un usuario
delimiter $$
create procedure eliminar_usuario(in p_id int)
begin
	declare v_id int;
	declare exit handler for sqlexception
	begin
		rollback;
		resignal;
	end;

start transaction;
select id_bibliotecario into v_id from bibliotecarios where id_bibliotecario = p_id for update;
if v_id is null then
	signal sqlstate '45000' set message_text = 'El usuario no existe';
end if;
-- si ya registro prestamos no se borra para no perder el historial
if exists (select 1 from prestamos where id_bibliotecario = p_id) then
	signal sqlstate '45000' set message_text = 'No se puede eliminar: el usuario tiene prestamos registrados';
end if;
delete from bibliotecarios where id_bibliotecario = p_id;
commit;
end $$
delimiter ;


-- Procedimiento 9: eliminar un alumno
delimiter $$
create procedure eliminar_alumno(in p_id int)
begin
	declare v_id int;
	declare exit handler for sqlexception
	begin
		rollback;
		resignal;
	end;

start transaction;
select id_alumno into v_id from alumnos where id_alumno = p_id for update;
if v_id is null then
	signal sqlstate '45000' set message_text = 'El alumno no existe';
end if;
-- si ya tiene prestamos no se borra para no perder el historial
if exists (select 1 from prestamos where id_alumno = p_id) then
	signal sqlstate '45000' set message_text = 'No se puede eliminar: el alumno tiene prestamos registrados';
end if;
delete from alumnos where id_alumno = p_id;
commit;
end $$
delimiter ;
