#!/usr/bin/env python3
"""
build_clean_repo.py

Creates a transparent open-source repository scaffold with:
- MANUSCRIPT_CD26.md
- LICENSE.txt
- APP_INTERFACE.py

This version contains no encryption, no hidden routing, no binary artifacts,
and no deceptive financial or legal logic.
"""

from pathlib import Path
from textwrap import dedent

MANUSCRIPT = dedent("""\
# CUECALABS - Open Science and Audio Signal Analysis

## Purpose
This repository provides an open and transparent framework for analyzing audio signals,
supporting reproducible scientific workflows, community-driven experimentation, and
accessible computational methods for signal inspection.

## Scope
The project is intended to support:
- reproducible audio analysis
- scientific documentation and review
- transparent signal processing workflows
- public, auditable tooling for citizen science and research collaboration

## Principles
1. Transparency
2. Reproducibility
3. Open review
4. Clear documentation
5. Ethical and auditable technical practice

## Technical Notes
The repository uses standard scientific Python tooling to inspect waveform structure,
compute frequency content, and estimate signal complexity with conventional,
well-documented numerical methods.
""")

LICENSE_TEXT = dedent("""\
MIT License

Copyright (c) 2026 Cueca Labs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")

APP_INTERFACE = dedent("""\
#!/usr/bin/env python3
"""
APP_INTERFACE.py

A transparent, open-source audio analysis interface.
This script reads a WAV file, computes basic signal metrics, and reports
simple descriptive values that can be reviewed and inspected by anyone.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import wave

import numpy as np


def rms(signal: np.ndarray) -> float:
    if signal.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(np.square(signal))))


def peak(signal: np.ndarray) -> float:
    if signal.size == 0:
        return 0.0
    return float(np.max(np.abs(signal)))


def dominant_frequency(signal: np.ndarray, sample_rate: int) -> float:
    if signal.size == 0 or sample_rate <= 0:
        return 0.0

    spectrum = np.abs(np.fft.rfft(signal))
    freqs = np.fft.rfftfreq(signal.size, d=1.0 / sample_rate)

    if spectrum.size == 0 or freqs.size == 0:
        return 0.0

    return float(freqs[int(np.argmax(spectrum))])


def spectral_entropy(signal: np.ndarray, bins: int = 64) -> float:
    if signal.size == 0:
        return 0.0

    spectrum = np.abs(np.fft.rfft(signal))
    spectrum = spectrum[spectrum > 0]

    if spectrum.size == 0:
        return 0.0

    hist, _ = np.histogram(spectrum, bins=bins)
    hist = hist[hist > 0]
    if hist.size == 0:
        return 0.0

    probs = hist / np.sum(hist)
    return float(-np.sum(probs * np.log2(probs)))


def load_wav(path: Path):
    with wave.open(str(path), "rb") as wav_file:
        sample_rate = wav_file.getframerate()
        channels = wav_file.getnchannels()
        frames = wav_file.getnframes()
        raw = wav_file.readframes(frames)

    data = np.frombuffer(raw, dtype=np.dtype("<i2")).astype(np.float64)
    if channels > 1:
        data = data.reshape(-1, channels)
        data = data.mean(axis=1)
    return data, sample_rate


def analyze_audio(path: Path):
    samples, sample_rate = load_wav(path)
    if np.max(np.abs(samples)) > 0:
        samples = samples / np.max(np.abs(samples))

    return {
        "sample_rate_hz": sample_rate,
        "total_samples": int(samples.size),
        "rms": rms(samples),
        "peak_amplitude": peak(samples),
        "dominant_frequency_hz": dominant_frequency(samples, sample_rate),
        "spectral_entropy": spectral_entropy(samples),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze a WAV file using standard signal-processing metrics."
    )
    parser.add_argument("audio_file", type=Path, help="Path to the WAV file to analyze.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {args.audio_file}")

    report = analyze_audio(args.audio_file)

    print("Audio Analysis Report")
    print("====================")
    for key, value in report.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
""")


def write_clean_repo(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)

    files = {
        "MANUSCRIPT_CD26.md": MANUSCRIPT,
        "LICENSE.txt": LICENSE_TEXT,
        "APP_INTERFACE.py": APP_INTERFACE,
    }

    for filename, content in files.items():
        (root / filename).write_text(content, encoding="utf-8")

    print("[OK] Clean repository scaffold created successfully.")
    print(f"Repository root: {root.resolve()}")
    print("Created files:")
    for filename in files:
        print(f"  - {filename}")


if __name__ == "__main__":
    write_clean_repo(Path(__file__).resolve().parent)
