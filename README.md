# Episodic Pyramid SLM

Laboratório acadêmico: treinar um **Small Language Model local (SmolLM2)** para
**comprimir memória episódica hierárquica** (pirâmide Strata).

| Campo | Valor |
|-------|--------|
| LLM principal | `HuggingFaceTB/SmolLM2-1.7B-Instruct` + LoRA `r16_1b7` |
| Sweep / baseline | também SmolLM2-360M-Instruct |
| Problema | Compressão Tier 1→2 (milestones) e Tier 2→3 (narrativa) |
| Método | LoRA (SFT) na GPU local (RTX 3060) |
| Frontend | Gradio (`app.py`) |
| Entrega | 15/10/2026 — ver [`ENTREGA.md`](ENTREGA.md) |

```
Tier 1 (traces)  --SLM-->  Tier 2 (milestones)  --SLM-->  Tier 3 (narrativa)
```

Motivação: o rollup atual do Strata usa template heurístico determinístico
`[Milestone Rollup] <medoid> | N outcomes, M files`. Isso conta invariantes, mas
não narra a decisão (ex.: HS256→RS256). O SLM gera o resumo narrativo.

---

## Entrega (o que o professor pediu)

Pelo enunciado, a entrega é **código + documentação no GitHub** e **print da GPU**.
**Não há pedido de vídeo** do treinamento.

Detalhes e checklist: [`ENTREGA.md`](ENTREGA.md).

---

## Setup (Windows + GPU)

```powershell
cd labs/episodic-pyramid-slm   # ou a pasta deste repo
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -U pip
pip install torch --index-url https://download.pytorch.org/whl/cu128
pip install -r requirements.txt
python smoke_test.py           # deve imprimir === AMBIENTE OK ===
```

> Sem o `--index-url` CUDA o PyTorch vem em build CPU.

---

## Pipeline

```powershell
python generate_synthetic.py          # dados sintéticos
python baseline.py                    # sem fine-tune
python train_lora.py --tag r16_1b7 --modelo HuggingFaceTB/SmolLM2-1.7B-Instruct --r 16 --lr 1e-4 --epochs 3 --include-t23
python evaluate.py --tag r16_1b7 --nome lora_r16_1b7
python bakeoff.py
python app.py                         # http://127.0.0.1:7860
```

Prévia dos dados: `python preview_dados.py`

---

## Dados sintéticos

| Arquivo | Qtd | Conteúdo |
|---------|-----|----------|
| `data/episodes_t1.jsonl` | 72 | Episódios Tier 1 |
| `data/sft_t1_to_t2.jsonl` | 63 | Pares SFT milestone |
| `data/sft_t2_to_t3.jsonl` | 4 | Pares SFT narrativa |
| `data/gabarito.json` | 12 | Held-out (factual/síntese/armadilha) |

Clusters: `task-auth-jwt` · `task-sqlite-pool` (com falha) · `task-cdc-outbox`

---

## Resultados (RTX 3060 12 GB)

| Config | Modelo | Acerto geral | Factual | Notas |
|--------|--------|--------------|---------|-------|
| baseline | 360M Instruct | 33% | 60% | sem FT |
| lora default / r8 | 360M LoRA | ~25% | 40% | dataset curto |
| lora r16_t23 | 360M LoRA | 50% | 80% | + pares T2→T3 |
| **r16_1b7** | **1.7B LoRA** | demo UI | — | melhor qualidade narrativa |

Demo Gradio (exemplo Auth JWT): **721 → ~200 chars (~3.5×)** no SLM;
heurística Strata ~7× (mais curta, sem narrativa).

VRAM pico treino 1.7B LoRA: ~4 GB.

---

## Nota Windows

Treino via `transformers.Trainer` + PEFT (TRL 1.15 exige Triton/Linux).

---

## Estrutura

```
episodic-pyramid-slm/
├── ENTREGA.md              # checklist da disciplina
├── README.md
├── app.py                  # frontend Gradio
├── generate_synthetic.py   # dados sintéticos
├── train_lora.py / evaluate.py / bakeoff.py
├── compressao.py           # heurística + SLM + métricas
├── data/                   # sintéticos + gabarito
├── runs/resultados/        # métricas JSON
├── runs/lora_r16_1b7/      # adapter treinado
└── docs/prints/            # prints GPU + Gradio (colar aqui)
```
