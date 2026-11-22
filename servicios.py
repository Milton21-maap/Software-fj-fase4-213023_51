"""
Módulo de servicios ofrecidos por Software FJ.
Implementa clase abstracta Servicio, herencia, polimorfismo y métodos sobrecargados.
"""

from abc import abstractmethod
from modelos import EntidadSistema
from excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    CalculoInconsistenteError,
)


class Servicio(EntidadSistema):
    """Clase abstracta base para todos los servicios de Software FJ."""

    def __init__(self, codigo: str, nombre_servicio: str, tarifa_base: float, disponible: bool = True):
        super().__init__(codigo)
        if not nombre_servicio or not str(nombre_servicio).strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if tarifa_base is None or tarifa_base <= 0:
            raise DatoInvalidoError("La tarifa base del servicio debe ser mayor a cero.")

        self.__nombre_servicio = str(nombre_servicio).strip()
        self.__tarifa_base = float(tarifa_base)
        self.__disponible = bool(disponible)

    @property
    def nombre_servicio(self) -> str:
        return self.__nombre_servicio

    @property
    def tarifa_base(self) -> float:
        return self.__tarifa_base

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        self.__disponible = bool(estado)

    @abstractmethod
    def calcular_costo(self) -> float:
        """Método polimórfico que cada subclase implementa según su lógica de negocio."""
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Método polimórfico que detalla las características específicas del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self) -> bool:
        """Método polimórfico que valida las reglas propias de cada servicio."""
        pass

    def calcular_costo_total(
        self,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        cargo_adicional: float = 0.0,
    ) -> float:
        """
        Método sobrecargado mediante parámetros opcionales para calcular costos con:
        - Solo impuesto por defecto (19%)
        - Impuesto + descuento promocional
        - Impuesto + descuento + cargos adicionales operativos
        """
        if impuesto < 0 or impuesto > 1:
            raise CalculoInconsistenteError("El impuesto debe estar entre 0.0 y 1.0 (0% a 100%).")
        if descuento < 0 or descuento >= 1:
            raise CalculoInconsistenteError("El descuento debe ser mayor o igual a 0 y menor al 100%.")
        if cargo_adicional < 0:
            raise CalculoInconsistenteError("El cargo adicional no puede ser negativo.")

        costo_base = self.calcular_costo()
        subtotal_con_descuento = costo_base * (1 - descuento)
        total = subtotal_con_descuento * (1 + impuesto) + cargo_adicional

        if total <= 0:
            raise CalculoInconsistenteError("El cálculo final del servicio arrojó un valor inválido (<= 0).")

        return round(total, 2)

    def validar(self) -> bool:
        return self.__tarifa_base > 0 and self.validar_parametros()

    def obtener_resumen(self) -> str:
        estado_texto = "Disponible" if self.__disponible else "No disponible"
        return f"[{self.identificador}] {self.__nombre_servicio} ({estado_texto}) - Base: ${self.__tarifa_base:,.2f}"


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas tecnológicas y de reuniones."""

    def __init__(self, codigo: str, nombre_sala: str, tarifa_hora: float, capacidad: int, horas: int, disponible: bool = True):
        super().__init__(codigo, nombre_sala, tarifa_hora, disponible)
        self.__capacidad = capacidad
        self.__horas = horas
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        if self.__capacidad <= 0 or self.__capacidad > 100:
            raise DatoInvalidoError("La capacidad de la sala debe estar entre 1 y 100 personas.")
        if self.__horas <= 0:
            raise DatoInvalidoError("Las horas de reserva de sala deben ser mayores a cero.")
        return True

    def calcular_costo(self) -> float:
        recargo_capacidad = 1.15 if self.__capacidad > 20 else 1.0
        return round(self.tarifa_base * self.__horas * recargo_capacidad, 2)

    def describir_servicio(self) -> str:
        return f"Sala '{self.nombre_servicio}' | Capacidad: {self.__capacidad} pers. | Duración: {self.__horas}h"


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos de cómputo y hardware."""

    def __init__(self, codigo: str, nombre_equipo: str, tarifa_dia: float, cantidad_equipos: int, dias: int, disponible: bool = True):
        super().__init__(codigo, nombre_equipo, tarifa_dia, disponible)
        self.__cantidad_equipos = cantidad_equipos
        self.__dias = dias
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        if self.__cantidad_equipos <= 0:
            raise DatoInvalidoError("La cantidad de equipos a alquilar debe ser al menos 1.")
        if self.__dias <= 0:
            raise DatoInvalidoError("Los días de alquiler deben ser mayores a cero.")
        return True

    def calcular_costo(self) -> float:
        return round(self.tarifa_base * self.__cantidad_equipos * self.__dias, 2)

    def describir_servicio(self) -> str:
        return f"Alquiler '{self.nombre_servicio}' | Equipos: {self.__cantidad_equipos} | Días: {self.__dias}"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para consultoría y asesoría técnica."""

    NIVELES_VALIDOS = {"BASICO": 1.0, "INTERMEDIO": 1.25, "AVANZADO": 1.5}

    def __init__(self, codigo: str, tema_asesoria: str, tarifa_hora: float, horas: int, nivel: str = "BASICO", disponible: bool = True):
        super().__init__(codigo, tema_asesoria, tarifa_hora, disponible)
        self.__horas = horas
        self.__nivel = str(nivel).strip().upper() if nivel else ""
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        if self.__horas <= 0:
            raise DatoInvalidoError("Las horas de asesoría deben ser mayores a cero.")
        if self.__nivel not in self.NIVELES_VALIDOS:
            raise DatoInvalidoError(
                f"Nivel de asesoría '{self.__nivel}' inválido. Use: {list(self.NIVELES_VALIDOS.keys())}"
            )
        return True

    def calcular_costo(self) -> float:
        multiplicador = self.NIVELES_VALIDOS[self.__nivel]
        return round(self.tarifa_base * self.__horas * multiplicador, 2)

    def describir_servicio(self) -> str:
        return f"Asesoría '{self.nombre_servicio}' | Nivel: {self.__nivel} | Horas: {self.__horas}"
