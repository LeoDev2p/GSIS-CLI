

```text
██   ██ ██████  ██████  ██████  ████████  ▄████▄  
██ ▄█   ██▄▄██▄   ██    ██▄▄██▄    ██     ██▄▄██   
██▀██   ██   ██ ██████  ██         ██     ██  ██  
                                          V0.2.0
```

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/security-Argon2%20%2B%20PBKDF2%20%2B%20Fernet-red.svg)](https://github.com/yourusername/GSIS-CLI)
[![SQLite](https://img.shields.io/badge/database-SQLite-blue.svg)](https://www.sqlite.org/)

**Un gestor de contraseñas seguro y robusto con interfaz de línea de comandos.**

</div>

Bóveda segura de credenciales con interfaz de línea de comandos.

Password manager en Python (patrón MVC) que combina cifrado de nivel empresarial:
Argon2id para hashing, PBKDF2 para derivación de claves y Fernet (AES-256) para el cifrado de credenciales.

## Caracteristicas

- Autenticacion con master password (Argon2id)
- Credenciales maestras (MASTER_KEY y SALT) cargadas desde USB (`key/key.key`)
- Cifrado Fernet con derivacion PBKDF2 (480k iteraciones)
- CRUD completo de credenciales y categorias
- Busqueda por filtros y coincidencia (LIKE)
- Update/Delete con seleccion visual por ID
- Cubo de fuerza bruta: borrado de la BD tras 3 intentos fallidos
- Descifrado tolerante: filas cifradas con un SALT anterior se muestran como `[no descifrado]`
- Interfaz moderna: banner ASCII, tablas con bordes y colores ANSI

## Instalacion

Requisitos: Python 3.10+ y [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/LeoDev2p/GSIS-CLI.git
cd GSIS-CLI
uv sync
```

### Configuracion

Edita `.env` con tu email y el nombre de la base de datos:

```env
SUPERUSER = "tu_email@example.com"
NAME_BD = "Secure.db"
```

El hash de la master password y el SALT se generan automaticamente al registrar las credenciales en el USB (primera ejecucion, opcion "Configuracion"). No hace falta crear nada a mano.

> Importante: la aplicacion necesita una unidad USB conectada para leer/escribir `key/key.key`. Sin la llave original, los datos cifrados no pueden descifrarse.

## Uso

```bash
uv run python main.py
```

Menú principal:

```
  KRIPTA · Menú principal
    01  Crear base de datos
    02  Agregar categorías
    03  Eliminar categorías
    04  Agregar datos
    05  Consultar datos
    06  Actualizar datos
    07  Eliminar datos
    08  Salir
```

## Seguridad

| Componente   | Tecnologia          | Proposito                                          |
|--------------|---------------------|------------------------------------------------------|
| Hashing      | Argon2id            | Proteccion de la master password                    |
| Key derivation | PBKDF2-HMAC-SHA256 | Generacion de la clave de cifrado (480k iteraciones) |
| Cifrado      | Fernet (AES-256)    | Cifrado de credenciales en la base de datos        |
| Almacenamiento| USB `key/key.key`   | MASTER_KEY y SALT fuera del repositorio             |
| Anti fuerza bruta | 3 intentos    | Borrado automatico de la base de datos              |

## Licencia

MIT. Ver `LICENSE`.
