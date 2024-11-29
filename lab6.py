# Programa: lab6.py implementación del algoritmo de Bresenham
# Autores : Vicente Santos 
#           Cristobal Gallardo         
# Fecha   : 28/11/2024

# Importar bibliotecas necesarias
import pygame
from Libgraphics import *


# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)



width = 1000
height = 1000
pixel_size = 2
win = GraphWin("Clipping pro 4k 100% real no fake", width, height)

class Button:
    def __init__(self, win, center, width, height, label):
        """Inicializa el botón en la ventana gráfica `win` con el centro, ancho, alto y etiqueta."""
        w, h = width / 2, height / 2
        x, y = center.getX(), center.getY()
        
        # Crear rectángulo para el botón
        self.rect = Rectangle(Point(x - w, y - h), Point(x + w, y + h))
        self.rect.setFill("lightgray")  # Color de fondo del botón
        self.rect.draw(win)
        
        
        self.label = Text(center, label)
        self.label.draw(win)
        
        self.deactivated = False  # Estado del botón (activo/inactivo)
    
    def is_clicked(self, p):
        """Devuelve True si el botón está activo y el punto `p` está dentro del botón."""
        return (self.rect.getP1().getX() <= p.getX() <= self.rect.getP2().getX() and
                self.rect.getP1().getY() <= p.getY() <= self.rect.getP2().getY())

    def undraw(self):
        self.rect.undraw() 
        self.label.undraw()  
        
    def activate(self):
        """Activa el botón (cambia el borde a negro y lo vuelve clicable)."""
        self.label.setFill("black")
        self.rect.setWidth(2)
        self.deactivated = False

    def desactivate(self):
        """Desactiva el botón (cambia el borde a gris claro y lo hace no clicable)."""
        self.label.setFill("darkgrey")
        self.rect.setWidth(1)
        self.deactivated = True
    
    def desactivate2(self):
        """Desactiva el botón (cambia el borde a gris claro y lo hace no clicable)."""
        self.label.setFill("darkgrey")
        self.rect.setWidth(1)
        self.deactivated = False
    
    def cambio_texto(self, win, center):
        self.label.undraw()
        self.label = Text(center, "Reiniciar")
        self.label.draw(win)


def leer_opcion(opciones):
    while (a := input('Opción: ')) not in opciones:
        print('Opción incorrecta, vuelva a intentarlo.')
    return a

def leer_variable(nombre):
    while True:
        a = input(f'{nombre} ')
        try:
            a = int(a)
            return a
        except ValueError:
            print('La variable no es un número entero, vuelva a intentarlo.')

def crear_ventana(win=None, pixel_size=2):
    LineaBresenham(-150,-100,50,-100, win, pixel_size) # bajo
    LineaBresenham(-150,100,50,100, win, pixel_size)   # arriba
    LineaBresenham(-150,-100,-150,100, win, pixel_size) # izquierda
    LineaBresenham(50,-100,50,100, win, pixel_size) # derecha
    
def crear_ventana_preview(win=None, pixel_size=2):
    LineaBresenham(125, -150, 225, -150, win, pixel_size) # bajo
    LineaBresenham(125, -50, 225, -50, win, pixel_size)   # arriba
    LineaBresenham(125, -50, 125, -150, win, pixel_size) # izquierda
    LineaBresenham(225, -50, 225, -150, win, pixel_size) # derecha

def crear_ventana_undraw(win=None, pixel_size=2):
    LineaBresenham_borrado(-150,-100,50,-100, win, pixel_size) # bajo
    LineaBresenham_borrado(-150,100,50,100, win, pixel_size)   # arriba
    LineaBresenham_borrado(-150,-100,-150,100, win, pixel_size) # izquierda
    LineaBresenham_borrado(50,-100,50,100, win, pixel_size) # derecha
    
def crear_ventana_preview_undraw(win=None, pixel_size=2):
    LineaBresenham_borrado(125, -150, 225, -150, win, pixel_size) # bajo
    LineaBresenham_borrado(125, -50, 225, -50, win, pixel_size)   # arriba
    LineaBresenham_borrado(125, -50, 125, -150, win, pixel_size) # izquierda
    LineaBresenham_borrado(225, -50, 225, -150, win, pixel_size) # derecha

def crear_ventana_activity(win=None, pixel_size=2):
    # Dibujar los bordes de la ventana usando LineaBresenham
    LineaBresenham(30, 50, 220, 50, win, pixel_size)   # línea inferior
    LineaBresenham(30, 240, 220, 240, win, pixel_size) # línea superior
    LineaBresenham(30, 50, 30, 240, win, pixel_size)   # línea izquierda
    LineaBresenham(220, 50, 220, 240, win, pixel_size) # línea derecha

def crear_ventana_activity_undraw(win=None, pixel_size=2):
    # Dibujar los bordes de la ventana usando LineaBresenham
    LineaBresenham_borrado(30, 50, 220, 50, win, pixel_size)   # línea inferior
    LineaBresenham_borrado(30, 240, 220, 240, win, pixel_size) # línea superior
    LineaBresenham_borrado(30, 50, 30, 240, win, pixel_size)   # línea izquierda
    LineaBresenham_borrado(220, 50, 220, 240, win, pixel_size) # línea derecha
    
personaje_elementos = []
personaje_original = []
def undraw_personaje(win, pixel_size):
    global personaje_elementos
    for elemento in personaje_elementos:
        x1, y1, x2, y2 = elemento
        # Desdibujamos ambos puntos de la línea (x1, y1) y (x2, y2)
        undraw_pixel(x1, y1, win, pixel_size)
        undraw_pixel(x2, y2, win, pixel_size)
    
    # Limpiamos la lista de elementos del personaje
    personaje_elementos.clear()  # Usamos clear() para vaciar la lista global
    vaciar_personaje()
    
def draw_personaje(win, puntos_rotados, pixel_size):
    undraw_personaje(win, pixel_size)
    for x, y in puntos_rotados:
        draw_pixel(x, y, win, pixel_size, color="black")  
        
def crear_obj(win=None, pixel_size=2):
    
    # Cabeza 
    LineaBresenham(-50, 12, -20, 12, win, pixel_size)
    LineaBresenham(-50, 42, -20, 42, win, pixel_size)
    LineaBresenham(-50, 12, -50, 42, win, pixel_size)
    LineaBresenham(-20, 12, -20, 42, win, pixel_size)
    # Torso
    LineaBresenham(-50, -50, -20, -50, win, pixel_size)
    LineaBresenham(-50, 10, -20, 10, win, pixel_size)
    LineaBresenham(-50, -50, -50, 10, win, pixel_size)
    LineaBresenham(-20, -50, -20, 10, win, pixel_size)
    # brazo 1
    LineaBresenham(-72, -50, -52, -50, win, pixel_size)
    LineaBresenham(-72, 10, -52, 10, win, pixel_size)
    LineaBresenham(-72, -50, -72, 10, win, pixel_size)
    LineaBresenham(-52, -50, -52, 10, win, pixel_size)
    # brazo 2
    LineaBresenham(-18, -50, 2, -50, win, pixel_size)
    LineaBresenham(-18, 10, 2, 10, win, pixel_size)
    LineaBresenham(-18, -50, -18, 10, win, pixel_size)
    LineaBresenham(2, -50, 2, 10, win, pixel_size)
    # pierna 1
    LineaBresenham(-50, -50, -35, -50, win, pixel_size)
    LineaBresenham(-50, -110, -35, -110, win, pixel_size)
    LineaBresenham(-50, -50, -50, -110, win, pixel_size)
    LineaBresenham(-35, -50, -35, -110, win, pixel_size)
    # pierna 2
    LineaBresenham(-35, -50, -20, -50, win, pixel_size)
    LineaBresenham(-35, -110, -20, -110, win, pixel_size)
    LineaBresenham(-35, -50, -35, -110, win, pixel_size)
    LineaBresenham(-20, -50, -20, -110, win, pixel_size)
    
    
    personaje_elementos = [
        # Cabeza
        (-50, 12, -20, 12),  # Línea superior izquierda
        (-50, 42, -20, 42),  # Línea superior derecha
        (-50, 12, -50, 42),  # Línea izquierda
        (-20, 12, -20, 42),  # Línea derecha
        
        # Torso
        (-50, -50, -20, -50),  # Línea inferior izquierda
        (-50, 10, -20, 10),    # Línea superior izquierda
        (-50, -50, -50, 10),   # Línea izquierda
        (-20, -50, -20, 10),   # Línea derecha
        
        # Brazo 1 (izquierdo)
        (-72, -50, -52, -50),  # Línea inferior
        (-72, 10, -52, 10),    # Línea superior
        (-72, -50, -72, 10),   # Línea izquierda
        (-52, -50, -52, 10),   # Línea derecha
        
        # Brazo 2 (derecho)
        (-18, -50, 2, -50),    # Línea inferior
        (-18, 10, 2, 10),      # Línea superior
        (-18, -50, -18, 10),   # Línea izquierda
        (2, -50, 2, 10),       # Línea derecha
        
        # Pierna 1 (izquierda)
        (-50, -50, -35, -50),  # Línea superior izquierda
        (-50, -110, -35, -110),  # Línea inferior izquierda
        (-50, -50, -50, -110),  # Línea izquierda
        (-35, -50, -35, -110),  # Línea derecha
        
        # Pierna 2 (derecha)
        (-35, -50, -20, -50),  # Línea superior izquierda
        (-35, -110, -20, -110),  # Línea inferior izquierda
        (-35, -50, -35, -110),  # Línea izquierda
        (-20, -50, -20, -110),  # Línea derecha
    ]
    
    return personaje_elementos

def crear_obj_inicial(win=None, pixel_size=2):
    # Función para transformar las coordenadas
    def transformar(x, y):
        escala_x, escala_y = 0.5, 0.5
        traslacion_x, traslacion_y = 200, -100
        return x * escala_x + traslacion_x, y * escala_y + traslacion_y

    # Función para dibujar las líneas usando el algoritmo de Bresenham
    def dibujar_linea(x1, y1, x2, y2):
        x1, y1 = transformar(x1, y1)
        x2, y2 = transformar(x2, y2)
        print(x1,y1,x2,y2, "\n")
        LineaBresenham(int(x1), int(y1), int(x2), int(y2), win, pixel_size)
    # Cabeza
    dibujar_linea(-50, 12, -20, 12)
    dibujar_linea(-50, 42, -20, 42)
    dibujar_linea(-50, 12, -50, 42)
    dibujar_linea(-20, 12, -20, 42)

    # Torso
    dibujar_linea(-50, -50, -20, -50)
    dibujar_linea(-50, 10, -20, 10)
    dibujar_linea(-50, -50, -50, 10)
    dibujar_linea(-20, -50, -20, 10)

    # Brazo 1
    dibujar_linea(-72, -50, -52, -50)
    dibujar_linea(-72, 10, -52, 10)
    dibujar_linea(-72, -50, -72, 10)
    dibujar_linea(-52, -50, -52, 10)

    # Brazo 2
    dibujar_linea(-18, -50, 2, -50)
    dibujar_linea(-18, 10, 2, 10)
    dibujar_linea(-18, -50, -18, 10)
    dibujar_linea(2, -50, 2, 10)

    # Pierna 1
    dibujar_linea(-50, -50, -34, -50)
    dibujar_linea(-50, -110, -34, -110)
    dibujar_linea(-50, -50, -50, -110)
    dibujar_linea(-34, -50, -34, -110)

    # Pierna 2
    dibujar_linea(-34, -50, -20, -50)
    dibujar_linea(-34, -110, -20, -110)
    dibujar_linea(-34, -50, -34, -110)
    dibujar_linea(-20, -50, -20, -110)

    personaje_original = [
        # Cabeza
        (175, -94, 190, -94),  # Línea superior izquierda
        (175, -79, 190, -79),  # Línea superior derecha
        (175, -94, 175, -79),  # Línea izquierda
        (190, -94, 190, -79),  # Línea derecha
        
        # Torso
        (175, -125, 190, -125),  # Línea inferior izquierda
        (175, -95, 190, -95),    # Línea superior izquierda
        (175, -125, 175, -95),   # Línea izquierda
        (190, -125, 190, -95),   # Línea derecha
        
        # Brazo 1 (izquierdo)
        (164, -125, 174, -125),  # Línea inferior
        (164, -95, 174, -95),    # Línea superior
        (164, -125, 164, -95),   # Línea izquierda
        (174, -125, 174, -95),   # Línea derecha
        
        # Brazo 2 (derecho)
        (191, -125, 201, -125),    # Línea inferior
        (191, -95, 201, -95),      # Línea superior
        (191, -125, 191, -95),   # Línea izquierda
        (201, -125, 201, -95),       # Línea derecha
        
        # Pierna 1 (izquierda)
        (175, -125, 183, -125),  # Línea superior izquierda
        (175, -155, 183, -155),  # Línea inferior izquierda
        (175, -125, 175, -155),  # Línea izquierda
        (183, -125, 183, -155),  # Línea derecha
        
        # Pierna 2 (derecha)
        (183, -125, 190, -125),  # Línea superior izquierda
        (183, -155, 190, -155),  # Línea inferior izquierda
        (183, -125, 183, -155),  # Línea izquierda
        (190, -125, 190, -155),  # Línea derecha
    ]
    
    return personaje_original

def codificar_punto(x, y, xmin, xmax, ymin, ymax):
    code = 0
    if x < xmin:  # A la izquierda de la ventana
        code |= 1  # bit 0
    elif x > xmax:  # A la derecha de la ventana
        code |= 2  # bit 1
    if y < ymin:  # Debajo de la ventana
        code |= 4  # bit 2
    elif y > ymax:  # Arriba de la ventana
        code |= 8  # bit 3
    return code

# Función de recorte Cohen-Sutherland
def cohen_sutherland_clip(x1, y1, x2, y2, xmin, xmax, ymin, ymax):
    # Códigos de los extremos
    code1 = codificar_punto(x1, y1, xmin, xmax, ymin, ymax)
    code2 = codificar_punto(x2, y2, xmin, xmax, ymin, ymax)
    aceptada = False

    while True:
        if (code1 == 0 and code2 == 0):  # Ambos puntos dentro de la ventana
            aceptada = True
            break
        elif (code1 & code2) != 0:  # Ambos puntos fuera de la ventana
            break
        else:
            # Determinar cuál de los puntos está fuera de la ventana
            code_out = code1 if code1 != 0 else code2
            if code_out & 8:  # Arriba de la ventana
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif code_out & 4:  # Abajo de la ventana
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif code_out & 2:  # A la derecha de la ventana
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif code_out & 1:  # A la izquierda de la ventana
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            # Actualizar el punto fuera de la ventana
            if code_out == code1:
                x1, y1 = x, y
                code1 = codificar_punto(x1, y1, xmin, xmax, ymin, ymax)
            else:
                x2, y2 = x, y
                code2 = codificar_punto(x2, y2, xmin, xmax, ymin, ymax)

    if aceptada:
        return (x1, y1, x2, y2)  # Retorna la línea recortada
    else:
        return None  # La línea está completamente fuera de la ventana
    
# Función para aplicar el algoritmo a todos los puntos
def recortar_personaje(personaje_elementos, xmin, xmax, ymin, ymax):
    personaje_recortado = []
    for (x1, y1, x2, y2) in personaje_elementos:
        recortado = cohen_sutherland_clip(x1, y1, x2, y2, xmin, xmax, ymin, ymax)
        if recortado:
            personaje_recortado.append(recortado)
    return personaje_recortado

def producto_punto(v1, v2):
    """Calcula el producto punto entre dos vectores v1 y v2."""
    return v1[0] * v2[0] + v1[1] * v2[1]

def intersecar_linea(p1, p2, borde):
    """Calcula el punto de intersección entre la línea p1-p2 y un borde dado."""
    # El borde se define como (P, N), donde P es un punto en el borde y N es el vector normal
    P, N = borde
    d1 = p1[0] - P[0], p1[1] - P[1]  # Vector desde P hasta p1
    d2 = p2[0] - P[0], p2[1] - P[1]  # Vector desde P hasta p2
    
    # Producto punto de los dos extremos con el normal del borde
    t = producto_punto(N, d1) / producto_punto(N, (d2[0] - d1[0], d2[1] - d1[1]))
    
    # Si t está entre 0 y 1, significa que la intersección está en el segmento
    if 0 <= t <= 1:
        # Calcular la intersección en el segmento
        interseccion = (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))
        return interseccion
    else:
        return None  # No hay intersección dentro del segmento

def cyrus_beck_clip(x1, y1, x2, y2, xmin, xmax, ymin, ymax):
    """Aplica el algoritmo Cyrus-Beck para recortar una línea dentro de una ventana rectangular."""
    # Definir los 4 bordes del rectángulo: (P, N), donde P es un punto del borde y N es el vector normal
    bordes = [
        ((xmin, ymin), (0, 1)),  # Borde inferior: (P, N)
        ((xmax, ymin), (1, 0)),  # Borde derecho
        ((xmax, ymax), (0, -1)),  # Borde superior
        ((xmin, ymax), (-1, 0))   # Borde izquierdo
    ]
    
    t_in = 0.0  # Parámetro t para la intersección
    t_out = 1.0  # Parámetro t para la intersección

    # Recorrer los bordes del rectángulo
    for P, N in bordes:
        # Calcular los productos puntos
        d1 = (x1 - P[0], y1 - P[1])
        d2 = (x2 - P[0], y2 - P[1])
        
        # Producto punto
        p1 = producto_punto(N, d1)
        p2 = producto_punto(N, d2)
        
        # Si ambos productos punto son positivos, la línea está completamente dentro del borde
        if p1 >= 0 and p2 >= 0:
            continue  # La línea está completamente dentro de la ventana (no se recorta)
        
        # Si ambos productos punto son negativos, la línea está completamente fuera del borde
        if p1 <= 0 and p2 <= 0:
            continue  # La línea está completamente fuera del borde (descartarla)
        
        # Calcular el parámetro t de la intersección
        t = p1 / (p1 - p2)
        
        # Actualizar t_in y t_out para limitar la línea
        if p1 > 0:
            t_in = max(t_in, t)  # El recorte debe estar dentro de la ventana
        else:
            t_out = min(t_out, t)  # El recorte debe estar dentro de la ventana
    
    # Si t_in > t_out, no hay intersección
    if t_in > t_out:
        return None
    
    # Si hay intersección, recortar la línea
    x1_recortado = x1 + (x2 - x1) * t_in
    y1_recortado = y1 + (y2 - y1) * t_in
    x2_recortado = x1 + (x2 - x1) * t_out
    y2_recortado = y1 + (y2 - y1) * t_out
    
    return (x1_recortado, y1_recortado, x2_recortado, y2_recortado)
# Función para aplicar el algoritmo a todos los puntos
def recortar_personaje_cyrus(personaje_elementos, xmin, xmax, ymin, ymax):
    personaje_recortado = []
    for (x1, y1, x2, y2) in personaje_elementos:
        recortado = cyrus_beck_clip(x1, y1, x2, y2, xmin, xmax, ymin, ymax)
        if recortado:
            personaje_recortado.append(recortado)
    return personaje_recortado

def esta_dentro(x, y, xmin, xmax, ymin, ymax):
    """Verifica si el punto (x, y) está dentro de los límites de la ventana."""
    return xmin <= x <= xmax and ymin <= y <= ymax

def intersecar_con_borde(x1, y1, x2, y2, xmin, xmax, ymin, ymax):
    """Recorta una línea a la ventana usando un método exhaustivo."""
    # Comprobar si ambos puntos están dentro de la ventana
    if esta_dentro(x1, y1, xmin, xmax, ymin, ymax) and esta_dentro(x2, y2, xmin, xmax, ymin, ymax):
        return (x1, y1, x2, y2)  # No hay recorte necesario
    
    # Recortar línea en cada borde de la ventana si es necesario
    # Los 4 bordes: inferior, derecho, superior, izquierdo
    puntos_recortados = []

    # Recortar con borde inferior (y = ymin)
    if y1 != y2:
        if (y1 < ymin and y2 > ymin) or (y1 > ymin and y2 < ymin):
            t = (ymin - y1) / (y2 - y1)
            x_interseccion = x1 + t * (x2 - x1)
            if xmin <= x_interseccion <= xmax:
                puntos_recortados.append((x_interseccion, ymin))
    
    # Recortar con borde superior (y = ymax)
    if y1 != y2:
        if (y1 > ymax and y2 < ymax) or (y1 < ymax and y2 > ymax):
            t = (ymax - y1) / (y2 - y1)
            x_interseccion = x1 + t * (x2 - x1)
            if xmin <= x_interseccion <= xmax:
                puntos_recortados.append((x_interseccion, ymax))

    # Recortar con borde izquierdo (x = xmin)
    if x1 != x2:
        if (x1 < xmin and x2 > xmin) or (x1 > xmin and x2 < xmin):
            t = (xmin - x1) / (x2 - x1)
            y_interseccion = y1 + t * (y2 - y1)
            if ymin <= y_interseccion <= ymax:
                puntos_recortados.append((xmin, y_interseccion))
    
    # Recortar con borde derecho (x = xmax)
    if x1 != x2:
        if (x1 > xmax and x2 < xmax) or (x1 < xmax and x2 > xmax):
            t = (xmax - x1) / (x2 - x1)
            y_interseccion = y1 + t * (y2 - y1)
            if ymin <= y_interseccion <= ymax:
                puntos_recortados.append((xmax, y_interseccion))

    if puntos_recortados:
        # Devuelve el primer y último punto recortado de la línea
        return (puntos_recortados[0][0], puntos_recortados[0][1], puntos_recortados[-1][0], puntos_recortados[-1][1])
    
    return None  # La línea no intersecta con la ventana

def recortar_personaje_exahustivo(personaje_elementos, xmin, xmax, ymin, ymax):
    """Recorta todos los elementos del personaje usando el algoritmo exhaustivo."""
    personaje_recortado = []
    for (x1, y1, x2, y2) in personaje_elementos:
        recortado = intersecar_con_borde(x1, y1, x2, y2, xmin, xmax, ymin, ymax)
        if recortado:
            personaje_recortado.append(recortado)
    return personaje_recortado

def menu(spacing = 40, button_width = 140, button_height = 30):
    # Crear un objeto de texto
    saludo_text = Text(Point(0, 5 * spacing), "¡Hola, Bienvenidos al Programa de Representaciones Graficas!")
    saludo_text.setSize(15)          
    saludo_text.setStyle("bold")      
    saludo_text.draw(win)
    
    lab_text = Text(Point(0, 4 * spacing), "Laboratorio 06: Clipping en 2D")
    lab_text.setSize(13)          
    lab_text.setStyle("bold")      
    lab_text.draw(win)
    
    autores_text = Text(Point(0, 2 * spacing), "Autores: \nVicente Santos\nCristobal Gallardo")
    autores_text.setSize(12) 
    autores_text.setStyle("bold")      
    autores_text.draw(win)
    
    iniciar_button = Button(win, Point(0, -50), button_width + 30, button_height, "Empezar programa")
    activity_button = Button(win, Point(0, -50- spacing), button_width + 30, button_height, "Empezar actividad")
    salir_button = Button(win, Point(0, -50 - 2 *spacing), button_width + 30, button_height, "Salir")
    
    iniciar_button.activate()
    activity_button.activate()
    salir_button.activate()
    
    while True:
        click_point = win.getMouse()
        
        if iniciar_button.is_clicked(click_point):
            # Borrar pantalla de inicio
            saludo_text.undraw()          
            lab_text.undraw()          
            autores_text.undraw()
            iniciar_button.undraw()     
            activity_button.undraw()
            salir_button.undraw()
            print("Mensaje y botón borrados")
            return 1
        elif activity_button.is_clicked(click_point):
            # Borrar pantalla de inicio
            saludo_text.undraw()          
            lab_text.undraw()          
            autores_text.undraw()
            iniciar_button.undraw()     
            activity_button.undraw()
            salir_button.undraw()
            print("Mensaje y botón borrados")
            return 2
        elif salir_button.is_clicked(click_point):
            win.close()
            return 0
        
# Función principal
def main():
    global personaje_elementos, win, personaje_original
    # Inicialización de variables
    width = 1000
    height = 1000
    # Coordenadas de los botones en el borde superior derecho
    button_width = 140
    button_height = 30
    x_position = 350
    y_start = 50
    spacing = 40
    
    # Inicializar la ventana
    win.setCoords(-width // 2, -height // 2, width // 2, height // 2)
    win.setBackground("white")

    # LLamar al menu
    print("\n\tBienvenidos al Programa de Representaciones Graficas")
    print("\nAutores : \n  Vicente Santos\n  Cristobal Gallardo")
    
    while True:
        program_on = menu(spacing, button_width, button_height)
        
        if program_on == 1:
            
            # Crear botones en el borde superior derecho
            crear_obj_button = Button(win, Point(x_position, y_start + 3 * spacing), button_width, button_height, "Crear personaje")
            aplicar_Sutherland_button = Button(win, Point(x_position, y_start + 2 * spacing), button_width, button_height, "Cohen-Sutherland")
            aplicarCyrus_button = Button(win, Point(x_position, y_start +  spacing), button_width, button_height, "Cyrus-Beck")
            aplicarExa_button = Button(win, Point(x_position, y_start), button_width, button_height, "Exahustivo")
            volver_button = Button(win, Point(x_position, y_start -  spacing), button_width, button_height, "Volver")
            salir_button = Button(win, Point(x_position, y_start - 2 * spacing), button_width, button_height, "Salir")
            
            error_text = Text(Point(0, 5 * spacing), "Ingrese un número valido")
            error_text.setSize(18) 
            error_text.setTextColor("red")
            error_text.setStyle("bold") 
            
            post_text = Text(Point(x_position, y_start - 4 * spacing + 20), "Pre-Clipping")
            post_text.setSize(10)          
            post_text.setStyle("bold")      
            post_text.draw(win)  
            # Activar los botones
            crear_obj_button.activate()
            aplicar_Sutherland_button.activate()
            aplicarCyrus_button.activate()
            aplicarExa_button.activate()
            volver_button.activate()
            salir_button.activate()
            # Declaraciones extras
            xmin, xmax, ymin, ymax = -150, 50, -100, 100
            
            # Esperar a que el usuario haga clic en uno de los botones
            running = True
            while running:
                    
                crear_ventana(win= win)
                crear_ventana_preview(win= win)
                click_point = win.getMouse()   
                    
                if crear_obj_button.is_clicked(click_point):
                    personaje_elementos = crear_obj(win, pixel_size)
                    personaje_original =  crear_obj_inicial(win,pixel_size)
                elif aplicar_Sutherland_button.is_clicked(click_point):
                    # Aplicar algoritmo de Cohen-Sutherland
                    personaje_recortado = recortar_personaje(personaje_elementos, xmin, xmax, ymin, ymax)
                    
                    # undraw_personaje(win,pixel_size)
                    for (x1, y1, x2, y2) in personaje_elementos:
                        LineaBresenham_borrado(x1, y1, x2, y2, win, 2)
                    # Dibujar las líneas del personaje recortadas
                    for (x1, y1, x2, y2) in personaje_recortado:
                        LineaBresenham(x1, y1, x2, y2, win, 2, color= "blue")
                        
                elif aplicarCyrus_button.is_clicked(click_point):
                    # Aplicar algoritmo de Cyrus-Beck
                    personaje_recortado = recortar_personaje_cyrus(personaje_elementos, xmin, xmax, ymin, ymax)
                    
                    # undraw_personaje(win,pixel_size)
                    for (x1, y1, x2, y2) in personaje_elementos:
                        LineaBresenham_borrado(x1, y1, x2, y2, win, 2)
                        
                    # Dibujar las líneas del personaje recortadas
                    for (x1, y1, x2, y2) in personaje_recortado:
                        LineaBresenham(x1, y1, x2, y2, win, 2, color= "red")
                        
                elif aplicarExa_button.is_clicked(click_point):
                    # Aplicar algoritmo de Cyrus-Beck
                    personaje_recortado = recortar_personaje_exahustivo(personaje_elementos, xmin, xmax, ymin, ymax)
                    
                    # undraw_personaje(win,pixel_size)
                    for (x1, y1, x2, y2) in personaje_elementos:
                        LineaBresenham_borrado(x1, y1, x2, y2, win, 2)
                        
                    # Dibujar las líneas del personaje recortadas
                    for (x1, y1, x2, y2) in personaje_recortado:
                        LineaBresenham(x1, y1, x2, y2, win, 2, color= "green")
                elif volver_button.is_clicked(click_point):
                    
                    crear_obj_button.undraw()
                    aplicar_Sutherland_button.undraw()
                    aplicarCyrus_button.undraw()
                    aplicarExa_button.undraw()
                    volver_button.undraw()
                    salir_button.undraw()
                    post_text.undraw()
                    crear_ventana_undraw(win= win)
                    crear_ventana_preview_undraw(win= win)
                    for (x1, y1, x2, y2) in personaje_elementos:
                        LineaBresenham_borrado(x1, y1, x2, y2, win, 2)
                    for (x1, y1, x2, y2) in personaje_original:
                        LineaBresenham_borrado(x1, y1, x2, y2, win, 2)
                    running = False
                elif salir_button.is_clicked(click_point):
                    win.close()
                    break
        elif program_on == 2:
            # Crear botones en el borde superior derecho
            crear_ventana_button = Button(win, Point(x_position * -1, y_start + 6 * spacing), button_width, button_height, "Crear ventana")
            crear_linea_button = Button(win, Point(x_position * -1, y_start + 5 * spacing), button_width, button_height, "Crear linea")
            aplicar_Sutherland_button = Button(win, Point(x_position  * -1, y_start ), button_width, button_height, "Cohen-Sutherland")
            aplicarCyrus_button = Button(win, Point(x_position  * -1, y_start - spacing), button_width, button_height, "Cyrus-Beck")
            aplicarExa_button = Button(win, Point(x_position  * -1, y_start - 2 * spacing), button_width, button_height, "Exahustivo")
            volver_button = Button(win, Point(x_position * -1, y_start - 3 * spacing), button_width, button_height, "Volver")
            salir_button = Button(win, Point(x_position * -1, y_start - 4 * spacing), button_width, button_height, "Salir")
            
            error_text = Text(Point(0, 5 * spacing), "Ingrese un número valido")
            error_text.setSize(18) 
            error_text.setTextColor("red")
            error_text.setStyle("bold") 
            
            x1_text = Text(Point((x_position * -1 )-30, y_start + 4 * spacing), "x1")
            x1_text.setSize(10)          
            x1_text.setStyle("bold")      
            x1_text.draw(win)  
            ingresar_texto_x1= Entry(Point((x_position * -1) + 30, y_start + 4 * spacing), 6)
            ingresar_texto_x1.setFill("lightgray")
            
            
            y1_text = Text(Point((x_position * -1 )-30, y_start + 3 * spacing), "y1")
            y1_text.setSize(10)          
            y1_text.setStyle("bold")      
            y1_text.draw(win)  
            ingresar_texto_y1= Entry(Point((x_position * -1) + 30, y_start + 3 * spacing), 6)
            ingresar_texto_y1.setFill("lightgray")
            
            x2_text = Text(Point((x_position * -1 )-30, y_start + 2 * spacing), "x2")
            x2_text.setSize(10)          
            x2_text.setStyle("bold")      
            x2_text.draw(win)  
            ingresar_texto_x2= Entry(Point((x_position * -1) + 30, y_start + 2 * spacing), 6)
            ingresar_texto_x2.setFill("lightgray")
            
            y2_text = Text(Point((x_position * -1 )-30, y_start +  spacing), "y2")
            y2_text.setSize(10)          
            y2_text.setStyle("bold")      
            y2_text.draw(win)  
            ingresar_texto_y2= Entry(Point((x_position * -1) + 30, y_start + spacing), 6)
            ingresar_texto_y2.setFill("lightgray")
            # Activar los botones
            crear_ventana_button.activate()
            crear_linea_button.activate()
            ingresar_texto_x1.draw(win)
            ingresar_texto_y1.draw(win)
            ingresar_texto_x2.draw(win)
            ingresar_texto_y2.draw(win)
            aplicar_Sutherland_button.activate()
            aplicarCyrus_button.activate()
            aplicarExa_button.activate()
            volver_button.activate()
            salir_button.activate()
            # Declaraciones extras
            xmin, xmax, ymin, ymax = 30, 220, 50, 240
            mensaje = 0
            puntos = []
            # Esperar a que el usuario haga clic en uno de los botones
            running = True
            while running:
                crear_ventana_activity(win=win)
                click_point = win.getMouse()   
                    
                if crear_ventana_button.is_clicked(click_point):
                    crear_ventana_activity(win=win)
                elif crear_linea_button.is_clicked(click_point):
                    texto_x1 = ingresar_texto_x1.getText()
                    texto_y1 = ingresar_texto_y1.getText()
                    texto_x2 = ingresar_texto_x2.getText()
                    texto_y2 = ingresar_texto_y2.getText()
                    
                    try:
                        P_x1 = int(texto_x1)
                        P_y1 = int(texto_y1)
                        P_x2 = int(texto_x2)
                        P_y2 = int(texto_y2)
                        
                        puntos.append((P_x1, P_y1, P_x2, P_y2))
                        LineaBresenham(P_x1,P_y1,P_x2,P_y2,win,pixel_size)
                        error_text.undraw()  
                    except ValueError:
                        print("Error: Ingresa un número entero.")
                        error_text.setText("Error: Ingresa un número entero.")
                        if mensaje == 0:
                            error_text.draw(win)
                            mensaje = 1
                        ingresar_texto_x1.setText("")
                        
                elif aplicar_Sutherland_button.is_clicked(click_point):
                    # Aplicar algoritmo de Cohen-Sutherland
                    puntos_recortado = recortar_personaje(puntos, xmin, xmax, ymin, ymax)
                    
                    # undraw_personaje(win,pixel_size)
                    for (x1, y1, x2, y2) in puntos:
                        LineaBresenham_borrado(x1, y1, x2, y2, win, 2)
                    # Dibujar las líneas del personaje recortadas
                    for (x1, y1, x2, y2) in puntos_recortado:
                        LineaBresenham(x1, y1, x2, y2, win, 2, color= "blue")
                        
                elif aplicarCyrus_button.is_clicked(click_point):
                    # Aplicar algoritmo de Cyrus-Beck
                    puntos_recortado = recortar_personaje_cyrus(puntos, xmin, xmax, ymin, ymax)
                    
                    # undraw_personaje(win,pixel_size)
                    for (x1, y1, x2, y2) in puntos:
                        LineaBresenham_borrado(x1, y1, x2, y2, win, 2)
                        
                    # Dibujar las líneas del personaje recortadas
                    for (x1, y1, x2, y2) in puntos_recortado:
                        LineaBresenham(x1, y1, x2, y2, win, 2, color= "red")
                        
                elif aplicarExa_button.is_clicked(click_point):
                    # Aplicar algoritmo de Cyrus-Beck
                    puntos_recortado = recortar_personaje_exahustivo(puntos, xmin, xmax, ymin, ymax)
                    
                    # undraw_personaje(win,pixel_size)
                    for (x1, y1, x2, y2) in puntos:
                        LineaBresenham_borrado(x1, y1, x2, y2, win, 2)
                        
                    # Dibujar las líneas del personaje recortadas
                    for (x1, y1, x2, y2) in puntos_recortado:
                        LineaBresenham(x1, y1, x2, y2, win, 2, color= "green")
                elif volver_button.is_clicked(click_point):
                    
                    crear_ventana_button.undraw()
                    crear_linea_button.undraw()
                    aplicar_Sutherland_button.undraw()
                    aplicarCyrus_button.undraw()
                    aplicarExa_button.undraw()
                    volver_button.undraw()
                    salir_button.undraw()
                    
                    crear_ventana_activity_undraw(win=win)
                    x1_text.undraw()
                    y1_text.undraw()
                    x2_text.undraw()
                    y2_text.undraw()
                    
                    ingresar_texto_x1.undraw()
                    ingresar_texto_y1.undraw()
                    ingresar_texto_x2.undraw()
                    ingresar_texto_y2.undraw()
                    # undraw_personaje(win,pixel_size)
                    for (x1, y1, x2, y2) in puntos:
                        LineaBresenham_borrado(x1, y1, x2, y2, win, 2)
                    running = False
                elif salir_button.is_clicked(click_point):
                    win.close()
                    break
        elif program_on == 0:
            break
main()