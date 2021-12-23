def strftime_filter(datetime, format=None):
    if datetime is None:
        return ''

    formatted = ''

    months = [
            'enero', 'febrero', 'marzo', 'abril',
            'mayo', 'junio', 'julio', 'agosto',
            'septiembre', 'octubre', 'noviembre', 'diciembre']

    weekdays = [
        'lunes', 'martes', 'miércoles', 'jueves',
        'viernes', 'sabado', 'domingo']

    if format is None:
        format = 'standard'

    standard_format = f'%d de {months[datetime.month-1]} de %Y'

    if format == 'short':
        formatted = datetime.strftime('%d/%m/%Y')
    elif format == 'standard':
        formatted = datetime.strftime(standard_format)
    elif format == 'full':
        formatted = datetime.strftime(f'{weekdays[datetime.weekday()]}, %d de {months[datetime.month-1]} de %Y')
    else:
        formatted = datetime.strftime(standard_format)
    return formatted
