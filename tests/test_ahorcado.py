import pytest
from unittest.mock import patch, MagicMock
import json
import os
import sys

# Añadir el directorio raíz al path para poder importar ahorcado
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ahorcado import (
    obtener_definicion,
    cargar_estadisticas,
    guardar_estadisticas,
    IDIOMAS,
    DIFICULTADES,
    INTENTOS_MAX
)


class TestObtenerDefinicion:
    """Tests para la función obtener_definicion"""
    
    def test_definicion_con_tabs(self):
        palabra_data = {'word': 'test', 'defs': ['n\tdefinición de prueba']}
        resultado = obtener_definicion(palabra_data)
        assert resultado == 'definición de prueba'
    
    def test_definicion_sin_tabs(self):
        palabra_data = {'word': 'test', 'defs': ['definición simple']}
        resultado = obtener_definicion(palabra_data)
        assert resultado == 'definición simple'
    
    def test_sin_definicion(self):
        palabra_data = {'word': 'test'}
        resultado = obtener_definicion(palabra_data)
        assert resultado is None
    
    def test_definiciones_vacias(self):
        palabra_data = {'word': 'test', 'defs': []}
        resultado = obtener_definicion(palabra_data)
        assert resultado is None
    
    def test_no_es_diccionario(self):
        resultado = obtener_definicion('palabra')
        assert resultado is None


class TestEstadisticas:
    """Tests para las funciones de estadísticas"""
    
    def test_estadisticas_default(self, tmp_path):
        # Usar un archivo temporal
        archivo_temp = tmp_path / "test_stats.json"
        
        with patch('ahorcado.ARCHIVO_STATS', str(archivo_temp)):
            stats = cargar_estadisticas()
            assert stats == {'partidas': 0, 'ganadas': 0, 'perdidas': 0}
    
    def test_guardar_y_cargar_estadisticas(self, tmp_path):
        archivo_temp = tmp_path / "test_stats.json"
        
        stats_test = {'partidas': 10, 'ganadas': 7, 'perdidas': 3}
        
        with patch('ahorcado.ARCHIVO_STATS', str(archivo_temp)):
            guardar_estadisticas(stats_test)
            stats_cargadas = cargar_estadisticas()
            
        assert stats_cargadas == stats_test
    
    def test_estadisticas_archivo_corrupto(self, tmp_path):
        archivo_temp = tmp_path / "test_stats.json"
        
        # Escribir JSON inválido
        with open(archivo_temp, 'w') as f:
            f.write("datos inválidos {{{")
        
        with patch('ahorcado.ARCHIVO_STATS', str(archivo_temp)):
            stats = cargar_estadisticas()
            # Debe retornar estadísticas por defecto
            assert stats == {'partidas': 0, 'ganadas': 0, 'perdidas': 0}


class TestConstantes:
    """Tests para verificar las constantes del juego"""
    
    def test_idiomas_disponibles(self):
        assert '1' in IDIOMAS
        assert '2' in IDIOMAS
        assert IDIOMAS['1'] == ('Español', 'es')
        assert IDIOMAS['2'] == ('Inglés', 'en')
    
    def test_dificultades_disponibles(self):
        assert '1' in DIFICULTADES
        assert '2' in DIFICULTADES
        assert '3' in DIFICULTADES
        
        # Verificar que los rangos son tuplas de 2 elementos
        for _, (nombre, rango) in DIFICULTADES.items():
            assert len(rango) == 2
            assert rango[0] < rango[1]  # Min < Max
    
    def test_intentos_max(self):
        assert INTENTOS_MAX == 6
        assert isinstance(INTENTOS_MAX, int)


class TestIntegracion:
    """Tests de integración básicos"""
    
    @patch('ahorcado.requests.get')
    def test_obtener_palabra_api_exitoso(self, mock_get):
        # Simular respuesta exitosa de la API
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {'word': 'python', 'defs': ['n\tun lenguaje de programación']},
            {'word': 'codigo', 'defs': ['n\tinstrucciones de programa']}
        ]
        mock_get.return_value = mock_response
        
        from ahorcado import obtener_palabra_api
        resultado = obtener_palabra_api('es', (5, 8))
        
        assert resultado is not None
        assert 'word' in resultado
        assert resultado['word'] in ['python', 'codigo']
    
    @patch('ahorcado.requests.get')
    def test_obtener_palabra_api_timeout(self, mock_get):
        # Simular timeout
        mock_get.side_effect = Exception("Timeout")
        
        from ahorcado import obtener_palabra_api
        resultado = obtener_palabra_api('es', (5, 8))
        
        assert resultado is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
