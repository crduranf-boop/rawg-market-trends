import os
import sys
import requests

def main():
    API_KEY = os.getenv("RAWG_API_KEY")
    if not API_KEY:
        print("[ERROR] No se detectó la variable de entorno RAWG_API_KEY.", file=sys.stderr)
        sys.exit(1)

    print("[INFO] Iniciando consulta a la API de RAWG (Período: Año 2026)...")
    
    URL = "https://api.rawg.io/api/games"
    
    # Filtramos estrictamente para el año 2026 ordenando por popularidad
    PARAMS = {
        "key": API_KEY,
        "page_size": 5,
        "dates": "2026-01-01,2026-12-31",
        "ordering": "-added"
    }

    try:
        response = requests.get(URL, params=PARAMS, timeout=10)
        response.raise_for_status()
        data = response.json()
        games = data.get("results", [])

        if not games:
            print("[ADVERTENCIA] La API no devolvió juegos para el año 2026. Es posible que falten registros de este año en la base de datos de RAWG.")
            return

        print("\n" + "="*60)
        print("  🎮  RAWG MARKET TRENDS — REPORTE DE VIDEOJUEGOS 2026")
        print("="*60)
        
        for i, game in enumerate(games, 1):
            # 1. Nombre
            name = game.get("name", "N/A")
            # 2. Rating promedio de usuarios
            rating = game.get("rating", "N/A")
            # 3. Puntuación Metacritic
            meta = game.get("metacritic", "N/A")
            if meta is None or meta == 0:
                meta = "N/A"
            # 4. Fecha de lanzamiento
            released = game.get("released", "N/A")
            
            # 5. Lista de géneros (Procesamiento)
            genres_list = game.get("genres", [])
            genres = ", ".join([g.get("name") for g in genres_list if g.get("name")]) if genres_list else "N/A"
            
            # 6. Plataformas disponibles (Procesamiento)
            platforms_list = game.get("platforms", [])
            platforms = ", ".join([p.get("platform", {}).get("name") for p in platforms_list if p.get("platform", {}).get("name")]) if platforms_list else "N/A"
            
            print(f"  [{i}] {name}")
            print(f"      📅 Lanzamiento: {released}")
            print(f"      ⭐ Rating: {rating}/5 | 📝 Metacritic: {meta}")
            print(f"      🎭 Géneros: {genres}")
            print(f"      🕹️  Plataformas: {platforms}")
            print("-" * 60)
            
        print("="*60)
        print("  ✅ Consulta de tendencias 2026 completada exitosamente.")
        print("="*60)

    except Exception as e:
        print(f"[ERROR] Ocurrió un fallo al consultar la API: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
