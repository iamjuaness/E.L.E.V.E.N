import customtkinter as ctk
from src.config.settings import Settings
from src.utils.logger import logger
import os
import sys
import threading
import tkinter as tk
from PIL import Image
import pystray

class SettingsGUI:
    """
    Configuration panel for ELEVEN settings.
    Now acts as the main application window.
    """
    
    def __init__(self, on_start_assistant=None, on_stop_assistant=None):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title(f"ELEVEN v{Settings.VERSION} - Control Panel")
        self.root.geometry("600x700")
        
        # Callbacks
        self.on_start_assistant = on_start_assistant
        self.on_stop_assistant = on_stop_assistant
        
        self._create_widgets()
        
        # Redirect stdout/stderr to console widget
        sys.stdout = self.ConsoleRedirector(self.console_text)
        sys.stderr = self.ConsoleRedirector(self.console_text, is_error=True)
        
        # Start assistant automatically if callback provided
        if self.on_start_assistant:
            self.root.after(1000, self.start_assistant_thread)

        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.tray_icon = None

    def start_assistant_thread(self):
        """Start the assistant in a background thread"""
        if self.on_start_assistant:
            threading.Thread(target=self.on_start_assistant, daemon=True).start()
            self.status_label.configure(text="✅ Assistant Running", text_color="green")

    def _create_widgets(self):
        # Main Tabview
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.tabview.add("Configuración")
        self.tabview.add("Consola")
        
        self._create_config_tab(self.tabview.tab("Configuración"))
        self._create_console_tab(self.tabview.tab("Consola"))

    def _create_console_tab(self, parent):
        self.console_text = ctk.CTkTextbox(parent, font=("Consolas", 12))
        self.console_text.pack(fill="both", expand=True, padx=10, pady=10)
        
    def _create_config_tab(self, parent):
        # Scrollable frame for config
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True)
        
        # Title
        title = ctk.CTkLabel(
            scroll_frame,
            text=f"⚙️ Configuración de ELEVEN v{Settings.VERSION}",
            font=("Segoe UI", 24, "bold")
        )
        title.pack(pady=10)
        
        # API Key Section
        api_frame = ctk.CTkFrame(scroll_frame)
        api_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(api_frame, text="Gemini API Key:", font=("Segoe UI", 14)).pack(anchor="w", padx=10, pady=5)
        self.api_key_entry = ctk.CTkEntry(api_frame, width=400, show="*")
        self.api_key_entry.pack(padx=10, pady=5)
        self.api_key_entry.insert(0, Settings.GEMINI_API_KEY or "")
        
        # Language Section
        lang_frame = ctk.CTkFrame(scroll_frame)
        lang_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(lang_frame, text="Idioma:", font=("Segoe UI", 14)).pack(anchor="w", padx=10, pady=5)
        self.language_var = ctk.StringVar(value=Settings.LANGUAGE)
        lang_menu = ctk.CTkOptionMenu(
            lang_frame,
            values=["es-ES", "en-US"],
            variable=self.language_var
        )
        lang_menu.pack(padx=10, pady=5, anchor="w")
        
        # Voice Selection
        voice_frame = ctk.CTkFrame(scroll_frame)
        voice_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(voice_frame, text="Voz:", font=("Segoe UI", 14)).pack(anchor="w", padx=10, pady=5)
        
        # Available voices
        spanish_voices = [
            "es-ES-AlvaroNeural (Hombre)",
            "es-ES-ElviraNeural (Mujer)",
            "es-MX-DaliaNeural (Mujer MX)",
            "es-MX-JorgeNeural (Hombre MX)"
        ]
        english_voices = [
            "en-US-ChristopherNeural (Hombre)",
            "en-US-JennyNeural (Mujer)",
            "en-US-GuyNeural (Hombre)",
            "en-US-AriaNeural (Mujer)"
        ]
        
        # Determine current voice display name
        current_voice = getattr(Settings, 'VOICE_NAME', 'es-ES-AlvaroNeural')
        voice_display = current_voice
        for v in spanish_voices + english_voices:
            if current_voice in v:
                voice_display = v
                break

        all_voices = spanish_voices + english_voices
        self.voice_var = ctk.StringVar(value=voice_display)
        voice_menu = ctk.CTkOptionMenu(
            voice_frame,
            values=all_voices,
            variable=self.voice_var,
            width=300
        )
        voice_menu.pack(padx=10, pady=5, anchor="w")
        
        # Assistant Name
        name_frame = ctk.CTkFrame(scroll_frame)
        name_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(name_frame, text="Nombre del Asistente:", font=("Segoe UI", 14)).pack(anchor="w", padx=10, pady=5)
        self.name_entry = ctk.CTkEntry(name_frame, width=200)
        self.name_entry.pack(padx=10, pady=5, anchor="w")
        self.name_entry.insert(0, Settings.ASSISTANT_NAME)
        
        # Personality Sliders
        personality_frame = ctk.CTkFrame(scroll_frame)
        personality_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(personality_frame, text="Personalidad:", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=10, pady=10)
        
        # Helper to create sliders
        def create_slider(label, key):
            ctk.CTkLabel(personality_frame, text=label, font=("Segoe UI", 12)).pack(anchor="w", padx=10)
            slider = ctk.CTkSlider(personality_frame, from_=0, to=100, number_of_steps=100)
            slider.set(Settings.PERSONALITY[key])
            slider.pack(padx=10, pady=2, fill="x")
            val_label = ctk.CTkLabel(personality_frame, text=f"{Settings.PERSONALITY[key]}%")
            val_label.pack(anchor="e", padx=10)
            slider.configure(command=lambda v, l=val_label: l.configure(text=f"{int(v)}%"))
            return slider

        self.humor_slider = create_slider("Humor:", "humor")
        self.sarcasm_slider = create_slider("Sarcasmo:", "sarcasm")
        self.sincerity_slider = create_slider("Sinceridad:", "sincerity")
        self.professionalism_slider = create_slider("Profesionalismo:", "professionalism")
        
        # Buttons Frame
        btn_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        btn_frame.pack(pady=20, fill="x")

        # Save Button
        save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Guardar Cambios",
            command=self.save_settings,
            font=("Segoe UI", 14, "bold"),
            height=40,
            fg_color="green",
            hover_color="darkgreen"
        )
        save_btn.pack(side="left", expand=True, padx=5)
        
        # Hide to Tray Button
        hide_btn = ctk.CTkButton(
            btn_frame,
            text="🙈 Ocultar en Bandeja",
            command=self.hide_to_tray,
            font=("Segoe UI", 14, "bold"),
            height=40,
            fg_color="gray",
            hover_color="darkgray"
        )
        hide_btn.pack(side="left", expand=True, padx=5)
        
        # Restart Button
        restart_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Reiniciar App",
            command=self.restart_app,
            font=("Segoe UI", 14, "bold"),
            height=40,
            fg_color="red",
            hover_color="darkred"
        )
        restart_btn.pack(side="right", expand=True, padx=5)
        
        # Status Label
        self.status_label = ctk.CTkLabel(scroll_frame, text="", font=("Segoe UI", 12))
        self.status_label.pack()

    def save_settings(self):
        """Save settings to database"""
        try:
            # Update runtime settings first
            Settings.GEMINI_API_KEY = self.api_key_entry.get()
            Settings.ASSISTANT_NAME = self.name_entry.get()
            Settings.LANGUAGE = self.language_var.get()
            
            # Extract voice ID
            voice_selection = self.voice_var.get()
            voice_id = voice_selection.split(" (")[0]
            Settings.VOICE_NAME = voice_id
            
            Settings.PERSONALITY["humor"] = int(self.humor_slider.get())
            Settings.PERSONALITY["sarcasm"] = int(self.sarcasm_slider.get())
            Settings.PERSONALITY["sincerity"] = int(self.sincerity_slider.get())
            Settings.PERSONALITY["professionalism"] = int(self.professionalism_slider.get())
            
            # Save to Database
            Settings.save()
            
            # Notify user
            self.status_label.configure(
                text="✅ Configuración guardada en base de datos.", 
                text_color="green"
            )
            logger.info("Settings saved to DB successfully")
            
        except Exception as e:
            self.status_label.configure(text=f"❌ Error: {e}", text_color="red")
            logger.error(f"Error saving settings: {e}")

    def restart_app(self):
        """Restart the entire application"""
        logger.info("Restarting application...")
        if self.tray_icon:
            self.tray_icon.stop()
        python = sys.executable
        os.execl(python, python, *sys.argv)
        
    def hide_to_tray(self):
        """Hide window and show tray icon"""
        self.root.withdraw()
        
        # Create a simple icon image (a colored square if no file)
        image = Image.new('RGB', (64, 64), color = (73, 109, 137))
        
        def show_window(icon, item):
            icon.stop()
            self.root.after(0, self.root.deiconify)

        def exit_app(icon, item):
            icon.stop()
            self.root.quit()
            sys.exit()

        menu = pystray.Menu(
            pystray.MenuItem("Mostrar", show_window, default=True),
            pystray.MenuItem("Salir", exit_app)
        )

        self.tray_icon = pystray.Icon("ELEVEN", image, f"ELEVEN v{Settings.VERSION}", menu)
        
        # Run tray icon in a separate thread to not block
        threading.Thread(target=self.tray_icon.run, daemon=True).start()
        
    def on_closing(self):
        """Handle window closing event"""
        # Uncomment to force minimize to tray on close
        # self.hide_to_tray()
        # For now, just close normally
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.destroy()
        sys.exit()
            
    def run(self):
        """Run GUI main loop"""
        self.root.mainloop()

    class ConsoleRedirector:
        def __init__(self, text_widget, is_error=False):
            self.text_widget = text_widget
            self.is_error = is_error

        def write(self, string):
            try:
                self.text_widget.configure(state="normal")
                if self.is_error:
                    self.text_widget.insert("end", string, "error")
                    self.text_widget.tag_config("error", foreground="red")
                else:
                    self.text_widget.insert("end", string)
                self.text_widget.see("end")
                self.text_widget.configure(state="disabled")
            except:
                pass

        def flush(self):
            pass

