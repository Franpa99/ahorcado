import random
import requests

IDIOMAS = {
    '1': ('Español', 'es'),
    '2': ('Inglés', 'en'),
}

INTENTOS_MAX = 6

def obtener_palabra_api(cod_idioma):
    longitud = random.randint(5, 8)
    patron = '?' * longitud

    if cod_idioma == 'en':
        url = f"https://api.datamuse.com/words?sp={patron}&max=20"
    else:
        url = f"https://api.datamuse.com/words?sp={patron}&v={cod_idioma}&max=20"
    
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        
        palabras_validas = []
        for palabra in datos:
            if 'word' in palabra and palabra['word'].isalpha():
                palabras_validas.append(palabra['word'].lower())
        
        if palabras_validas:
            return random.choice(palabras_validas)
    
    except Exception as e:
        print(f"Error al conectar con la API: {e}")
    
    return None

def jugar_ahorcado():
    print("Selecciona un idioma:")
    for clave, (nombre, _) in IDIOMAS.items():
        print(f"{clave}. {nombre}")
    eleccion = input("Ingrese el número del idioma: ")

    if eleccion not in IDIOMAS:
        print("Idioma no válido.")
        return
    
    nombre_idioma, cod_idioma = IDIOMAS[eleccion]
    palabra = obtener_palabra_api(cod_idioma)

    if not palabra:
        print("No se pudo obtener una palabra válida. Intente de nuevo.")
        return
    
    letras_adivinadas = set()
    letras_erroneas = set()
    intentos_restantes = INTENTOS_MAX

    while intentos_restantes > 0:
        mostrar = ' '.join([letra if letra in letras_adivinadas else '_' for letra in palabra])
        print(f"\nPalabra: {mostrar}")
        print(f"Letras incorrectas: {' '.join(sorted(letras_erroneas))} | Intentos restantes: {intentos_restantes}")
        intento = input("Ingrese una letra: ").lower()

        if not intento.isalpha() or len(intento) != 1:
            print("Ingrese solo una letra.")
            continue

        if intento in letras_adivinadas or intento in letras_adivinadas:
            print("Ya usaste esa letra.")
            continue

        if intento in palabra:
            letras_adivinadas.add(intento)
            if all(letra in letras_adivinadas for letra in palabra):
                print(f"\n¡GANASTE! La palabra era: {palabra}")
                break
        else:
            letras_erroneas.add(intento)
            intentos_restantes -= 1
    else:
        print(f"\nPerdiste. La palabra era: {palabra}")

if __name__ == "__main__":
    jugar_ahorcado()