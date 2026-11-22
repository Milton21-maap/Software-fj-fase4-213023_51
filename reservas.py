"""
Módulo de gestión de reservas de Software FJ.
Integra Cliente, Servicio, duración y estado, aplicando bloques try/except/else y try/except/finally.
"""

from modelos import EntidadSistema, Cliente
from servicios import Servicio
from excepciones import (
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    ErrorSoftwareFJ,
)


class Reserva(EntidadSistema):
    """Gestiona el ciclo de vida de una reserva (PENDIENTE -> CONFIRMADA -> PROCESADA / CANCELADA)."""

    def __init__(self, codigo_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        super().__init__(codigo_reserva)

        # Valida que se reciban instancias válidas de Cliente y Servicio
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere una instancia válida de Servicio.")
        if duracion is None or duracion <= 0:
            raise ReservaInvalidaError("La duración de la reserva debe ser mayor a cero.")

        # Verifica disponibilidad antes de crear la reserva
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre_servicio}' ({servicio.identificador}) no está disponible."
            )

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = int(duracion)
        self.__estado = "PENDIENTE"
        self.__valor_total = 0.0

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def valor_total(self) -> float:
        return self.__valor_total

    def confirmar(self) -> None:
        """
        Confirma la reserva usando try/except/finally y bloquea la disponibilidad del servicio.
        """
        verificacion_completada = False
        try:
            if self.__estado != "PENDIENTE":
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar la reserva {self.identificador} porque está en estado '{self.__estado}'."
                )
            if not self.__servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self.__servicio.nombre_servicio}' ya fue ocupado por otra reserva."
                )
            # Cambia el estado y marca el servicio como ocupado
            self.__estado = "CONFIRMADA"
            self.__servicio.disponible = False
            verificacion_completada = True
        except ErrorSoftwareFJ:
            # Propaga la excepción controlada hacia el llamador para su registro en el log
            raise
        finally:
            # Bloque finally que deja traza interna de auditoría de intento de confirmación
            if not verificacion_completada and self.__estado == "PENDIENTE":
                self.__estado = "PENDIENTE"

    def procesar(self, impuesto: float = 0.19, descuento: float = 0.0, cargo_adicional: float = 0.0) -> float:
        """
        Procesa el cobro final de la reserva usando try/except/else y encadenamiento de excepciones.
        """
        if self.__estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"La reserva {self.identificador} debe estar CONFIRMADA antes de procesarse (actual: {self.__estado})."
            )

        try:
            # Utiliza el método sobrecargado del servicio para calcular el valor total
            monto = self.__servicio.calcular_costo_total(
                impuesto=impuesto,
                descuento=descuento,
                cargo_adicional=cargo_adicional,
            )
        except ErrorSoftwareFJ as error_calculo:
            # Encadena la excepción de cálculo dentro de una ReservaInvalidaError
            raise ReservaInvalidaError(
                f"Fallo al procesar el cobro de la reserva {self.identificador}."
            ) from error_calculo
        else:
            # Solo se ejecuta si el cálculo no lanzó ninguna excepción
            self.__valor_total = monto
            self.__estado = "PROCESADA"
            return self.__valor_total

    def cancelar(self) -> None:
        """
        Cancela la reserva si aún no ha sido procesada y libera el servicio.
        """
        if self.__estado == "PROCESADA":
            raise OperacionNoPermitidaError(
                f"No es posible cancelar la reserva {self.identificador} porque ya fue PROCESADA."
            )
        if self.__estado == "CANCELADA":
            raise OperacionNoPermitidaError(
                f"La reserva {self.identificador} ya se encuentra CANCELADA."
            )

        self.__estado = "CANCELADA"
        # Libera nuevamente el servicio para futuros clientes
        self.__servicio.disponible = True

    def validar(self) -> bool:
        return self.__cliente.validar() and self.__servicio.validar() and self.__duracion > 0

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.identificador}] | Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre_servicio} | Duración: {self.__duracion} | "
            f"Estado: {self.__estado} | Total: ${self.__valor_total:,.2f}"
        )