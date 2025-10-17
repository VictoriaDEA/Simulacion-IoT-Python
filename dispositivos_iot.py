# ============================================================
# Archivo: dispositivos_iot.py
# Autor: Victoria De Abreu PiRES
# ============================================================

from __future__ import annotations  # Para anotaciones de tipos hacia adelante
import random
import time
from typing import List

# ------------------------------------------------------------
# Clase base: DispositivoIoT
# ------------------------------------------------------------
class DispositivoIoT:
    """
    Clase base abstracta (no estrictamente abstracta, pero pensada para heredar)
    que modela el comportamiento común de cualquier dispositivo IoT.

    Atributos privados:
        __id_dispositivo (str): Identificador único legible para el usuario.
        __estado (bool): True si el dispositivo está encendido, False si está apagado.

    Encapsulamiento:
        - Ambos atributos son privados (doble guión bajo __).
        - Se exponen a través de propiedades de solo lectura o métodos específicos.
    """

    def __init__(self, id_dispositivo: str) -> None:
        # Guardamos el ID en un atributo privado para evitar accesos directos externos
        self.__id_dispositivo: str = id_dispositivo
        # Por diseño, todo dispositivo inicia apagado para evitar acciones no controladas
        self.__estado: bool = False

    # ---------- Propiedades (getters) ----------
    @property
    def id_dispositivo(self) -> str:
        """Devuelve el identificador del dispositivo (solo lectura)."""
        return self.__id_dispositivo

    @property
    def estado(self) -> bool:
        """Devuelve el estado del dispositivo (True=encendido, False=apagado)."""
        return self.__estado


    # ---------- Métodos de control ----------
    def encender(self) -> None:
        """Cambia el estado interno a encendido."""
        self.__estado = True
        print(f"[INFO] {self.__id_dispositivo} encendido.")

    def apagar(self) -> None:
        """Cambia el estado interno a apagado."""
        self.__estado = False
        print(f"[INFO] {self.__id_dispositivo} apagado.")

    # ---------- Método polimórfico ----------
    def mostrar_datos(self) -> None:
        """
        Muestra información común del dispositivo.
        Este método será extendido (sobrescrito) por las subclases.
        """
        estado_str = "Encendido" if self.__estado else "Apagado"
        print(f"[{self.__class__.__name__}] ID: {self.__id_dispositivo} | Estado: {estado_str}")


# ------------------------------------------------------------
# Subclase: SensorTemperatura
# ------------------------------------------------------------
class SensorTemperatura(DispositivoIoT):
    """
    Sensor de temperatura que simula lecturas en °C.

    Atributos privados:
        __temperatura (float): Última lectura de temperatura.

    Encapsulamiento:
        - Propiedad de solo lectura 'temperatura' para consultar el valor.
        - La actualización ocurre exclusivamente mediante 'leer_temperatura()'.
    """

    def __init__(self, id_dispositivo: str) -> None:
        super().__init__(id_dispositivo)
        self.__temperatura: float = 0.0  # Valor inicial “neutro”

    def leer_temperatura(self) -> float:
        """
        Simula la lectura de temperatura.
        - Si el sensor está encendido, genera un valor aleatorio (20.00 a 40.00 °C).
        - Si está apagado, el valor vuelve a 0.0 para indicar inactividad.
        """
        if self.estado:
            # random.uniform genera valores flotantes; redondeamos a 2 decimales
            self.__temperatura = round(random.uniform(20.0, 40.0), 2)
        else:
            self.__temperatura = 0.0
        return self.__temperatura

    @property
    def temperatura(self) -> float:
        """Devuelve la última temperatura leída (°C)."""
        return self.__temperatura

    # Polimorfismo: sobrescribimos mostrar_datos para agregar la temperatura
    def mostrar_datos(self) -> None:
        super().mostrar_datos()  # Muestra ID y estado desde la clase base
        print(f"   • Temperatura actual: {self.__temperatura} °C\n")


# ------------------------------------------------------------
# Subclase: SensorHumedad
# ------------------------------------------------------------
class SensorHumedad(DispositivoIoT):
    """
    Sensor de humedad relativa del aire, en porcentaje (%).

    Atributos privados:
        __humedad (float): Última lectura de humedad.

    Encapsulamiento:
        - Propiedad de solo lectura 'humedad'.
        - La actualización ocurre mediante 'leer_humedad()'.
    """

    def __init__(self, id_dispositivo: str) -> None:
        super().__init__(id_dispositivo)
        self.__humedad: float = 0.0

    def leer_humedad(self) -> float:
        """
        Simula la lectura de humedad.
        - Si el sensor está encendido, genera un valor aleatorio (30% a 90%).
        - Si está apagado, reinicia a 0.0.
        """
        if self.estado:
            self.__humedad = round(random.uniform(30.0, 90.0), 2)
        else:
            self.__humedad = 0.0
        return self.__humedad

    @property
    def humedad(self) -> float:
        """Devuelve la última humedad leída (%)."""
        return self.__humedad

    # Polimorfismo: sobrescribimos mostrar_datos para agregar la humedad
    def mostrar_datos(self) -> None:
        super().mostrar_datos()
        print(f"   • Humedad actual: {self.__humedad} %\n")


# ------------------------------------------------------------
# Subclase: ActuadorLuz
# ------------------------------------------------------------
class ActuadorLuz(DispositivoIoT):
    """
    Actuador tipo luz que puede modificar su intensidad (0-100%).

    Atributos privados:
        __intensidad (int): Porcentaje de potencia luminosa.

    Encapsulamiento:
        - Propiedad de lectura 'intensidad'.
        - Método 'ajustar_intensidad(valor)' controla validaciones y cambios.
    """

    def __init__(self, id_dispositivo: str) -> None:
        super().__init__(id_dispositivo)
        self.__intensidad: int = 0  # Arranca en 0% para seguridad

    def ajustar_intensidad(self, valor: int) -> None:
        """
        Ajusta la intensidad si el dispositivo está encendido y el valor es válido.
        Reglas:
            - Solo acepta enteros de 0 a 100.
            - Si está apagado, no se modifica (se informa por consola).
        """
        if not self.estado:
            print(f"[ADVERTENCIA] {self.id_dispositivo} está apagado; no se puede ajustar intensidad.")
            return

        if not isinstance(valor, int):
            print("[ERROR] La intensidad debe ser un entero (0-100).")
            return

        if 0 <= valor <= 100:
            self.__intensidad = valor
            print(f"[INFO] Intensidad de {self.id_dispositivo} ajustada a {valor}%")
        else:
            print("[ERROR] Valor fuera de rango (0-100). No se aplica cambio.")

    @property
    def intensidad(self) -> int:
        """Devuelve la intensidad actual del actuador (%)."""
        return self.__intensidad

    # Polimorfismo: sobrescribimos mostrar_datos para agregar la intensidad
    def mostrar_datos(self) -> None:
        super().mostrar_datos()
        print(f"   • Intensidad actual: {self.__intensidad} %\n")


# ------------------------------------------------------------
# Función de simulación de monitoreo
# ------------------------------------------------------------
def simulacion_monitoreo(dispositivos: List[DispositivoIoT],
                         ciclos: int = 5,
                         pausa_seg: float = 1.5,
                         umbral_temp: float = 30.0) -> None:
    """
    Ejecuta un ciclo de monitoreo donde:
      1) Los sensores leen valores nuevos (si están encendidos).
      2) Se evalúan reglas simples:
           - Si alguna temperatura > umbral_temp -> luces al 80%.
           - En caso contrario -> luces al 20%.
      3) Se demuestra polimorfismo invocando mostrar_datos() para cada objeto.

    """
    print("\n================ INICIO DE MONITOREO ================\n")

    for ciclo in range(1, ciclos + 1):
        print(f"------------------- Ciclo {ciclo} -------------------")

        # 1) ACTUALIZACIÓN DE SENSORES
        # Recorremos la lista y, mediante isinstance, invocamos su lectura correspondiente
        # (esto mantiene el código claro y explícito para el evaluador).
        for d in dispositivos:
            if isinstance(d, SensorTemperatura):
                d.leer_temperatura()
            elif isinstance(d, SensorHumedad):
                d.leer_humedad()
            # Si es un actuador, no “lee” valores externos aquí.

        # 2) REGLAS DE ACTUACIÓN (lógica simple basada en temperatura)
        # Identificamos temperaturas presentes para decidir la intensidad de las luces.
        temperaturas = [d.temperatura for d in dispositivos if isinstance(d, SensorTemperatura)]
        # Comprobamos si hay alguna temperatura por encima del umbral
        alarma_calor = any(t > umbral_temp for t in temperaturas)

        # Según la condición, ajustamos todos los actuadores de luz presentes
        for d in dispositivos:
            if isinstance(d, ActuadorLuz):
                d.ajustar_intensidad(80 if alarma_calor else 20)

        # 3) POLIMORFISMO: cada objeto muestra lo que le corresponde
        for d in dispositivos:
            d.mostrar_datos()

        # Pausa para simular el tiempo entre lecturas (p.ej., 1.5 segundos)
        time.sleep(pausa_seg)

    print("================= FIN DE MONITOREO =================\n")


# ------------------------------------------------------------
# Punto de entrada del script
# ------------------------------------------------------------
if __name__ == "__main__":
    random.seed(42)

    # 1) CREACIÓN DE OBJETOS (≥5, de distintos tipos)
    temp1 = SensorTemperatura("TempSensor_01")
    temp2 = SensorTemperatura("TempSensor_02")
    hum1 = SensorHumedad("HumSensor_01")
    luz1 = ActuadorLuz("Luz_Sala")
    luz2 = ActuadorLuz("Luz_Cocina")

    # Lista heterogénea para demostrar polimorfismo
    dispositivos: List[DispositivoIoT] = [temp1, temp2, hum1, luz1, luz2]

    # 2) ENCENDER TODOS LOS DISPOSITIVOS (por simplicidad en la demo)
    for d in dispositivos:
        d.encender()

    # 3) EJECUTAR SIMULACIÓN
    simulacion_monitoreo(
        dispositivos=dispositivos,
        ciclos=5,        # número de iteraciones a ejecutar
        pausa_seg=1.5,   # segundos entre ciclos
        umbral_temp=30.0 # regla: si alguna T > 30°C, luces al 80%
    )
    
