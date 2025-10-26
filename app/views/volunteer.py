from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from ..utils.security import volunteer_required
from ..models.event import Evento, SolicitudEvento, ComentarioCalificacion
from ..models.activity import HistorialActividad
from .. import db
from datetime import datetime

volunteer_bp = Blueprint('volunteer', __name__)

@volunteer_bp.route('/dashboard')
@login_required
@volunteer_required
def dashboard():
    """Panel de voluntario"""
    # Obtener solicitudes del usuario
    solicitudes = SolicitudEvento.query.filter_by(usuario_id=current_user.id).all()
    
    # Obtener historial de actividades
    historial = HistorialActividad.query.filter_by(usuario_id=current_user.id).all()
    
    # Obtener eventos próximos (solicitudes aprobadas para eventos futuros)
    eventos_proximos = []
    for solicitud in solicitudes:
        if solicitud.estado == 'aprobado' and solicitud.evento.fecha >= datetime.utcnow().date():
            eventos_proximos.append(solicitud.evento)
    
    return render_template('volunteer/dashboard.html', 
                          solicitudes=solicitudes,
                          historial=historial,
                          eventos_proximos=eventos_proximos)

@volunteer_bp.route('/events')
@login_required
@volunteer_required
def events():
    """Explorar eventos disponibles"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Construir la consulta base
    query = Evento.query
    
    # Aplicar filtros si existen
    search = request.args.get('search', '').strip()
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Evento.nombre.ilike(search_term),
                Evento.descripcion.ilike(search_term),
                Evento.ubicacion.ilike(search_term)
            )
        )
    
    fecha_desde = request.args.get('fecha_desde')
    if fecha_desde:
        query = query.filter(Evento.fecha >= datetime.strptime(fecha_desde, '%Y-%m-%d').date())
    
    fecha_hasta = request.args.get('fecha_hasta')
    if fecha_hasta:
        query = query.filter(Evento.fecha <= datetime.strptime(fecha_hasta, '%Y-%m-%d').date())
    
    # Ordenar por fecha y luego por ID para MSSQL
    query = query.order_by(Evento.fecha.asc(), Evento.id.asc())
    
    # Paginar resultados
    eventos = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Obtener solicitudes del usuario para verificar si ya se ha inscrito
    solicitudes_usuario = SolicitudEvento.query.filter_by(usuario_id=current_user.id).all()
    eventos_inscritos = [s.evento_id for s in solicitudes_usuario]
    
    return render_template('volunteer/events.html', 
                          eventos=eventos,
                          eventos_inscritos=eventos_inscritos)

@volunteer_bp.route('/event/<int:event_id>')
@login_required
@volunteer_required
def event_detail(event_id):
    """Detalle de evento"""
    evento = Evento.query.get_or_404(event_id)
    
    # Verificar si el usuario ya se ha inscrito
    solicitud = SolicitudEvento.query.filter_by(usuario_id=current_user.id, evento_id=evento.id).first()
    
    # Obtener comentarios del evento
    comentarios = ComentarioCalificacion.query.filter_by(evento_id=evento.id).all()
    
    return render_template('volunteer/event_detail.html', 
                          evento=evento,
                          solicitud=solicitud,
                          comentarios=comentarios)

@volunteer_bp.route('/event/<int:event_id>/inscribirse', methods=['POST'])
@login_required
@volunteer_required
def inscribirse_evento(event_id):
    """Inscribirse a un evento"""
    evento = Evento.query.get_or_404(event_id)
    
    # Verificar si el evento ya pasó
    if evento.fecha < datetime.utcnow().date():
        flash('No puedes inscribirte a un evento que ya pasó', 'error')
        return redirect(url_for('volunteer.event_detail', event_id=event_id))
    
    # Verificar si el usuario ya se ha inscrito
    solicitud_existente = SolicitudEvento.query.filter_by(usuario_id=current_user.id, evento_id=evento.id).first()
    if solicitud_existente:
        if solicitud_existente.estado == 'pendiente':
            flash('Ya tienes una solicitud pendiente para este evento', 'warning')
        elif solicitud_existente.estado == 'aprobado':
            flash('Ya estás inscrito en este evento', 'info')
        elif solicitud_existente.estado == 'rechazado':
            flash('Tu solicitud anterior fue rechazada', 'warning')
        return redirect(url_for('volunteer.event_detail', event_id=event_id))
    
    # Crear solicitud
    nueva_solicitud = SolicitudEvento(
        usuario_id=current_user.id,
        evento_id=evento.id,
        estado='pendiente',
        solicitado_en=datetime.utcnow()
    )
    
    try:
        db.session.add(nueva_solicitud)
        db.session.commit()
        flash('Te has inscrito correctamente. Tu solicitud está pendiente de aprobación.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al procesar tu solicitud. Por favor, intenta nuevamente.', 'error')
    
    return redirect(url_for('volunteer.event_detail', event_id=event_id))

@volunteer_bp.route('/event/<int:event_id>/cancelar', methods=['POST'])
@login_required
@volunteer_required
def cancelar_inscripcion(event_id):
    """Cancelar inscripción a un evento"""
    solicitud = SolicitudEvento.query.filter_by(usuario_id=current_user.id, evento_id=event_id).first_or_404()
    
    # Verificar si el evento ya pasó
    if solicitud.evento.fecha < datetime.utcnow().date():
        flash('No puedes cancelar la inscripción a un evento que ya pasó', 'danger')
        return redirect(url_for('volunteer.event_detail', event_id=event_id))
    
    # Eliminar solicitud
    db.session.delete(solicitud)
    db.session.commit()
    
    flash('Has cancelado tu inscripción correctamente', 'success')
    return redirect(url_for('volunteer.event_detail', event_id=event_id))

@volunteer_bp.route('/event/<int:event_id>/comentar', methods=['POST'])
@login_required
@volunteer_required
def comentar_evento(event_id):
    """Comentar y calificar un evento"""
    evento = Evento.query.get_or_404(event_id)
    
    # Verificar si el evento ya pasó
    if evento.fecha >= datetime.utcnow().date():
        flash('Solo puedes comentar eventos que ya han pasado', 'danger')
        return redirect(url_for('volunteer.event_detail', event_id=event_id))
    
    # Verificar si el usuario participó en el evento
    participacion = HistorialActividad.query.filter_by(usuario_id=current_user.id, evento_id=evento.id).first()
    if not participacion:
        flash('Solo puedes comentar eventos en los que has participado', 'danger')
        return redirect(url_for('volunteer.event_detail', event_id=event_id))
    
    # Verificar si el usuario ya ha comentado
    comentario_existente = ComentarioCalificacion.query.filter_by(usuario_id=current_user.id, evento_id=evento.id).first()
    if comentario_existente:
        # Actualizar comentario existente
        comentario_existente.comentario = request.form.get('comentario')
        comentario_existente.calificacion = request.form.get('calificacion', type=int)
        db.session.commit()
        flash('Tu comentario ha sido actualizado', 'success')
    else:
        # Crear nuevo comentario
        nuevo_comentario = ComentarioCalificacion(
            usuario_id=current_user.id,
            evento_id=evento.id,
            comentario=request.form.get('comentario'),
            calificacion=request.form.get('calificacion', type=int),
            creado_en=datetime.utcnow()
        )
        db.session.add(nuevo_comentario)
        db.session.commit()
        flash('Tu comentario ha sido publicado', 'success')
    
    return redirect(url_for('volunteer.event_detail', event_id=event_id))

@volunteer_bp.route('/historial')
@login_required
@volunteer_required
def historial():
    """Historial de participación"""
    historial = HistorialActividad.query.filter_by(usuario_id=current_user.id).all()
    
    return render_template('volunteer/historial.html', historial=historial)
