from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from ..utils.security import organizer_required
from ..models.organization import Organizacion, TipoOrganizacion
from ..models.event import Evento, AreaIntervencion, SolicitudEvento
from ..models.user import User
from .. import db
from datetime import datetime

organizer_bp = Blueprint('organizer', __name__)

@organizer_bp.route('/dashboard')
@login_required
@organizer_required
def dashboard():
    """Panel de organizador"""
    # Obtener organizaciones del usuario con sus relaciones
    organizaciones = Organizacion.query.join(
        Organizacion.usuarios
    ).filter(
        User.id == current_user.id
    ).all()
    
    # Preparar datos de organizaciones con conteos
    orgs_data = []
    for org in organizaciones:
        orgs_data.append({
            'id': org.id,
            'nombre': org.nombre,
            'tipo': org.tipo_organizacion,
            'usuarios_count': db.session.query(User).join(
                Organizacion.usuarios
            ).filter(
                Organizacion.id == org.id
            ).count(),
            'eventos_count': Evento.query.filter_by(
                organizacion_id=org.id
            ).count()
        })
    
    # Obtener todos los eventos de las organizaciones del usuario
    eventos = Evento.query.join(
        Organizacion
    ).join(
        Organizacion.usuarios
    ).filter(
        User.id == current_user.id
    ).order_by(
        Evento.fecha
    ).all()
    
    return render_template('organizer/dashboard.html', 
                          organizaciones=orgs_data, 
                          eventos=eventos,
                          now=datetime.utcnow())

@organizer_bp.route('/events')
@login_required
@organizer_required
def events():
    """Gestión de eventos"""
    # Obtener eventos de las organizaciones del usuario
    eventos = Evento.query.join(
        Organizacion
    ).join(
        Organizacion.usuarios
    ).filter(
        User.id == current_user.id
    ).order_by(
        Evento.fecha
    ).all()
    
    return render_template('organizer/events.html', eventos=eventos)

@organizer_bp.route('/eventos/crear', methods=['GET', 'POST'])
@login_required
@organizer_required
def create_event():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.form.get('nombre')
            fecha = datetime.strptime(request.form.get('fecha'), '%Y-%m-%d')
            
            # Validar que la fecha sea actual o posterior
            if fecha.date() < datetime.utcnow().date():
                flash('La fecha del evento debe ser la fecha actual o una fecha posterior', 'error')
                return redirect(url_for('organizer.create_event'))
                
            descripcion = request.form.get('descripcion')
            ubicacion = request.form.get('ubicacion')
            localidad = request.form.get('localidad')
            organizacion_id = request.form.get('organizacion_id')
            requisitos = request.form.get('requisitos')
            latitud = request.form.get('latitud')
            longitud = request.form.get('longitud')
            areas = request.form.getlist('areas')

            # Validar que el usuario pertenece a la organización
            organizacion = Organizacion.query.join(
                Organizacion.usuarios
            ).filter(
                Organizacion.id == organizacion_id,
                User.id == current_user.id
            ).first()
            
            if not organizacion:
                flash('No tienes permiso para crear eventos en esta organización', 'error')
                return redirect(url_for('organizer.create_event'))

            # Crear el evento usando SQL nativo
            stmt = db.text("""
                INSERT INTO eventos (nombre, fecha, descripcion, ubicacion, latitud, longitud, 
                                   localidad, organizacion_id, requisitos, estado)
                VALUES (:nombre, :fecha, :descripcion, :ubicacion, :latitud, :longitud,
                        :localidad, :organizacion_id, :requisitos, :estado)
            """)
            
            db.session.execute(stmt, {
                'nombre': nombre,
                'fecha': fecha,
                'descripcion': descripcion,
                'ubicacion': ubicacion,
                'latitud': latitud if latitud else None,
                'longitud': longitud if longitud else None,
                'localidad': localidad,
                'organizacion_id': organizacion_id,
                'requisitos': requisitos,
                'estado': 'pendiente'
            })
            
            # Obtener el ID del evento insertado
            result = db.session.execute(db.text("SELECT IDENT_CURRENT('eventos') AS id"))
            evento_id = int(result.scalar())
            
            # Agregar áreas de intervención
            if areas:
                for area_id in areas:
                    area = AreaIntervencion.query.get(area_id)
                    if area:
                        db.session.execute(
                            db.text("INSERT INTO intervenciones_evento (evento_id, area_intervencion_id) VALUES (:evento_id, :area_id)"),
                            {'evento_id': evento_id, 'area_id': area_id}
                        )

            db.session.commit()

            flash('Evento creado exitosamente', 'success')
            return redirect(url_for('organizer.events'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el evento: {str(e)}', 'error')
            return redirect(url_for('organizer.create_event'))

    # GET request - mostrar formulario
    organizaciones = Organizacion.query.join(
        Organizacion.usuarios
    ).filter(
        User.id == current_user.id
    ).all()
    
    areas = AreaIntervencion.query.all()
    
    return render_template('organizer/create_event.html',
                         organizaciones=organizaciones,
                         areas=areas)

@organizer_bp.route('/organization/<int:org_id>')
@login_required
@organizer_required
def organization_detail(org_id):
    """Ver detalles de una organización"""
    organizacion = Organizacion.query.join(
        Organizacion.usuarios
    ).filter(
        Organizacion.id == org_id,
        User.id == current_user.id
    ).first_or_404()
    
    return render_template('organizer/organization_detail.html', 
                          organizacion=organizacion,
                          now=datetime.utcnow())

@organizer_bp.route('/event/<int:event_id>')
@login_required
@organizer_required
def event_detail(event_id):
    """Ver detalles de un evento"""
    evento = Evento.query.join(
        Organizacion
    ).join(
        Organizacion.usuarios
    ).filter(
        Evento.id == event_id,
        User.id == current_user.id
    ).first_or_404()
    
    # Obtener solicitudes pendientes
    solicitudes_pendientes = evento.solicitudes.filter_by(estado='pendiente').all()
    
    return render_template('organizer/event_detail.html', 
                          evento=evento,
                          solicitudes_pendientes=solicitudes_pendientes)

@organizer_bp.route('/event/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
@organizer_required
def edit_event(event_id):
    """Editar evento"""
    evento = Evento.query.join(
        Organizacion
    ).join(
        Organizacion.usuarios
    ).filter(
        Evento.id == event_id,
        User.id == current_user.id
    ).first_or_404()
    
    # Obtener organizaciones del usuario y áreas de intervención
    organizaciones = Organizacion.query.join(
        Organizacion.usuarios
    ).filter(
        User.id == current_user.id
    ).all()
    
    areas = AreaIntervencion.query.all()
    
    if request.method == 'POST':
        try:
            # Validar que el usuario pertenezca a la organización
            org_id = request.form.get('organizacion_id', type=int)
            organizacion = Organizacion.query.join(
                Organizacion.usuarios
            ).filter(
                Organizacion.id == org_id,
                User.id == current_user.id
            ).first()
            
            if not organizacion:
                flash('No tienes permiso para asignar este evento a esta organización', 'danger')
                return redirect(url_for('organizer.edit_event', event_id=event_id))
            
            # Validar que la fecha sea actual o posterior
            nueva_fecha = datetime.strptime(request.form.get('fecha'), '%Y-%m-%d')
            if nueva_fecha.date() < datetime.utcnow().date():
                flash('La fecha del evento debe ser la fecha actual o una fecha posterior', 'error')
                return redirect(url_for('organizer.edit_event', event_id=event_id))
            
            # Actualizar evento
            evento.nombre = request.form.get('nombre')
            evento.fecha = nueva_fecha
            evento.descripcion = request.form.get('descripcion')
            evento.ubicacion = request.form.get('ubicacion')
            evento.localidad = request.form.get('localidad')
            evento.organizacion_id = org_id
            
            # Actualizar coordenadas
            lat = request.form.get('latitud')
            lng = request.form.get('longitud')
            if lat and lng:
                evento.latitud = float(lat)
                evento.longitud = float(lng)
            
            # Actualizar áreas de intervención
            evento.areas = []
            areas_ids = request.form.getlist('areas')
            for area_id in areas_ids:
                area = AreaIntervencion.query.get(area_id)
                if area:
                    evento.areas.append(area)
            
            db.session.commit()
            
            flash('Evento actualizado correctamente', 'success')
            return redirect(url_for('organizer.event_detail', event_id=event_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el evento: {str(e)}', 'error')
            return redirect(url_for('organizer.edit_event', event_id=event_id))
    
    return render_template('organizer/edit_event.html', 
                          evento=evento,
                          organizaciones=organizaciones,
                          areas=areas)

@organizer_bp.route('/event/<int:event_id>/solicitud/<int:solicitud_id>/aprobar', methods=['POST'])
@login_required
@organizer_required
def aprobar_solicitud(event_id, solicitud_id):
    """Aprobar una solicitud de participación"""
    evento = Evento.query.join(
        Organizacion
    ).join(
        Organizacion.usuarios
    ).filter(
        Evento.id == event_id,
        User.id == current_user.id
    ).first_or_404()
    
    solicitud = SolicitudEvento.query.get_or_404(solicitud_id)
    
    if solicitud.evento_id != evento.id:
        flash('La solicitud no corresponde a este evento', 'error')
        return redirect(url_for('organizer.event_detail', event_id=event_id))
    
    # Aprobar solicitud
    solicitud.estado = 'aprobado'
    solicitud.decidido_en = datetime.utcnow()
    db.session.commit()
    
    flash('Solicitud aprobada exitosamente', 'success')
    return redirect(url_for('organizer.event_detail', event_id=event_id))

@organizer_bp.route('/event/<int:event_id>/solicitud/<int:solicitud_id>/rechazar', methods=['POST'])
@login_required
@organizer_required
def rechazar_solicitud(event_id, solicitud_id):
    """Rechazar una solicitud de participación"""
    evento = Evento.query.join(
        Organizacion
    ).join(
        Organizacion.usuarios
    ).filter(
        Evento.id == event_id,
        User.id == current_user.id
    ).first_or_404()
    
    solicitud = SolicitudEvento.query.get_or_404(solicitud_id)
    
    if solicitud.evento_id != evento.id:
        flash('La solicitud no corresponde a este evento', 'error')
        return redirect(url_for('organizer.event_detail', event_id=event_id))
    
    # Rechazar solicitud
    solicitud.estado = 'rechazado'
    solicitud.decidido_en = datetime.utcnow()
    db.session.commit()
    
    flash('Solicitud rechazada', 'success')
    return redirect(url_for('organizer.event_detail', event_id=event_id))

@organizer_bp.route('/organizations')
@login_required
@organizer_required
def organizations():
    """Lista de organizaciones del usuario"""
    organizaciones = Organizacion.query.join(
        Organizacion.usuarios
    ).filter(
        User.id == current_user.id
    ).all()
    
    return render_template('organizer/organizations.html', 
                         organizaciones=organizaciones,
                         now=datetime.utcnow())

@organizer_bp.route('/create-organization', methods=['GET', 'POST'])
@login_required
@organizer_required
def create_organization():
    """Crear nueva organización"""
    if request.method == 'POST':
        try:
            # Validar datos requeridos
            nombre = request.form.get('nombre')
            tipo_id = request.form.get('tipo_id')
            localidad = request.form.get('localidad')
            descripcion = request.form.get('descripcion')
            correo_electronico = request.form.get('correo_electronico')
            
            if not all([nombre, tipo_id, localidad, descripcion, correo_electronico]):
                flash('Por favor completa todos los campos requeridos', 'error')
                return redirect(url_for('organizer.create_organization'))
            
            # Crear la organización
            nueva_org = Organizacion(
                nombre=nombre,
                tipo_organizacion_id=tipo_id,
                localidad=localidad,
                descripcion=descripcion,
                correo_electronico=correo_electronico,
                telefono=request.form.get('telefono')
            )
            
            # Agregar el usuario actual como organizador
            nueva_org.usuarios.append(current_user)
            
            # Agregar áreas de trabajo
            areas_ids = request.form.getlist('areas[]')
            if not areas_ids:
                flash('Debes seleccionar al menos un área de trabajo', 'error')
                return redirect(url_for('organizer.create_organization'))
                
            for area_id in areas_ids:
                area = AreaIntervencion.query.get(area_id)
                if area:
                    nueva_org.areas_trabajo.append(area)
            
            db.session.add(nueva_org)
            db.session.commit()
            
            flash('Organización creada correctamente', 'success')
            return redirect(url_for('organizer.organizations'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la organización: {str(e)}', 'error')
            return redirect(url_for('organizer.create_organization'))
    
    # GET request - mostrar formulario
    tipos = TipoOrganizacion.query.all()
    areas = AreaIntervencion.query.all()
    
    return render_template('organizer/create_organization.html', 
                          tipos=tipos,
                          areas=areas)

@organizer_bp.route('/organization/<int:org_id>/edit', methods=['GET', 'POST'])
@login_required
@organizer_required
def edit_organization(org_id):
    """Editar organización"""
    organizacion = Organizacion.query.join(
        Organizacion.usuarios
    ).filter(
        Organizacion.id == org_id,
        User.id == current_user.id
    ).first_or_404()
    
    if request.method == 'POST':
        try:
            # Validar datos requeridos
            nombre = request.form.get('nombre')
            tipo_id = request.form.get('tipo_id')
            localidad = request.form.get('localidad')
            descripcion = request.form.get('descripcion')
            correo_electronico = request.form.get('correo_electronico')
            
            if not all([nombre, tipo_id, localidad, descripcion, correo_electronico]):
                flash('Por favor completa todos los campos requeridos', 'error')
                return redirect(url_for('organizer.edit_organization', org_id=org_id))
            
            # Actualizar organización
            organizacion.nombre = nombre
            organizacion.tipo_organizacion_id = tipo_id
            organizacion.localidad = localidad
            organizacion.descripcion = descripcion
            organizacion.correo_electronico = correo_electronico
            organizacion.telefono = request.form.get('telefono')
            
            # Actualizar áreas de trabajo
            organizacion.areas_trabajo = []
            areas_ids = request.form.getlist('areas[]')
            if not areas_ids:
                flash('Debes seleccionar al menos un área de trabajo', 'error')
                return redirect(url_for('organizer.edit_organization', org_id=org_id))
                
            for area_id in areas_ids:
                area = AreaIntervencion.query.get(area_id)
                if area:
                    organizacion.areas_trabajo.append(area)
            
            db.session.commit()
            
            flash('Organización actualizada correctamente', 'success')
            return redirect(url_for('organizer.organization_detail', org_id=org_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la organización: {str(e)}', 'error')
            return redirect(url_for('organizer.edit_organization', org_id=org_id))
    
    # GET request - mostrar formulario
    tipos = TipoOrganizacion.query.all()
    areas = AreaIntervencion.query.all()
    
    return render_template('organizer/edit_organization.html', 
                          organizacion=organizacion,
                          tipos=tipos,
                          areas=areas)

@organizer_bp.route('/event/<int:event_id>/eliminar', methods=['POST'])
@login_required
@organizer_required
def delete_event(event_id):
    """Eliminar evento"""
    evento = Evento.query.join(
        Organizacion
    ).join(
        Organizacion.usuarios
    ).filter(
        Evento.id == event_id,
        User.id == current_user.id
    ).first_or_404()
    db.session.delete(evento)
    db.session.commit()
    flash('Evento eliminado correctamente.', 'success')
    return redirect(url_for('organizer.events'))
