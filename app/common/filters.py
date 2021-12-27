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

def pluralize_filter(data, word, other_word = None):
    """
    Agrega el plural al la palabra

    :param data:
        un tipo de dato, numérico o de tipo lista

    :param word:
        palabra a pluralizar

    :param new_word:
        palabra que reemplaza a word en caso de ser plural
    """
    
    new_word = ''
    try:
        if data.__len__() > 1:
            if other_word is None:
                new_word = f'{data.__len__()} {word}s'
            else:
                new_word = f'{data.__len__()} {other_word}'
        else:
            new_word = word
    except AttributeError:
        if data > 1:
            if other_word is None:
                new_word = f'{data} {word}s'
            else:
                new_word = f'{data} {other_word}'
        else:
            new_word = word
            
    return new_word