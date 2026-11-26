-- Reportes
use biblioteca;

-- Reporte 1: libros mas solicitados (los que se han prestado 2 veces o mas)
select l.titulo, l.autor, count(*) as veces_prestado
from libros l join ejemplares e on e.id_libro = l.id_libro join prestamos p on p.id_ejemplar = e.id_ejemplar
group by l.id_libro, l.titulo, l.autor
having count(*) >= 2
order by veces_prestado desc;

-- Reporte 2: alumnos con prestamos vencidos y cuantos dias llevan de atraso
select a.matricula, a.nombre_completo, count(*) as prestamos_vencidos, max(dias_retraso(p.id_prestamo)) as dias_atraso, group_concat(l.titulo separator ', ') as libros
from alumnos a join prestamos p on p.id_alumno = a.id_alumno join ejemplares e on e.id_ejemplar = p.id_ejemplar join libros l on l.id_libro = e.id_libro
where p.fecha_devolucion is null and dias_retraso(p.id_prestamo) > 0
group by a.id_alumno, a.matricula, a.nombre_completo
order by dias_atraso desc;
