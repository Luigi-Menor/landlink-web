# LandLink - Plataforma de Conexión Comunitaria

LandLink es una aplicación web completa que conecta organizadores de proyectos comunitarios con voluntarios. La plataforma facilita la gestión de proyectos sociales, eventos comunitarios y la participación voluntaria a través de un sistema robusto de roles y permisos.

## 🏗️ Arquitectura del Sistema

### Backend (Python Flask)
- **Framework**: Flask con arquitectura modular
- **Base de Datos**: SQL Server con SQLAlchemy ORM
- **Autenticación**: Sistema híbrido (Sesiones + JWT)
- **Seguridad**: Bcrypt, CSRF Protection, Rate Limiting
- **Migraciones**: Flask-Migrate con Alembic

### Frontend (HTML/CSS/JavaScript)
- **Templates**: Jinja2 con herencia de plantillas
- **Estilos**: CSS3 con variables personalizadas y diseño responsivo
- **Interactividad**: JavaScript vanilla con funcionalidades modales y AJAX
- **UI/UX**: Diseño moderno con componentes reutilizables

## 🚀 Características Principales

### 🔐 Sistema de Autenticación y Autorización
- **Registro de usuarios** con validación de email
- **Inicio de sesión** con protección contra ataques de fuerza bruta
- **Recuperación de contraseña** por email
- **Sistema de roles**: Administrador, Organizador, Voluntario
- **Gestión de sesiones** con tokens JWT y cookies seguras
- **Bloqueo automático** después de múltiples intentos fallidos

### 👥 Gestión de Usuarios
- **Perfiles de usuario** con información personal
- **Cambio de roles** por administradores
- **Estados de usuario**: Activo, Inactivo, Bloqueado
- **Historial de actividades** y auditoría completa
- **Gestión de organizaciones** y membresías

### 📋 Gestión de Proyectos y Eventos
- **Creación de eventos** con información detallada
- **Sistema de áreas de intervención** para categorización
- **Gestión de recursos** y requisitos
- **Estados de eventos**: Pendiente, Activo, Cancelado, Finalizado
- **Eliminación de eventos** con confirmación
- **Sistema de comentarios y calificaciones**

### 🤝 Sistema de Participación
- **Solicitudes de participación** en eventos
- **Aprobación/rechazo** de solicitudes por organizadores
- **Historial de participación** para voluntarios
- **Seguimiento de horas** y actividades completadas
- **Sistema de roles en eventos** (Coordinador, Asistente, etc.)

### 🛠️ Panel de Administración
- **Dashboard administrativo** con estadísticas globales
- **Gestión de usuarios** (crear, editar, bloquear, cambiar roles)
- **Gestión de organizaciones** y tipos de organización
- **Monitoreo de actividades** y logs del sistema
- **Configuración del sistema** y parámetros globales

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.8+** - Lenguaje principal
- **Flask** - Framework web
- **SQLAlchemy** - ORM para base de datos
- **Flask-Login** - Gestión de sesiones de usuario
- **Flask-JWT-Extended** - Autenticación JWT
- **Flask-Bcrypt** - Hash de contraseñas
- **Flask-WTF** - Formularios y CSRF protection
- **Flask-Migrate** - Migraciones de base de datos
- **pyodbc** - Conector para SQL Server
- **email-validator** - Validación de emails
- **python-dotenv** - Gestión de variables de entorno

### Frontend
- **HTML5** - Estructura semántica
- **CSS3** - Estilos con variables personalizadas
- **JavaScript ES6+** - Interactividad del cliente
- **Jinja2** - Motor de plantillas
- **Font Awesome** - Iconografía
- **Responsive Design** - Adaptable a dispositivos móviles

### Base de Datos
- **SQL Server** - Base de datos principal
- **Migraciones** - Control de versiones de esquema
- **Relaciones complejas** - Muchos a muchos, claves foráneas
- **Índices optimizados** - Para consultas eficientes

## 📁 Estructura del Proyecto

```
landlink-final12/
├── app/                          # Aplicación principal
│   ├── __init__.py              # Configuración de la app
│   ├── config.py                # Configuraciones del sistema
│   ├── models/                   # Modelos de base de datos
│   │   ├── user.py              # Usuarios y roles
│   │   ├── event.py             # Eventos y solicitudes
│   │   ├── organization.py       # Organizaciones
│   │   ├── activity.py          # Actividades e historial
│   │   └── resource.py          # Recursos y gestión
│   ├── views/                    # Controladores de vistas
│   │   ├── auth.py              # Autenticación
│   │   ├── admin.py             # Panel administrativo
│   │   ├── organizer.py         # Panel de organizador
│   │   └── volunteer.py         # Panel de voluntario
│   ├── controllers/              # Lógica de negocio
│   │   ├── auth.py              # Controlador de autenticación
│   │   └── project.py           # Controlador de proyectos
│   ├── forms/                    # Formularios WTF
│   │   └── login_form.py        # Formulario de login
│   ├── auth/                     # Autenticación JWT
│   │   ├── jwt_auth.py          # Configuración JWT
│   │   └── routes.py            # Rutas de API
│   ├── utils/                    # Utilidades
│   │   ├── security.py          # Funciones de seguridad
│   │   ├── validators.py        # Validadores personalizados
│   │   ├── data_structures.py   # Estructuras de datos
│   │   └── error_handlers.py    # Manejo de errores
│   ├── static/                   # Archivos estáticos
│   │   ├── css/                 # Hojas de estilo
│   │   ├── js/                  # JavaScript
│   │   └── uploads/             # Archivos subidos
│   └── templates/               # Plantillas HTML
│       ├── base.html            # Plantilla base
│       ├── admin/               # Templates administrativos
│       ├── auth/                # Templates de autenticación
│       ├── organizer/           # Templates de organizador
│       └── volunteer/           # Templates de voluntario
├── migrations/                   # Migraciones de base de datos
├── requirements.txt             # Dependencias Python
├── run.py                       # Punto de entrada
└── README.md                    # Este archivo
```

## 🔧 Instalación y Configuración

### Requisitos del Sistema
- **Python 3.8+**
- **SQL Server** (2016 o superior)
- **pip** (gestor de paquetes Python)
- **Git** (control de versiones)

### Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd landlink-final12
```

2. **Crear entorno virtual**
```bash
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Crear archivo .env
SECRET_KEY=tu-clave-secreta-aqui
JWT_SECRET_KEY=tu-jwt-clave-secreta-aqui
DATABASE_URL=mssql+pyodbc://usuario:contraseña@servidor/base_de_datos?driver=ODBC+Driver+17+for+SQL+Server
FLASK_CONFIG=development
```

5. **Configurar base de datos**
```bash
# Ejecutar migraciones
flask db upgrade

# Inicializar datos básicos
python run.py
```

6. **Ejecutar la aplicación**
```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## 🎯 Funcionalidades Detalladas

### 🔐 Autenticación y Seguridad
- **Registro seguro** con validación de email
- **Login con protección** contra ataques de fuerza bruta
- **Recuperación de contraseña** por email
- **Sesiones seguras** con cookies HTTPOnly
- **Protección CSRF** en todos los formularios
- **Hash de contraseñas** con Bcrypt (12 rounds)

### 👤 Gestión de Usuarios
- **Perfiles completos** con información personal
- **Sistema de roles** jerárquico (Admin > Organizador > Voluntario)
- **Estados de usuario** (Activo, Inactivo, Bloqueado)
- **Historial de cambios** con auditoría completa
- **Gestión de organizaciones** y membresías

### 📅 Gestión de Eventos
- **Creación de eventos** con información detallada
- **Sistema de áreas** de intervención
- **Gestión de recursos** y requisitos
- **Estados de eventos** (Pendiente, Activo, Cancelado, Finalizado)
- **Eliminación segura** con confirmación
- **Sistema de comentarios** y calificaciones

### 🤝 Participación Voluntaria
- **Solicitudes de participación** en eventos
- **Aprobación/rechazo** por organizadores
- **Historial de participación** detallado
- **Seguimiento de horas** y actividades
- **Sistema de roles** en eventos

### 🛠️ Panel Administrativo
- **Dashboard** con estadísticas en tiempo real
- **Gestión de usuarios** completa
- **Monitoreo de actividades** y logs
- **Configuración del sistema**
- **Reportes y análisis**

## 🔒 Seguridad

- **Autenticación robusta** con múltiples capas
- **Protección CSRF** en todos los formularios
- **Validación de entrada** en todos los endpoints
- **Hash seguro** de contraseñas
- **Sesiones seguras** con cookies HTTPOnly
- **Rate limiting** para prevenir ataques
- **Auditoría completa** de actividades

## 📊 Base de Datos

### Modelos Principales
- **User**: Usuarios del sistema
- **Role**: Roles de usuario
- **Organization**: Organizaciones
- **Event**: Eventos y proyectos
- **SolicitudEvento**: Solicitudes de participación
- **HistorialActividad**: Registro de actividades
- **AreaIntervencion**: Áreas de trabajo
- **TipoOrganizacion**: Tipos de organización

### Relaciones
- **Muchos a muchos**: Usuarios-Organizaciones, Eventos-Áreas
- **Uno a muchos**: Usuario-Eventos, Organización-Eventos
- **Auditoría**: Historial de cambios y actividades

## 🎨 Frontend

### Diseño
- **Responsive Design** adaptable a todos los dispositivos
- **CSS Grid y Flexbox** para layouts modernos
- **Variables CSS** para consistencia visual
- **Componentes reutilizables** para eficiencia

### Interactividad
- **JavaScript vanilla** para funcionalidades
- **Modales dinámicos** para confirmaciones
- **Validación en tiempo real** de formularios
- **AJAX** para operaciones asíncronas

## 🚀 Despliegue

### Configuración de Producción
1. **Variables de entorno** configuradas
2. **Base de datos** en servidor dedicado
3. **HTTPS** habilitado
4. **Logs** configurados
5. **Backup** de base de datos

### Consideraciones de Seguridad
- **Claves secretas** únicas y seguras
- **Conexión segura** a base de datos
- **Cookies seguras** en producción
- **Validación** de todas las entradas

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## 🤝 Contribución

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Realiza los cambios
4. Envía un Pull Request

## 📞 Soporte

Para soporte técnico o preguntas sobre el proyecto, contacta al equipo de desarrollo.
