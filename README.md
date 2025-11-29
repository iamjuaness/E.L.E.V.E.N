# ELEVEN - AI Voice Assistant

## Descripción

ELEVEN es un asistente de voz avanzado con capacidades de IA, similar a JARVIS. Utiliza Gemini 2.0 Flash para procesamiento de lenguaje natural, reconocimiento de voz, síntesis de voz neural, y control completo del sistema.

## Características Principales

- 🎙️ **Wake Word**: Activación manos libres con "Hey Eleven"
- 🧠 **IA Avanzada**: Gemini 2.0 Flash para comprensión natural
- 🗣️ **Voz Neural**: EdgeTTS con múltiples voces en español e inglés
- 👁️ **Visión**: Análisis de pantalla con IA
- 💾 **Memoria**: Historial de conversaciones persistente
- 📁 **Sistema de Archivos**: Búsqueda inteligente de archivos/carpetas
- ⚙️ **Configuración GUI**: Panel de ajustes con sliders de personalidad
- 🎭 **Personalidad Dinámica**: Ajusta humor, sarcasmo, sinceridad

## Instalación

### Requisitos

- Python 3.8+
- Windows 10/11
- Gemini API Key (obtener en [Google AI Studio](https://makersuite.google.com/app/apikey))

### Pasos

1. Clona el repositorio:

```bash
git clone https://github.com/iamjuaness/E.L.E.V.E.N.git
cd E.L.E.V.E.N
```

2. Crea un entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instala dependencias:

```bash
pip install -r requirements.txt
```

4. Configura tu API Key:

   - Copia `.env.example` a `.env`
   - Edita `.env` y añade tu `GEMINI_API_KEY`

5. Ejecuta ELEVEN:

```bash
python src/main.py
```

## Uso

### Comandos de Voz

- **Activación**: "Hey Eleven" o "Oye Eleven"
- **Búsqueda de archivos**: "Abre la carpeta documentos"
- **Crear carpetas**: "Crea una carpeta llamada test en el escritorio"
- **Análisis de pantalla**: "¿Qué ves en mi pantalla?"
- **Control de sistema**: "Sube el volumen"
- **Búsqueda web**: "Busca en Google..."

### Panel de Configuración

Al ejecutar `python src/main.py`, se abre automáticamente un panel donde puedes configurar:

- API Key de Gemini
- Idioma (Español/Inglés)
- Voz (múltiples opciones)
- Nombre del asistente
- Sliders de personalidad

## Estructura del Proyecto

```
E.L.E.V.E.N/
├── src/
│   ├── audio/          # Sistema de audio (TTS, reconocimiento)
│   ├── brain/          # IA y procesamiento (LLM, memoria)
│   ├── capabilities/   # Capacidades (visión, web, sistema)
│   ├── config/         # Configuración
│   ├── gui/            # Interfaz gráfica
│   ├── system/         # Control del sistema
│   └── utils/          # Utilidades
├── logs/               # Archivos de log
├── requirements.txt    # Dependencias
└── README.md
```

## Desarrollo

### Ejecutar desde código

```bash
python src/main.py
```

### Ejecutar como .exe

Descarga la última versión desde [Releases](https://github.com/iamjuaness/E.L.E.V.E.N/releases)

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles

## Autor

**Juan Esteban** - [@iamjuaness](https://github.com/iamjuaness)

## Agradecimientos

- Google Gemini AI
- EdgeTTS
- CustomTkinter
