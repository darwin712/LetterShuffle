import urllib.request
import unicodedata

def quitar_acentos(texto):
    """Elimina los acentos de una palabra (ej. ÁRBOL -> ARBOL)."""
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    return texto.upper()

print("Descargando el diccionario base y generando plurales matemáticamente...")

# Volvemos a la URL que SABEMOS que nunca falla
url = "https://raw.githubusercontent.com/javierarce/palabras/master/listado-general.txt"

try:
    respuesta = urllib.request.urlopen(url)
    contenido = respuesta.read().decode('utf-8')
    
    palabras_validas = set()
    
    for linea in contenido.splitlines():
        palabra = linea.strip()
        palabra_limpia = quitar_acentos(palabra)
        
        # Ignorar si tiene números o símbolos raros
        if not palabra_limpia.isalpha():
            continue
            
        # 1. Si la palabra ya tiene 5 letras, la agregamos (ej. AMIGO)
        if len(palabra_limpia) == 5:
            palabras_validas.add(palabra_limpia)
            
        # 2. TRUCO: Si tiene 4 letras y termina en vocal, le agregamos 'S' (ej. PAPA -> PAPAS)
        elif len(palabra_limpia) == 4 and palabra_limpia[-1] in "AEIOU":
            palabras_validas.add(palabra_limpia + "S")
            
        # 3. TRUCO: Si tiene 3 letras y termina en consonante, agregamos 'ES' (ej. RED -> REDES)
        elif len(palabra_limpia) == 3 and palabra_limpia[-1] not in "AEIOU":
            palabras_validas.add(palabra_limpia + "ES")
            
    # Tus palabras originales por si acaso
    palabras_tech = [
        "ALGOR", "ARBOL", "AUDIO", "BANDA", "BUCLE", "BYTES", "CABLE", "CACHE", 
        "CANAL", "CAPAS", "CEROS", "CHIPS", "CICLO", "CLAVE", "CLOUD", "DATOS", 
        "DISCO", "FIBRA", "FLUJO", "GRAFO", "JAPON", "LENTE", "MACRO", "MARCA", "MEDIO", 
        "MICRO", "MODEM", "NODOS", "NUBES", "ONDAS", "PANEL", "PERRO", "PISTA", "PIXEL", 
        "PLACA", "POLOS", "PULSO", "RAMAS", "RANGO", "RATON", "REDES", "REGLA", 
        "RELOJ", "RUTAS", "SALTO", "SENAL", "SERIE", "TAREA", "TECLA", "TEXTO", 
        "VIDEO", "VIRUS"
    ]
    
    for p in palabras_tech:
        palabras_validas.add(p)
        
    # Ordenamos (Obligatorio para Búsqueda Binaria)
    lista_final = sorted(list(palabras_validas))
    
    with open("banco_palabras.txt", "w", encoding="utf-8") as f:
        for p in lista_final:
            f.write(p + "\n")
            
    print(f"¡Éxito! Se generaron y guardaron {len(lista_final)} palabras válidas.")
    
except Exception as e:
    print(f"Ocurrió un error al descargar: {e}")