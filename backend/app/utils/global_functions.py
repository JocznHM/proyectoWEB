"""
    Funciones globales que se utilizan en el proyecto
"""
import datetime

def paginate(arrelgo: list, page: int, per_page: int):
    """
    La función `paginar` toma una lista, un número de página y elementos por página como entrada,
    calcula el número total de páginas y devuelve los elementos para la página especificada junto con el
    total de elementos y páginas.
    
    :param arrelgo: El parámetro `arrelgo` es una lista que contiene los elementos a paginar. Representa
    el conjunto de datos que debe dividirse en páginas
    :type arrelgo: list
    :param page: El parámetro `página` en la función `paginar` representa el número de página que desea
    recuperar de la lista. Indica qué subconjunto de elementos de la lista original deben devolverse
    según la configuración de paginación
    :type page: int
    :param per_page: El parámetro `per_page` en la función `paginar` representa la cantidad de elementos
    que desea mostrar por página al paginar una lista. Determina cuántos elementos se mostrarán en cada
    página de la lista paginada
    :type per_page: int
    :return: La función "paginar" devuelve una tupla que contiene el número total de elementos de la
    lista, el número total de páginas según el valor "por_página" especificado, el número de página
    actual y una sublista de elementos de la lista original correspondiente al página especificada y
    valor `por_página`.
    """
    print(arrelgo, page, per_page)
    #se obtiene el tamaño de la lista
    total_items = len(arrelgo)
    
    #se calcula el total de páginas
    total_pages = total_items // per_page
    #se verifica si hay elementos sobrantes para agregar una página más
    if total_pages % per_page != 0:
        total_pages += 1
    if total_pages == 0:
        total_pages = 1
    #se obtiene el índice de inicio de la página
    start_index = (page - 1) * per_page
    #se obtiene el índice de fin de la página
    end_index = start_index + per_page
    #se obtiene la lista de elementos de la página
    items_from_page = arrelgo[start_index:end_index]
    #se retorna el total de elementos, el total de páginas, la página actual y los elementos de la página
    return total_items, total_pages, page, items_from_page

def calcular_numero_juliano(fecha):
    # Obtener el día del año
    dia_del_año = fecha.timetuple().tm_yday

    # Obtener el número total de días en el año
    año = fecha.year

    # Construir la fracción del número juliano
    numero_juliano = f"{dia_del_año}/{año}"
    
    return numero_juliano