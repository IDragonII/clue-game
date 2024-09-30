import pygame
import sys

# Inicializa Pygame
pygame.init()

# Configuración de la ventana
screen = pygame.display.set_mode((556, 666))
pygame.display.set_caption("Juego Clue")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BUTTON_COLOR = (100, 150, 200)
BUTTON_HOVER_COLOR = (150, 200, 250)

# Variables globales
dialogo_visible = False
habitacion_texto = ''
personaje_texto = ''
arma_texto = ''
active_input = 0  # 0 para habitación, 1 para personaje, 2 para arma

# Función para mostrar el cuadro de diálogo
def dibujar_cuadro_dialogo():
    pygame.draw.rect(screen, GRAY, (100, 100, 356, 466))  # Cuadro de diálogo
    pygame.draw.rect(screen, BLACK, (100, 100, 356, 466), 2)  # Borde

    # Cuadros de llenado
    input_rect_1 = pygame.Rect(120, 150, 316, 40)  # Habitación
    input_rect_2 = pygame.Rect(120, 220, 316, 40)  # Personaje
    input_rect_3 = pygame.Rect(120, 290, 316, 40)  # Arma
    
    # Dibuja los cuadros de llenado
    pygame.draw.rect(screen, WHITE, input_rect_1)
    pygame.draw.rect(screen, WHITE, input_rect_2)
    pygame.draw.rect(screen, WHITE, input_rect_3)

    # Texto en los cuadros
    font = pygame.font.Font(None, 36)
    text_surface_1 = font.render("Nombre de la habitación:", True, BLACK)
    text_surface_2 = font.render("Nombre del personaje:", True, BLACK)
    text_surface_3 = font.render("Nombre del arma:", True, BLACK)
    screen.blit(text_surface_1, (120, 120))
    screen.blit(text_surface_2, (120, 190))
    screen.blit(text_surface_3, (120, 260))

    # Mostrar texto ingresado
    text_surface_habitacion = font.render(habitacion_texto, True, BLACK)
    text_surface_personaje = font.render(personaje_texto, True, BLACK)
    text_surface_arma = font.render(arma_texto, True, BLACK)
    screen.blit(text_surface_habitacion, (120, 150))
    screen.blit(text_surface_personaje, (120, 220))
    screen.blit(text_surface_arma, (120, 290))

    # Botón Comprobar
    button_rect = pygame.Rect(120, 370, 316, 40)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)  # Borde
    button_text = font.render("Comprobar", True, WHITE)
    screen.blit(button_text, (button_rect.x + 90, button_rect.y + 5))

    return button_rect

# Función para dibujar el botón principal
def dibujar_boton():
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(200, 600, 150, 50)

    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)  # Color al pasar el mouse
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)  # Color normal

    font = pygame.font.Font(None, 36)
    text_surface = font.render("Resolver", True, WHITE)
    screen.blit(text_surface, (button_rect.x + 25, button_rect.y + 10))

    return button_rect

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el botón principal es presionado
            if boton_rect.collidepoint(event.pos):
                dibujar_cuadro_dialogo()
            
            # Si el botón Comprobar es presionado
            if dialogo_visible:
                button_rect = pygame.Rect(120, 370, 316, 40)
                if button_rect.collidepoint(event.pos):
                    print("Habitación:", habitacion_texto)
                    print("Personaje:", personaje_texto)
                    print("Arma:", arma_texto)

            # Determina cuál cuadro de entrada se activa
            input_rect_1 = pygame.Rect(120, 150, 316, 40)
            input_rect_2 = pygame.Rect(120, 220, 316, 40)
            input_rect_3 = pygame.Rect(120, 290, 316, 40)
            if input_rect_1.collidepoint(event.pos):
                active_input = 0  # Habitación
            elif input_rect_2.collidepoint(event.pos):
                active_input = 1  # Personaje
            elif input_rect_3.collidepoint(event.pos):
                active_input = 2  # Arma

        if event.type == pygame.KEYDOWN and dialogo_visible:
            if event.key == pygame.K_RETURN:
                print("Habitación:", habitacion_texto)
                print("Personaje:", personaje_texto)
                print("Arma:", arma_texto)
                dialogo_visible = False  # Cierra el diálogo después de resolver
                habitacion_texto = ''  # Resetea el texto
                personaje_texto = ''  # Resetea el texto
                arma_texto = ''  # Resetea el texto
                active_input = 0  # Resetea el cuadro activo
            elif event.key == pygame.K_BACKSPACE:
                # Eliminar el último carácter del texto activo
                if active_input == 0 and len(habitacion_texto) > 0:
                    habitacion_texto = habitacion_texto[:-1]
                elif active_input == 1 and len(personaje_texto) > 0:
                    personaje_texto = personaje_texto[:-1]
                elif active_input == 2 and len(arma_texto) > 0:
                    arma_texto = arma_texto[:-1]
            else:
                # Agrega el carácter al texto activo
                if event.unicode:
                    if active_input == 0 and len(habitacion_texto) < 30:  # Limita el tamaño
                        habitacion_texto += event.unicode
                    elif active_input == 1 and len(personaje_texto) < 30:  # Limita el tamaño
                        personaje_texto += event.unicode
                    elif active_input == 2 and len(arma_texto) < 30:  # Limita el tamaño
                        arma_texto += event.unicode

    screen.fill(WHITE)  # Limpia la pantalla

    # Dibuja el botón principal
    boton_rect = dibujar_boton()

    # Dibuja el cuadro de diálogo si está visible
    if dialogo_visible:
        dibujar_cuadro_dialogo()

    pygame.display.flip()  # Actualiza la pantalla
