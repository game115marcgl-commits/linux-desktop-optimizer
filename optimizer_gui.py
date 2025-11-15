#!/usr/bin/env python3
"""
Linux Desktop Optimizer - GUI Version
Autor: Marcel
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk
import threading
import subprocess
import psutil
from datetime import datetime
import os

class OptimizerGUI(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Linux Desktop Optimizer 🐧")
        self.set_default_size(600, 500)
        self.set_border_width(10)
        
        # Kolor tła
        css = b"""
        window {
            background: linear-gradient(135deg, #2c3e50, #3498db);
        }
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        self.create_widgets()
        
    def create_widgets(self):
        # Główny kontener
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)
        
        # Nagłówek
        header = Gtk.Label()
        header.set_markup("<span size='xx-large' weight='bold'>🐧 Linux Desktop Optimizer</span>")
        main_box.pack_start(header, False, False, 0)
        
        # Data i czas
        self.time_label = Gtk.Label()
        self.update_time()
        main_box.pack_start(self.time_label, False, False, 0)
        
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.pack_start(separator, False, False, 5)
        
        # Przyciski akcji
        button_box = Gtk.Box(spacing=5)
        main_box.pack_start(button_box, False, False, 0)
        
        buttons = [
            ("💾 Sprawdź dysk", self.check_disk),
            ("🌡️ Temperatury", self.check_temps),
            ("🧠 Pamięć RAM", self.check_memory),
            ("⚡ CPU", self.check_cpu),
            ("📊 Pełny raport", self.full_report)
        ]
        
        for label, callback in buttons:
            btn = Gtk.Button(label=label)
            btn.connect("clicked", callback)
            button_box.pack_start(btn, True, True, 0)
        
        # Obszar wyników
        self.result_text = Gtk.TextView()
        self.result_text.set_editable(False)
        self.result_text.set_wrap_mode(Gtk.WrapMode.WORD)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)
        scrolled.add(self.result_text)
        main_box.pack_start(scrolled, True, True, 0)
        
        # Stopka
        footer = Gtk.Label(label="https://github.com/game11smarcgl/linux-desktop-optimizer")
        main_box.pack_start(footer, False, False, 5)
        
        # Timer do aktualizacji czasu
        GLib.timeout_add_seconds(1, self.update_time)
    
    def update_time(self):
        current_time = datetime.now().strftime("Data: %Y-%m-%d | Godzina: %H:%M:%S")
        self.time_label.set_text(current_time)
        return True
    
    def append_text(self, text):
        buffer = self.result_text.get_buffer()
        end_iter = buffer.get_end_iter()
        buffer.insert(end_iter, text + "\n")
        
        # Auto-scroll
        mark = buffer.get_insert()
        end_iter = buffer.get_end_iter()
        buffer.place_cursor(end_iter)
    
    def clear_text(self):
        buffer = self.result_text.get_buffer()
        buffer.set_text("")
    
    def check_disk(self, widget):
        self.clear_text()
        self.append_text("💾 SPRAWDZANIE MIEJSCA NA DYSKU...")
        
        def disk_task():
            try:
                result = subprocess.run(['df', '-h', '/dev/sda3'], 
                                      capture_output=True, text=True)
                GLib.idle_add(self.append_text, result.stdout)
            except Exception as e:
                GLib.idle_add(self.append_text, f"❌ Błąd: {e}")
        
        threading.Thread(target=disk_task).start()
    
    def check_temps(self, widget):
        self.clear_text()
        self.append_text("🌡️ SPRAWDZANIE TEMPERATUR...")
        
        def temp_task():
            try:
                # Sprawdź temperatury przez sensors
                result = subprocess.run(['sensors'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines[:15]:
                        if '°C' in line:
                            GLib.idle_add(self.append_text, f"  {line.strip()}")
                else:
                    GLib.idle_add(self.append_text, "  ❌ Zainstaluj: sudo apt install lm-sensors")
            except Exception as e:
                GLib.idle_add(self.append_text, f"  ❌ Błąd: {e}")
        
        threading.Thread(target=temp_task).start()
    
    def check_memory(self, widget):
        self.clear_text()
        self.append_text("🧠 SPRAWDZANIE PAMIĘCI RAM...")
        
        def memory_task():
            try:
                memory = psutil.virtual_memory()
                text = f"  Użyte: {memory.percent}%\n"
                text += f"  Wolne: {memory.available / (1024**3):.1f} GB\n"
                text += f"  Całkowita: {memory.total / (1024**3):.1f} GB"
                GLib.idle_add(self.append_text, text)
            except Exception as e:
                GLib.idle_add(self.append_text, f"  ❌ Błąd: {e}")
        
        threading.Thread(target=memory_task).start()
    
    def check_cpu(self, widget):
        self.clear_text()
        self.append_text("⚡ SPRAWDZANIE PROCESORA...")
        
        def cpu_task():
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                cores = psutil.cpu_count()
                text = f"  Obciążenie: {cpu_percent}%\n"
                text += f"  Rdzenie: {cores}\n"
                text += f"  Częstotliwość: {psutil.cpu_freq().current if psutil.cpu_freq() else 'N/A'} MHz"
                GLib.idle_add(self.append_text, text)
            except Exception as e:
                GLib.idle_add(self.append_text, f"  ❌ Błąd: {e}")
        
        threading.Thread(target=cpu_task).start()
    
    def full_report(self, widget):
        self.clear_text()
        self.append_text("📊 GENEROWANIE PEŁNEGO RAPORTU...")
        
        def full_task():
            try:
                # Dysk
                disk_result = subprocess.run(['df', '-h', '/dev/sda3'], 
                                           capture_output=True, text=True)
                GLib.idle_add(self.append_text, "💾 DYSK:")
                GLib.idle_add(self.append_text, disk_result.stdout)
                
                # Pamięć
                memory = psutil.virtual_memory()
                GLib.idle_add(self.append_text, "🧠 PAMIĘĆ:")
                GLib.idle_add(self.append_text, f"  Użyte: {memory.percent}%")
                
                # CPU
                cpu_percent = psutil.cpu_percent(interval=1)
                GLib.idle_add(self.append_text, "⚡ CPU:")
                GLib.idle_add(self.append_text, f"  Obciążenie: {cpu_percent}%")
                
                GLib.idle_add(self.append_text, "✅ RAPORT ZAKOŃCZONY")
                
            except Exception as e:
                GLib.idle_add(self.append_text, f"❌ Błąd: {e}")
        
        threading.Thread(target=full_task).start()

def main():
    win = OptimizerGUI()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
