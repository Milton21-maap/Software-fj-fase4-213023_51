"""
Módulo de entidades base y modelo Cliente.
Implementa abstracción, encapsulación estricta, validaciones y encadenamiento de excepciones.
"""

from abc import ABC, abstractmethod
from excepciones import DatoInvalidoError, ParametroFaltanteError


class EntidadSistema(ABC):
    """Clase abstracta general que representa cualquier entidad del sistema Software FJ."""

    def __init__(self, identificador: str):
        # Valida que el identificador exista antes de asignarlo
        if not identificador or not str(identificador).strip():
            raise ParametroFaltanteError("El identificador de la entidad es obligatorio.")
        # Atributo privado encapsulado
        self.__identificador = str(identificador).strip()

    @property
    def identificador(self) -> str:
        """Retorna el identificador único de la entidad."""
        return self.__identificador

    @abstractmethod
    def validar(self) -> bool:
        """Método abstracto que obliga a las subclases a validar su estado interno."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto para representar textualmente la entidad."""
        pass


class Cliente(EntidadSistema):
    """Representa un cliente de Software FJ con encapsulación y validaciones estrictas."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        # Inicializa el identificador en la clase abstracta padre
        super().__init__(id_cliente)
        # Inicializa atributos privados mediante sus setters validados
        self.__nombre = ""
        self.__correo = ""
        self.__telefono = ""

        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        """Obtiene el nombre del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre completo del cliente."""
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del cliente no puede estar vacío.")
        if len(str(valor).strip()) < 3:
            raise DatoInvalidoError("El nombre del cliente debe tener al menos 3 caracteres.")
        self.__nombre = str(valor).strip()

    @property
    def correo(self) -> str:
        """Obtiene el correo electrónico del cliente."""
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida estructura básica de correo electrónico antes de asignarlo."""
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El correo electrónico del cliente es obligatorio.")
        correo_limpio = str(valor).strip()
        if "@" not in correo_limpio or "." not in correo_limpio.split("@")[-1]:
            raise DatoInvalidoError(f"El correo '{correo_limpio}' no tiene un formato válido.")
        self.__correo = correo_limpio

    @property
    def telefono(self) -> str:
        """Obtiene el teléfono del cliente."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida que el teléfono sea numérico y usa encadenamiento de excepciones."""
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        telefono_limpio = str(valor).strip()
        try:
            # Intenta convertir a entero para verificar que solo contenga dígitos
            int(telefono_limpio)
        except ValueError as error_conversion:
            # Encadena la excepción original ValueError hacia nuestra excepción de dominio
            raise DatoInvalidoError(
                f"El teléfono '{telefono_limpio}' debe contener únicamente números."
            ) from error_conversion

        if len(telefono_limpio) < 7:
            raise DatoInvalidoError("El teléfono debe tener al menos 7 dígitos.")
        self.__telefono = telefono_limpio

    def validar(self) -> bool:
        """Verifica que todos los atributos del cliente sean consistentes."""
        return bool(self.__nombre and self.__correo and self.__telefono)

    def obtener_resumen(self) -> str:
        """Devuelve la ficha resumida del cliente."""
        return f"Cliente [{self.identificador}] - {self.__nombre} | Correo: {self.__correo}"