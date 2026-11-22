# Software-fj-fase4-213023_51
Proyecto de trabajo colaborativo en python para la Fase 4 de Programación -- Grupo 213023_51
# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto desarrollado para la *Fase 4 – Prácticas simuladas* del curso *Programación (213023)* de la Universidad Nacional Abierta y a Distancia (UNAD) – Grupo 213023_51.

## Arquitectura del Proyecto

El sistema aplica Programación Orientada a Objetos (POO) en Python sin uso de bases de datos, gestionando la información en memoria mediante objetos y listas internas, y registrando toda la actividad y errores en un archivo de logs (eventos_software_fj.log).

* excepciones.py: Jerarquía de excepciones personalizadas (ErrorSoftwareFJ, DatoInvalidoError, ParametroFaltanteError, OperacionNoPermitidaError, ReservaInvalidaError, ServicioNoDisponibleError, CalculoInconsistenteError).
* logger.py: Clase GestorLogs encargada de escribir eventos y errores en archivo plano utilizando bloques try/except/finally.
* modelos.py: Clase abstracta EntidadSistema y clase Cliente con encapsulación (@property), validaciones estrictas, registro directo en logs y encadenamiento de excepciones (raise ... from ...).
* servicios.py: Clase abstracta Servicio, método sobrecargado calcular_costo_total() y tres subclases especializadas (ReservaSala, AlquilerEquipo, AsesoriaEspecializada).
* reservas.py: Clase Reserva con gestión de estados (PENDIENTE, CONFIRMADA, PROCESADA, CANCELADA) y bloques try/except/else y try/except/finally.
* main.py: Ejecución de 12 simulaciones completas (casos válidos e inválidos) que demuestran la estabilidad continua de la aplicación.

## Ejecución

Requiere Python 3.10 o superior (sin dependencias externas):

bash
python main.py


Al finalizar, el sistema genera automáticamente el archivo eventos_software_fj.log con la trazabilidad completa de operaciones y errores capturados.

## Integrantes Participantes

* Milton Arturo Acosta Palomino (@Milton21-maap)
* Carlos Josué Ortiz (@carlosjosueortiz97-beep)
* John Mendez Rangel (manbebe100)
