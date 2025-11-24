# Ahorcado 🎮

Un juego de **Ahorcado por consola** mejorado y colorido, donde el jugador puede elegir el idioma (español o inglés), nivel de dificultad, usar pistas, y ver sus estadísticas. Las palabras son reales y se obtienen desde la API de Datamuse.

---

## ✨ Características

- 🌍 **Multiidioma**: Español e Inglés
- 🎯 **3 Niveles de dificultad**: Fácil (3-5 letras), Media (6-8 letras), Difícil (9-12 letras)
- 🎨 **Interfaz colorida** con gráficos ASCII del ahorcado
- 💡 **Sistema de pistas**: Definiciones de palabras o revelar letras
- 📊 **Estadísticas persistentes**: Rastrea partidas ganadas, perdidas y porcentaje de victorias
- 🔄 **Modo replay**: Juega varias partidas sin reiniciar
- ✅ **Validación completa**: Adivina letra por letra o la palabra completa
- 🧪 **Tests incluidos**: Suite de pruebas unitarias con pytest

---

## 📋 Requisitos

- Python 3.7+
- Bibliotecas: `requests`, `colorama`

### Instalación de dependencias:

```bash
pip install -r requirements.txt
```

---

## 🎮 Cómo jugar

Ejecutá el juego desde consola:

```bash
python ahorcado.py
```

### Flujo del juego:

1. **Selecciona el idioma** (Español o Inglés)
2. **Elige la dificultad** (Fácil, Media o Difícil)
3. **Adivina la palabra**:
   - Ingresa una letra a la vez
   - O intenta adivinar la palabra completa
   - Usa `pista` para obtener ayuda (máximo 2 pistas por partida)
4. **Tienes 6 intentos** para fallar antes de perder
5. **Gana** completando la palabra
6. **Ve tus estadísticas** después de cada partida

---

## 🎯 Niveles de dificultad

| Nivel | Longitud de palabra | Descripción |
|-------|---------------------|-------------|
| Fácil | 3-5 letras | Ideal para principiantes |
| Media | 6-8 letras | Balance perfecto |
| Difícil | 9-12 letras | Para expertos |

---

## 💡 Sistema de pistas

- **Primera pista**: Muestra la definición de la palabra (si está disponible)
- **Segunda pista**: Revela una letra aleatoria
- Máximo 2 pistas por partida

---

## 📊 Estadísticas

El juego guarda automáticamente tus estadísticas en `estadisticas.json`:
- Total de partidas jugadas
- Partidas ganadas
- Partidas perdidas
- Porcentaje de victorias

---

## 🧪 Tests

Ejecuta los tests unitarios:

```bash
pytest tests/ -v
```

O ejecuta todos los tests con coverage:

```bash
pytest tests/ --cov=ahorcado --cov-report=html
```

---

## 🌐 Idiomas disponibles

- 🇪🇸 Español (es)
- 🇬🇧 Inglés (en)

---

## 🔌 Fuente de palabras

Las palabras se obtienen desde la [API pública de Datamuse](https://www.datamuse.com/api/), lo que garantiza que sean reales, variadas y con definiciones disponibles.

---

## 📁 Estructura del proyecto

```
ahorcado/
├── ahorcado.py           # Código principal del juego
├── requirements.txt      # Dependencias del proyecto
├── README.md            # Este archivo
├── .gitignore           # Archivos ignorados por Git
├── tests/               # Suite de tests
│   ├── __init__.py
│   └── test_ahorcado.py
└── estadisticas.json    # Generado automáticamente (tus stats)
```

---

## 🚀 Mejoras implementadas

✅ Gráficos ASCII del ahorcado  
✅ Sistema de colores con colorama  
✅ Tres niveles de dificultad  
✅ Sistema de pistas (definiciones + revelar letras)  
✅ Estadísticas persistentes  
✅ Modo replay sin reiniciar  
✅ Validación de palabra completa  
✅ Tests unitarios  
✅ .gitignore configurado  
✅ Manejo mejorado de errores y timeouts

---

## 🔮 Mejoras futuras

- [ ] Versión web con Flask/Django
- [ ] Más idiomas (Francés, Alemán, Portugués)
- [ ] Categorías de palabras (animales, colores, deportes)
- [ ] Modo multijugador
- [ ] Ranking global
- [ ] Efectos de sonido
- [ ] Tiempo límite por turno
- [ ] Modo desafío diario

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT.  
Podés usarlo, modificarlo y compartirlo libremente.

---

## 👤 Autor

[@Franpa99](https://github.com/Franpa99)

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tenés ideas para mejorar el juego:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

**¡Divertite jugando al Ahorcado! 🎉**
