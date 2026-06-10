# TP3 Backend 
Desarrollo Back-End de una aplicacion Web
## Participantes

- Tiziano Longo
- Pedro Osorio
- Hernan Condori
- Lucas Vera
- Facundo Nunes
- Lucas Fontana
- Agustin Tarcaya 
- Rodrigo Cuellar
- Yachak Vilcapuma

## Credenciales por defecto

> Este proyecto es únicamente para fines educativos y de desarrollo.  
> **No utilizar en producción.**

Configuración utilizada por el script `setup.sh`.

### Configuración MySQL

- **USER**: `root`
- **PASSWORD**: `password`

### Variables de entorno (.env)

```env
MYSQL_USER=root
MYSQL_NAME_DB=techlibre
MYSQL_PASSWORD=password
MYSQL_PORT=3306
MYSQL_HOST=127.0.0.1

FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

## Estructura del proyecto

- `app.py` → Archivo principal de la aplicación
- `database/` → Configuración y gestión de base de datos
- `services/` → Validación y lógica de endpoints
- `tests/` → Tests de confirmación

## Setup

Ejecutar:

```bash
bash setup.sh
```sos para poder visualizar esta aplicación

### 1. Clonar el repositorio
Tener Git instalado y ejecutar:

```bash
git clone <url>
```

### 2. Acceder a la carpeta clonada

```bash
cd tp3_ids_backend
```

### 3. Ejecutar el setup

```bash
bash setup.sh
```