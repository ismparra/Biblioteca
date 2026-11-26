-- datos de prueba, correr solo una vez con la base vacia
use biblioteca;
-- las contraseñas se guardan con sha2, se le pega el usuario para que dos contraseñas iguales no den el mismo hash
-- es decir, se esta usando una sal para que dos usuarios con la misma contraseña no tengan el mismo hash, y se evita que alguien pueda usar un diccionario de hashes para adivinar la contraseña
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

-- este se devolvio a tiempo
insert into prestamos values(1,1,1,2, now() - interval 30 day, curdate() - interval 23 day, now() - interval 25 day);
-- este se devolvio tarde
insert into prestamos values(2,2,3,2, now() - interval 20 day, curdate() - interval 13 day, now() - interval 10 day);
-- este esta vencido y no lo han devuelto
insert into prestamos values(3,1,4,2, now() - interval 10 day, curdate() - interval 3 day, null);
update ejemplares set estado = 'prestado' where id_ejemplar = 4;


-- pruebas de las funciones
select id_libro, titulo, autor, ejemplares_disponibles(id_libro) as disponibles from libros;
select id_prestamo, fecha_limite, fecha_devolucion, dias_retraso(id_prestamo) as retraso from prestamos;
-- prestamo que no existe
select dias_retraso(100000000);


-- pruebas de los procedimientos
-- este prestamo si se puede
call registrar_prestamo('A002','7501000000011',2, date_add(curdate(), interval 7 day));
select * from prestamos;
select * from ejemplares;
-- alumno con un prestamo vencido
call consultar_alumno('A001', @nombre, @activos, @vencidos);
select @nombre, @activos, @vencidos;
-- alumno que no existe
call consultar_alumno('IPC', @nombre, @activos, @vencidos);
select @nombre, @activos, @vencidos;
-- devolucion que si se puede
call registrar_devolucion('7501000000011');
select * from prestamos;
select * from ejemplares;
-- este libro no tiene prestamos asi que se puede borrar
call eliminar_libro(5);
select * from libros;


-- login correcto
call iniciar_sesion('admin','admin123');
-- contraseña incorrecta, no regresa nada
call iniciar_sesion('admin','1234');
-- usuario que no existe, no regresa nada
call iniciar_sesion('IPC','admin123');


-- registrar un usuario y entrar con el
call registrar_usuario('Rosa Diaz','rosa','rosa123','operador');
call iniciar_sesion('rosa','rosa123');


-- ver lo que guardaron los triggers de auditoria
select * from auditoria;


-- estos deben marcar error
-- correrlos de uno en uno porque con el error se detiene el script

-- alumno suspendido
call registrar_prestamo('A004','7501000000028',2, date_add(curdate(), interval 7 day));
-- codigo de barras que no existe
call registrar_prestamo('A002','0000000000000',2, date_add(curdate(), interval 7 day));
-- ejemplar ya prestado
call registrar_prestamo('A002','7501000000042',2, date_add(curdate(), interval 7 day));
-- usuario sin permiso
call registrar_prestamo('A002','7501000000028',3, date_add(curdate(), interval 7 day));
-- fecha limite que ya paso
call registrar_prestamo('A002','7501000000028',2,'2000-01-01');

-- devolver algo que no esta prestado
call registrar_devolucion('7501000000028');
-- devolver un codigo que no existe
call registrar_devolucion('0000000000000');

-- borrar un libro con prestamos
call eliminar_libro(1);
-- borrar un libro que no existe
call eliminar_libro(100000000);

-- usuario repetido
call registrar_usuario('Otro Admin','admin','1234','administrador');

-- trigger: alumno suspendido
insert into prestamos(id_alumno, id_ejemplar, id_bibliotecario, fecha_limite) values(4,2,2,curdate());
-- trigger: ejemplar no disponible
insert into prestamos(id_alumno, id_ejemplar, id_bibliotecario, fecha_limite) values(2,4,2,curdate());
-- trigger: fecha limite antes del prestamo
insert into prestamos(id_alumno, id_ejemplar, id_bibliotecario, fecha_limite) values(2,2,2,'2000-01-01');

-- trigger: codigo vacio
insert into ejemplares values(default,'  ',1,'disponible');
-- trigger: ejemplar nuevo como prestado
insert into ejemplares values(default,'7501000000080',1,'prestado');
