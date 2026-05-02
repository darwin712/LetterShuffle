import os
import random

# ==========================================
# LÓGICA DEL BANCO DE PALABRAS Y ALGORITMOS
# ==========================================

# Tu lista original de respuestas de tecnología
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
    """Elige una palabra al azar SOLO de la lista de tecnología."""
    return random.choice(PALABRAS_TECH)

def inicializar_banco_palabras():
    """Lee el diccionario masivo para validar los intentos."""
    nombre_archivo = "banco_palabras.txt"
    if not os.path.exists(nombre_archivo):
        # Por si borras el archivo por accidente, lo crea con las básicas
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            for palabra in PALABRAS_TECH:
                f.write(palabra + "\n")
    
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        palabras = [linea.strip().upper() for linea in f.readlines()]
    
    palabras.sort() 
    return palabras

def busqueda_binaria_recursiva(lista, objetivo, inicio, fin):
    """Implementación de búsqueda binaria para validar si la palabra existe."""
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
    """Devuelve una lista de 5 colores evaluando aciertos, posiciones y descartes."""
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