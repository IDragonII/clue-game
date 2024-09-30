import pygame
import sys
from pygame.locals import *
from z3 import *

pygame.init()

ancho, alto = 556, 666
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Menú Principal')

color_fondo = (30, 30, 30)
color_boton = (200, 200, 200)
color_boton_hover = (150, 150, 150)
color_texto = (255, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

intentos_comprobar = 0 

fuente_boton = pygame.font.Font(None, 50)
fuente_boton_volver = pygame.font.Font(None, 20)
fuente_dialogo = pygame.font.Font(None, 30)

dialogo_visible = False

resultado_visible = False 
habitacion_texto = ''
personaje_texto = ''
arma_texto = ''

active_input = 0
resuelto = False

fondo = pygame.image.load("fondo_clue2.png").convert()
fondo = pygame.transform.scale(fondo, (ancho, alto))

colonel_mustard = Bool("colonel mustard")  # Coronel Mustard es el culpable.
miss_scarlet = Bool("miss scarlet")         # Miss Scarlet es la culpable.
professor_plum = Bool("professor plum")     # Profesor Plum es el culpable.
mrs_peacock = Bool("mrs peacock")           # Mrs. Peacock es la culpable.
reverend_green = Bool("reverend green")     # Reverend Green es el culpable.
mrs_white = Bool("mrs white")               # Mrs. White es la culpable.

kitchen = Bool("cocina")                    # El crimen ocurrió en la Cocina.
dining_room = Bool("comedor")            # El crimen ocurrió en el Comedor.
living_room = Bool("sala")            # El crimen ocurrió en la Sala.
library = Bool("libreria")                    # El crimen ocurrió en la Biblioteca.
study = Bool("studio")                        # El crimen ocurrió en el Estudio.
garden = Bool("conservatorio")                      # El crimen ocurrió en el Jardín.

knife = Bool("cuchillo")                        # Se utilizó el cuchillo.
revolver = Bool("revolver")                  # Se utilizó el revólver.
rope = Bool("cuerda")                          # Se utilizó la cuerda.
poison = Bool("veneno")                      # Se utilizó el veneno.
candlestick = Bool("candelabro")            # Se utilizó el candelabro.

knowledge = And(
    Not(living_room),            # El crimen NO ocurrió en la Sala.
    Not(library),                # El crimen NO ocurrió en la Biblioteca.
    Not(study),                  # El crimen NO ocurrió en el Estudio.
    Not(garden),                 # El crimen NO ocurrió en el Jardín.
    
    Or(kitchen, dining_room),    # El crimen ocurrió en la Cocina o en el Comedor.
    
    Not(revolver),               # El revólver NO fue usado.
    Implies(knife, Not(kitchen)),     # Si se usó el cuchillo, el crimen fue en la Cocina.
    Implies(candlestick, dining_room),  # Si se usó el candelabro, el crimen fue en el Comedor.
    
    Implies(professor_plum, Not(kitchen)),   # Si el Profesor Plum es el culpable, NO fue en la Cocina.
    Implies(miss_scarlet, dining_room),      # Si Miss Scarlet es la culpable, el crimen fue en el Comedor.

    Implies(mrs_white, Not(candlestick)),    # Si Mrs. White es culpable, no se usó el candelabro.
    Implies(colonel_mustard, knife),         # Si el Coronel Mustard es culpable, se usó el cuchillo.
    
    Or(knife, poison, candlestick),  # El crimen se cometió con el cuchillo, veneno o candelabro.
    Not(rope),                       # La cuerda NO fue usada.
    
    Implies(dining_room, knife),     # Si el crimen fue en el comedor, no se usó el cuchillo.
    Implies(kitchen, Not(candlestick)),   # Si el crimen fue en la cocina, no se usó el candelabro.
    
    Implies(Not(miss_scarlet), mrs_peacock),  # Si no fue Miss Scarlet, entonces fue Mrs. Peacock.
    Not(mrs_peacock)                          # Mrs. Peacock no fue la culpable.
)

def check_accusation(knowledge, query):
    s = Solver()
    s.add(knowledge)
    s.add(Not(query))
    if s.check() == unsat:
        return True
    else:
        return False
    
habitaciones_rects = {
    "Conservatorio": pygame.Rect(40, 160, 100, 100),
    "Cuarto de billar": pygame.Rect(40, 280, 100, 100),
    "Biblioteca": pygame.Rect(40, 420, 110, 100),
    "Estudio": pygame.Rect(35, 550, 120, 100),
    "Salón de baile": pygame.Rect(185, 195, 120, 100),
    "Entrada": pygame.Rect(200, 515, 105, 115),
    "Cocina": pygame.Rect(350, 195, 100, 100),
    "Comedor": pygame.Rect(340, 365, 110, 100),
    "Salón": pygame.Rect(350, 540, 100, 100),
}

personajes_rects = {
    "Miss Scarlett": pygame.Rect(0, 0, 80, 145),
    "Professor Plum": pygame.Rect(80, 0, 80, 145),
    "Mrs. Peacock": pygame.Rect(160, 0, 80, 145),
    "Mr. Green": pygame.Rect(240, 0, 80, 145),
    "Colonel Mustard": pygame.Rect(320, 0, 80, 145),
    "Mrs. White": pygame.Rect(400, 0, 80, 145),
}

armas_rects = {
    "Cuchillo": pygame.Rect(480, 0, 75, 110),
    "Llave": pygame.Rect(480, 110, 75, 110),
    "Pistola": pygame.Rect(480, 220, 75, 110),
    "Gancho": pygame.Rect(480, 330, 75, 110),
    "Candelabro": pygame.Rect(480, 440, 75, 110),
    "Bomba": pygame.Rect(480, 550, 75, 110),
}

pistas = {
    "Conservatorio": "Pista: Un perfume femenino muy fuerte se percibe aquí.",
    "Cuarto de billar": "Pista: Alguien dejó una copa de vino sin terminar.",
    "Biblioteca": "Pista: Un libro de recetas está fuera de lugar.",
    "Estudio": "Pista: Alguien mencionó una fuerte discusión en este cuarto.",
    "Salón de baile": "Pista: Un tacón roto fue encontrado en el suelo.",
    "Entrada": "Pista: Se encontraron marcas de barro recientes.",
    "Cocina": "Pista: Faltaba un cuchillo del soporte, pero se limpió rápidamente.",
    "Comedor": "Pista: Restos de vino y una ligera mancha de sangre se ven en la mesa.",
    "Salón": "Pista: Alguien dejó caer una llave al suelo.",

    "Miss Scarlett": "Pista: Miss Scarlett mencionó que pasó por la cocina antes de ir al comedor.",
    "Professor Plum": "Pista: Professor Plum estaba discutiendo con Miss Scarlett sobre algo antes del crimen.",
    "Mrs. Peacock": "Pista: Mrs. Peacock dijo que vio a Miss Scarlett entrar al comedor después de la cena.",
    "Mr. Green": "Pista: Mr. Green escuchó un sonido metálico en la cocina justo antes del incidente.",
    "Colonel Mustard": "Pista: El Coronel comentó que el cuchillo de la cocina fue utilizado recientemente.",
    "Mrs. White": "Pista: Mrs. White estaba limpiando cerca del comedor cuando escuchó un ruido extraño.",

    "Cuchillo": "Pista: Aunque estaba limpio, se notaba un pequeño arañazo en el mango.",
    "Llave": "Pista: La llave del salón fue encontrada cerca del comedor.",
    "Pistola": "Pista: Aunque estaba en su sitio, la pistola no fue usada.",
    "Gancho": "Pista: No parece haber signos de lucha con este objeto.",
    "Candelabro": "Pista: Estaba intacto, con una vela casi consumida.",
    "Bomba": "Pista: No se encontraron señales de explosivos en la casa."
}

texto_dialogo = ""
oportunidades = 6
cuadro_dialogo_visible = False
resuelto = False

def mostrar_dialogo():
    if cuadro_dialogo_visible:
        cuadro_rect = pygame.Rect(50, 300, 400, 200)
        pygame.draw.rect(pantalla, (50, 50, 50), cuadro_rect)
        pygame.draw.rect(pantalla, (200, 200, 200), cuadro_rect, 5)
        
        if oportunidades > 0:
            # Divide el texto en varias líneas
            lineas = dividir_texto(texto_dialogo, fuente_dialogo, cuadro_rect.width - 20)
            y_offset = cuadro_rect.y + 20  # Ajuste para la altura de las líneas
            for linea in lineas:
                texto_renderizado = fuente_dialogo.render(linea, True, color_texto)
                pantalla.blit(texto_renderizado, (cuadro_rect.x + 10, y_offset))
                y_offset += fuente_dialogo.get_height() + 5  # Ajusta la separación entre líneas
        else:
            mensaje = "No tienes más oportunidades."
            texto_renderizado = fuente_dialogo.render(mensaje, True, color_texto)
            texto_rect = texto_renderizado.get_rect(center=(cuadro_rect.centerx, cuadro_rect.centery))
            pantalla.blit(texto_renderizado, texto_rect)

def manejar_clic(mouse_x, mouse_y):
    global texto_dialogo, oportunidades, cuadro_dialogo_visible
    if oportunidades > 0:
        for nombre, rect in habitaciones_rects.items():
            if rect.collidepoint(mouse_x, mouse_y):
                texto_dialogo = pistas[nombre]
                oportunidades -= 1
                cuadro_dialogo_visible = True
                return
        for nombre, rect in personajes_rects.items():
            if rect.collidepoint(mouse_x, mouse_y):
                texto_dialogo = pistas[nombre]
                oportunidades -= 1
                cuadro_dialogo_visible = True
                return
        for nombre, rect in armas_rects.items():
            if rect.collidepoint(mouse_x, mouse_y):
                texto_dialogo = pistas[nombre]
                oportunidades -= 1
                cuadro_dialogo_visible = True
                return
    cuadro_dialogo_visible = False

def dividir_texto(texto, fuente, ancho_maximo):
    palabras = texto.split(' ')
    lineas = []
    linea_actual = ""
    
    for palabra in palabras:
        linea_con_palabra = linea_actual + palabra + " "
        if fuente.size(linea_con_palabra)[0] <= ancho_maximo:
            linea_actual = linea_con_palabra
        else:
            lineas.append(linea_actual)
            linea_actual = palabra + " "
    
    if linea_actual:
        lineas.append(linea_actual)
    
    return lineas


def intentar_resolver():
    global dialogo_visible, resuelto
    dialogo_visible = True
    resuelto = True

def menu_principal():
    while True:
        pantalla.fill(color_fondo)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        iniciar_hover = 200 <= mouse_x <= 400 and 200 <= mouse_y <= 300
        salir_hover = 200 <= mouse_x <= 400 and 350 <= mouse_y <= 450
        dibujar_boton("Iniciar", 200, 200, 200, 100, color_boton_hover if iniciar_hover else color_boton, fuente_boton)
        dibujar_boton("Salir", 200, 350, 200, 100, color_boton_hover if salir_hover else color_boton, fuente_boton)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if iniciar_hover:
                    juego()
                if salir_hover:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
def dibujar_cuadro_dialogo():
    pygame.draw.rect(pantalla, GRAY, (100, 100, 356, 466))
    pygame.draw.rect(pantalla, BLACK, (100, 100, 356, 466), 2)

    input_rect_1 = pygame.Rect(120, 150, 316, 40)
    input_rect_2 = pygame.Rect(120, 220, 316, 40)
    input_rect_3 = pygame.Rect(120, 290, 316, 40)

    pygame.draw.rect(pantalla, WHITE, input_rect_1)
    pygame.draw.rect(pantalla, WHITE, input_rect_2)
    pygame.draw.rect(pantalla, WHITE, input_rect_3)

    text_surface_1 = fuente_dialogo.render("Nombre de la habitación:", True, BLACK)
    text_surface_2 = fuente_dialogo.render("Nombre del personaje:", True, BLACK)
    text_surface_3 = fuente_dialogo.render("Nombre del arma:", True, BLACK)
    pantalla.blit(text_surface_1, (120, 120))
    pantalla.blit(text_surface_2, (120, 190))
    pantalla.blit(text_surface_3, (120, 260))

    text_surface_habitacion = fuente_dialogo.render(habitacion_texto, True, BLACK)
    text_surface_personaje = fuente_dialogo.render(personaje_texto, True, BLACK)
    text_surface_arma = fuente_dialogo.render(arma_texto, True, BLACK)
    pantalla.blit(text_surface_habitacion, (120, 150))
    pantalla.blit(text_surface_personaje, (120, 220))
    pantalla.blit(text_surface_arma, (120, 290))

    button_rect = pygame.Rect(120, 370, 316, 40)
    pygame.draw.rect(pantalla, color_boton, button_rect)
    pygame.draw.rect(pantalla, BLACK, button_rect, 2)
    button_text = fuente_dialogo.render("Comprobar", True, WHITE)
    pantalla.blit(button_text, (button_rect.x + 90, button_rect.y + 5))

    cerrar_rect = pygame.Rect(120, 420, 316, 40) 
    pygame.draw.rect(pantalla, color_boton, cerrar_rect)
    pygame.draw.rect(pantalla, BLACK, cerrar_rect, 2)
    cerrar_text = fuente_dialogo.render("Cerrar", True, WHITE)
    pantalla.blit(cerrar_text, (cerrar_rect.x + 120, cerrar_rect.y + 5))

    return button_rect,cerrar_rect 
def dibujar_cuadro_resultado(res_acusado,res_lugar,res_arma):
    pygame.draw.rect(pantalla, GRAY, (100, 100, 356, 200))
    pygame.draw.rect(pantalla, BLACK, (100, 100, 356, 200), 2) 
    if res_lugar == 1 and res_acusado == 1 and res_arma == 1:
        resultado_texto = f"Felicidades\ndescubriste el crimen"
    else:
        resultado_texto = f"Sigue intentando\nfallaste algo o todo"
    for i, line in enumerate(resultado_texto.split("\n")):
        text_surface = fuente_dialogo.render(line, True, BLACK)
        pantalla.blit(text_surface, (120, 130 + i * 40))
def juego():
    global dialogo_visible,resultado_visible, habitacion_texto, intentos_comprobar,tiempo_resultado, personaje_texto, arma_texto, active_input, resuelto
    while True:
        pantalla.blit(fondo, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        volver_hover = 223 <= mouse_x <= 273 and 450 <= mouse_y <= 475
        resolver_hover = 223 <= mouse_x <= 273 and 400 <= mouse_y <= 425

        dibujar_boton("Volver", 223, 450, 50, 25, color_boton_hover if volver_hover else color_boton, fuente_boton_volver)
        dibujar_boton("Resolver", 223, 400, 50, 25, color_boton_hover if resolver_hover else color_boton, fuente_boton_volver)
        mostrar_dialogo()
        if dialogo_visible:
            button_rect,cerrar_rect = dibujar_cuadro_dialogo()
        if resultado_visible:
            button_rect_resultado = dibujar_cuadro_resultado(res_acusado,res_lugar,res_arma)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if volver_hover:
                    menu_principal()
                elif resolver_hover:
                    intentar_resolver()
                elif dialogo_visible and button_rect.collidepoint(evento.pos):
                    acusado = Bool(personaje_texto)
                    lugar = Bool(habitacion_texto)
                    arma = Bool(arma_texto)
                    res_acusado=check_accusation(knowledge, acusado)
                    res_lugar=check_accusation(knowledge, lugar)
                    res_arma=check_accusation(knowledge, arma)
                    if intentos_comprobar < 3:
                        resultado_visible = True
                        print("El culpable es", check_accusation(knowledge, acusado))
                        print("El Lugar es", check_accusation(knowledge, lugar))
                        print("El arma es", check_accusation(knowledge, arma))
                        tiempo_resultado = pygame.time.get_ticks()
                        intentos_comprobar += 1
                    else:
                        print("Se ha alcanzado el límite de intentos para comprobar.")
                elif dialogo_visible and cerrar_rect.collidepoint(evento.pos):
                    dialogo_visible = False
                else:
                    manejar_clic(mouse_x, mouse_y)

            if evento.type == pygame.MOUSEBUTTONDOWN and dialogo_visible:
                input_rect_1 = pygame.Rect(120, 150, 316, 40)
                input_rect_2 = pygame.Rect(120, 220, 316, 40)
                input_rect_3 = pygame.Rect(120, 290, 316, 40)
                
                if input_rect_1.collidepoint(evento.pos):
                    active_input = 0
                elif input_rect_2.collidepoint(evento.pos):
                    active_input = 1
                elif input_rect_3.collidepoint(evento.pos):
                    active_input = 2

            if evento.type == pygame.KEYDOWN and dialogo_visible:
                if evento.key == pygame.K_RETURN:
                    dialogo_visible = False
                    habitacion_texto = ''  
                    personaje_texto = ''
                    arma_texto = ''
                    active_input = 0
                elif evento.key == pygame.K_BACKSPACE:
                    if active_input == 0 and len(habitacion_texto) > 0:
                        habitacion_texto = habitacion_texto[:-1]
                    elif active_input == 1 and len(personaje_texto) > 0:
                        personaje_texto = personaje_texto[:-1]
                    elif active_input == 2 and len(arma_texto) > 0:
                        arma_texto = arma_texto[:-1]
                else:
                    if evento.unicode:
                        if active_input == 0 and len(habitacion_texto) < 30:
                            habitacion_texto += evento.unicode
                        elif active_input == 1 and len(personaje_texto) < 30:
                            personaje_texto += evento.unicode
                        elif active_input == 2 and len(arma_texto) < 30:
                            arma_texto += evento.unicode
        if resultado_visible and pygame.time.get_ticks() - tiempo_resultado > 3000:
            resultado_visible = False
        pygame.display.flip()

def dibujar_boton(texto, x, y, ancho, alto, color, fuente):
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto))
    texto_renderizado = fuente.render(texto, True, color_texto)
    pantalla.blit(texto_renderizado, (x + (ancho - texto_renderizado.get_width()) // 2, y + (alto - texto_renderizado.get_height()) // 2))

menu_principal()
