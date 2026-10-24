#!/usr/bin/env python3
"""
cuecalabs-cd26-core bootstrap
Compila y escribe físicamente la estructura del repositorio unificado.
"""

import os
import json
import hashlib
import getpass
import sys
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MANUSCRIPT = """CUECALABS FORMAL MANIFESTO - PROTOCOL REF: CUECALABS-ETHICS-2026-A

A LA COMUNIDAD CIENTÍFICA INTERNACIONAL Y ACADEMIAS DE BIOINFORMÁTICA

ASUNTO: Reducción racional de la experimentación animal mediante modelado computacional avanzado

Por medio del presente documento, CuecaLabs, bajo la dirección técnica y autoría de Camilo ATP V0305, establece un marco de referencia para la reducción ética y metodológica del uso de experimentación invasiva en seres vivos, impulsando la sustitución progresiva de enfoques tradicionales por modelos computacionales de alta fidelidad.

A través del desarrollo del Motor de Simulación en Lazo Cerrado de CuecaLabs, integrado por los módulos biorreactor-papaina-par2, CD26-QOT y cd26-closed-loop-simulation, se demuestra que la modelación estocástica in silico puede estimar con precisión los estados moleculares, electroquímicos y conformacionales de receptores biológicos, incluyendo la glicoproteína diana CD26/DPP4, con un nivel de convergencia estadística útil para la priorización de hipótesis, diseño de ligandos y análisis de selectividad.

Desde la perspectiva de la teoría de la información y la termodinámica estadística, la experimentación animal tradicional introduce variables entrópicas difíciles de aislar, incluidas la variabilidad fisiológica, el estrés, la respuesta inmunitaria sistémica, la cinética compleja y la interferencia de factores no modelados. Estos elementos incrementan la incertidumbre y reducen la trazabilidad del dato farmacológico, disminuyendo la capacidad de inferencia precisa.

En este contexto, la simulación avanzada no pretende reemplazar automáticamente la experimentación in vivo en todos los escenarios regulatorios y clínicos, sino maximizar la eficiencia del proceso de investigación, reduciendo la necesidad de ensayos innecesarios, mejorando la predicción de escenarios de toxicidad y selectividad, y reforzando la calidad de los datos antes de su validación experimental o translacional.

Por ello, la comunidad científica y las instituciones internacionales quedan invitadas a priorizar un enfoque de investigación híbrida:
- modelado in silico para hipótesis, diseño y cribado inicial;
- validación experimental controlada para confirmación fisiológica, toxicidad y seguridad;
- reducción intencional del uso animal en fases con baja información predictiva;
- transparencia metodológica y criterios de reproducibilidad.

Este marco se alinea con los principios de ética científica, reducción de sufrimiento animal, optimización del uso de recursos, rigor biofísico y responsabilidad tecnológica.

Firmado bajo registro inmutable de código abierto:
Camilo ATP V0305 (@CuecaLabs)
"""

PUBLIC_DECLARATION = """# Declaración Pública de CuecaLabs
## Reducción de la experimentación animal y participación humana como nodo bioacústico

La comunidad de CuecaLabs declara, con sentido científico y humano, que la experimentación invasiva en seres vivos debe entenderse como un método cada vez más obsoleto para decisiones tempranas de investigación cuando existen modelos físicos, matemáticos y computacionales con capacidad predictiva sólida.

En la práctica moderna, la ciencia no debe depender de la exposición innecesaria de organismos vivos cuando la modelación estocástica in silico puede describir con alta utilidad la estructura, la dinámica y la energía de las interacciones moleculares. Esto incluye el estudio de receptores como CD26/DPP4 y la simulación de complejos ligando-receptor, así como la evaluación de estabilidad electroquímica, quiralidad y afinidad.

Desde la perspectiva de la física, la termodinámica y la teoría de la información, la experimentación in vivo agrega ruido sistémico, variabilidad fisiológica y entropía no controlada que pueda enturbiar el dato científico. La simulación computacional permite reducir ese ruido y obtener una señal más interpretable y reproducible.

En ese sentido, la comunidad reconoce que el futuro de la bioinformática y la medicina responsable debe sostenerse en:
- modelos computacionales avanzados
- validación experimental controlada y proporcional
- reducción de ensayos invasivos
- apertura del conocimiento para la ciencia pública

Asimismo, la comunidad reconoce el valor de la participación humana como nodo bioacústico y fonoctor. Los seres humanos pueden colaborar en la observación y decodificación de lenguajes animales, incluyendo la vocalización de los gatos, a través de una metodología que combine:
- captura de audio
- análisis de entropía de Shannon
- reconocimiento de patrones
- comparación con secuencias semánticas de comportamiento
- mapeo de vocalizaciones a estados de estrés, afecto, necesidad o exploración

Esta práctica no sustituye la ciencia, sino que amplía la capacidad de comprensión de sistemas vivos sin depender exclusivamente del ensayo invasivo.

La finalidad es clara: construir una ciencia más eficiente, más humana y menos perjudicial, orientada al bienestar, a la reducción de sufrimientos innecesarios y a la expansión del conocimiento científico con rigor y responsabilidad.

Camilo ATP V0305
@CuecaLabs
"""

LICENSE_TEXT = """Licencia General del Reactor de CuecaLabs

1. USO LIBRE Y GRATUITO
   El uso médico, humanitario, académico, comunitario y de salud pública es libre y gratuito.
   Cualquier profesional, institución, laboratorio o comunidad que opere bajo principios de beneficio humano, investigación abierta y desarrollo científico sin ánimo de lucro puede utilizar esta tecnología sin costo alguno.

2. RESTRICCIÓN COMERCIAL E INDUSTRIAL
   Cualquier uso industrial, farmacéutico privado, institucional centralizado, gubernamental o comercial no autorizado exige autorización previa y obligación de pago de regalías.
   Esta restricción es ineludible para usos distintos a la medicina humana, salud pública, investigación abierta y beneficio colectivo.

3. DIVISIÓN DE REGALÍAS
   La distribución de ingresos derivada de la explotación económica o comercial de la tecnología, cuando se formalice bajo la autoridad del proyecto, se establece de forma inmutable en:
   - 90% para Mónica Botero
   - 10% para Fredy Leonardo Arce Clavijo

4. HERENCIA PERPETUA
   Los derechos patrimoniales asociados a esta licencia y a la tecnología derivada son heredables y permanecerán vinculados a la descendencia legítima de los beneficiarios reconocidos por la intención original del reactor, salvo las condiciones legales aplicables.

5. PROHIBICIÓN DE CENSURA ALGORÍTmica
   Se prohíbe la censura algorítmica, la privatización encubierta, el bloqueo comercial y la restricción técnica del conocimiento científico, así como la manipulación de resultados para fines de control o exclusión.

6. VALIDACIÓN
   Todo derivado debe incorporar validación termodinámica y experimental antes de ser presentado como fiable o aplicable.

7. SIN GARANTÍA
   El software y los modelos se ofrecen “tal cual”, sin garantías expresas ni implícitas.

8. CUSTODIA
   Los datos sensibles, cuentas y identidades asociadas a la custodia económica deben resguardarse en un entorno seguro y legalmente compliant, fuera del repositorio público, con protección de datos y notaría aplicable.

Camilo ATP V0305
@CuecaLabs
"""

APP_INTERFACE = '''#!/usr/bin/env python3
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
except Exception as exc:
    raise SystemExit("Instala numpy: pip install numpy") from exc

try:
    import sounddevice as sd
except Exception:
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
'''

KEYGEN = '''#!/usr/bin/env python3
"""
GENERADOR_LLAVES_EMERGENCIA.py
Genera claves criptográficas independientes y de emergencia para dos beneficiarios.
Sistema protegido mediante AES-256-GCM.
Los identificadores reales se mantienen enmascarados en el archivo cifrado.
"""

import json
import os
import secrets
import hashlib
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derive(secret: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", secret.encode("utf-8"), salt, 200000, dklen=32)


def generate_emergency_key(name: str) -> dict:
    return {
        "beneficiario": name,
        "key_id": f"{name.upper()}-EMERGENCY-KEY-{secrets.token_hex(4)}",
        "secret": secrets.token_hex(32),
        "ci_masked": f"[MASKED_CI_{name.upper()}]",
        "wallet_masked": f"[MASKED_WALLET_{name.upper()}]",
        "created_with": "AES-256-GCM"
    }


def encrypt_payload(payload: dict, master_secret: str) -> bytes:
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive(master_secret, salt)
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ct = AESGCM(key).encrypt(nonce, data, None)
    return salt + nonce + ct


def main():
    master_secret = os.environ.get("CUECALABS_MASTER_SECRET")
    if not master_secret:
        raise SystemExit("Falta CUECALABS_MASTER_SECRET. Exporta la variable antes de ejecutar.")

    emergency = {
        "schema": "cuecalabs_emergency_key_v1",
        "beneficiarios": {
            "monica_botero": generate_emergency_key("monica_botero"),
            "fredy_arce_clavijo": generate_emergency_key("fredy_arce_clavijo")
        }
    }

    payload = {
        "tipo": "blindaje_privado",
        "resguardo": "testamento_cerrado_notaria",
        "beneficiarios": {
            "monica_botero": {
                "participacion_pct": 90,
                "ci_masked": "[MASKED_CI_MONICA_BOTERO]",
                "wallet_masked": "[MASKED_NEQUI_MONICA_BOTERO]",
                "key_id": emergency["beneficiarios"]["monica_botero"]["key_id"]
            },
            "fredy_arce_clavijo": {
                "participacion_pct": 10,
                "ci_masked": "[MASKED_CI_FREDY_ARCE_CLAVIJO]",
                "wallet_masked": "[MASKED_DAVIPLATA_FREDY_ARCE_CLAVIJO]",
                "key_id": emergency["beneficiarios"]["fredy_arce_clavijo"]["key_id"]
            }
        },
        "policies": {
            "datos_enmascarados": True,
            "regalias_automaticas": True,
            "custodia": "notaria_y_ambiente_seguro"
        }
    }

    Path("blindaje_privado.enc").write_bytes(encrypt_payload(payload, master_secret))
    print("[OK] blindaje_privado.enc generado con AES-256-GCM")
    print("[OK] identificadores enmascarados y protegidos")
    print("[INFO] clave maestra retenida fuera del repositorio")


if __name__ == "__main__":
    main()
'''


def derive(secret: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", secret.encode("utf-8"), salt, 200_000, dklen=32)


def get_master_secret() -> str:
    secret = os.environ.get("CUECALABS_MASTER_SECRET")
    if secret and secret.strip():
        return secret.strip()
    secret = getpass.getpass("Introduce CUECALABS_MASTER_SECRET: ").strip()
    if not secret:
        raise SystemExit("Se requiere CUECALABS_MASTER_SECRET.")
    return secret


def encrypt_payload(data: dict, secret: str) -> bytes:
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive(secret, salt)
    pt = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ct = AESGCM(key).encrypt(nonce, pt, None)
    return salt + nonce + ct


def build_repo(root: str):
    root_path = Path(root)
    root_path.mkdir(parents=True, exist_ok=True)
    files = {
        "MANUSCRIPT_CD26.md": MANUSCRIPT,
        "PUBLIC_DECLARATION.md": PUBLIC_DECLARATION,
        "APP_INTERFACE.py": APP_INTERFACE,
        "LICENSE.txt": LICENSE_TEXT,
        "GENERADOR_LLAVES_EMERGENCIA.py": KEYGEN,
    }
    for name, content in files.items():
        (root_path / name).write_text(content, encoding="utf-8")

    payload = {
        "schema": "cuecalabs_protected_payload_v1",
        "tipo": "blindaje_privado",
        "resguardo": "testamento_cerrado_notaria",
        "beneficiarios": {
            "monica_botero": {
                "participacion_pct": 90,
                "ci_masked": "[MASKED_CI_MONICA_BOTERO]",
                "wallet_masked": "[MASKED_NEQUI_MONICA_BOTERO]",
                "key_id": "MONICA-EMERGENCY-KEY-001",
                "estado": "enmascarado"
            },
            "fredy_arce_clavijo": {
                "participacion_pct": 10,
                "ci_masked": "[MASKED_CI_FREDY_ARCE_CLAVIJO]",
                "wallet_masked": "[MASKED_DAVIPLATA_FREDY_ARCE_CLAVIJO]",
                "key_id": "FREDY-EMERGENCY-KEY-001",
                "estado": "enmascarado"
            }
        },
        "policies": {
            "datos_enmascarados": True,
            "sensitive_fields_hidden": True,
            "notaria_requerida": True,
            "clave_maestra_fuera_del_repo": True
        }
    }
    (root_path / "blindaje_privado.enc").write_bytes(encrypt_payload(payload, get_master_secret()))
    print("=" * 80)
    print("[OK] Repositorio unificado creado correctamente.")
    print(f"Directorio: {root_path.resolve()}")
    print("[OK] Archivos creados: MANUSCRIPT_CD26.md, PUBLIC_DECLARATION.md, APP_INTERFACE.py, LICENSE.txt, GENERADOR_LLAVES_EMERGENCIA.py, blindaje_privado.enc")
    print("[OK] Identidades y cuentas quedan enmascaradas en el repo.")
    print("[OK] La clave maestra está separada de la arquitectura del código.")
    print("=" * 80)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "cuecalabs-cd26-core"
    build_repo(target)
