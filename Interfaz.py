import pygame
import sys

pygame.init()

#Colores (En formato RGB)
COLOR_FONDO = (255, 255, 255)
COLOR_BORDE = (58, 58, 60)
COLOR_TEXTO = (18, 18, 19)
COLOR_TECLA = (232, 232, 232)

#Dimensiones
ANCHO, ALTO = 600, 800
TAMANO_CELDA = 65
MARGEN = 5
RADIO_ESQUINA = 4

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Iggy's Letter Shuffle!")
fuente_letras = pygame.font.SysFont("Helvetica", 36, bold=True)
fuente_teclado = pygame.font.SysFont("Helvetica", 18, bold=True)

#CUADRICULA
def dibujar_cuadricula():
    inicio_x = (ANCHO - (5 * TAMANO_CELDA + 4 * MARGEN)) // 2
    inicio_y = 100
    
    for fila in range(6):
        for col in range(5):
            rect = pygame.Rect(
                inicio_x + col * (TAMANO_CELDA + MARGEN),
                inicio_y + fila * (TAMANO_CELDA + MARGEN),
                TAMANO_CELDA,
                TAMANO_CELDA
            )
            pygame.draw.rect(ventana, COLOR_BORDE, rect, 2, RADIO_ESQUINA)

#TECLADO
def dibujar_teclado():
    filas_teclado = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    alto_tecla = 55
    ancho_tecla = 40
    inicio_y_teclado = 550
    
    for i, fila in enumerate(filas_teclado):
        offset_x = (ANCHO - (len(fila) * (ancho_tecla + MARGEN))) // 2
        for j, letra in enumerate(fila):
            rect = pygame.Rect(
                offset_x + j * (ancho_tecla + MARGEN),
                inicio_y_teclado + i * (alto_tecla + MARGEN),
                ancho_tecla,
                alto_tecla
            )
            pygame.draw.rect(ventana, COLOR_TECLA, rect, 0, RADIO_ESQUINA)
            
            texto = fuente_teclado.render(letra, True, COLOR_TEXTO)
            texto_rect = texto.get_rect(center=rect.center)
            ventana.blit(texto, texto_rect)

#METODO MAIN
def main():
    reloj = pygame.time.Clock()
    
    while True:
        ventana.fill(COLOR_FONDO)
        
        titulo = fuente_letras.render("Iggy's Letter Shuffle", True, COLOR_TEXTO)
        ventana.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 30))
        
        dibujar_cuadricula()
        dibujar_teclado()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()