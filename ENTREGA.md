# Entrega — Episodic Pyramid SLM

**Disciplina:** IA Generativa para Engenharia  
**Data:** 15/10/2026  
**Formato pedido pelo enunciado:** código + documentação no **GitHub** (+ prints da GPU).  
**Não é exigido** vídeo do treinamento nem apresentação ao vivo (salvo se o professor pedir depois em sala).

---

## Checklist do enunciado

| Exigência | Como cobrimos | Evidência no repo |
|-----------|----------------|-------------------|
| Escolher LLM | SmolLM2-1.7B-Instruct (+ sweep no 360M) | `config.py`, `README.md` |
| Problema específico | Compressão episódica T1→T2 / T2→T3 (pirâmide Strata) | `README.md`, `compressao.py` |
| Testar parâmetros | LoRA r/lr/epochs em várias tags | `train_*.json`, tabela no README |
| Avaliar respostas | Gabarito + bakeoff | `evaluate.py`, `runs/resultados/`, `bakeoff.py` |
| Tudo na GPU | RTX 3060 + CUDA PyTorch | prints + `config.py` / `nvidia-smi` |
| Frontend de prompt | Gradio | `app.py` → http://127.0.0.1:7860 |
| Print GPU no VSCode | Gerenciador + `nvidia-smi` + Gradio | pasta `docs/prints/` (colar prints) |
| Código + docs no GitHub | este lab | link do repositório |

---

## Organização do repo

```
app.py              <- frontend (abrir/demonstrar)
train_lora.py       <- treinamento GPU
config.py utils.py compressao.py
data/               <- datasets sinteticos
runs/lora_r16_1b7/  <- adapter treinado
docs/prints/        <- prints GPU + Gradio
scripts/            <- geracao de dados, eval, bakeoff (suporte)
```

## O que subir no GitHub

**Incluir**
- Código da raiz + `scripts/`, `requirements.txt`, `README.md`, `ENTREGA.md`
- `data/` (sintéticos — leves)
- `runs/resultados/*.json` e adapters
- Prints em `docs/prints/`

**Não incluir**
- `.venv/`
- checkpoints intermediários `runs/lora_*/checkpoint-*`

---

## Texto curto para colar no Classroom / e-mail

> Segue o link do repositório do trabalho (grupo N):  
> **https://github.com/USER/REPO**  
>  
> **LLM:** HuggingFaceTB/SmolLM2-1.7B-Instruct + LoRA (`r16_1b7`)  
> **Problema:** compressão de memória episódica hierárquica (Tier 1→2 e 2→3)  
> **GPU:** NVIDIA RTX 3060 (treinos e inferência locais)  
> **Frontend:** Gradio (`python app.py`)  
> Documentação, dados sintéticos, métricas e prints estão no README / `ENTREGA.md`.

---

## Prints recomendados (colar em `docs/prints/`)

1. `01-gpu-vscode.png` — VSCode + `nvidia-smi` + Gerenciador (RTX 3060)  
2. `02-gradio-compressao.png` — Gradio com SLM + heurística + taxa ~3.5×  
3. Opcional: `03-bakeoff.png` — gráfico comparativo

O print que você já tirou (Gradio + nvidia-smi + Task Manager) **serve como o principal**.
