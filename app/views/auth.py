from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_required, current_user, login_user, logout_user
from ..controllers.auth import AuthController
from ..controllers.project import ProjectController
from ..utils.validators import validate_email
from ..utils.security import validate_password
from ..models.event import Evento, AreaIntervencion, SolicitudEvento
from ..models.event import ComentarioCalificacion
from ..models.user import User
from datetime import datetime
from ..forms.login_form import LoginForm
from urllib.parse import urlparse
from .. import db
from flask import current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    """Página de inicio"""
    # Obtener estadísticas para la página de inicio
    stats = ProjectController.get_project_stats()
    # Obtener eventos destacados
    eventos_destacados = ProjectController.get_projects({'limit': 3})
    
    return render_template('index.html', 
                         eventos_destacados=eventos_destacados,
                         stats=stats)

@auth_bp.route('/proyectos')
def proyectos():
    """Lista de proyectos/eventos"""
    # Obtener filtros de la URL
    filters = {
        'search': request.args.get('search'),
        'area': request.args.get('area', type=int),
        'fecha_inicio': request.args.get('fecha_inicio'),
        'fecha_fin': request.args.get('fecha_fin'),
        'organizador': request.args.get('organizador', type=int)
    }
    
    # Obtener proyectos y áreas para el filtro
    proyectos = ProjectController.get_projects(filters)
    areas = ProjectController.get_areas()
    
    return render_template('proyectos.html', 
                         proyectos=proyectos,
                         areas=areas,
                         filters=filters)

@auth_bp.route('/proyectos/<int:project_id>')
def detalle_proyecto(project_id):
    """Detalle de un proyecto/evento"""
    proyecto = ProjectController.get_project_details(project_id)
    proyectos_relacionados = ProjectController.get_related_projects(proyecto)
    
    solicitud = None
    if current_user.is_authenticated:
        solicitud = SolicitudEvento.query.filter_by(
            usuario_id=current_user.id, 
            evento_id=project_id
        ).first()
    
    return render_template('detalle_proyecto.html', 
                         proyecto=proyecto,
                         proyectos_relacionados=proyectos_relacionados,
                         solicitud=solicitud)

@auth_bp.route('/proyectos/<int:project_id>/solicitar', methods=['POST'])
@login_required
def solicitar_proyecto(project_id):
    """Solicitar participación en un proyecto"""
    mensaje = request.form.get('mensaje')
    
    success, message = ProjectController.create_project_request(
        current_user.id,
        project_id,
        mensaje
    )
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('auth.detalle_proyecto', project_id=project_id))

@auth_bp.route('/sobre-nosotros')
def sobre_nosotros():
    """Página Sobre Nosotros"""
    return render_template('sobre_nosotros.html')

@auth_bp.route('/contacto', methods=['GET', 'POST'])
def contacto():
    """Página de contacto"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        asunto = request.form.get('asunto')
        mensaje = request.form.get('mensaje')
        
        # Aquí se procesaría el formulario de contacto
        # Por ejemplo, enviar un correo electrónico
        
        flash('Tu mensaje ha sido enviado correctamente. Nos pondremos en contacto contigo pronto.', 'success')
        return redirect(url_for('auth.contacto'))
    
    return render_template('contacto.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        data = {
            'nombre': request.form.get('nombre'),
            'apellido': request.form.get('apellido'),
            'correo_electronico': request.form.get('correo_electronico'),
            'telefono': request.form.get('telefono'),
            'fecha_nacimiento': request.form.get('fecha_nacimiento'),
            'genero': request.form.get('genero'),
            'contrasena': request.form.get('contrasena')
        }
        
        result = AuthController.register(data)
        
        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(result['message'], 'error')
            return render_template('auth/register.html', data=data)
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            result = AuthController.login(form.email.data, form.password.data, form.remember.data)
            
            if result['success']:
                next_page = request.args.get('next')
                if not next_page or urlparse(next_page).netloc != '':
                    if current_user.is_admin():
                        next_page = url_for('admin.dashboard')
                    elif current_user.is_organizer():
                        next_page = url_for('organizer.dashboard')
                    else:
                        next_page = url_for('volunteer.dashboard')
                return redirect(next_page)
            else:
                flash(result['message'], 'error')
        except Exception as e:
            current_app.logger.error(f'Error en login: {str(e)}')
            flash('Error al iniciar sesión. Por favor, inténtalo de nuevo.', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()  # Limpiar toda la sesión
    logout_user()
    return redirect(url_for('auth.index'))

@auth_bp.route('/profile')
@login_required
def profile():
    """Perfil del usuario"""
    return render_template('auth/profile.html')

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Cambio de contraseña"""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validar datos
        if not current_password or not new_password or not confirm_password:
            flash('Por favor complete todos los campos', 'danger')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('auth/change_password.html')
        
        if not validate_password(new_password):
            flash('La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial', 'danger')
            return render_template('auth/change_password.html')
        
        # Cambiar contraseña
        result = AuthController.change_password(current_user.id, current_password, new_password)
        
        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash(result['message'], 'danger')
            return render_template('auth/change_password.html')
    
    return render_template('auth/change_password.html')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Recuperación de contraseña"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            flash('Por favor ingrese su correo electrónico', 'danger')
            return render_template('auth/forgot_password.html')
        
        result = AuthController.request_password_reset(email)
        
        flash(result['message'], 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Restablecimiento de contraseña"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validar datos
        if not new_password or not confirm_password:
            flash('Por favor complete todos los campos', 'danger')
            return render_template('auth/reset_password.html', token=token)
        
        if new_password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('auth/reset_password.html', token=token)
        
        if not validate_password(new_password):
            flash('La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial', 'danger')
            return render_template('auth/reset_password.html', token=token)
        
        # Restablecer contraseña
        result = AuthController.reset_password(token, new_password)
        
        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(result['message'], 'danger')
            return render_template('auth/reset_password.html', token=token)
    
    return render_template('auth/reset_password.html', token=token)
