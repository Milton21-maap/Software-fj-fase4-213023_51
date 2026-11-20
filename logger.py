"""
Módulo de registro de eventos y errores en archivo plano.
Cumple con la restricción de no usar bases de datos y registrar toda la actividad en logs.
"""

from datetime import datetime


class GestorLogs:
    """Administra la escritura segura de eventos y errores en un archivo de texto."""

    def __init__(self, ruta_archivo: str = "eventos_software_fj.log"):
        # Define la ruta del archivo donde se almacenarán los registros
        self.__ruta_archivo = ruta_archivo

    def registrar(self, nivel: str, origen: str, mensaje: str) -> None:
        """
        Escribe una línea de registro en el archivo de logs usando try/except/finally.
        """
        # Obtiene la marca de tiempo actual en formato legible
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Construye la línea estructurada del evento
        linea_log = f"[{marca_tiempo}] [{nivel.upper()}] [{origen}] {mensaje}\n"
        archivo = None

        try:
            # Abre el archivo en modo anexar ('a') con codificación UTF-8
            archivo = open(self.__ruta_archivo, mode="a", encoding="utf-8")
            # Escribe la línea de registro en el archivo
            archivo.write(linea_log)
        except OSError as error_io:
            # Si ocurre un problema de escritura en disco, lo informa sin detener el programa
            print(f"[FALLO CRÍTICO DE LOG] No se pudo escribir en el archivo: {error_io}")
        finally:
            # Garantiza el cierre del recurso de archivo sin importar si hubo error o no
            if archivo is not None and not archivo.closed:
                archivo.close()