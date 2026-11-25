-- Triggers de validacion

-- Trigger 1: revisar el prestamo antes de insertarlo
use biblioteca;
delimiter $$
create trigger validar_prestamo before insert on prestamos
for each row
begin
if not exists (select 1 from alumnos where id_alumno = new.id_alumno and estado = 'activo') then
	signal sqlstate '45000' set message_text = 'El alumno no existe o esta suspendido';
end if;
if not exists (select 1 from ejemplares where id_ejemplar = new.id_ejemplar and estado = 'disponible') then
	signal sqlstate '45000' set message_text = 'El ejemplar no esta disponible';
end if;
if new.fecha_limite < date(new.fecha_prestamo) then
	signal sqlstate '45000' set message_text = 'La fecha limite no puede ser anterior a la fecha del prestamo';
end if;
end $$
delimiter ;


-- Trigger 2: revisar el ejemplar antes de insertarlo
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


-- Triggers de auditoria
-- use user() porque current_user() aqui da el usuario que creo el trigger

-- Trigger 3: guardar en auditoria cada prestamo
delimiter $$
create trigger auditar_prestamo after insert on prestamos
for each row
begin
	insert into auditoria values(default, 'prestamos', 'INSERT', now(), user(), null,
	concat('id_prestamo: ', new.id_prestamo, ', id_alumno: ', new.id_alumno, ', id_ejemplar: ', new.id_ejemplar, ', id_bibliotecario: ', new.id_bibliotecario, ', fecha_limite: ', new.fecha_limite));
end $$
delimiter ;

-- Trigger 4: guardar en auditoria cada devolucion
delimiter $$
create trigger auditar_devolucion after update on prestamos
for each row
begin
if not (new.fecha_devolucion <=> old.fecha_devolucion) then
	insert into auditoria values(default, 'prestamos', 'UPDATE', now(), user(),
	concat('id_prestamo: ', old.id_prestamo, ', fecha_devolucion: ', ifnull(old.fecha_devolucion, 'sin devolver')),
	concat('id_prestamo: ', new.id_prestamo, ', fecha_devolucion: ', ifnull(new.fecha_devolucion, 'sin devolver')));
end if;
end $$
delimiter ;
