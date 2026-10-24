#!/usr/bin/env python3
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
