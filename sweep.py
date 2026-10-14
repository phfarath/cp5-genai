"""
Roda o sweep de hiperparâmetros + avaliações em sequência.

  python sweep.py
"""
from __future__ import annotations

import subprocess
import sys

CMDS = [
    [sys.executable, "generate_synthetic.py"],
    [sys.executable, "baseline.py"],
    [sys.executable, "train_lora.py", "--tag", "default", "--r", "16", "--lr", "2e-4", "--epochs", "2"],
    [sys.executable, "evaluate.py", "--tag", "default"],
    [sys.executable, "train_lora.py", "--tag", "r8_lr1e4", "--r", "8", "--lr", "1e-4", "--epochs", "2"],
    [sys.executable, "evaluate.py", "--tag", "r8_lr1e4", "--nome", "lora_r8_lr1e4"],
    [sys.executable, "train_lora.py", "--tag", "r16_t23", "--r", "16", "--lr", "2e-4", "--epochs", "2", "--include-t23"],
    [sys.executable, "evaluate.py", "--tag", "r16_t23", "--nome", "lora_r16_t23"],
    [sys.executable, "bakeoff.py"],
]


def main() -> None:
    for cmd in CMDS:
        print("\n>>>", " ".join(cmd), flush=True)
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
