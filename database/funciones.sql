-- Funcion 1: cuantos ejemplares disponibles tiene un libro
use biblioteca;
delimiter $$
create function ejemplares_disponibles(p_libro int) returns int reads sql data
begin
	declare cantidad int;
	select count(*) into cantidad from ejemplares where id_libro = p_libro and estado = 'disponible';
	return cantidad;
end $$
delimiter ;


-- Funcion 2: dias de retraso de un prestamo (-1 si no existe)
delimiter $$
create function dias_retraso(p_prestamo int) returns int reads sql data
begin
	declare existe boolean default true;
	declare v_fecha_limite date;
	declare v_fecha_devolucion datetime;
	declare dias int;
	declare continue handler for not found set existe = false;
	select fecha_limite, fecha_devolucion into v_fecha_limite, v_fecha_devolucion from prestamos where id_prestamo = p_prestamo;
	if existe = false then
		return -1;
	end if;
	-- si todavia no lo devuelven se cuenta hasta hoy
	set dias = datediff(ifnull(v_fecha_devolucion, curdate()), v_fecha_limite);
	if dias < 0 then
		return 0;
	end if;
	return dias;
end $$
delimiter ;
