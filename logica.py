import os
import random
import diccionario
import sys

PALABRAS_TECH = [
    "ALGOR", "ARBOL", "AUDIO", "BANDA", "BUCLE", "BYTES", "CABLE", "CACHE", 
    "CANAL", "CAPAS", "CEROS", "CHIPS", "CICLO", "CLAVE", "CLOUD", "DATOS", 
    "DISCO", "FIBRA", "FLUJO", "GRAFO", "JAPON", "LENTE", "MACRO", "MARCA", "MEDIO", 
    "MICRO", "MODEM", "NODOS", "NUBES", "ONDAS", "PANEL", "PERRO", "PISTA", "PIXEL", 
    "PLACA", "POLOS", "PULSO", "RAMAS", "RANGO", "RATON", "REDES", "REGLA", 
    "RELOJ", "RUTAS", "SALTO", "SENAL", "SERIE", "TAREA", "TECLA", "TEXTO", 
    "VIDEO", "VIRUS"
]

def obtener_palabra_secreta():
    return random.choice(PALABRAS_TECH)

def obtener_ruta_diccionario():
    if getattr(sys, 'frozen', False):
        directorio_base = os.path.dirname(sys.executable)
    else:
        directorio_base = os.path.dirname(os.path.abspath(__file__))
        
    return os.path.join(directorio_base, "banco_palabras.txt")

def inicializar_banco_palabras():
    ruta_archivo = obtener_ruta_diccionario()
    
    if not os.path.exists(ruta_archivo):
        print(f"No se encontró el archivo. Descargando en: {ruta_archivo}")
        diccionario.generar_diccionario(ruta_archivo)
    
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        palabras = [linea.strip().upper() for linea in f.readlines()]
    
    palabras.sort() 
    return palabras

def busqueda_binaria_recursiva(lista, objetivo, inicio, fin):
    if inicio > fin: 
        return False
    
    medio = (inicio + fin) // 2
    
    if lista[medio] == objetivo: 
        return True
    elif lista[medio] > objetivo: 
        return busqueda_binaria_recursiva(lista, objetivo, inicio, medio - 1)
    else: 
        return busqueda_binaria_recursiva(lista, objetivo, medio + 1, fin)

def evaluar_intento(intento, secreta):
    resultado = ["gris_estado"] * 5
    secreta_lista = list(secreta)
    
    for i in range(5):
        if intento[i] == secreta[i]:
            resultado[i] = "verde"
            secreta_lista[i] = None 
            
    for i in range(5):
        if resultado[i] == "verde": 
            continue
        if intento[i] in secreta_lista:
            resultado[i] = "amarillo"
            secreta_lista[secreta_lista.index(intento[i])] = None 
            
    return resultado