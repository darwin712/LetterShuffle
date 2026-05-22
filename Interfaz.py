import pygame
import sys
import random

from logica import inicializar_banco_palabras, busqueda_binaria_recursiva, evaluar_intento, obtener_palabra_secreta

pygame.init()

ANCHO, ALTO = 600, 800
TAMANO_CELDA = 65
MARGEN = 5
RADIO_ESQUINA = 4

TEMA_CLARO = {
    "fondo": (255, 255, 255), "borde": (211, 214, 218), "borde_activo": (135, 138, 140), "texto": (18, 18, 19),
    "tecla": (211, 214, 218), "boton": (200, 200, 200), "boton_hover": (180, 180, 180),
    "boton_press": (150, 150, 150), "switch_bg": (200, 200, 200), "switch_knob": (255, 255, 255),
    "verde": (106, 170, 100), "amarillo": (201, 180, 88), "gris_estado": (120, 124, 126), "texto_resalte": (255, 255, 255)
}

TEMA_OSCURO = {
    "fondo": (18, 18, 19), "borde": (58, 58, 60), "borde_activo": (86, 87, 88), "texto": (255, 255, 255),
    "tecla": (129, 131, 132), "boton": (86, 87, 88), "boton_hover": (106, 107, 108),
    "boton_press": (66, 67, 68), "switch_bg": (86, 87, 88), "switch_knob": (18, 18, 19),
    "verde": (83, 141, 78), "amarillo": (181, 159, 59), "gris_estado": (58, 58, 60), "texto_resalte": (255, 255, 255)
}

ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("Iggy's Letter Shuffle!")

fuente_letras = pygame.font.SysFont("Helvetica", 36, bold=True)
fuente_teclado = pygame.font.SysFont("Helvetica", 18, bold=True)
fuente_botones = pygame.font.SysFont("Helvetica", 14, bold=True)
fuente_mensajes = pygame.font.SysFont("Helvetica", 18, bold=True)

rect_switch = pygame.Rect(20, 20, 60, 30) 
rect_boton_dinamico = pygame.Rect(ANCHO - 145, ALTO - 50, 130, 35)

def lerp_color(color_actual, color_objetivo, velocidad):
    return (
        int(color_actual[0] + (color_objetivo[0] - color_actual[0]) * velocidad),
        int(color_actual[1] + (color_objetivo[1] - color_actual[1]) * velocidad),
        int(color_actual[2] + (color_objetivo[2] - color_actual[2]) * velocidad)
    )

def dibujar_cuadricula(tema, intentos_pasados, intento_actual):
    inicio_x = (ANCHO - (5 * TAMANO_CELDA + 4 * MARGEN)) // 2
    inicio_y = max(80, int(ALTO * 0.4) - 200)
    
    for fila in range(6):
        for col in range(5):
            rect = pygame.Rect(
                inicio_x + col * (TAMANO_CELDA + MARGEN),
                inicio_y + fila * (TAMANO_CELDA + MARGEN),
                TAMANO_CELDA, TAMANO_CELDA
            )
            
            letra = ""
            color_fondo = tema["fondo"]
            color_texto = tema["texto"]
            color_borde = tema["borde"]
            grosor = 2
            
            if fila < len(intentos_pasados):
                palabra, colores = intentos_pasados[fila]
                letra = palabra[col]
                color_fondo = tema[colores[col]] 
                color_texto = tema["texto_resalte"]
                color_borde = color_fondo
                grosor = 0 
                
            elif fila == len(intentos_pasados):
                if col < len(intento_actual):
                    letra = intento_actual[col]
                    color_borde = tema["borde_activo"]

            if grosor == 0:
                pygame.draw.rect(ventana, color_fondo, rect, 0, RADIO_ESQUINA)
            else:
                pygame.draw.rect(ventana, color_fondo, rect, 0, RADIO_ESQUINA)
                pygame.draw.rect(ventana, color_borde, rect, grosor, RADIO_ESQUINA)

            if letra:
                texto_surface = fuente_letras.render(letra, True, color_texto)
                ventana.blit(texto_surface, texto_surface.get_rect(center=rect.center))

def dibujar_teclado(tema, estado_teclado):
    filas_teclado = ["QWERTYUIOP", "ASDFGHJKLÑ", "ZXCVBNM"]
    alto_tecla = 55
    ancho_tecla = 40
    inicio_y_teclado = max(500, int(ALTO * 0.8) - 90)
    
    for i, fila in enumerate(filas_teclado):
        offset_x = (ANCHO - (len(fila) * (ancho_tecla + MARGEN))) // 2
        for j, letra in enumerate(fila):
            rect = pygame.Rect(
                offset_x + j * (ancho_tecla + MARGEN),
                inicio_y_teclado + i * (alto_tecla + MARGEN),
                ancho_tecla, alto_tecla
            )
            
            estado = estado_teclado[letra]
            if estado == "neutro":
                color_tecla = tema["tecla"]
                color_texto_tecla = tema["texto"]
            else:
                color_tecla = tema[estado]
                color_texto_tecla = tema["texto_resalte"]
            
            pygame.draw.rect(ventana, color_tecla, rect, 0, RADIO_ESQUINA)
            texto = fuente_teclado.render(letra, True, color_texto_tecla)
            ventana.blit(texto, texto.get_rect(center=rect.center))

def dibujar_ui(tema, switch_x, mouse_pos, mouse_pressed, mensaje_superior, juego_terminado):
    pygame.draw.rect(ventana, tema["switch_bg"], rect_switch, 0, 15)
    pygame.draw.circle(ventana, tema["switch_knob"], (int(switch_x), rect_switch.centery), 11)

    color_boton = tema["boton"]
    desplazamiento_y = 0
    if rect_boton_dinamico.collidepoint(mouse_pos):
        if mouse_pressed[0]: 
            color_boton = tema["boton_press"]
            desplazamiento_y = 2 
        else:
            color_boton = tema["boton_hover"]
            
    pygame.draw.rect(ventana, color_boton, rect_boton_dinamico, 0, RADIO_ESQUINA)
    texto_a_mostrar = "Nuevo Juego" if juego_terminado else "Revelar"
    texto_boton = fuente_botones.render(texto_a_mostrar, True, tema["texto"])
    ventana.blit(texto_boton, texto_boton.get_rect(center=(rect_boton_dinamico.centerx, rect_boton_dinamico.centery + desplazamiento_y)))

    if mensaje_superior:
        texto_msg = fuente_mensajes.render(mensaje_superior, True, tema["texto"])
        fondo_msg = pygame.Rect(0, 0, texto_msg.get_width() + 20, texto_msg.get_height() + 10)
        fondo_msg.center = (ANCHO // 2, 75)
        
        pygame.draw.rect(ventana, tema["fondo"], fondo_msg, 0, RADIO_ESQUINA)
        pygame.draw.rect(ventana, tema["borde"], fondo_msg, 2, RADIO_ESQUINA)
        ventana.blit(texto_msg, texto_msg.get_rect(center=fondo_msg.center))

def reiniciar_juego():
    palabra_secreta = obtener_palabra_secreta() 
    intentos_pasados = [] 
    intento_actual = ""
    
    # ¡INICIALIZAMOS EL TECLADO CON LA Ñ INCLUIDA!
    estado_teclado = {letra: "neutro" for fila in ["QWERTYUIOP", "ASDFGHJKLÑ", "ZXCVBNM"] for letra in fila}
    
    juego_terminado = False
    mensaje_pantalla = ""
    return palabra_secreta, intentos_pasados, intento_actual, estado_teclado, juego_terminado, mensaje_pantalla

def main():
    global ANCHO, ALTO, ventana 

    reloj = pygame.time.Clock()
    
    diccionario_validacion = inicializar_banco_palabras()
    
    palabra_secreta, intentos_pasados, intento_actual, estado_teclado, juego_terminado, mensaje_pantalla = reiniciar_juego()
    
    modo_oscuro = False
    tema_objetivo = TEMA_CLARO
    tema_dinamico = {clave: valor for clave, valor in TEMA_CLARO.items()}
    switch_x = rect_switch.left + 15
    velocidad_transicion = 0.1

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        for clave in tema_dinamico:
            tema_dinamico[clave] = lerp_color(tema_dinamico[clave], tema_objetivo[clave], velocidad_transicion)
        objetivo_x = rect_switch.right - 15 if modo_oscuro else rect_switch.left + 15
        switch_x += (objetivo_x - switch_x) * velocidad_transicion

        ventana.fill(tema_dinamico["fondo"])
        titulo = fuente_letras.render("Iggy's Letter Shuffle", True, tema_dinamico["texto"])
        ventana.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 25))
        
        dibujar_cuadricula(tema_dinamico, intentos_pasados, intento_actual)
        dibujar_teclado(tema_dinamico, estado_teclado)
        dibujar_ui(tema_dinamico, switch_x, mouse_pos, mouse_pressed, mensaje_pantalla, juego_terminado)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.VIDEORESIZE:
                ANCHO, ALTO = evento.w, evento.h
                ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
                rect_boton_dinamico.topleft = (ANCHO - 145, ALTO - 50)
                
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: 
                    if rect_switch.collidepoint(evento.pos):
                        modo_oscuro = not modo_oscuro
                        tema_objetivo = TEMA_OSCURO if modo_oscuro else TEMA_CLARO
                        
                    elif rect_boton_dinamico.collidepoint(evento.pos):
                        if juego_terminado:
                            palabra_secreta, intentos_pasados, intento_actual, estado_teclado, juego_terminado, mensaje_pantalla = reiniciar_juego()
                        else:
                            mensaje_pantalla = f"Pista: {palabra_secreta}"
                        
            elif evento.type == pygame.KEYDOWN and not juego_terminado:
                mensaje_pantalla = "" 
                
                if evento.key == pygame.K_BACKSPACE:
                    intento_actual = intento_actual[:-1]
                    
                elif evento.key == pygame.K_RETURN:
                    if len(intento_actual) == 5:
                        
                        es_valida = busqueda_binaria_recursiva(diccionario_validacion, intento_actual, 0, len(diccionario_validacion) - 1)
                        
                        if es_valida:
                            colores_resultado = evaluar_intento(intento_actual, palabra_secreta)
                            intentos_pasados.append((intento_actual, colores_resultado))
                            
                            for i, letra in enumerate(intento_actual):
                                estado_previo = estado_teclado[letra]
                                nuevo_estado = colores_resultado[i]
                                
                                if nuevo_estado == "verde":
                                    estado_teclado[letra] = "verde"
                                elif nuevo_estado == "amarillo" and estado_previo != "verde":
                                    estado_teclado[letra] = "amarillo"
                                elif nuevo_estado == "gris_estado" and estado_previo not in ["verde", "amarillo"]:
                                    estado_teclado[letra] = "gris_estado"
                                    
                            intento_actual = ""
                            
                            if intentos_pasados[-1][0] == palabra_secreta:
                                juego_terminado = True
                                mensaje_pantalla = "¡Genial! Has ganado."
                            elif len(intentos_pasados) == 6:
                                juego_terminado = True
                                mensaje_pantalla = f"Fin del juego. La palabra era: {palabra_secreta}"
                                
                        else:
                            mensaje_pantalla = "No está en el diccionario"

                    else:
                        mensaje_pantalla = "Faltan letras"
                        
                elif evento.unicode.isalpha() and len(intento_actual) < 5:
                    intento_actual += evento.unicode.upper()
        
        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()