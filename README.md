# Episodic Pyramid SLM

Laboratório acadêmico: treinar um **Small Language Model local (SmolLM2)** para
**comprimir memória episódica hierárquica** (pirâmide Strata).

| Campo | Valor |
|-------|--------|
| LLM principal | `HuggingFaceTB/SmolLM2-1.7B-Instruct` + LoRA `r16_1b7` |
| Problema | Compressão Tier 1→2 (milestones) e Tier 2→3 (narrativa) |
| Método | LoRA (SFT) na GPU local (RTX 3060) |
| Frontend | Gradio (`app.py`) |
| Entrega | 15/10/2026 — ver [`ENTREGA.md`](ENTREGA.md) |

```
Tier 1 (traces)  --SLM-->  Tier 2 (milestones)  --SLM-->  Tier 3 (narrativa)
```

Pelo enunciado, a entrega é **código + documentação no GitHub** e **print da GPU**.

---

## Estrutura (entrega)

Na **raiz** ficam só o essencial que o professor precisa abrir:

| Arquivo | Papel |
|---------|--------|
| `app.py` | Frontend Gradio (prompt → compressão) |
| `train_lora.py` | Treino LoRA na GPU |
| `config.py` / `utils.py` / `compressao.py` | Config e runtime do app/treino |
| `data/` | Datasets sintéticos |
| `runs/` | Adapters treinados + métricas |
| `docs/prints/` | Prints da GPU / Gradio |
| `scripts/` | Geração de dados, baseline, eval, bakeoff (suporte) |

---

## Setup (Windows + GPU)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -U pip
pip install torch --index-url https://download.pytorch.org/whl/cu128
pip install -r requirements.txt
python scripts/smoke_test.py
```

---

## Uso principal (entrega)

```powershell
# (opcional) regenerar dados sinteticos
python scripts/generate_synthetic.py

# treinar
python train_lora.py --tag r16_1b7 --modelo HuggingFaceTB/SmolLM2-1.7B-Instruct --r 16 --lr 1e-4 --epochs 3 --include-t23

# frontend
python app.py
# -> http://127.0.0.1:7860
```

---

## Scripts de suporte

```powershell
python scripts/preview_dados.py
python scripts/baseline.py
python scripts/evaluate.py --tag r16_1b7 --nome lora_r16_1b7
python scripts/bakeoff.py
python scripts/sweep.py
```

---

## Dados sintéticos

| Arquivo | Qtd | Conteúdo |
|---------|-----|----------|
| `data/episodes_t1.jsonl` | 72+ | Episódios Tier 1 |
| `data/sft_t1_to_t2.jsonl` | 63+ | Pares SFT milestone |
| `data/sft_t2_to_t3.jsonl` | 4 | Pares SFT narrativa |
| `data/gabarito.json` | 12 | Held-out |

Clusters: `task-auth-jwt` · `task-sqlite-pool` · `task-cdc-outbox`

---

## Resultados (RTX 3060)

Demo Gradio: **~3.5×** compressão no SLM (heurística ~7×, sem narrativa).  
Adapter: `runs/lora_r16_1b7/`. Print: `docs/prints/01-gpu-gradio-nvidia.png`.
