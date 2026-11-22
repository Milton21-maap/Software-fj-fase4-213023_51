"""
Archivo principal de ejecución y simulación del Sistema Integral de Software FJ.
Ejecuta 12 operaciones completas (válidas e inválidas) sin bases de datos,
demostrando estabilidad total y registro continuo en el archivo de logs.
"""

from excepciones import ErrorSoftwareFJ
from logger import GestorLogs
from modelos import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import Reserva


class SistemaSoftwareFJ:
    """Controlador en memoria que gestiona listas de clientes, servicios y reservas."""

    def __init__(self):
        # Listas internas en memoria (sin uso de bases de datos)
        self.clientes = []
        self.servicios = []
        self.reservas = []
        # Instancia del gestor de archivos de logs
        self.logger = GestorLogs("eventos_software_fj.log")

    def registrar_cliente(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        """Intenta crear y almacenar un cliente registrando el resultado en el log."""
        try:
            nuevo_cliente = Cliente(id_cliente, nombre, correo, telefono)
        except ErrorSoftwareFJ as error:
            self.logger.registrar("ERROR", "CLIENTES", f"Fallo al registrar cliente: {error}")
            print(f"  [ERROR CONTROLADO] {error}")
            return None
        else:
            self.clientes.append(nuevo_cliente)
            self.logger.registrar("INFO", "CLIENTES", f"Cliente registrado: {nuevo_cliente.obtener_resumen()}")
            print(f"  [OK] {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente

    def registrar_servicio(self, servicio_obj):
        """Almacena un servicio previamente instanciado y registra el evento."""
        if servicio_obj is not None:
            self.servicios.append(servicio_obj)
            self.logger.registrar("INFO", "SERVICIOS", f"Servicio creado: {servicio_obj.describir_servicio()}")
            print(f"  [OK] {servicio_obj.describir_servicio()}")
        return servicio_obj


def ejecutar_simulaciones():
    """Ejecuta 12 operaciones completas demostrando manejo robusto de errores."""
    sistema = SistemaSoftwareFJ()
    sistema.logger.registrar("INFO", "SISTEMA", "=== INICIO DE SIMULACIÓN SOFTWARE FJ ===")
    print("\n=== INICIANDO SIMULACIONES DEL SISTEMA SOFTWARE FJ ===\n")

    # -------------------------------------------------------------------------
    # OPERACIÓN 1: Registro válido de Cliente 1
    # -------------------------------------------------------------------------
    print("Operación 1: Registro válido de cliente (Ana Martínez)")
    cliente_1 = sistema.registrar_cliente("CLI-001", "Ana Martínez", "ana.martinez@correo.com", "3001234567")

    # -------------------------------------------------------------------------
    # OPERACIÓN 2: Registro válido de Cliente 2
    # -------------------------------------------------------------------------
    print("\nOperación 2: Registro válido de cliente (Carlos Gómez)")
    cliente_2 = sistema.registrar_cliente("CLI-002", "Carlos Gómez", "carlos.gomez@empresa.co", "3109876543")

    # -------------------------------------------------------------------------
    # OPERACIÓN 3: Registro inválido de Cliente (correo mal formado)
    # -------------------------------------------------------------------------
    print("\nOperación 3: Registro inválido de cliente (correo sin dominio)")
    sistema.registrar_cliente("CLI-003", "Pedro Pérez", "pedro_sin_arroba.com", "3005554433")

    # -------------------------------------------------------------------------
    # OPERACIÓN 4: Registro inválido de Cliente (teléfono no numérico -> encadenamiento)
    # -------------------------------------------------------------------------
    print("\nOperación 4: Registro inválido de cliente (teléfono con letras)")
    sistema.registrar_cliente("CLI-004", "Laura Díaz", "laura@correo.com", "300ABC99")

    # -------------------------------------------------------------------------
    # OPERACIÓN 5: Creación válida de 3 tipos de Servicios especializados
    # -------------------------------------------------------------------------
    print("\nOperación 5: Creación válida de servicios especializados (Sala, Equipo, Asesoría)")
    sala_1 = None
    equipo_1 = None
    asesoria_1 = None
    try:
        sala_1 = sistema.registrar_servicio(
            ReservaSala("SRV-01", "Sala Innovación", 80000, capacidad=25, horas=4)
        )
        equipo_1 = sistema.registrar_servicio(
            AlquilerEquipo("SRV-02", "Workstation Dell Precision", 45000, cantidad_equipos=3, dias=2)
        )
        asesoria_1 = sistema.registrar_servicio(
            AsesoriaEspecializada("SRV-03", "Arquitectura Cloud", 120000, horas=5, nivel="AVANZADO")
        )
    except ErrorSoftwareFJ as error:
        sistema.logger.registrar("ERROR", "SERVICIOS", str(error))

    # -------------------------------------------------------------------------
    # OPERACIÓN 6: Creación inválida de Servicio (tarifa negativa y nivel inválido)
    # -------------------------------------------------------------------------
    print("\nOperación 6: Creación inválida de servicios (tarifa negativa y nivel erróneo)")
    try:
        ReservaSala("SRV-ERR1", "Sala Fantasma", -50000, capacidad=10, horas=2)
    except ErrorSoftwareFJ as error:
        sistema.logger.registrar("ERROR", "SERVICIOS", f"Error creando sala: {error}")
        print(f"  [ERROR CONTROLADO] {error}")

    try:
        AsesoriaEspecializada("SRV-ERR2", "Asesoría IA", 90000, horas=3, nivel="EXPERTO_SUPREMO")
    except ErrorSoftwareFJ as error:
        sistema.logger.registrar("ERROR", "SERVICIOS", f"Error creando asesoría: {error}")
        print(f"  [ERROR CONTROLADO] {error}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 7: Prueba de métodos sobrecargados de cálculo de costos
    # -------------------------------------------------------------------------
    print("\nOperación 7: Cálculo de costos sobrecargado (estándar, con descuento y con cargo extra)")
    try:
        costo_estandar = sala_1.calcular_costo_total()
        costo_descuento = sala_1.calcular_costo_total(impuesto=0.19, descuento=0.10)
        costo_completo = sala_1.calcular_costo_total(impuesto=0.19, descuento=0.10, cargo_adicional=25000)
        msg = (
            f"Costos Sala -> Estándar: ${costo_estandar:,.2f} | "
            f"Con 10% desc.: ${costo_descuento:,.2f} | Con cargo extra: ${costo_completo:,.2f}"
        )
        sistema.logger.registrar("INFO", "COSTOS", msg)
        print(f"  [OK] {msg}")
    except ErrorSoftwareFJ as error:
        sistema.logger.registrar("ERROR", "COSTOS", str(error))

    # -------------------------------------------------------------------------
    # OPERACIÓN 8: Reserva exitosa completa (Crear -> Confirmar -> Procesar)
    # -------------------------------------------------------------------------
    print("\nOperación 8: Flujo completo exitoso de Reserva RES-001")
    reserva_1 = None
    try:
        reserva_1 = Reserva("RES-001", cliente_1, sala_1, duracion=4)
        reserva_1.confirmar()
        total_pagado = reserva_1.procesar(impuesto=0.19, descuento=0.05)
        sistema.reservas.append(reserva_1)
        sistema.logger.registrar("INFO", "RESERVAS", f"Reserva procesada: {reserva_1.obtener_resumen()}")
        print(f"  [OK] {reserva_1.obtener_resumen()} (Cobrado: ${total_pagado:,.2f})")
    except ErrorSoftwareFJ as error:
        sistema.logger.registrar("ERROR", "RESERVAS", str(error))

    # -------------------------------------------------------------------------
    # OPERACIÓN 9: Reserva fallida por servicio no disponible (ya ocupado en RES-001)
    # -------------------------------------------------------------------------
    print("\nOperación 9: Intento de reservar un servicio ya ocupado (Sala Innovación)")
    try:
        Reserva("RES-002", cliente_2, sala_1, duracion=2)
    except ErrorSoftwareFJ as error:
        sistema.logger.registrar("ERROR", "RESERVAS", f"Reserva rechazada: {error}")
        print(f"  [ERROR CONTROLADO] {error}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 10: Reserva fallida por duración inválida y cliente nulo
    # -------------------------------------------------------------------------
    print("\nOperación 10: Intento de reserva con duración inválida (0 horas)")
    try:
        Reserva("RES-003", cliente_2, equipo_1, duracion=0)
    except ErrorSoftwareFJ as error:
        sistema.logger.registrar("ERROR", "RESERVAS", f"Parámetros inválidos en reserva: {error}")
        print(f"  [ERROR CONTROLADO] {error}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 11: Cálculo inconsistente encadenado al procesar reserva
    # -------------------------------------------------------------------------
    print("\nOperación 11: Fallo controlado por descuento inconsistente (>100%) al procesar reserva")
    reserva_2 = None
    try:
        reserva_2 = Reserva("RES-004", cliente_2, equipo_1, duracion=2)
        reserva_2.confirmar()
        # Intenta aplicar un descuento imposible del 150% (1.5)
        reserva_2.procesar(impuesto=0.19, descuento=1.5)
    except ErrorSoftwareFJ as error:
        sistema.logger.registrar("ERROR", "RESERVAS", f"Error de cálculo encadenado: {error} | Causa: {error.__cause__}")
        print(f"  [ERROR CONTROLADO] {error} -> Causa original: {error.__cause__}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 12: Cancelación válida de reserva pendiente/confirmada vs cancelación inválida
    # -------------------------------------------------------------------------
    print("\nOperación 12: Cancelación válida de RES-004 y rechazo de cancelación de RES-001 (ya procesada)")
    try:
        # Cancelar RES-004 (que quedó en estado CONFIRMADA tras fallar su cobro) debe funcionar y liberar equipo_1
        reserva_2.cancelar()
        sistema.reservas.append(reserva_2)
        sistema.logger.registrar("INFO", "RESERVAS", f"Reserva cancelada correctamente: {reserva_2.obtener_resumen()}")
        print(f"  [OK] {reserva_2.obtener_resumen()} | Equipo disponible nuevamente: {equipo_1.disponible}")

        # Intentar cancelar RES-001 (ya PROCESADA) debe lanzar OperacionNoPermitidaError
        reserva_1.cancelar()
    except ErrorSoftwareFJ as error:
        sistema.logger.registrar("ERROR", "RESERVAS", f"Operación bloqueada: {error}")
        print(f"  [ERROR CONTROLADO] {error}")

    sistema.logger.registrar("INFO", "SISTEMA", "=== FIN DE SIMULACIÓN SOFTWARE FJ (SISTEMA ESTABLE) ===")
    print("\n=== SIMULACIÓN FINALIZADA SIN INTERRUPCIONES. REVISA 'eventos_software_fj.log' ===\n")


if __name__ == "__main__":
    ejecutar_simulaciones()