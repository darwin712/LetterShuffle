import urllib.request
import unicodedata

def quitar_acentos(texto):
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    return texto.upper()

def generar_diccionario(ruta_destino="banco_palabras.txt"):
    print("Descargando el diccionario base y generando plurales matemáticamente...")
    url = "https://raw.githubusercontent.com/javierarce/palabras/master/listado-general.txt"
    try:
        respuesta = urllib.request.urlopen(url)
        contenido = respuesta.read().decode('utf-8')
        
        palabras_validas = set()
        
        for linea in contenido.splitlines():
            palabra = linea.strip()
            palabra_limpia = quitar_acentos(palabra)
            
            if not palabra_limpia.isalpha():
                continue
                
            if len(palabra_limpia) == 5:
                palabras_validas.add(palabra_limpia)
                
            elif len(palabra_limpia) == 4 and palabra_limpia[-1] in "AEIOU":
                palabras_validas.add(palabra_limpia + "S")
                
            elif len(palabra_limpia) == 3 and palabra_limpia[-1] not in "AEIOU":
                palabras_validas.add(palabra_limpia + "ES")
                
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
            
        lista_final = sorted(list(palabras_validas))
        
        with open(ruta_destino, "w", encoding="utf-8") as f:
            for p in lista_final:
                f.write(p + "\n")
                
        print(f"¡Éxito! Se generaron y guardaron {len(lista_final)} palabras válidas.")
        
    except Exception as e:
        print(f"Ocurrió un error al descargar: {e}")

if __name__ == "__main__":
    generar_diccionario()