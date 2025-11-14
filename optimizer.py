def check_disk_health(self):
    """Sprawdza zdrowie dysku SSD"""
    print("🔍 ZDROWIE DYSKU SSD:")
    try:
        # Temperatura dysku
        result = subprocess.run(['sudo', 'smartctl', '-A', '/dev/sda'], 
                              capture_output=True, text=True)
        if 'Temperature' in result.stdout:
            for line in result.stdout.split('\n'):
                if 'Temperature' in line:
                    print(f"🌡️ {line.strip()}")
    except:
        print("❌ Wymagany: sudo apt install smartmontools")
def optimize_nvidia(self):
    """Optymalizuje ustawienia karty NVIDIA"""
    print("🎮 OPTYMALIZACJA NVIDIA GTX 1050:")
    commands = [
        "nvidia-settings -a '[gpu:0]/GpuPowerMizerMode=1'",
        "nvidia-settings -a '[gpu:0]/GPUFanControlState=1'"
    ]
    for cmd in commands:
        try:
            subprocess.run(cmd, shell=True)
            print(f"✅ {cmd}")
        except:
            print(f"❌ Nie można wykonać: {cmd}")
def optimize_nvidia(self):
    """Optymalizuje ustawienia karty NVIDIA"""
    print("🎮 OPTYMALIZACJA NVIDIA GTX 1050:")
    commands = [
        "nvidia-settings -a '[gpu:0]/GpuPowerMizerMode=1'",
        "nvidia-settings -a '[gpu:0]/GPUFanControlState=1'"
    ]
    for cmd in commands:
        try:
            subprocess.run(cmd, shell=True)
            print(f"✅ {cmd}")
        except:
            print(f"❌ Nie można wykonać: {cmd}")
