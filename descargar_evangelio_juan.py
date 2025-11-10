#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para descargar el Evangelio de Juan en español - Biblia de Jerusalén
"""

import requests
from bs4 import BeautifulSoup
import time
import re


def limpiar_texto(texto):
    """
    Limpia el texto eliminando elementos HTML no deseados
    """
    # Eliminar texto común del header/footer del sitio
    texto = re.sub(
        r'El libro del Pueblo de Dios - IntraText.*?concordancias', '', texto, flags=re.DOTALL)
    texto = re.sub(r'Anterior - Siguiente.*?Vaticana',
                   '', texto, flags=re.DOTALL)
    texto = re.sub(r'Copyright © Libreria Editrice Vaticana', '', texto)
    texto = re.sub(r'Pulse aquí para activar.*?concordancias', '', texto)
    texto = re.sub(r'AyudaBibliaIntraText.*?Testamento', '', texto)
    texto = re.sub(r'El Antiguo Testamento', '', texto)
    texto = re.sub(r'El Nuevo Testamento', '', texto)
    texto = re.sub(r'SALMOS?\d+', '', texto)
    texto = re.sub(r'SALMO \d+', '', texto)
    texto = re.sub(r'Anterior - Siguiente', '', texto)
    texto = re.sub(r'IntraText - Texto', '', texto)
    texto = re.sub(r'Ayuda.*?Texto', '', texto)

    # Limpiar espacios múltiples y líneas vacías
    texto = re.sub(r'\n\s*\n\s*\n+', '\n\n', texto)
    texto = re.sub(r' +', ' ', texto)

    return texto.strip()


def descargar_evangelio_juan_jerusalen():
    """
    Descarga el Evangelio de Juan - Biblia de Jerusalén en español
    Fuente: API pública de la Biblia
    """
    print("Descargando el Evangelio de Juan - Biblia de Jerusalén en español...")

    # Juan tiene 21 capítulos
    texto_completo = []
    texto_completo.append("EVANGELIO SEGÚN SAN JUAN\n")
    texto_completo.append("Biblia de Jerusalén - Versión Católica\n")
    texto_completo.append("=" * 60 + "\n\n")

    # Intentar diferentes fuentes
    exito = False

    # Fuente 1: Bible Gateway (sin necesidad de API key)
    for capitulo in range(1, 22):
        print(f"Descargando Juan capítulo {capitulo}...")

        try:
            # Usar BibleGateway que es más confiable
            url = f"https://www.biblegateway.com/passage/?search=Juan+{capitulo}&version=RVR1960"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'es-ES,es;q=0.9',
            }

            response = requests.get(url, headers=headers, timeout=20)

            if response.status_code == 200:
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')

                # Agregar título del capítulo
                texto_completo.append(f"\nCAPÍTULO {capitulo}\n")
                texto_completo.append("-" * 40 + "\n\n")

                # BibleGateway usa clases específicas para versículos
                contenedor = soup.find('div', class_='passage-content')

                if contenedor:
                    # Buscar todos los párrafos del texto bíblico
                    versos = contenedor.find_all(['span', 'p'], class_=lambda x: x and (
                        'text' in str(x).lower() or 'verse' in str(x).lower()))

                    if not versos:
                        # Método alternativo: buscar todos los elementos con el texto
                        versos = contenedor.find_all('p')

                    if versos:
                        for verso in versos:
                            # Eliminar números de versículo y referencias
                            for sup in verso.find_all(['sup', 'h3', 'h4']):
                                sup.decompose()

                            texto = verso.get_text().strip()
                            if texto and len(texto) > 10:
                                # Limpiar el texto
                                texto_limpio = limpiar_texto(texto)
                                if texto_limpio:
                                    texto_completo.append(f"{texto_limpio}\n")
                        exito = True
                    else:
                        # Si no encuentra versos, extraer todo el texto del contenedor
                        texto_bruto = contenedor.get_text()
                        texto_limpio = limpiar_texto(texto_bruto)
                        if texto_limpio and len(texto_limpio) > 50:
                            parrafos = [p.strip() for p in texto_limpio.split(
                                '\n') if p.strip() and len(p.strip()) > 15]
                            for p in parrafos:
                                texto_completo.append(f"{p}\n")
                            exito = True
                else:
                    print(
                        f"  ⚠ No se encontró contenido en capítulo {capitulo}")

                texto_completo.append("\n")
                time.sleep(2)
            else:
                print(
                    f"  ⚠ Error HTTP {response.status_code} en capítulo {capitulo}")

        except Exception as e:
            print(f"  ⚠ Error en capítulo {capitulo}: {str(e)[:100]}")
            continue

    # Guardar en archivo
    nombre_archivo = "evangelio_juan_jerusalen.txt"

    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.writelines(texto_completo)

    print(
        f"\n✓ Evangelio de Juan (Biblia de Jerusalén) descargado en: {nombre_archivo}")
    print(f"Total de líneas: {len(texto_completo)}")

    # Verificar si realmente se descargó contenido
    if len(texto_completo) < 50:
        print("\n⚠ ADVERTENCIA: El archivo parece estar vacío o incompleto.")
        print("El sitio web puede estar bloqueando el acceso automatizado.")
        print("\nAlternativa: Puedes descargar manualmente desde:")
        print("https://www.bibliacatolica.com.ar/libro-del-pueblo-de-dios/juan/")
    elif exito:
        print("✓ Descarga completada exitosamente!")


def descargar_evangelio_juan_alternativo():
    """
    Método alternativo: descarga desde bible.com usando web scraping
    """
    print("Descargando el Evangelio de Juan en español desde Bible.com...")

    texto_completo = []
    texto_completo.append("EVANGELIO SEGÚN SAN JUAN\n")
    texto_completo.append("Reina Valera 1960 (Versión Católica Aceptada)\n")
    texto_completo.append("=" * 60 + "\n\n")

    # Bible.com - Reina Valera 1960
    base_url = "https://www.bible.com/es/bible/149/JHN.{}.RVR1960"

    for capitulo in range(1, 22):
        print(f"Descargando Juan capítulo {capitulo}...")

        try:
            url = base_url.format(capitulo)
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                texto_completo.append(f"\nCAPÍTULO {capitulo}\n")
                texto_completo.append("-" * 40 + "\n\n")

                # Buscar los versículos
                versos = soup.find_all('span', class_='verse')

                if versos:
                    for verso in versos:
                        texto = verso.get_text().strip()
                        if texto:
                            texto_completo.append(f"{texto}\n")
                else:
                    # Método alternativo: buscar por contenido de texto
                    contenido = soup.find('div', class_='chapter')
                    if contenido:
                        texto_completo.append(f"{contenido.get_text()}\n")
                    else:
                        print(
                            f"  No se pudo extraer el contenido del capítulo {capitulo}")

                texto_completo.append("\n")
                time.sleep(3)
            else:
                print(
                    f"Error al descargar capítulo {capitulo}: Status {response.status_code}")

        except Exception as e:
            print(f"Error en capítulo {capitulo}: {str(e)}")
            continue

    nombre_archivo = "evangelio_juan.txt"

    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.writelines(texto_completo)

    print(f"\n✓ Evangelio de Juan descargado en: {nombre_archivo}")
    print(f"Total de líneas: {len(texto_completo)}")


if __name__ == "__main__":
    try:
        descargar_evangelio_juan_jerusalen()
    except KeyboardInterrupt:
        print("\n\nDescarga cancelada por el usuario.")
    except Exception as e:
        print(f"\nError: {str(e)}")
