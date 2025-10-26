from ..models.event import Evento, AreaIntervencion, SolicitudEvento
from ..models.user import User
from datetime import datetime
from .. import db
from sqlalchemy import or_

class ProjectController:
    @staticmethod
    def get_projects(filters=None):
        """Obtiene proyectos con filtros opcionales"""
        query = Evento.query.filter(Evento.fecha >= datetime.utcnow().date())
        
        if filters:
            if filters.get('search'):
                search = f"%{filters['search']}%"
                query = query.filter(
                    or_(
                        Evento.nombre.ilike(search),
                        Evento.descripcion.ilike(search),
                        Evento.ubicacion.ilike(search)
                    )
                )
            
            if filters.get('area'):
                query = query.filter(Evento.area_id == filters['area'])
            
            if filters.get('fecha_inicio'):
                query = query.filter(Evento.fecha >= filters['fecha_inicio'])
            
            if filters.get('fecha_fin'):
                query = query.filter(Evento.fecha <= filters['fecha_fin'])
            
            if filters.get('organizador'):
                query = query.filter(Evento.organizador_id == filters['organizador'])
        
        # Ordenar por fecha
        query = query.order_by(Evento.fecha.asc())
        
        return query.all()
    
    @staticmethod
    def get_project_details(project_id):
        """Obtiene detalles de un proyecto específico"""
        return Evento.query.get_or_404(project_id)
    
    @staticmethod
    def get_related_projects(project):
        """Obtiene proyectos relacionados"""
        return Evento.query.filter(
            Evento.area_id == project.area_id,
            Evento.id != project.id,
            Evento.fecha >= datetime.utcnow().date()
        ).limit(3).all()
    
    @staticmethod
    def get_project_stats():
        """Obtiene estadísticas de proyectos"""
        total_projects = Evento.query.count()
        active_projects = Evento.query.filter(Evento.fecha >= datetime.utcnow().date()).count()
        total_volunteers = User.query.filter_by(rol_id=3).count()  # Asumiendo que 3 es el ID del rol voluntario
        total_organizations = User.query.filter_by(rol_id=2).count()  # Asumiendo que 2 es el ID del rol organizador
        
        return {
            'total_projects': total_projects,
            'active_projects': active_projects,
            'total_volunteers': total_volunteers,
            'total_organizations': total_organizations
        }
    
    @staticmethod
    def get_areas():
        """Obtiene todas las áreas de intervención"""
        return AreaIntervencion.query.all()
    
    @staticmethod
    def create_project_request(user_id, project_id, mensaje=None):
        """Crea una solicitud para participar en un proyecto"""
        # Verificar si ya existe una solicitud
        existing_request = SolicitudEvento.query.filter_by(
            usuario_id=user_id,
            evento_id=project_id
        ).first()
        
        if existing_request:
            return False, "Ya has enviado una solicitud para este proyecto"
        
        # Crear nueva solicitud
        solicitud = SolicitudEvento(
            usuario_id=user_id,
            evento_id=project_id,
            mensaje=mensaje,
            estado='pendiente'
        )
        
        try:
            db.session.add(solicitud)
            db.session.commit()
            return True, "Solicitud enviada correctamente"
        except Exception as e:
            db.session.rollback()
            return False, f"Error al enviar la solicitud: {str(e)}"
    
    @staticmethod
    def get_user_requests(user_id):
        """Obtiene las solicitudes de un usuario"""
        return SolicitudEvento.query.filter_by(usuario_id=user_id).all() 