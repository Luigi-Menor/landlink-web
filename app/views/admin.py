from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from ..utils.security import admin_required
from ..models.user import User, Role, HistorialCambiosUsuario
from ..models.organization import Organizacion, TipoOrganizacion
from ..models.event import Evento, AreaIntervencion
from .. import db
from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from ..utils.data_structures import Stack, Queue, DynamicArray

admin_bp = Blueprint('admin', __name__)

class EventForm(FlaskForm):
    pass  # El formulario solo se usa para el token CSRF

class EventLog:
    def __init__(self, timestamp, type, message):
        self.timestamp = timestamp
        self.type = type
        self.message = message

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Panel de administración"""
    # Obtener estadísticas para el dashboard
    total_usuarios = User.query.count()
    total_organizaciones = Organizacion.query.count()
    total_eventos = Evento.query.count()
    
    # Obtener usuarios recientes
    usuarios_recientes = User.query.order_by(User.id.desc()).limit(5).all()
    
    # Obtener eventos recientes
    eventos_recientes = Evento.query.order_by(Evento.id.desc()).limit(5).all()
    
    # Generar logs de ejemplo (en una implementación real, estos vendrían de la base de datos)
    logs = [
        EventLog(
            datetime.now() - timedelta(minutes=5),
            'info',
            'Nuevo evento creado: Limpieza de Playa'
        ),
        EventLog(
            datetime.now() - timedelta(minutes=15),
            'success',
            'Evento actualizado: Reforestación Parque Central'
        ),
        EventLog(
            datetime.now() - timedelta(minutes=30),
            'warning',
            'Evento próximo a iniciar: Taller de Reciclaje'
        ),
        EventLog(
            datetime.now() - timedelta(hours=1),
            'error',
            'Error al procesar solicitudes del evento: Limpieza de Río'
        ),
        EventLog(
            datetime.now() - timedelta(hours=2),
            'info',
            'Nuevo organizador registrado: Fundación Verde'
        )
    ]
    
    return render_template('admin/dashboard.html', 
                          total_usuarios=total_usuarios,
                          total_organizaciones=total_organizaciones,
                          total_eventos=total_eventos,
                          usuarios_recientes=usuarios_recientes,
                          eventos_recientes=eventos_recientes,
                          logs=logs)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """Gestión de usuarios"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        search = request.args.get('search', '').strip()
        role_id = request.args.get('role', type=int)
        status = request.args.get('status', '').strip()
        
        # Construir la consulta base
        query = User.query.join(Role)
        
        # Aplicar filtros
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    User.nombre.ilike(search_term),
                    User.apellido.ilike(search_term),
                    User.correo_electronico.ilike(search_term)
                )
            )
        
        if role_id:
            query = query.filter(User.rol_id == role_id)
        
        if status:
            query = query.filter(User.estado == status)
        
        # Ordenar por ID descendente (más recientes primero)
        query = query.order_by(User.id.desc())
        
        # Obtener todos los roles para el formulario de filtro
        roles = Role.query.all()
        
        # Paginar resultados
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        if pagination.pages > 0 and page > pagination.pages:
            return redirect(url_for('admin.users', page=pagination.pages, **request.args))
        
        return render_template('admin/users.html',
                             users=pagination.items,
                             pagination=pagination,
                             roles=roles,
                             search=search,
                             selected_role=role_id,
                             selected_status=status)
                             
    except Exception as e:
        flash('Error al cargar la lista de usuarios. Por favor, inténtalo de nuevo.', 'error')
        return redirect(url_for('admin.users', page=1))

@admin_bp.route('/users/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Editar usuario"""
    user = User.query.get_or_404(user_id)
    roles = Role.query.all()
    
    if request.method == 'POST':
        try:
            # Obtener y validar el rol_id
            rol_id = request.form.get('rol_id')
            if not rol_id:
                flash('El rol es requerido', 'danger')
                return render_template('admin/edit_user.html', user=user, roles=roles)
            
            # Verificar que el rol existe
            role = Role.query.get(rol_id)
            if not role:
                flash('El rol seleccionado no existe', 'danger')
                return render_template('admin/edit_user.html', user=user, roles=roles)
            
            # Actualizar datos del usuario
            user.nombre = request.form.get('nombre')
            user.apellido = request.form.get('apellido')
            user.correo_electronico = request.form.get('correo_electronico')
            user.telefono = request.form.get('telefono')
            user.rol_id = int(rol_id)
            user.estado = request.form.get('estado')
            
            # Registrar cambio
            cambio = HistorialCambiosUsuario(
                usuario_id=user.id,
                administrador_id=current_user.id,
                cambio=f"Actualización de datos: rol={role.nombre}, estado={user.estado}"
            )
            db.session.add(cambio)
            
            db.session.commit()
            flash('Usuario actualizado correctamente', 'success')
            return redirect(url_for('admin.users'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el usuario: {str(e)}', 'danger')
            return render_template('admin/edit_user.html', user=user, roles=roles)
    
    return render_template('admin/edit_user.html', user=user, roles=roles)

@admin_bp.route('/organizations')
@login_required
@admin_required
def organizations():
    """Gestión de organizaciones"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    organizations = Organizacion.query.order_by(Organizacion.id.desc()).paginate(page=page, per_page=per_page)
    tipos = TipoOrganizacion.query.all()
    
    return render_template('admin/organizations.html', organizations=organizations, tipos=tipos)

@admin_bp.route('/events')
@login_required
@admin_required
def events():
    """Gestión de eventos"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    events = Evento.query.order_by(Evento.id.desc()).paginate(page=page, per_page=per_page)
    areas = AreaIntervencion.query.all()
    
    return render_template('admin/events.html', events=events, areas=areas)

@admin_bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_event(event_id):
    """Editar evento"""
    evento = Evento.query.get_or_404(event_id)
    organizaciones = Organizacion.query.all()
    areas = AreaIntervencion.query.all()
    form = EventForm()
    
    if request.method == 'POST':
        try:
            # Actualizar datos básicos
            evento.nombre = request.form.get('nombre')
            evento.fecha = datetime.strptime(request.form.get('fecha'), '%Y-%m-%d')
            evento.descripcion = request.form.get('descripcion')
            evento.organizacion_id = int(request.form.get('organizacion_id'))
            evento.ubicacion = request.form.get('ubicacion')
            evento.localidad = request.form.get('localidad')
            evento.estado = request.form.get('estado')
            evento.requisitos = request.form.get('requisitos')
            
            # Actualizar coordenadas si se proporcionan
            latitud = request.form.get('latitud')
            longitud = request.form.get('longitud')
            if latitud and longitud:
                evento.latitud = float(latitud)
                evento.longitud = float(longitud)
            
            # Actualizar áreas de intervención
            areas_seleccionadas = request.form.getlist('areas')
            evento.areas = AreaIntervencion.query.filter(AreaIntervencion.id.in_(areas_seleccionadas)).all()
            
            db.session.commit()
            flash('Evento actualizado correctamente', 'success')
            return redirect(url_for('admin.events'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el evento: {str(e)}', 'danger')
    
    return render_template('admin/edit_event.html',
                         evento=evento,
                         organizaciones=organizaciones,
                         areas=areas,
                         form=form)

@admin_bp.route('/settings')
@login_required
@admin_required
def settings():
    """Configuración del sistema"""
    return render_template('admin/settings.html')

@admin_bp.route('/data-structures')
@login_required
@admin_required
def data_structures():
    """Visualización de estructuras de datos con datos reales"""
    # Obtener datos reales de la base de datos
    eventos = Evento.query.order_by(Evento.id.desc()).limit(5).all()
    organizaciones = Organizacion.query.order_by(Organizacion.id.desc()).limit(5).all()
    usuarios = User.query.order_by(User.id.desc()).limit(8).all()

    # Crear instancias de las estructuras
    stack = Stack(max_size=5)
    queue = Queue()
    dynamic_array = DynamicArray(capacity=8)

    # Llenar la pila con nombres de eventos (LIFO)
    for evento in eventos:
        stack.push(evento.nombre)

    # Llenar la cola con nombres de organizaciones (FIFO)
    for org in organizaciones:
        queue.enqueue(org.nombre)

    # Llenar el arreglo dinámico con nombres de usuarios
    for usuario in usuarios:
        dynamic_array.append(usuario.get_full_name())

    # Preparar datos para la plantilla
    array_items = []
    for i in range(dynamic_array.capacity):
        if i < dynamic_array.size:
            array_items.append({
                'value': dynamic_array.array[i],
                'status': 'Ocupado'
            })
        else:
            array_items.append({
                'value': None,
                'status': 'Espacio Disponible'
            })

    return render_template('admin/data_structures.html',
                          stack_items=stack.items,
                          queue_items=queue.items,
                          array_items=array_items,
                          stack_info={
                              'max_size': stack.max_size,
                              'current_size': stack.size(),
                              'is_full': stack.size() == stack.max_size
                          },
                          queue_info={
                              'size': queue.size(),
                              'is_empty': queue.is_empty()
                          },
                          array_info={
                              'capacity': dynamic_array.capacity,
                              'size': dynamic_array.size,
                              'utilization': f"{(dynamic_array.size/dynamic_array.capacity)*100:.1f}%"
                          })
