import re
from datetime import datetime

def validate_email(email):
    """
    Valida que el correo electrónico tenga un formato válido
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """
    Valida que el número de teléfono tenga un formato válido
    """
    # Eliminar espacios, guiones y paréntesis
    clean_phone = re.sub(r'[\s\-$$$$]', '', phone)
    # Verificar que solo contenga dígitos y tenga entre 8 y 15 caracteres
    return clean_phone.isdigit() and 8 <= len(clean_phone) <= 15

def validate_date(date_str, format='%Y-%m-%d'):
    """
    Valida que la fecha tenga un formato válido
    """
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False

def validate_coordinates(lat, lng):
    """
    Valida que las coordenadas sean válidas
    """
    try:
        lat_float = float(lat)
        lng_float = float(lng)
        return -90 <= lat_float <= 90 and -180 <= lng_float <= 180
    except (ValueError, TypeError):
        return False

def validate_text_length(text, min_length=0, max_length=None):
    """
    Valida que el texto tenga una longitud válida
    """
    if text is None:
        return min_length == 0
    
    text_length = len(text)
    
    if min_length > 0 and text_length < min_length:
        return False
    
    if max_length is not None and text_length > max_length:
        return False
    
    return True

def validate_integer(value, min_value=None, max_value=None):
    """
    Valida que el valor sea un entero válido
    """
    try:
        int_value = int(value)
        
        if min_value is not None and int_value < min_value:
            return False
        
        if max_value is not None and int_value > max_value:
            return False
        
        return True
    except (ValueError, TypeError):
        return False

def validate_rating(rating):
    """
    Valida que la calificación sea un entero entre 1 y 5
    """
    return validate_integer(rating, 1, 5)
