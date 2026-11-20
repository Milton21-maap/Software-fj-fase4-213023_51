"""
Módulo de excepciones personalizadas para el sistema de Software FJ.
Define una jerarquía clara de errores de negocio para mantener la aplicación estable.
"""


class ErrorSoftwareFJ(Exception):
    """Clase base para todas las excepciones personalizadas del sistema Software FJ."""

    def __init__(self, mensaje: str, codigo_error: str = "ERR-000"):
        # Almacena el mensaje descriptivo del fallo
        self.mensaje = mensaje
        # Almacena un código identificador para facilitar el rastreo en los logs
        self.codigo_error = codigo_error
        # Llama al constructor de la clase base Exception con el formato estándar
        super().__init__(f"[{self.codigo_error}] {self.mensaje}")


class DatoInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando un dato ingresado no cumple con el formato o reglas esperadas."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-DATO-001")


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un argumento obligatorio o llega vacío/nulo."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-PARAM-002")


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta ejecutar una acción inválida según el estado actual."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-OPER-003")


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando los parámetros o condiciones de una reserva son incorrectos."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-RES-004")


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta reservar un servicio inactivo u ocupado."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-SERV-005")


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando un cálculo financiero arroja valores negativos o incoherentes."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-CALC-006")