# ELEVEN - Voice AI Assistant

Un asistente de voz inteligente tipo JARVIS para Windows, potenciado por Google Gemini.

## 🚀 Instalación

1. **Requisitos Previos**:

   - Python 3.10 o superior
   - Micrófono y altavoces

2. **Configuración**:

   ```bash
   # 1. Crear entorno virtual (opcional pero recomendado)
   python -m venv venv
   .\venv\Scripts\activate

   # 2. Instalar dependencias
   pip install -r requirements.txt

   # 3. Configurar variables de entorno
   copy .env.example .env
   ```

3. **API Key**:
   - Abre el archivo `.env` y pega tu API Key de Google Gemini en `GEMINI_API_KEY`.
   - Puedes obtenerla gratis en [Google AI Studio](https://aistudio.google.com/).

## 🎮 Uso

Ejecuta el asistente:

```bash
python src/main.py
```

Di **"Hey ELEVEN"** (o simplemente empieza a hablar si el micrófono está activo) y prueba comandos como:

- "Abre Google y busca noticias de IA"
- "¿Qué hora es?"
- "Sube el volumen"
- "¿Cómo está el uso de mi CPU?"
- "Abre el bloc de notas"

## 🛠️ Estructura del Proyecto

- `src/brain`: Lógica de inteligencia (LLM, Intenciones)
- `src/audio`: Reconocimiento de voz y TTS
- `src/system`: Control del sistema operativo
- `src/capabilities`: Habilidades específicas (Web, Info Sistema)

## ⚠️ Nota de Seguridad

Por defecto, el modo seguro está activado (`SAFE_MODE=true`). Comandos peligrosos como borrar archivos masivamente serán bloqueados.
