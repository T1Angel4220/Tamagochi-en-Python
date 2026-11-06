#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor local para Tamagotchi RPG
---------------------------------
Inicia un servidor HTTP ligero en el puerto 8000 y abre automáticamente
la aplicación web en el navegador.

Uso:
    python server.py
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PUERTO = 8000

def main():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    os.chdir(directorio_actual)

    Handler = http.server.SimpleHTTPRequestHandler

    print("=" * 60)
    print("   🎮 Servidor de Desarrollo - Tamagotchi RPG")
    print("=" * 60)
    print(f"Directorio raíz: {directorio_actual}")
    print(f"Iniciando en:    http://localhost:{PUERTO}/index.html")
    print("Presiona Ctrl+C en la terminal para detener el servidor.")
    print("=" * 60)

    # Abrir navegador automáticamente
    webbrowser.open(f"http://localhost:{PUERTO}/index.html")

    try:
        with socketserver.TCPServer(("", PUERTO), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido correctamente.")
        sys.exit(0)

if __name__ == "__main__":
    main()
