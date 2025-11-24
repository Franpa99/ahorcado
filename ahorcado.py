import random
import requests
import json
import os
from colorama import init, Fore, Style

# Inicializar colorama para Windows
init(autoreset=True)

IDIOMAS = {
    '1': ('Español', 'es'),
    '2': ('Inglés', 'en'),
}

DIFICULTADES = {
    '1': ('Fácil', (3, 5)),
    '2': ('Media', (6, 8)),
    '3': ('Difícil', (9, 12)),
}

INTENTOS_MAX = 6
ARCHIVO_STATS = 'estadisticas.json'

AHORCADO_DIBUJOS = [
    """
       ┌─────┐
       │     
       │     
       │     
       │     
       │     
    ═══════════
    """,
    """
       ┌─────┐
       │     │
       │     
       │     
       │     
       │     
    ═══════════
    """,
    """
       ┌─────┐
       │     │
       │     O
       │     
       │     
       │     
    ═══════════
    """,
    """
       ┌─────┐
       │     │
       │     O
       │     │
       │     
       │     
    ═══════════
    """,
    """
       ┌─────┐
       │     │
       │     O
       │    ─│
       │     
       │     
    ═══════════
    """,
    """
       ┌─────┐
       │     │
       │     O
       │    ─│─
       │     
       │     
    ═══════════
    """,
    """
       ┌─────┐
       │     │
       │     O
       │    ─│─
       │    ╱ 
       │     
    ═══════════
    """,
    """
       ┌─────┐
       │     │
       │     O
       │    ─│─
       │    ╱ ╲
       │     
    ═══════════
    """
]

def obtener_palabra_api(cod_idioma, rango_longitud):
    longitud = random.randint(rango_longitud[0], rango_longitud[1])
    patron = '?' * longitud

    if cod_idioma == 'en':
        url = f"https://api.datamuse.com/words?sp={patron}&max=50&md=d"
    else:
        url = f"https://api.datamuse.com/words?sp={patron}&v={cod_idioma}&max=50&md=d"
    
    try:
        respuesta = requests.get(url, timeout=5)
        datos = respuesta.json()
        
        palabras_validas = []
        for palabra in datos:
            if 'word' in palabra and palabra['word'].isalpha():
                palabras_validas.append(palabra)
        
        if palabras_validas:
            return random.choice(palabras_validas)
    
    except Exception as e:
        print(f"{Fore.RED}Error al conectar con la API: {e}")
    
    return None

def obtener_definicion(palabra_data):
    """Obtiene la definición de la palabra si está disponible."""
    if isinstance(palabra_data, dict) and 'defs' in palabra_data:
        definiciones = palabra_data['defs']
        if definiciones:
            return definiciones[0].split('\t')[1] if '\t' in definiciones[0] else definiciones[0]
    return None

def cargar_estadisticas():
    """Carga las estadísticas desde el archivo JSON."""
    if os.path.exists(ARCHIVO_STATS):
        try:
            with open(ARCHIVO_STATS, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {'partidas': 0, 'ganadas': 0, 'perdidas': 0}

def guardar_estadisticas(stats):
    """Guarda las estadísticas en el archivo JSON."""
    try:
        with open(ARCHIVO_STATS, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"{Fore.RED}Error al guardar estadísticas: {e}")

def mostrar_estadisticas(stats):
    """Muestra las estadísticas del jugador."""
    print(f"\n{Fore.CYAN}{'='*40}")
    print(f"{Fore.CYAN}ESTADÍSTICAS")
    print(f"{Fore.CYAN}{'='*40}")
    print(f"Partidas jugadas: {stats['partidas']}")
    print(f"{Fore.GREEN}Ganadas: {stats['ganadas']}")
    print(f"{Fore.RED}Perdidas: {stats['perdidas']}")
    if stats['partidas'] > 0:
        porcentaje = (stats['ganadas'] / stats['partidas']) * 100
        print(f"Porcentaje de victorias: {porcentaje:.1f}%")
    print(f"{Fore.CYAN}{'='*40}\n")

def jugar_ahorcado():
    print(f"{Fore.YELLOW}{Style.BRIGHT}")
    print("╔═══════════════════════════════════════╗")
    print("║        JUEGO DEL AHORCADO            ║")
    print("╚═══════════════════════════════════════╝")
    print(Style.RESET_ALL)
    
    # Cargar estadísticas
    stats = cargar_estadisticas()
    
    while True:
        # Selección de idioma
        print(f"\n{Fore.CYAN}Selecciona un idioma:")
        for clave, (nombre, _) in IDIOMAS.items():
            print(f"{clave}. {nombre}")
        eleccion_idioma = input("Ingrese el número del idioma: ")

        if eleccion_idioma not in IDIOMAS:
            print(f"{Fore.RED}Idioma no válido.")
            continue
        
        nombre_idioma, cod_idioma = IDIOMAS[eleccion_idioma]
        
        # Selección de dificultad
        print(f"\n{Fore.CYAN}Selecciona la dificultad:")
        for clave, (nombre, rango) in DIFICULTADES.items():
            print(f"{clave}. {nombre} ({rango[0]}-{rango[1]} letras)")
        eleccion_dificultad = input("Ingrese el número de dificultad: ")
        
        if eleccion_dificultad not in DIFICULTADES:
            print(f"{Fore.RED}Dificultad no válida.")
            continue
        
        nombre_dificultad, rango_longitud = DIFICULTADES[eleccion_dificultad]
        
        print(f"\n{Fore.GREEN}Obteniendo palabra...")
        palabra_data = obtener_palabra_api(cod_idioma, rango_longitud)

        if not palabra_data:
            print(f"{Fore.RED}No se pudo obtener una palabra válida. Intente de nuevo.")
            continue
        
        # Extraer la palabra
        palabra = palabra_data['word'].lower() if isinstance(palabra_data, dict) else palabra_data.lower()
        definicion = obtener_definicion(palabra_data)
        
        letras_adivinadas = set()
        letras_erroneas = set()
        intentos_restantes = INTENTOS_MAX
        pistas_usadas = 0
        max_pistas = 2

        print(f"\n{Fore.YELLOW}¡Comienza el juego!")
        print(f"Idioma: {nombre_idioma} | Dificultad: {nombre_dificultad}")
        print(f"Longitud de la palabra: {len(palabra)} letras\n")

        while intentos_restantes > 0:
            # Mostrar dibujo del ahorcado
            errores = INTENTOS_MAX - intentos_restantes
            print(f"{Fore.RED}{AHORCADO_DIBUJOS[errores]}")
            
            # Mostrar estado de la palabra
            mostrar = ' '.join([letra if letra in letras_adivinadas else '_' for letra in palabra])
            print(f"\n{Fore.CYAN}Palabra: {Fore.WHITE}{Style.BRIGHT}{mostrar}")
            
            if letras_erroneas:
                print(f"{Fore.RED}Letras incorrectas: {' '.join(sorted(letras_erroneas))}")
            
            print(f"{Fore.YELLOW}Intentos restantes: {intentos_restantes}")
            print(f"{Fore.MAGENTA}Pistas disponibles: {max_pistas - pistas_usadas}")
            
            # Opción de pista
            accion = input(f"\n{Fore.WHITE}Ingrese una letra, palabra completa, o 'pista': ").lower().strip()

            if accion == 'pista':
                if pistas_usadas >= max_pistas:
                    print(f"{Fore.RED}Ya no tienes pistas disponibles.")
                    continue
                
                if definicion:
                    print(f"{Fore.GREEN}💡 Pista (definición): {definicion}")
                else:
                    # Revelar una letra aleatoria
                    letras_no_adivinadas = [l for l in palabra if l not in letras_adivinadas]
                    if letras_no_adivinadas:
                        letra_revelada = random.choice(letras_no_adivinadas)
                        letras_adivinadas.add(letra_revelada)
                        print(f"{Fore.GREEN}💡 Pista: La palabra contiene la letra '{letra_revelada}'")
                
                pistas_usadas += 1
                definicion = None  # Solo mostrar definición una vez
                continue

            # Intentar palabra completa
            if len(accion) > 1:
                if not accion.isalpha():
                    print(f"{Fore.RED}Ingrese solo letras.")
                    continue
                
                if accion == palabra:
                    letras_adivinadas = set(palabra)
                    print(f"\n{Fore.GREEN}{Style.BRIGHT}{'='*40}")
                    print(f"¡GANASTE! ¡Adivinaste la palabra completa!")
                    print(f"La palabra era: {palabra.upper()}")
                    print(f"{'='*40}")
                    stats['ganadas'] += 1
                    stats['partidas'] += 1
                    guardar_estadisticas(stats)
                    break
                else:
                    print(f"{Fore.RED}¡Palabra incorrecta!")
                    intentos_restantes -= 1
                    continue

            # Intentar letra individual
            if not accion.isalpha() or len(accion) != 1:
                print(f"{Fore.RED}Ingrese solo una letra.")
                continue

            if accion in letras_adivinadas or accion in letras_erroneas:
                print(f"{Fore.YELLOW}Ya usaste esa letra.")
                continue

            if accion in palabra:
                letras_adivinadas.add(accion)
                print(f"{Fore.GREEN}¡Correcto!")
                
                if all(letra in letras_adivinadas for letra in palabra):
                    print(f"\n{Fore.GREEN}{Style.BRIGHT}{'='*40}")
                    print(f"¡GANASTE!")
                    print(f"La palabra era: {palabra.upper()}")
                    print(f"{'='*40}")
                    stats['ganadas'] += 1
                    stats['partidas'] += 1
                    guardar_estadisticas(stats)
                    break
            else:
                letras_erroneas.add(accion)
                intentos_restantes -= 1
                print(f"{Fore.RED}Letra incorrecta.")
        else:
            # Se acabaron los intentos
            print(f"{Fore.RED}{AHORCADO_DIBUJOS[-1]}")
            print(f"\n{Fore.RED}{Style.BRIGHT}{'='*40}")
            print(f"PERDISTE")
            print(f"La palabra era: {palabra.upper()}")
            print(f"{'='*40}")
            stats['perdidas'] += 1
            stats['partidas'] += 1
            guardar_estadisticas(stats)
        
        # Mostrar estadísticas
        mostrar_estadisticas(stats)
        
        # Preguntar si quiere jugar de nuevo
        jugar_otra = input(f"{Fore.CYAN}¿Quieres jugar otra vez? (s/n): ").lower()
        if jugar_otra != 's':
            print(f"\n{Fore.YELLOW}¡Gracias por jugar! ¡Hasta pronto!")
            break

if __name__ == "__main__":
    jugar_ahorcado()