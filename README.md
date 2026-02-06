# GSIS-CLI - Gestor Seguro de Información Sensible

![GSIS-CLI Banner](./assets/banner.svg)

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/security-Argon2%20%2B%20Fernet-red.svg)](https://github.com/yourusername/GSIS-CLI)
[![SQLite](https://img.shields.io/badge/database-SQLite-blue.svg)](https://www.sqlite.org/)

**Un gestor de contraseñas seguro y robusto con interfaz de línea de comandos**

[Características](#características) • [Instalación](#instalación) • [Uso](#uso) • [Seguridad](#seguridad) • [Documentación](#documentación)

</div>

---

## 📋 Descripción

**GSIS-CLI** (Gestor Seguro de Información Sensible - CLI) es un administrador de contraseñas profesional desarrollado en Python que combina seguridad de nivel empresarial con una interfaz de línea de comandos intuitiva. Diseñado siguiendo el patrón arquitectónico **MVC (Modelo-Vista-Controlador)**, garantiza la máxima protección de tus credenciales mediante algoritmos de cifrado y hashing de última generación.

### 🎯 ¿Por qué GSIS-CLI?

- **🔒 Seguridad Robusta**: Implementa Argon2id para hashing y Fernet (AES-256) para cifrado
- **🏗️ Arquitectura Profesional**: Código limpio siguiendo principios SOLID y patrón MVC
- **📊 Gestión Inteligente**: Organiza tus contraseñas por categorías con fechas de expiración
- **🔍 Búsquedas Avanzadas**: Múltiples filtros para encontrar tus credenciales rápidamente
- **📝 Registro Completo**: Sistema de logging para auditoría y debugging
- **💻 Interfaz Intuitiva**: CLI moderna y fácil de usar

---

## ✨ Características

### 🔐 Seguridad Avanzada

- **Autenticación Robusta**: Sistema de login con credenciales maestras
- **Hashing Argon2id**: Protección contra ataques de fuerza bruta y rainbow tables
- **Cifrado Fernet (AES-256)**: Cifrado simétrico de última generación para datos sensibles
- **Validación de Contraseñas**: Verificación de integridad mediante hashes

### 📂 Gestión de Datos

- **Base de Datos SQLite**: Almacenamiento local seguro y eficiente
- **Categorización**: Organiza tus credenciales por categorías personalizadas
- **Campos Completos**: Almacena sitio, URL, usuario, email, contraseña, nivel de seguridad
- **Fechas de Expiración**: Control de vencimiento de contraseñas
- **Última Modificación**: Seguimiento de cambios con timestamps

### 🔍 Filtros y Búsquedas

1. **Ver Todo**: Consulta todas las credenciales almacenadas
2. **Por Sitio Web**: Busca credenciales específicas por nombre del sitio
3. **Por Categoría**: Filtra por tipo de servicio (redes sociales, bancos, etc.)
4. **Por Fecha**: Busca por mes/año de última modificación
5. **Por Rango de Fechas**: Consulta credenciales modificadas en un período específico

### ⚙️ Operaciones CRUD

- ✅ **Create**: Agregar nuevas credenciales y categorías
- 📖 **Read**: Consultar con múltiples filtros
- ✏️ **Update**: Actualizar credenciales existentes
- 🗑️ **Delete**: Eliminar registros con confirmación

---

## 🚀 Instalación

### Prerrequisitos

- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)
- **Git** (opcional, para clonar el repositorio)

### Pasos de Instalación

#### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/yourusername/GSIS-CLI.git
cd GSIS-CLI
```

#### 2️⃣ Crear Entorno Virtual (Recomendado)

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux/MacOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

#### 4️⃣ Configurar Variables de Entorno

Crea o edita el archivo `.env` en la raíz del proyecto:

```env
# Credenciales de Autenticación
SUPERUSER = "tu_email@ejemplo.com"
MASTER_KEY = "$argon2id$v=19$m=65536,t=3,p=2$..." # Hash de tu contraseña maestra

# Clave de Cifrado Fernet
SECRET_KEY_FERNET = "tu_clave_fernet_aqui"

# Nombre de la Base de Datos
NAME_BD = "Secure.db"
```

> **⚠️ IMPORTANTE**: Nunca compartas tu archivo `.env`. Ya está incluido en `.gitignore`

#### 5️⃣ Generar Claves de Seguridad

Para generar tu propia clave Fernet:

```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

Para generar el hash de tu contraseña maestra:

```python
from argon2 import PasswordHasher
ph = PasswordHasher()
print(ph.hash("tu_contraseña_maestra"))
```

---

## 📖 Uso

### Iniciar la Aplicación

```bash
python main.py
```

### Menú Principal

Una vez autenticado, verás el siguiente menú:

```
╔═══════════════════════════════════════════╗
║           GSIS-CLI - MAIN MENU            ║
╚═══════════════════════════════════════════╝

1. 📊 Create Tables (Primera vez)
2. 📁 Add Category
3. ➕ Add New Credential
4. 🔍 Search/Filter Credentials
5. ✏️  Update Credential
6. 🗑️  Delete Credential
7. 🚪 Exit

Select an option:
```

### Flujo de Trabajo Típico

#### 1. Primera Ejecución - Crear Tablas

En el primer uso, selecciona la opción **1** para crear las tablas de la base de datos:

```bash
Select an option: 1
✅ Tables created successfully
```

#### 2. Agregar Categorías

Organiza tus credenciales creando categorías:

```bash
Select an option: 2
Enter category name: Redes Sociales
✅ Redes Sociales added successfully
```

**Categorías sugeridas**: Correos, Bancos, Redes Sociales, Trabajo, Streaming, Juegos, etc.

#### 3. Agregar Credenciales

Guarda una nueva contraseña:

```bash
Select an option: 3

📝 Enter credential details:
Site name: Facebook
Category: Redes Sociales
URL: https://facebook.com
Username: mi_usuario
Email: usuario@ejemplo.com
Password: ************
Expiry days: 90
Security level (1-5): 4

✅ Data successfully inserted
```

#### 4. Buscar Credenciales

Accede a tus contraseñas guardadas:

```bash
Select an option: 4

╔═══════════════════════════════════════════╗
║          SEARCH/FILTER MENU               ║
╚═══════════════════════════════════════════╝

1. 📋 View All
2. 🔍 Search by Site Name
3. 📁 Search by Category
4. 📅 Search by Month/Year
5. 📆 Search by Date Range
6. ⬅️  Back

Select filter:
```

#### 5. Actualizar Contraseñas

Modifica credenciales existentes:

```bash
Select an option: 5
Enter site name: Facebook

[Muestra datos actuales]

Do you want to update? (S/N): S
Enter new username: nuevo_usuario
Enter new password: ************
...
✅ Facebook successfully updated
```

#### 6. Eliminar Credenciales

Borra registros que ya no necesitas:

```bash
Select an option: 6
Enter credential ID: 5

[Muestra información del registro]

Confirm deletion? (S/N): S
✅ Facebook successfully removed
```

---

## 🔐 Seguridad

### Tecnologías Implementadas

| Componente | Tecnología | Propósito |
|------------|------------|-----------|
| **Hashing** | Argon2id | Protección de contraseña maestra |
| **Cifrado** | Fernet (AES-256) | Cifrado de datos sensibles |
| **Base de Datos** | SQLite | Almacenamiento local |
| **Logging** | Python logging | Registro de operaciones |

### Buenas Prácticas Implementadas

✅ **Separación de Credenciales**: Variables de entorno en `.env`  
✅ **Cifrado en Reposo**: Contraseñas cifradas en la BD  
✅ **Validación de Entrada**: Prevención de inyección SQL  
✅ **Manejo de Excepciones**: Sistema robusto de errores personalizados  
✅ **Logging Seguro**: No se registran datos sensibles en logs  
✅ **Arquitectura Modular**: Separación de responsabilidades (MVC)

### Recomendaciones de Seguridad

🔒 **Contraseña Maestra Fuerte**: Mínimo 16 caracteres con mayúsculas, minúsculas, números y símbolos  
🔒 **Backup Seguro**: Respalda tu archivo `Secure.db` en un lugar cifrado  
🔒 **Actualización Regular**: Cambia tus contraseñas periódicamente  
🔒 **No Compartas**: Nunca compartas tu `.env` o base de datos

---

## 📁 Estructura del Proyecto

```
GSIS-CLI/
│
├── 📄 main.py                          # Punto de entrada de la aplicación
├── 📄 requirements.txt                 # Dependencias del proyecto
├── 📄 .env                             # Variables de entorno (NO compartir)
├── 📄 .gitignore                       # Archivos ignorados por Git
├── 📄 README.md                        # Este archivo
│
├── 📂 controllers/                     # Lógica de negocio
│   ├── Auth_controller.py              # Autenticación de usuarios
│   └── Database_controllers.py         # Operaciones CRUD
│
├── 📂 models/                          # Modelos de datos
│   ├── database.py                     # Configuración de BD
│   ├── safe_models.py                  # Modelo de credenciales
│   └── category_models.py              # Modelo de categorías
│
├── 📂 views/                           # Interfaz de usuario
│   └── app.py                          # Vistas CLI
│
├── 📂 security/                        # Módulos de seguridad
│   ├── encryption.py                   # Cifrado Fernet
│   └── hashing.py                      # Hashing Argon2
│
├── 📂 core/                            # Configuración central
│   ├── config.py                       # Configuración global
│   ├── logger.py                       # Sistema de logs
│   └── Exceptions.py                   # Excepciones personalizadas
│
├── 📂 utils/                           # Utilidades
│   └── utils.py                        # Funciones auxiliares
│
├── 📂 db/                              # Base de datos
│   └── Secure.db                       # BD SQLite (generada)
│
└── 📂 log/                             # Archivos de log
    └── app.log                         # Logs de la aplicación
```

---

## 🛠️ Tecnologías Utilizadas

- **[Python 3.8+](https://www.python.org/)** - Lenguaje de programación
- **[Argon2-cffi](https://argon2-cffi.readthedocs.io/)** - Hashing de contraseñas
- **[Cryptography](https://cryptography.io/)** - Cifrado Fernet (AES-256)
- **[SQLite](https://www.sqlite.org/)** - Base de datos embebida
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** - Manejo de variables de entorno

---

## 🤝 Contribución

Las contribuciones son bienvenidas. Para contribuir:

1. **Fork** el proyecto
2. Crea una **rama** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. Abre un **Pull Request**

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

## 👤 Autor

**LeoDev Development**

- 📧 Email: whoamy0608@gmail.com
- 🌐 GitHub: [@LeoDev2p](https://github.com/LeoDev2p)

---

## 🙏 Agradecimientos

- A la comunidad de Python por las excelentes librerías de seguridad
- A todos los contribuidores y usuarios de GSIS-CLI
- Inspirado en las mejores prácticas de gestión de credenciales

---

<div align="center">

**⭐ Si te resulta útil este proyecto, considera darle una estrella en GitHub ⭐**

Hecho con ❤️ por Kriptom Development

</div>
