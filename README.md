# 🎮 RAWG Market Trends Dashboard

> Herramienta de análisis de tendencias del mercado de videojuegos para Game Developers.

---

## 👤 Stakeholder

**Game Developer Independiente / Estudio de desarrollo de videojuegos**

Un desarrollador de videojuegos necesita tomar decisiones estratégicas basadas en datos reales del mercado: ¿qué géneros están dominando las listas de valoración?, ¿qué plataformas concentran los títulos mejor recibidos?, ¿cuál es el rango de puntuación Metacritic de los juegos exitosos este año?

---

## 💡 Propuesta de Valor (Problema / Solución)

**Problema:** Un Game Developer que planifica su próximo proyecto necesita conocer qué tipo de juegos están siendo mejor valorados por usuarios y crítica en el período reciente. Revisar manualmente decenas de fuentes (Steam, Metacritic, IGN) es ineficiente y no escalable.

**Solución:** `rawg-market-trends` consulta automáticamente la API de RAWG —la mayor base de datos de videojuegos del mundo con más de 500.000 títulos— y entrega en consola un reporte con los 5 juegos mejor valorados del último período, incluyendo rating de usuarios, puntuación Metacritic, géneros y plataformas. En segundos, el desarrollador tiene una fotografía clara de las tendencias del mercado para fundamentar sus decisiones creativas y de negocio.

---

## 📁 Estructura del Repositorio

```
mi-proyecto/
├── app.py              # Script principal — consulta la API de RAWG
├── build.sh            # Script de automatización (Dockerfile + build + run)
├── requirements.txt    # Dependencias Python
├── .gitignore
├── README.md
└── evidencias/
    ├── docker/
    │   ├── output.txt          # docker ps -a + logs con datos reales de la API
    │   └── screenshot.png      # Captura de la salida en consola
    └── jenkins/
        ├── stage_view.png
        ├── console_output_build.png
        ├── credentials.png
        └── pipeline_script.txt
```

---

## ⚙️ Guía de Configuración

### 1. Obtener API Key de RAWG

1. Crear cuenta gratuita en [rawg.io](https://rawg.io/apidocs)
2. Ir al panel de tu cuenta → **Get API Key**
3. Copiar la clave generada

### 2. Configurar Variable de Entorno

La clave **nunca** se escribe en el código. Se configura como variable de entorno:

**Linux / macOS (Bash):**
```bash
export RAWG_API_KEY="tu_clave_aqui"
```

**Windows (PowerShell):**
```powershell
$env:RAWG_API_KEY = "tu_clave_aqui"
```

**Jenkins:** Configurar como credencial tipo *Secret text* en el gestor de credenciales de Jenkins e inyectarla como variable de entorno en el BuildAppJob.

---

## 🐳 Instrucciones de Ejecución con Docker

### Opción A — Script automatizado (recomendado)

```bash
# Dar permisos de ejecución al script
chmod +x build.sh

# Ejecutar el pipeline completo (genera Dockerfile, construye y corre)
./build.sh
```

### Opción B — Comandos manuales

```bash
# 1. Construir la imagen
docker build -t rawg-market-trends .

# 2. Ejecutar el contenedor
docker run --name samplerunning --env RAWG_API_KEY="$RAWG_API_KEY" rawg-market-trends

# 3. Ver estado del contenedor (debe mostrar Exited (0))
docker ps -a --filter "name=samplerunning"

# 4. Ver logs del contenedor
docker logs samplerunning
```

---

## 📊 Campos de Datos Procesados

La aplicación extrae y procesa **6 campos** de cada juego:

| Campo | Descripción |
|-------|-------------|
| `name` | Nombre del juego |
| `rating` | Rating promedio de usuarios (0–5) |
| `metacritic` | Puntuación de la crítica especializada |
| `released` | Fecha de lanzamiento |
| `genres` | Lista de géneros del juego |
| `platforms` | Plataformas disponibles |

---

## 🛡️ Manejo de Errores

El script maneja robustamente **5 tipos de errores**:

| Error | Causa | Acción |
|-------|-------|--------|
| Variable no definida | `RAWG_API_KEY` ausente | Mensaje descriptivo + `exit 1` |
| `401 Unauthorized` | API Key inválida | Mensaje + `exit 1` |
| `404 Not Found` | Endpoint incorrecto | Mensaje + URL consultada |
| `ConnectionError` | Sin acceso a internet | Mensaje de red + `exit 1` |
| `Timeout` | Servidor no responde en 10s | Mensaje de timeout + `exit 1` |

---

## 🔄 Pipeline CI/CD (Jenkins)

```
GitHub Repo → BuildAppJob → Docker Build → Docker Run → Exited (0)
     ↑                ↑
SamplePipeline    clona repo y ejecuta build.sh
```

**SamplePipeline** orquesta dos etapas:
- **Preparation:** detiene y elimina el contenedor previo (con `catchError` para continuar si no existe)
- **Build:** ejecuta `BuildAppJob` que clona el repo y corre `build.sh`

---

## 📋 Dependencias

- Python 3.11+
- `requests==2.31.0`
- Docker
- Jenkins (para CI/CD)
