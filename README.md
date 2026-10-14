# Episodic Pyramid SLM

Small Language Model local (SmolLM2) treinado com LoRA para **comprimir memória episódica hierárquica**: traces Tier 1 → milestones Tier 2 → narrativa de sessão Tier 3.

| | |
|---|---|
| **Modelo** | `HuggingFaceTB/SmolLM2-1.7B-Instruct` + LoRA (`r=16`, lr=`1e-4`, 3 epochs) |
| **GPU** | NVIDIA GeForce RTX 3060 12 GB (CUDA / PyTorch `cu128`, bf16) |
| **Problema** | Sumarização de clusters episódicos (Auth JWT, SQLite pool, CDC outbox) |
| **Frontend** | Gradio — `python app.py` |

```
Tier 1 (traces)  -->  Tier 2 (milestones)  -->  Tier 3 (narrativa de sessão)
```

O rollup heurístico de referência usa o template  
`[Milestone Rollup] <medoid> | N outcomes, M files`.  
O SLM gera o resumo narrativo (ex.: migração HS256→RS256).

---

## Estrutura

```
app.py              # frontend Gradio
train_lora.py       # treinamento LoRA
config.py           # hiperparâmetros e paths
utils.py            # carga/geração/VRAM
compressao.py       # heurística + SLM + métricas
data/               # datasets sintéticos e gabarito
runs/               # adapters e resultados
scripts/            # geração de dados, baseline, avaliação, bake-off
docs/prints/        # evidências de GPU e execução
```

---

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -U pip
pip install torch --index-url https://download.pytorch.org/whl/cu128
pip install -r requirements.txt
python scripts/smoke_test.py
```

---

## Treino e inferência

```powershell
python scripts/generate_synthetic.py

python train_lora.py --tag r16_1b7 `
  --modelo HuggingFaceTB/SmolLM2-1.7B-Instruct `
  --r 16 --lr 1e-4 --epochs 3 --include-t23

python app.py
# http://127.0.0.1:7860
```

Avaliação / comparação:

```powershell
python scripts/baseline.py
python scripts/evaluate.py --tag r16_1b7 --nome lora_r16_1b7
python scripts/bakeoff.py
```

---

## Dados

Gerados por `scripts/generate_synthetic.py` (3 clusters):

| Arquivo | Conteúdo |
|---------|----------|
| `data/episodes_t1.jsonl` | Episódios Tier 1 |
| `data/sft_t1_to_t2.jsonl` | Pares SFT compressão milestone |
| `data/sft_t2_to_t3.jsonl` | Pares SFT narrativa de sessão |
| `data/gabarito.json` | Avaliação held-out (factual / síntese / armadilha) |

---

## Resultados

- Adapter: `runs/lora_r16_1b7/`
- Métricas: `runs/resultados/`
- Bake-off: `runs/bakeoff.png`
- Compressão no Gradio (exemplo Auth JWT): ~721 → ~200 caracteres (**~3.5×**) no SLM; heurística ~7× (mais curta, sem narrativa)

### Evidências

![GPU + Gradio](docs/prints/01-gpu-gradio-nvidia.png)

![Bake-off](docs/prints/03-bakeoff.png)
