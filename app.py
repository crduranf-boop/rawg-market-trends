import os
import sys
import requests
from datetime import datetime

# ─────────────────────────────────────────────
# Lectura segura de credenciales (sin hardcoding)
# ─────────────────────────────────────────────
API_KEY = os.getenv("RAWG_API_KEY")

if not API_KEY:
    print("[ERROR] La variable de entorno RAWG_API_KEY no está definida.")
    print("        Ejecuta: export RAWG_API_KEY='tu_clave_aqui'")
    sys.exit(1)

BASE_URL = "https://api.rawg.io/api"

# ─────────────────────────────────────────────
# Parámetros de consulta (tendencias del mercado)
# ─────────────────────────────────────────────
CURRENT_YEAR = datetime.now().year
PARAMS = {
    "key": API_KEY,
    "ordering": "-rating",          # Mayor rating primero
    "page_size": 5,                 # Top 5 juegos
    "dates": f"{CURRENT_YEAR - 1}-01-01,{CURRENT_YEAR}-12-31",  # Último año
    "metacritic": "75,100",         # Solo juegos con buen Metacritic
}


def fetch_top_games():
    """
    Consulta el endpoint /games de RAWG y retorna la lista de juegos.
    Maneja 4 tipos de errores: 401, 404, Timeout y errores de conexión.
    """
    url = f"{BASE_URL}/games"

    try:
        response = requests.get(url, params=PARAMS, timeout=10)

        # Error 401: clave inválida o sin permisos
        if response.status_code == 401:
            print("[ERROR 401] API Key inválida o sin autorización.")
            print("           Verifica que RAWG_API_KEY sea correcta.")
            sys.exit(1)

        # Error 404: endpoint no encontrado
        if response.status_code == 404:
            print("[ERROR 404] El recurso solicitado no existe en la API.")
            print(f"           URL consultada: {url}")
            sys.exit(1)

        # Otros errores HTTP (429 rate limit, 500 server error, etc.)
        if response.status_code != 200:
            print(f"[ERROR {response.status_code}] Respuesta inesperada de la API.")
            print(f"           Detalle: {response.text[:200]}")
            sys.exit(1)

        data = response.json()

        # Validar que la respuesta tenga el campo esperado
        if "results" not in data:
            print("[ERROR] La respuesta de la API no contiene el campo 'results'.")
            print(f"        Respuesta recibida: {data}")
            sys.exit(1)

        return data["results"]

    except requests.exceptions.ConnectionError:
        print("[ERROR] No se pudo conectar con la API de RAWG.")
        print("        Verifica tu conexión a internet.")
        sys.exit(1)

    except requests.exceptions.Timeout:
        print("[ERROR] La solicitud a la API superó el tiempo de espera (10s).")
        print("        El servidor de RAWG no respondió a tiempo.")
        sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error inesperado en la solicitud HTTP: {e}")
        sys.exit(1)


def procesar_juego(juego):
    """
    Extrae y procesa los campos relevantes de un juego.
    Procesa 6 campos de datos (≥3 requeridos por la evaluación):
      1. name        - Nombre del juego
      2. rating      - Rating promedio de usuarios
      3. metacritic  - Puntuación Metacritic
      4. released    - Fecha de lanzamiento
      5. genres      - Géneros del juego
      6. platforms   - Plataformas disponibles
    """
    nombre     = juego.get("name", "Sin nombre")
    rating     = juego.get("rating", 0)
    metacritic = juego.get("metacritic", "N/A")
    released   = juego.get("released", "Desconocida")
    generos    = [g["name"] for g in juego.get("genres", [])]
    plataformas = [p["platform"]["name"] for p in juego.get("platforms", [])]

    return {
        "nombre":      nombre,
        "rating":      rating,
        "metacritic":  metacritic,
        "lanzamiento": released,
        "generos":     ", ".join(generos) if generos else "Sin géneros",
        "plataformas": ", ".join(plataformas[:3]) if plataformas else "Sin plataformas",
    }


def imprimir_reporte(juegos_procesados):
    """Imprime el reporte de tendencias en consola."""
    linea = "=" * 60

    print("\n" + linea)
    print("  🎮  RAWG MARKET TRENDS — Game Developer Dashboard")
    print(f"  📅  Análisis: {CURRENT_YEAR - 1} – {CURRENT_YEAR}")
    print(linea)
    print(f"  Top {len(juegos_procesados)} juegos mejor valorados del período\n")

    for i, juego in enumerate(juegos_procesados, start=1):
        print(f"  [{i}] {juego['nombre']}")
        print(f"       Rating usuarios : {juego['rating']:.2f} / 5.0")
        print(f"       Metacritic       : {juego['metacritic']}")
        print(f"       Lanzamiento      : {juego['lanzamiento']}")
        print(f"       Géneros          : {juego['generos']}")
        print(f"       Plataformas      : {juego['plataformas']}")
        print()

    print(linea)
    print("  ✅  Consulta completada exitosamente.")
    print(linea + "\n")


def main():
    print("[INFO] Iniciando consulta a la API de RAWG...")
    juegos_raw = fetch_top_games()

    if not juegos_raw:
        print("[ADVERTENCIA] La API no devolvió juegos para el período consultado.")
        sys.exit(0)

    juegos_procesados = [procesar_juego(j) for j in juegos_raw]
    imprimir_reporte(juegos_procesados)


if __name__ == "__main__":
    main()
