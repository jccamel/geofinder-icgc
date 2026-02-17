# GeoFinder MCP Server

> **Geocoding server for Catalonia** using the ICGC service through the Model Context Protocol.  
> 🔄 Completely asynchronous architecture with **integrated smart caching**.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.13+-green.svg)](https://gofastmcp.com)
[![License: GPL-2.0](https://img.shields.io/badge/License-GPL--2.0-yellow.svg)](LICENSE)

---

## 📚 Quick Guide

| Section | Description |
|---------|-------------|
| [🚀 Quick Start](#-quick-start) | Install and run in 2 minutes |
| [🛠️ Tools](#️-tools) | 5 available MCP tools |
| [🔌 Integration](#-integration-with-claude-desktop) | Connect with Claude Desktop |
| [⚙️ Configuration](#️-advanced-configuration) | Environment variables and options |
| [🐛 Troubleshooting](#-troubleshooting) | Common troubleshooting |

---

## 🚀 Quick Start

### Installation

```bash
# Option 1: PyPI (recommended for users)
pip install geofinder-icgc[mcp,pyproj]

# Option 2: Development
git clone https://github.com/jccamel/geofinder-icgc.git
cd geofinder-icgc
uv pip install -e ".[mcp,dev,pyproj]"
```

### Run the Server

```bash
# Run as Python module
python -m geofinder.mcp_server

# HTTP (for local testing)
python -m geofinder.mcp_server --transport http --port 8000
```

### Test with the Inspector

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run
npx @modelcontextprotocol/inspector python -m geofinder.mcp_server
```

---

## 🛠️ Tools

The server provides **10 tools** for geocodification:

### Summary Table

| # | Tool | Usage | Example |
|---|-------------|-----|---------|
| 9 | 🔎 `parse_search_query` | Detector inteligente | Analiza tipo de consulta |

<details>
<summary><strong>📖 Documentación Detallada de Herramientas</strong></summary>

### 1. `find_place` - Búsqueda General

Busca lugares con detección automática del tipo de consulta.

**Parámetros:**
- `query` (string): Texto de búsqueda
- `default_epsg` (int): Sistema de referencia (default: 25831)
- `size` (int, opcional): Máximo de resultados

**Tipos soportados:**
- Topónimos: `"Montserrat"`, `"Barcelona"`
- Coordenadas: `"430000 4580000 EPSG:25831"`
- Direcciones: `"Barcelona, Diagonal 100"`
- Carreteras: `"C-32 km 10"`

**Respuesta:**
```json
[{
  "nom": "Barcelona",
  "nomTipus": "Municipi",
  "x": 2.1734,
  "y": 41.3851,
  "epsg": 4326
}]
```

---

### 2. `find_reverse` - Geocodificación Inversa

Encuentra lugares en coordenadas dadas.

#### 📺 Demostración: Coordenadas a DMS
Ejemplo de cómo obtener coordenadas en grados minutos y segundos a partir de unas decimales utilizando el MCP:

![Ejemplo de coordenadas DMS con MCP](assets/media/reverse.mp4)

**Parámetros:**
- `longitude`, `latitude` (float): Coordenadas
- `epsg` (int): Sistema de referencia (4326, 25831, 3857)
- `layers` (string): Capas a buscar (`"address,tops,pk"`)
- `max_results` (int): Máximo resultados (default: 5)

**Ejemplo:**
```json
{
  "longitude": 2.1734,
  "latitude": 41.3851,
  "epsg": 4326
}
```

---

### 3. `autocomplete` - Autocompletado

Sugerencias para búsqueda tipo "as you type".

**Parámetros:**
- `partial_text` (string): Texto parcial
- `max_suggestions` (int): Máximo sugerencias (default: 10)

---

### 4. `find_address` - Búsqueda Estructurada (MEJORADO)

Búsqueda precisa con componentes separados. Usa método interno para mayor precisión.

**Parámetros:**
- `street`, `number` (string): **Requeridos**
- `municipality` (string): Recomendado para precisión
- `street_type` (string): Tipo de vía (default: "Carrer")
- `size` (int, opcional): Máximo de resultados

**Ejemplo:**
```json
{
  "street": "Diagonal",
  "number": "100",
  "municipality": "Barcelona",
  "street_type": "Avinguda"
}
```

---

### 5. `find_road_km` - Punto Kilométrico 🆕

Busca puntos kilométricos específicos en carreteras.

**Parámetros:**
- `road` (string): Código de carretera (ej: "C-32", "AP-7")
- `kilometer` (float): Kilómetro (puede ser decimal)

**Ejemplo:**
```json
{
  "road": "C-32",
  "kilometer": 10.5
}
```

**Formatos aceptados:** C-32, C32, AP7, AP-7, N-II, A-2

---

### 6. `find_by_coordinates` - Búsqueda Avanzada 🆕

Búsqueda con control de radio y filtrado de capas.

**Parámetros:**
- `x`, `y` (float): Coordenadas
- `epsg` (int): Sistema de referencia (default: 25831)
- `search_radius_km` (float): Radio en km (default: 0.05 = 50m)
- `layers` (string): Capas (`"address,tops,pk"`)
- `max_results` (int): Máximo resultados (default: 5)

**Radios comunes:**
- 0.01 = 10 metros (muy preciso)
- 0.05 = 50 metros (default)
- 0.5 = 500 metros (área amplia)

**Ejemplo:**
```json
{
  "x": 430000,
  "y": 4580000,
  "epsg": 25831,
  "search_radius_km": 0.1,
  "layers": "address"
}
```

---

### 7. `transform_coordinates` - Conversión EPSG

Transforma entre sistemas de referencia.

**Parámetros:**
- `x`, `y`, `from_epsg` (required)
- `to_epsg` (opcional, default: 4326)

**Sistemas comunes:**
- `4326`: WGS84 (GPS)
- `25831`: ETRS89 UTM 31N (Cataluña)
- `3857`: Web Mercator

**Respuesta:**
```json
{
  "success": true,
  "x": 2.1734,
  "y": 41.3851,
  "from_epsg": 25831,
  "to_epsg": 4326
}
```

> **⚠️ Requiere:** `pip install geofinder-icgc[pyproj]`

---

### 8. `search_nearby` - Búsqueda de Proximidad 🆕

Busca lugares cerca de una ubicación nombrada.

**Parámetros:**
- `place_name` (string): Lugar de referencia
- `radius_km` (float): Radio en km (default: 1.0)
- `layers` (string): Capas a buscar
- `max_results` (int): Máximo resultados (default: 10)

**Casos de uso:**
- "Buscar cerca de Barcelona"
- "Hoteles cerca del Montserrat"
- "Direcciones cerca de Sagrada Família"

**Ejemplo:**
```json
{
  "place_name": "Montserrat",
  "radius_km": 5.0,
  "layers": "tops",
  "max_results": 20
}
```

**Nota:** Incluye el lugar de referencia + lugares cercanos

---

### 9. `parse_search_query` - Detector Inteligente 🆕

Analiza consultas y detecta su tipo automáticamente.

**Parámetro:**
- `query` (string): Texto a analizar

**Respuesta:**
```json
{
  "query_type": "coordinate",
  "confidence": "high",
  "details": {"x": 430000, "y": 4580000, "epsg": 25831},
  "suggestion": "Use find_by_coordinates()",
  "example": "find_by_coordinates(430000, 4580000, epsg=25831)"
}
```

**Tipos detectados:**
- `coordinate`: Coordenadas
- `rectangle`: Área rectangular
- `road`: Carretera + km
- `address`: Dirección postal
- `placename`: Topónimo (por defecto)

**Uso:** Ayuda al AI a decidir qué herramienta usar



</details>

---

## 🔌 Integración con Claude Desktop

### Configuración

**Archivo:** `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

```json
{
  "mcpServers": {
    "geofinder": {
      "command": "python",
      "args": ["-m", "geofinder.mcp_server"],
      "env": {
        "ICGC_URL": "https://eines.icgc.cat"
      }
    }
  }
}
```

<details>
<summary><strong>Otras opciones de configuración</strong></summary>

### Con `geofinder-icgc` (si está en PATH)

```json
{
  "mcpServers": {
    "geofinder": {
      "command": "geofinder-icgc"
    }
  }
}
```

### Con `uv` (desarrollo)

```json
{
  "mcpServers": {
    "geofinder": {
      "command": "uv",
      "args": ["run", "python", "-m", "geofinder.mcp_server"],
      "cwd": "C:\\ruta\\completa\\a\\geofinder-icgc"
    }
  }
}
```

</details>

### Reiniciar Claude

Cierra completamente Claude Desktop y vuelve a abrirlo para aplicar los cambios.

---

## ⚙️ Configuración Avanzada

### Variables de Entorno

Crea `.env` en el directorio del proyecto:

```bash
# Servicio ICGC
ICGC_URL=https://eines.icgc.cat
GEOFINDER_TIMEOUT=5

# FastMCP
FASTMCP_LOG_LEVEL=INFO
FASTMCP_MASK_ERROR_DETAILS=False
```

<details>
<summary><strong>Todas las variables disponibles</strong></summary>

| Variable | Descripción | Default |
|----------|-------------|---------|
| `ICGC_URL` | URL del geocodificador | `https://eines.icgc.cat` |
| `GEOFINDER_TIMEOUT` | Timeout peticiones (s) | `5` |
| `FASTMCP_LOG_LEVEL` | Nivel logging | `INFO` |
| `FASTMCP_MASK_ERROR_DETAILS` | Ocultar errores | `False` |
| `FASTMCP_STRICT_INPUT_VALIDATION` | Validación estricta | `False` |
| `FASTMCP_INCLUDE_FASTMCP_META` | Incluir metadata | `True` |

</details>

### Opciones de Línea de Comandos

```bash
# Ver todas las opciones
python -m geofinder.mcp_server --help

# Ejemplos
python -m geofinder.mcp_server --transport http --port 8000
python -m geofinder.mcp_server --log-level DEBUG
python -m geofinder.mcp_server --transport http --host 0.0.0.0
```

---

## 🐛 Solución de Problemas

### Problemas Comunes

<details>
<summary><strong>❌ Comando no encontrado: `geofinder-icgc`</strong></summary>

**Solución:**
```bash
# Usar forma de módulo
python -m geofinder.mcp_server

# O reinstalar
pip install --force-reinstall geofinder[mcp]
```

</details>

<details>
<summary><strong>❌ Error de conexión con ICGC</strong></summary>

**Verificar configuración:**
```bash
# Windows
echo %ICGC_URL%

# Linux/macOS
echo $ICGC_URL
```

**Aumentar timeout:**
```bash
export GEOFINDER_TIMEOUT=10  # Linux/macOS
set GEOFINDER_TIMEOUT=10     # Windows
```

</details>

<details>
<summary><strong>❌ Claude Desktop no encuentra el servidor</strong></summary>

1. **Verificar ruta del archivo de configuración**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. **Usar ruta absoluta a Python:**
   ```json
   {
     "command": "C:\\Python312\\python.exe",
     "args": ["-m", "geofinder.mcp_server"]
   }
   ```

3. **Reiniciar Claude Desktop completamente**

</details>

<details>
<summary><strong>❌ Error de importación de módulos</strong></summary>

**Verificar entorno virtual:**
```bash
# Windows
where python

# Linux/macOS
which python
```

**Reinstalar:**
```bash
pip install -e ".[mcp,pyproj]"
```

</details>

<details>
<summary><strong>❌ Error transformación de coordenadas</strong></summary>

**Instalar pyproj:**
```bash
pip install geofinder-icgc[pyproj]
```

**Alternativa GDAL:**
```bash
pip install geofinder-icgc[gdal]
```

</details>

### Debugging

```bash
# Logs detallados
python -m geofinder.mcp_server --log-level DEBUG

# Verificar puerto (HTTP mode)
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/macOS
```

---

## 📚 Recursos

- [Documentación FastMCP](https://gofastmcp.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Geocodificador ICGC](https://www.icgc.cat/es/Herramientas-y-visores/Herramientas/Geocodificador-ICGC)
- [Repositorio GitHub](https://github.com/jccamel/geofinder-icgc)
- [Issues](https://github.com/jccamel/geofinder-icgc/issues)

---

## 💡 ¿Qué es MCP?

El [Model Context Protocol](https://modelcontextprotocol.io) es un estándar abierto que permite a las aplicaciones de IA conectarse con fuentes de datos y herramientas de forma segura y estandarizada.

**GeoFinder MCP** permite que asistentes como Claude Desktop accedan a:
- 🔍 Geocodificación de Cataluña
- 📍 Búsqueda inversa de coordenadas
- 🗺️ Transformación entre sistemas EPSG
- ⌨️ Autocompletado inteligente
- 🚀 **Caché en memoria** para respuestas instantáneas
- 🛡️ **Validación robusta** con Pydantic

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

Basado en el plugin OpenICGC del ICGC.
<!-- YOLO Badge Retry: Small change for badge obtainment 🤘 -->
