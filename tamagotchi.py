#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tamagotchi RPG - Simulación en Python
------------------------------------
Implementación con Programación Orientada a Objetos (POO) del juego Tamagotchi.
Permite interactuar con la mascota virtual desde la terminal o lanzar la versión web.

Autor: Ángel Ayuquina
Licencia: MIT
"""

import os
import sys
import time
import json
import webbrowser
from typing import Dict, Any

class Tamagotchi:
    """Clase que modela el estado y comportamiento de la mascota virtual."""

    def __init__(self, nombre: str = "Papa RPG"):
        self.nombre: str = nombre
        self.hambre: int = 40        # 0 = satisfecho, 100 = hambriento
        self.aburrimiento: int = 30  # 0 = entretenido, 100 = aburrido
        self.sueno: int = 20         # 0 = descansado, 100 = agotado
        self.suciedad: int = 10      # 0 = limpio, 100 = muy sucio
        self.esta_dormido: bool = False
        self.esta_vivo: bool = True
        self.turnos_vividos: int = 0

    def alimentar(self) -> str:
        """Alimenta a la mascota reduciendo su nivel de hambre."""
        if not self.esta_vivo:
            return f"❌ {self.nombre} no puede comer porque no tiene energía vital."
        if self.esta_dormido:
            return f"💤 {self.nombre} está durmiendo. Despiértalo antes de alimentarlo."
        if self.hambre <= 5:
            return f"🥞 {self.nombre} ya está lleno y no quiere comer más."

        self.hambre = max(0, self.hambre - 25)
        self.suciedad = min(100, self.suciedad + 5)
        self.turnos_vividos += 1
        return f"🍎 ¡Ñam ñam! Alimentaste a {self.nombre}. (-25 Hambre, +5 Suciedad)"

    def dormir(self) -> str:
        """Cambia el estado de sueño de la mascota."""
        if not self.esta_vivo:
            return f"❌ {self.nombre} no responde."
        
        if self.esta_dormido:
            self.esta_dormido = False
            return f"☀️ ¡Buenos días! {self.nombre} se ha despertado."
        else:
            self.esta_dormido = True
            self.sueno = max(0, self.sueno - 40)
            self.hambre = min(100, self.hambre + 5)
            self.turnos_vividos += 1
            return f"💤 {self.nombre} se ha dormido plácidamente. (-40 Sueño)"

    def limpiar(self) -> str:
        """Baña y limpia a la mascota."""
        if not self.esta_vivo:
            return f"❌ {self.nombre} no responde."
        if self.suciedad == 0:
            return f"✨ {self.nombre} ya está impecable."

        self.suciedad = 0
        self.turnos_vividos += 1
        return f"🧼🫧 Bañaste a {self.nombre}. ¡Ahora está reluciente!"

    def jugar(self) -> str:
        """Juega con la mascota para reducir su aburrimiento."""
        if not self.esta_vivo:
            return f"❌ {self.nombre} no puede jugar en este momento."
        if self.esta_dormido:
            return f"💤 {self.nombre} está durmiendo profundamente."
        if self.sueno > 80:
            return f"🥱 {self.nombre} está demasiado exhausto para jugar."

        self.aburrimiento = max(0, self.aburrimiento - 30)
        self.hambre = min(100, self.hambre + 8)
        self.sueno = min(100, self.sueno + 10)
        self.turnos_vividos += 1
        return f"🎮 ¡Qué divertido! Jugaste con {self.nombre}. (-30 Aburrimiento)"

    def pasar_tiempo(self) -> None:
        """Simula el paso natural del tiempo incrementando las necesidades."""
        if not self.esta_vivo:
            return

        if self.esta_dormido:
            self.sueno = max(0, self.sueno - 15)
            self.hambre = min(100, self.hambre + 2)
            if self.sueno == 0:
                self.esta_dormido = False
        else:
            self.hambre = min(100, self.hambre + 3)
            self.aburrimiento = min(100, self.aburrimiento + 2)
            self.sueno = min(100, self.sueno + 2)
            self.suciedad = min(100, self.suciedad + 1)

        self._verificar_estado()

    def _verificar_estado(self) -> None:
        """Evalúa si alguna estadística vital llegó a niveles críticos."""
        if self.hambre >= 100 or self.aburrimiento >= 100 or self.sueno >= 100 or self.suciedad >= 100:
            self.esta_vivo = False

    def obtener_barra(self, valor: int, longitud: int = 15) -> str:
        """Genera una barra de progreso visual en texto."""
        lleno = int((valor / 100) * longitud)
        vacio = longitud - lleno
        color = "🟩" if valor < 50 else ("🟨" if valor < 80 else "🟥")
        return f"[{'█' * lleno}{'-' * vacio}] {valor:3d}% {color}"

    def guardar(self, ruta: str = "partida.json") -> bool:
        """Guarda el estado actual en un archivo JSON."""
        datos = {
            "nombre": self.nombre,
            "hambre": self.hambre,
            "aburrimiento": self.aburrimiento,
            "sueno": self.sueno,
            "suciedad": self.suciedad,
            "esta_dormido": self.esta_dormido,
            "esta_vivo": self.esta_vivo,
            "turnos_vividos": self.turnos_vividos
        }
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False

    def cargar(self, ruta: str = "partida.json") -> bool:
        """Carga el estado guardado desde un archivo JSON."""
        if not os.path.exists(ruta):
            return False
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
            self.nombre = datos.get("nombre", self.nombre)
            self.hambre = datos.get("hambre", self.hambre)
            self.aburrimiento = datos.get("aburrimiento", self.aburrimiento)
            self.sueno = datos.get("sueno", self.sueno)
            self.suciedad = datos.get("suciedad", self.suciedad)
            self.esta_dormido = datos.get("esta_dormido", self.esta_dormido)
            self.esta_vivo = datos.get("esta_vivo", self.esta_vivo)
            self.turnos_vividos = datos.get("turnos_vividos", self.turnos_vividos)
            return True
        except (IOError, json.JSONDecodeError):
            return False


def dibujar_mascota(pet: Tamagotchi) -> None:
    """Muestra el dibujo ASCII y estado de la mascota."""
    if not pet.esta_vivo:
        print("""
            ( x . x )
           (   ---   )   [Mascota Desmayada / Crítica]
            `-------'
        """)
    elif pet.esta_dormido:
        print("""
            ( - . - )  z Z z
           (   ~~~   )
            `-------'
        """)
    elif pet.suciedad > 70:
        print("""
            ( . _ . ) *sucio*
           (  ~ ~ ~  )
            `-------'
        """)
    else:
        print("""
            ( ^ . ^ )
           (   > <   )   ¡Hola!
            `-------'
        """)


def limpiar_pantalla() -> None:
    """Limpia la terminal según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')


def ejecutar_juego_consola() -> None:
    """Bucle principal interactivo para consola."""
    pet = Tamagotchi()
    mensaje = "¡Bienvenido a Tamagotchi RPG en Python!"

    while True:
        limpiar_pantalla()
        print("=" * 55)
        print(f"      TAMAGOTCHI RPG (Python Edition) - Mascota: {pet.nombre}")
        print("=" * 55)
        dibujar_mascota(pet)

        print(f"  Hambre:      {pet.obtener_barra(pet.hambre)}")
        print(f"  Aburrimiento:{pet.obtener_barra(pet.aburrimiento)}")
        print(f"  Sueño:       {pet.obtener_barra(pet.sueno)}")
        print(f"  Suciedad:    {pet.obtener_barra(pet.suciedad)}")
        print(f"  Estado:      {'💤 Durmiendo' if pet.esta_dormido else ('❤️ Saludable' if pet.esta_vivo else '💔 Crítico')}")
        print(f"  Turnos:      {pet.turnos_vividos}")
        print("-" * 55)
        print(f"  💬 {mensaje}")
        print("-" * 55)

        if not pet.esta_vivo:
            print("\n⚠️ ¡Tu mascota no resistió el descuido! Llegó a valores críticos.")
            print("[1] Reiniciar nueva partida")
            print("[0] Salir")
            op = input("\nElige una opción: ").strip()
            if op == "1":
                pet = Tamagotchi()
                mensaje = "¡Nueva mascota adoptada!"
                continue
            else:
                break

        print("[1] 🍔 Comer")
        print("[2] 💤 Dormir / Despertar")
        print("[3] 🧼 Limpiarse")
        print("[4] 🎮 Jugar")
        print("[5] ⏳ Esperar (pasar tiempo)")
        print("[6] 💾 Guardar partida")
        print("[7] 📂 Cargar partida")
        print("[8] 🌐 Abrir versión Web")
        print("[0] 🚪 Salir")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            mensaje = pet.alimentar()
            pet.pasar_tiempo()
        elif opcion == "2":
            mensaje = pet.dormir()
            pet.pasar_tiempo()
        elif opcion == "3":
            mensaje = pet.limpiar()
            pet.pasar_tiempo()
        elif opcion == "4":
            mensaje = pet.jugar()
            pet.pasar_tiempo()
        elif opcion == "5":
            pet.pasar_tiempo()
            mensaje = "Pasó el tiempo..."
        elif opcion == "6":
            if pet.guardar():
                mensaje = "Partida guardada exitosamente en partida.json."
            else:
                mensaje = "Error al intentar guardar la partida."
        elif opcion == "7":
            if pet.cargar():
                mensaje = "Partida cargada exitosamente."
            else:
                mensaje = "No se encontró archivo de guardado previo."
        elif opcion == "8":
            ruta_html = os.path.abspath("index.html")
            webbrowser.open(f"file://{ruta_html}")
            mensaje = "Abriendo versión Web en tu navegador predeterminado..."
        elif opcion == "0":
            print("\n¡Gracias por jugar Tamagotchi RPG!")
            break
        else:
            mensaje = "Opción inválida. Ingresa un número del 0 al 8."


if __name__ == "__main__":
    ejecutar_juego_consola()
