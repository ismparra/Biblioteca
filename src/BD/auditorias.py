from BD.connection import consultar, ejecutar

def obtener_auditorias():
    return consultar(
        """
        SELECT * FROM AUDITORIA
        """
    )