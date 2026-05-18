#!/bin/bash
# ─────────────────────────────────────────────────────────────
# build.sh — Script de automatización: Dockerfile + Build + Run
# Proyecto: RAWG Market Trends Dashboard
# ─────────────────────────────────────────────────────────────

set -e  # Detener si cualquier comando falla

IMAGE_NAME="rawg-market-trends"
CONTAINER_NAME="samplerunning"

echo "============================================================"
echo "  RAWG Market Trends — Pipeline de Automatización"
echo "============================================================"

# ── 1. Verificar que la API Key esté disponible ──────────────
if [ -z "$RAWG_API_KEY" ]; then
  echo "[ERROR] La variable RAWG_API_KEY no está definida."
  echo "        Ejecuta: export RAWG_API_KEY='tu_clave_aqui'"
  exit 1
fi
echo "[OK] Variable de entorno RAWG_API_KEY detectada."

# ── 2. Generar el Dockerfile dinámicamente ───────────────────
echo "[INFO] Generando Dockerfile..."

cat > Dockerfile <<'EOF'
# Imagen base oficial Python 3.11 slim
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar dependencias e instalarlas primero (mejor cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script principal
COPY app.py .

# Comando de ejecución
CMD ["python", "app.py"]
EOF

echo "[OK] Dockerfile generado correctamente."

# ── 3. Construir la imagen Docker ────────────────────────────
echo "[INFO] Construyendo imagen Docker: $IMAGE_NAME..."
docker build -t "$IMAGE_NAME" .
echo "[OK] Imagen $IMAGE_NAME construida exitosamente."

# ── 4. Ejecutar el contenedor ────────────────────────────────
echo "[INFO] Ejecutando contenedor: $CONTAINER_NAME..."
docker run \
  --name "$CONTAINER_NAME" \
  --env RAWG_API_KEY="$RAWG_API_KEY" \
  "$IMAGE_NAME"

echo "============================================================"
echo "[OK] Contenedor ejecutado. Revisando estado final..."

# ── 5. Mostrar estado del contenedor ────────────────────────
docker ps -a --filter "name=$CONTAINER_NAME"

echo "============================================================"
echo "  Pipeline completado exitosamente."
echo "============================================================"
