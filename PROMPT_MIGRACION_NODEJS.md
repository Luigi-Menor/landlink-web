# 🚀 Prompt para Crear LandLink Backend con Node.js + Express

## 📋 Contexto del Proyecto

LandLink es una plataforma de conexión comunitaria que conecta organizadores de proyectos comunitarios con voluntarios. Este prompt define la creación completa del backend desde cero usando Node.js + Express, manteniendo toda la lógica de negocio y funcionalidades de la plataforma original.

## 🏗️ Arquitectura Objetivo (Node.js + Express)

### Tecnologías a Utilizar:
- **Backend**: Node.js + Express.js
- **Base de Datos**: SQL Server con Sequelize ORM
- **Autenticación**: JWT (Access + Refresh Tokens)
- **Seguridad**: bcryptjs, helmet, rate limiting, CORS
- **Migraciones**: Sequelize CLI

### Modelos de Base de Datos:
1. **User** - Usuarios del sistema
2. **Role** - Roles de usuario (administrador, organizador, voluntario)
3. **Organization** - Organizaciones
4. **Event** - Eventos y proyectos
5. **SolicitudEvento** - Solicitudes de participación
6. **HistorialActividad** - Registro de actividades
7. **AreaIntervencion** - Áreas de trabajo
8. **TipoOrganizacion** - Tipos de organización
9. **Recurso** - Recursos de organizaciones
10. **ComentarioCalificacion** - Comentarios y calificaciones

## 🎯 Objetivo del Desarrollo

Crear un backend REST API completo desde cero en Node.js + Express que implemente toda la lógica de negocio de LandLink y esté optimizado para aplicaciones móviles y web.

## 🛠️ Stack Tecnológico Objetivo

### Backend:
- **Node.js** (v18+)
- **Express.js** (v4.18+)
- **Sequelize** como ORM
- **SQL Server** como base de datos
- **JWT** para autenticación
- **bcryptjs** para hash de contraseñas
- **express-rate-limit** para rate limiting
- **helmet** para seguridad
- **cors** para CORS
- **express-validator** para validación
- **multer** para upload de archivos

### Estructura de Proyecto:
```
landlink-backend/
├── src/
│   ├── controllers/          # Lógica de negocio
│   ├── models/              # Modelos de base de datos
│   ├── routes/              # Rutas de la API
│   ├── middleware/          # Middlewares personalizados
│   ├── services/            # Servicios de negocio
│   ├── utils/               # Utilidades
│   ├── config/              # Configuraciones
│   └── app.js               # Aplicación principal
├── migrations/              # Migraciones de base de datos
└── package.json
```

## 📊 Especificaciones de la API

### Autenticación y Autorización:
```javascript
// Endpoints de autenticación
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/refresh
POST /api/auth/forgot-password
POST /api/auth/reset-password
GET  /api/auth/me
PUT  /api/auth/profile
PUT  /api/auth/change-password
```

### Gestión de Usuarios:
```javascript
// Endpoints de usuarios (Admin)
GET    /api/users
GET    /api/users/:id
POST   /api/users
PUT    /api/users/:id
DELETE /api/users/:id
PUT    /api/users/:id/status
PUT    /api/users/:id/role
GET    /api/users/:id/activities
```

### Gestión de Eventos:
```javascript
// Endpoints de eventos
GET    /api/events
GET    /api/events/:id
POST   /api/events
PUT    /api/events/:id
DELETE /api/events/:id
GET    /api/events/:id/participants
POST   /api/events/:id/request
PUT    /api/events/:id/request/:requestId
GET    /api/events/search
GET    /api/events/filter
```

### Gestión de Organizaciones:
```javascript
// Endpoints de organizaciones
GET    /api/organizations
GET    /api/organizations/:id
POST   /api/organizations
PUT    /api/organizations/:id
DELETE /api/organizations/:id
GET    /api/organizations/:id/events
GET    /api/organizations/:id/members
POST   /api/organizations/:id/members
DELETE /api/organizations/:id/members/:userId
```

### Solicitudes y Participación:
```javascript
// Endpoints de solicitudes
GET    /api/requests
GET    /api/requests/:id
POST   /api/requests
PUT    /api/requests/:id/status
DELETE /api/requests/:id
GET    /api/requests/user/:userId
GET    /api/requests/event/:eventId
```

### Áreas de Intervención:
```javascript
// Endpoints de áreas
GET    /api/areas
GET    /api/areas/:id
POST   /api/areas
PUT    /api/areas/:id
DELETE /api/areas/:id
```

### Comentarios y Calificaciones:
```javascript
// Endpoints de comentarios
GET    /api/comments/event/:eventId
POST   /api/comments
PUT    /api/comments/:id
DELETE /api/comments/:id
```

## 🔐 Sistema de Autenticación

### Características:
- **JWT** con access token (1 hora) y refresh token (30 días)
- **Rate limiting** para prevenir ataques de fuerza bruta
- **Hash de contraseñas** con bcryptjs (12 rounds)
- **Validación de email** con confirmación
- **Recuperación de contraseña** por email
- **Sistema de roles** jerárquico
- **Estados de usuario** (activo, inactivo, bloqueado)

### Middleware de Seguridad:
```javascript
// Middlewares requeridos
- authenticateToken
- authorizeRole(['admin', 'organizer'])
- rateLimiter
- validateRequest
- sanitizeInput
- helmet
- cors
```

## 📱 Optimizaciones para Móvil

### Características Específicas:
- **Paginación** en todas las listas
- **Filtros avanzados** para eventos
- **Búsqueda por geolocalización**
- **Notificaciones push** (preparado)
- **Upload de imágenes** optimizado
- **Respuestas comprimidas** con gzip
- **Caché** para datos estáticos
- **Rate limiting** por IP y usuario

### Endpoints Móviles Específicos:
```javascript
// Endpoints optimizados para móvil
GET /api/mobile/events/nearby?lat=:lat&lng=:lng&radius=:radius
GET /api/mobile/events/featured
GET /api/mobile/user/dashboard
GET /api/mobile/notifications
POST /api/mobile/notifications/register
GET /api/mobile/events/categories
```

## 🗄️ Modelos de Base de Datos

### User Model:
```javascript
{
  id: Number,
  nombre: String,
  apellido: String,
  correo_electronico: String (unique),
  telefono: String,
  fecha_nacimiento: Date,
  genero: String,
  rol_id: Number (FK),
  contrasena_hash: String,
  estado: String, // 'activo', 'inactivo', 'bloqueado'
  intentos_fallidos: Number,
  ultimo_intento_fallido: Date,
  created_at: Date,
  updated_at: Date
}
```

### Event Model:
```javascript
{
  id: Number,
  nombre: String,
  fecha: Date,
  descripcion: String,
  ubicacion: String,
  latitud: Float,
  longitud: Float,
  localidad: String,
  organizacion_id: Number (FK),
  requisitos: Text,
  estado: String, // 'pendiente', 'activo', 'cancelado', 'finalizado'
  max_voluntarios: Number,
  created_at: Date,
  updated_at: Date
}
```

### Organization Model:
```javascript
{
  id: Number,
  nombre: String,
  tipo_organizacion_id: Number (FK),
  localidad: String,
  descripcion: Text,
  correo_electronico: String,
  telefono: String,
  fecha_creacion: Date,
  created_at: Date,
  updated_at: Date
}
```

## 🔧 Configuración del Proyecto

### package.json:
```json
{
  "name": "landlink-backend",
  "version": "1.0.0",
  "description": "LandLink Community Platform Backend API",
  "main": "src/app.js",
  "scripts": {
    "start": "node src/app.js",
    "dev": "nodemon src/app.js",
    "migrate": "sequelize-cli db:migrate",
    "seed": "sequelize-cli db:seed:all"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "helmet": "^7.0.0",
    "bcryptjs": "^2.4.3",
    "jsonwebtoken": "^9.0.2",
    "express-rate-limit": "^6.8.1",
    "express-validator": "^7.0.1",
    "sequelize": "^6.32.1",
    "tedious": "^16.7.1",
    "multer": "^1.4.5-lts.1",
    "compression": "^1.7.4"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  }
}
```

### Configuración de Base de Datos:
```javascript
// config/database.js
const { Sequelize } = require('sequelize');

const sequelize = new Sequelize('landlink1', 'Luigi', '123', {
  host: 'localhost',
  port: 1433,
  dialect: 'mssql',
  dialectOptions: {
    options: {
      encrypt: true,
      trustServerCertificate: true
    }
  }
});

module.exports = sequelize;
```

## 📚 Documentación API

### Endpoints Principales:
- Documentación de todos los endpoints en comentarios
- Ejemplos de request/response en el código
- Esquemas de validación
- Códigos de error estándar
- Autenticación requerida por endpoint

### Ejemplo de Documentación:
```javascript
/**
 * @route POST /api/auth/login
 * @desc Iniciar sesión de usuario
 * @access Public
 * @body { email: string, password: string }
 * @returns { success: boolean, token: string, user: object }
 */
```

## 📋 Checklist de Implementación

### Fase 1: Configuración Base
- [ ] Inicializar proyecto Node.js desde cero
- [ ] Configurar Express y middleware esencial
- [ ] Configurar conexión a SQL Server
- [ ] Configurar ORM (Sequelize)
- [ ] Configurar variables de entorno
- [ ] Configurar estructura de carpetas

### Fase 2: Base de Datos y Modelos
- [ ] Crear base de datos SQL Server
- [ ] Crear modelos de base de datos desde cero
- [ ] Implementar migraciones con Sequelize CLI
- [ ] Crear seeders de datos iniciales
- [ ] Implementar relaciones entre modelos
- [ ] Configurar índices optimizados

### Fase 3: Autenticación y Seguridad
- [ ] Implementar registro de usuarios
- [ ] Implementar login/logout con JWT
- [ ] Implementar recuperación de contraseña
- [ ] Implementar middleware de autenticación
- [ ] Implementar sistema de roles y permisos
- [ ] Implementar rate limiting y seguridad

### Fase 4: API Endpoints Core
- [ ] Implementar endpoints de usuarios
- [ ] Implementar endpoints de eventos
- [ ] Implementar endpoints de organizaciones
- [ ] Implementar endpoints de solicitudes
- [ ] Implementar endpoints de comentarios
- [ ] Implementar endpoints de áreas de intervención

### Fase 5: Lógica de Negocio
- [ ] Implementar flujos de solicitudes de participación
- [ ] Implementar sistema de aprobación/rechazo
- [ ] Implementar historial de actividades
- [ ] Implementar gestión de recursos
- [ ] Implementar sistema de calificaciones
- [ ] Implementar notificaciones

### Fase 6: Funcionalidades Avanzadas
- [ ] Implementar búsqueda y filtros avanzados
- [ ] Implementar geolocalización
- [ ] Implementar upload de archivos
- [ ] Implementar notificaciones push
- [ ] Implementar dashboard con estadísticas
- [ ] Implementar reportes

### Fase 7: Documentación y Optimización
- [ ] Documentar todos los endpoints
- [ ] Crear ejemplos de uso
- [ ] Optimizar rendimiento
- [ ] Validar lógica de negocio
- [ ] Crear README completo

### Fase 8: Producción
- [ ] Configurar servidor de producción
- [ ] Configurar backup de base de datos
- [ ] Configurar logs básicos
- [ ] Deploy a servidor

## 🎯 Criterios de Aceptación

### Funcionalidad:
- [ ] Todos los endpoints funcionan correctamente
- [ ] Autenticación y autorización implementadas
- [ ] Validación de datos completa
- [ ] Manejo de errores robusto
- [ ] Compatibilidad con la base de datos actual

### Rendimiento:
- [ ] Tiempo de respuesta < 200ms para endpoints simples
- [ ] Tiempo de respuesta < 500ms para endpoints complejos
- [ ] Soporte para 1000+ usuarios concurrentes
- [ ] Caché implementado para consultas frecuentes

### Seguridad:
- [ ] Autenticación JWT segura
- [ ] Rate limiting implementado
- [ ] Validación de entrada completa
- [ ] Headers de seguridad configurados
- [ ] Logs de seguridad implementados

### Documentación:
- [ ] API documentada en comentarios
- [ ] README completo
- [ ] Ejemplos de uso
- [ ] Guía de instalación
- [ ] Guía de desarrollo

## 🗄️ Inicialización de Base de Datos

### Estrategia:
1. **Crear base de datos** SQL Server desde cero
2. **Implementar migraciones** con Sequelize CLI
3. **Crear seeders** para datos iniciales
4. **Configurar índices** para optimizar consultas
5. **Validar integridad** de datos después de la creación

### Scripts de Inicialización:
- Scripts para crear todas las tablas
- Scripts para insertar datos iniciales (roles, tipos de organización, áreas)
- Scripts para crear índices optimizados
- Scripts para validar integridad de datos
- Scripts para crear usuario administrador por defecto

## 📞 Soporte y Mantenimiento

### Monitoreo Básico:
- **Logs básicos** con console.log
- **Manejo de errores** centralizado
- **Health checks** simples para endpoints

### Mantenimiento:
- **Backup manual** de base de datos
- **Monitoreo básico** de rendimiento
- **Documentación actualizada**

---

## 🚀 Instrucciones de Implementación

1. **Crear el proyecto** con la estructura especificada
2. **Configurar las dependencias** según package.json
3. **Implementar la configuración** de base de datos
4. **Crear los modelos** de base de datos desde cero
5. **Implementar la autenticación** JWT completa
6. **Crear los controladores** para cada entidad
7. **Implementar las rutas** de la API
8. **Agregar middleware** de seguridad y validación
9. **Documentar la API** en comentarios
10. **Crear README** con instrucciones
11. **Configurar servidor** de producción
12. **Realizar pruebas** manuales de funcionalidad

## 📋 Lógica de Negocio a Implementar

### Sistema de Roles y Permisos:
- **Administrador**: Acceso completo al sistema
- **Organizador**: Gestión de organizaciones y eventos
- **Voluntario**: Participación en eventos

### Flujos de Negocio Principales:
1. **Registro de Usuarios** con validación de email
2. **Gestión de Organizaciones** con múltiples organizadores
3. **Creación de Eventos** con áreas de intervención
4. **Solicitudes de Participación** con aprobación/rechazo
5. **Sistema de Comentarios y Calificaciones**
6. **Historial de Actividades** y auditoría
7. **Gestión de Recursos** para eventos
8. **Notificaciones** en tiempo real

### Reglas de Negocio:
- Usuarios bloqueados después de 5 intentos fallidos
- Eventos con estados: pendiente, activo, cancelado, finalizado
- Solicitudes con estados: pendiente, aprobado, rechazado
- Validación de email obligatoria
- Contraseñas con requisitos de seguridad
- Rate limiting para prevenir abuso

Este prompt proporciona una guía completa para crear el backend de LandLink desde cero con Node.js + Express, implementando toda la lógica de negocio y optimizándolo para aplicaciones móviles.
