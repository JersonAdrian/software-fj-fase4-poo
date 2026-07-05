#-----------------------------------------------------------------------#
# Software de gestión de servicios - FJ
#-----------------------------------------------------------------------#

import logging
 
logging.basicConfig(
    filename="eventos.log",
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
 
# COMMIT 1: Optimización con if/else limpio
def registrar_evento(mensaje, es_error=False):
    if es_error:
        logging.error(mensaje)
    else:
        logging.info(mensaje)

#-----------------------------------------------------------------------#
# Excepciones personalizadas para el software de gestión de servicios
#-----------------------------------------------------------------------#

# Commit 2 (Ya aplicado por Ingrith Toro)
class ErrorSoftwareFJ(Exception):
    """Clase base para los errores del sistema."""
    pass
class ClienteInvalidoError(ErrorSoftwareFJ): pass
class ServicioNoDisponibleError(ErrorSoftwareFJ): pass
class ReservaInvalidaError(ErrorSoftwareFJ): pass
class DatosFaltantesError(ErrorSoftwareFJ): pass

#-----------------------------------------------------------------------#
# Validacion de datos y clases base para el software de gestión de servicios
#-----------------------------------------------------------------------#
from abc import ABC, abstractmethod
 
class EntidadBase(ABC):
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad
    @property
    def id_entidad(self):
        return self._id_entidad
    @abstractmethod
    def describir(self):
        pass

class Cliente(EntidadBase):
    def __init__(self, id_cliente, nombre, email):
        super().__init__(id_cliente)
        self.nombre = nombre   
        self.email = email     
    @property
    def nombre(self): return self._nombre
    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ClienteInvalidoError("El nombre no puede estar vacio.")
        self._nombre = valor
    @property
    def email(self): return self._email
    @email.setter
    def email(self, valor):
        if "@" not in valor or "." not in valor:
            raise ClienteInvalidoError(f"Correo invalido: '{valor}'")
        self._email = valor
    def describir(self):
        return f"Cliente {self.id_entidad}: {self.nombre} ({self.email})"

#-----------------------------------------------------------------------#
# Servicios y sus implementaciones para el software de gestión de servicios
#-----------------------------------------------------------------------#

class Servicio(EntidadBase):
    def __init__(self, id_servicio, nombre_servicio, costo_base):
        super().__init__(id_servicio)
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base
    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass
 
class ReservaSala(Servicio):
    def __init__(self, id_servicio, nombre_servicio, costo_base, capacidad):
        super().__init__(id_servicio, nombre_servicio, costo_base)
        self.capacidad = capacidad
    def calcular_costo(self, horas, descuento=0.0):
        # COMMIT 4: Validar horas mayores a cero y redondear
        if horas <= 0:
            raise ReservaInvalidaError("Las horas deben ser mayores a cero.")
        return round((self.costo_base * horas) * (1 - descuento), 2)
    def describir(self):
        return "Sala " + self.nombre_servicio
 
class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre_servicio, costo_base, valor_seguro):
        super().__init__(id_servicio, nombre_servicio, costo_base)
        self.valor_seguro = valor_seguro
    def calcular_costo(self, dias, aplicar_seguro=False):
        # COMMIT 4: Validar días mayores a cero y redondear
        if dias <= 0:
            raise ReservaInvalidaError("Los dias deben ser mayores a cero.")
        total = self.costo_base * dias
        if aplicar_seguro:
            total = total + self.valor_seguro
        return round(total, 2)
    def describir(self):
        return "Equipo " + self.nombre_servicio
 
class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, nombre_servicio, costo_base, especialidad):
        super().__init__(id_servicio, nombre_servicio, costo_base)
        self.especialidad = especialidad
    def calcular_costo(self, horas, tarifa_urgencia=0.0):
        # COMMIT 4: Validar horas mayores a cero y redondear
        if horas <= 0:
            raise ReservaInvalidaError("Las horas deben ser mayores a cero.")
        total = (self.costo_base * horas) + tarifa_urgencia
        return round(total, 2)
    def describir(self):
        return "Asesoria " + self.especialidad

#-----------------------------------------------------------------------#
# Clases de reserva y excepciones para el software de gestión de servicios
#-----------------------------------------------------------------------#

class Reserva(EntidadBase):
    def __init__(self, id_reserva, cliente, servicio, duracion):
        super().__init__(id_reserva)
        if cliente is None or servicio is None:
            raise DatosFaltantesError("La reserva necesita cliente y servicio.")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        # COMMIT 5: Atributos encapsulados y protegidos
        self._estado = "Pendiente"     
        self._costo_total = 0.0        
 
    @property
    def estado(self): return self._estado
    @property
    def costo_total(self): return self._costo_total

    def procesar_y_confirmar(self, **parametros_extra):
        if self._estado == "Cancelada":
            raise ReservaInvalidaError("No se puede confirmar una reserva cancelada.")
        
        # COMMIT 6 y 7: try/except/else/finally con encadenamiento raise...from
        try:
            self._costo_total = self.servicio.calcular_costo(self.duracion, **parametros_extra)
        except TypeError as error_tecnico:
            raise ReservaInvalidaError("Parametros incompatibles al calcular el costo.") from error_tecnico
        else:
            self._estado = "Confirmada"
            registrar_evento(f"Reserva {self.id_entidad} confirmada. Total: ${self._costo_total}")
        finally:
            registrar_evento(f"Procesamiento de {self.id_entidad} finalizado.")
 
    def cancelar(self):
        if self._estado == "Confirmada":
            self._costo_total = self._costo_total * 0.2
        self._estado = "Cancelada"
 
    def describir(self):
        return "Reserva " + self.id_entidad

#-----------------------------------------------------------------------#
# Simulaciones de casos de prueba para el software de gestión de servicios
#-----------------------------------------------------------------------#

clientes = []
servicios = []
reservas = []
 
# COMMIT 9: Mensajes informativos y mejor legibilidad
print("=" * 60)
print("INICIO DE LAS 10 SIMULACIONES - SOFTWARE FJ")
print("=" * 60)

# COMMIT 8: Envolver ciclo completo en control robusto
for caso in range(1, 11):
    print(f"\n[ Caso #{caso} ]")
    try:
        if caso == 1:
            c = Cliente("C01", "Ingrith Toro", "ingrith@gmail.com")
            clientes.append(c)
            print(f"  OK -> {c.describir()}")
        elif caso == 2:
            c = Cliente("C02", "", "correo")
        elif caso == 3:
            s1 = ReservaSala("S01", "Sala VIP", 50000, 12)
            s2 = AlquilerEquipo("S02", "Proyector", 30000, 15000)
            servicios.append(s1)
            servicios.append(s2)
            print("  OK -> Servicios creados con éxito.")
        elif caso == 4:
            s3 = AsesoriaEspecializada("S03", "Asesoria Ciber", 120000, "Sistemas")
            servicios.append(s3)
            print("  OK -> Asesoría especializada configurada.")
        elif caso == 5:
            r = Reserva("R01", clientes[0], servicios[0], 4)
            r.procesar_y_confirmar(descuento=0.10)
            reservas.append(r)
            print(f"  OK -> Costo reserva total: ${r.costo_total}")
        elif caso == 6:
            r_err = Reserva("R02", clientes[0], servicios[2], -2)
            r_err.procesar_y_confirmar()   
            print(f"  OK -> Horas negativas calculadas: ${r_err.costo_total}")
        elif caso == 7:
            r = reservas[0]
            r.cancelar()
            print(f"  OK -> Reserva cancelada. Penalización: ${r.costo_total}")
        elif caso == 8:
            r = reservas[0]
            r.procesar_y_confirmar() 
            print(f"  OK -> Reconfirmar estado: {r.estado}")
        elif caso == 9:
            r_eq = Reserva("R03", clientes[0], servicios[1], 3)
            r_eq.procesar_y_confirmar(aplicar_seguro=True)
            reservas.append(r_eq)
            print(f"  OK -> Equipo con seguro total: ${r_eq.costo_total}")
        elif caso == 10:
            c_fail = Cliente("C10", "", "correo@fj.com")

    except ErrorSoftwareFJ as e:
        causa = f" | Causa: {e.__cause__}" if e.__cause__ else ""
        msg = f"  FALLA CONTROLADA caso {caso}: {e}{causa}"
        print(msg)
        registrar_evento(msg.strip(), es_error=True)
    except Exception as e:
        print(f"  ERROR INESPERADO caso {caso}: {e}")
    else:
        print(f"  --> Caso {caso} procesado sin excepciones.")
    finally:
        registrar_evento(f"Caso {caso} finalizado. Sistema activo.")

print("\n" + "=" * 60)

# COMMIT 10: Verificación y lectura final del archivo log
try:
    with open("eventos.log", "r", encoding="utf-8") as archivo:
        print("CONTENIDO DE eventos.log:")
        print(archivo.read())
except FileNotFoundError:
    print("Aún no se ha generado el archivo de logs.")

print("=" * 60)
print("FIN DEL PROGRAMA")