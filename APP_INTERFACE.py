#!/usr/bin/env python3
"""
APP_INTERFACE.py
Interfaz móvil amigable para CuecaLabs.
Funcionalidades:
- reproducir tono homeostático de 432 Hz para el receptor CD26
- captura de audio y análisis bioacústico
- cálculo de entropía de Shannon
- documento JSON con resultados
"""

import json
import math
import wave
from pathlib import Path

try:
    import numpy as np
except Exception as exc:  # pragma: no cover
    raise SystemExit("Instala numpy: pip install numpy") from exc

try:
    import sounddevice as sd
except Exception:  # pragma: no cover
    sd = None


def tone_432(sample_rate=44100, seconds=2.0, amplitude=0.5):
    t = np.linspace(0, seconds, int(sample_rate * seconds), endpoint=False)
    y = amplitude * np.sin(2 * math.pi * 432.0 * t)
    return y.astype(np.float32)


def save_wav(path, signal, sample_rate=44100):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes((signal * 32767).astype("<i2").tobytes())


def entropy_shannon(signal):
    if signal.size == 0:
        return 0.0
    hist, _ = np.histogram(signal, bins=256, density=True)
    hist = hist[hist > 0]
    return float(-(hist * np.log2(hist)).sum())


def play_tone():
    s = tone_432()
    save_wav("flauta_432hz.wav", s)
    print("[OK] Tono 432 Hz generado:", "flauta_432hz.wav")
    if sd is not None:
        sd.play(s, samplerate=44100)
        sd.wait()


def record_audio(seconds=5.0, sample_rate=44100):
    if sd is None:
        print("[WARN] sounddevice no disponible; no se puede grabar audio desde el micrófono.")
        return
    print(f"[INFO] grabando {seconds} segundos...")
    rec = sd.rec(int(sample_rate * seconds), samplerate=sample_rate, channels=1, dtype="float32")
    sd.wait()
    sig = rec[:, 0]
    save_wav("registro_vocalizacion.wav", sig, sample_rate)
    ent = entropy_shannon(sig)
    meta = {
        "archivo": "registro_vocalizacion.wav",
        "entropia_shannon": ent,
        "sample_rate": sample_rate,
        "duracion_segundos": seconds,
        "descripcion": "registro bioacústico para mapear vocalizaciones animales"
    }
    Path("registro_vocalizacion.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    print("[OK] grabación finalizada:", "registro_vocalizacion.wav")
    print("[OK] metadatos:", "registro_vocalizacion.json")
    print(f"[INFO] Entropía de Shannon: {ent:.6f}")


def main():
    print("CuecaLabs - Interfaz de Ciencia Ciudadana")
    print("1) Emitir tono homeostático 432 Hz")
    print("2) Grabar vocalización animal")
    print("3) Ambos")
    choice = input("Seleccione una opción [1/2/3]: ").strip()
    if choice in ("1", "3"):
        play_tone()
    if choice in ("2", "3"):
        record_audio()


if __name__ == "__main__":
    main()
