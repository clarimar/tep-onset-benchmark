# Roteiro para preencher a Tabela 1

Cinco linhas pendentes. Todas exigem texto completo — acessível pelo Portal de
Periódicos da CAPES com login da PUC Goiás.

---

## O que procurar em cada artigo

Vá direto à seção de dados (normalmente "Dataset", "Data description",
"Experimental setup" ou "Case study"). Procure:

**1. Variante do conjunto** — a resposta está em como descrevem a origem:
- "expanded" / "extended TEP" / Rieth / Harvard Dataverse / 500 simulation runs → **expanded**
- Downs & Vogel / Chiang / Braatz / `d00.dat`, `d01_te.dat` / 480 e 960 amostras → **original**
- simulador próprio / Bathelt / Andersen GUI → **other** (anotar qual)

**2. Unidade de divisão** — procure como treino e teste são separados:
- arquivos de simulação distintos → `simulation file`
- runs completos amostrados → `complete run`
- divisão percentual das linhas (70/30, 80/20) sem mencionar run → `observation`
- validação cruzada k-fold sobre linhas → `observation`

**3. Janela de injeção — a coluna decisiva.** Busque no PDF por:

```
"1 hour"    "8 hours"    "after 1 h"    "after 8 h"
"sample 160"   "sample 20"   "160th"   "introduced"
"onset"   "injection"   "fault-free period"   "first 160"
"pre-fault"   "normal operation period"
```

Classifique:
- **yes** — declaram o instante E o que fizeram com o segmento anterior
- **partial** — mencionam o instante mas não dizem se descartaram ou mantiveram
- **no** — não mencionam

A distinção entre `partial` e `no` importa: `partial` significa que sabiam e
não trataram; `no` significa que possivelmente não sabiam. As duas sustentam o
argumento, mas de formas diferentes.

**4. Métrica** — FDR/FAR, acurácia, F1, taxa de detecção, etc.

---

## Ordem sugerida

| # | Artigo | Por quê primeiro | Acesso |
|---|--------|------------------|--------|
| 1 | Lomov et al. (2021) | Único que usa o conjunto expandido; comparador direto | Elsevier / CAPES |
| 2 | Yin et al. (2012) | O mais citado; referência de protocolo para muitos | Elsevier / CAPES |
| 3 | Chadha & Schwung (2017) | Deep learning inicial no TEP | IEEE Xplore / CAPES |
| 4 | Gao & Hou (2016) | Método clássico híbrido | Elsevier / CAPES |
| 5 | Anitha et al. (2023) | Mais recente; mostra que o problema persiste | Springer / CAPES |

Se o tempo for curto, os dois primeiros já bastam para escrever o parágrafo de
síntese com honestidade: "de N estudos examinados, M declaram...".

---

## Como escrever a síntese

O parágrafo final da Seção 2.5 muda conforme o resultado. Três cenários:

**Se a maioria não declara** (o mais provável):
> Of the six studies examined, only X state the instant of fault injection, and
> none describe how the pre-onset segment was handled. Reported figures are
> therefore not directly comparable, and the differences between them may
> reflect labeling convention as much as method.

**Se declaram mas divergem:**
> Of the six studies examined, X state the treatment explicitly, and they do not
> agree: Y discard the pre-onset segment while Z retain it. A difference of
> 0.085 in macro-F1 for an identical model therefore separates two subsets of
> the literature that are routinely compared as if commensurable.

**Se a maioria declara e concorda:**
> Of the six studies examined, X state the treatment explicitly and adopt the
> literal convention. Reported figures are thus mutually comparable but
> collectively understate post-onset performance by a factor predictable from
> Table 6.

O terceiro cenário é o menos provável e o menos favorável, mas continua sendo
um resultado publicável: a literatura seria internamente consistente e
uniformemente deslocada.

---

## Registre o que encontrar

Sugestão: anote em `results/wp1a_survey/onset_survey.csv` com colunas
`study, doi, dataset, split_unit, onset_stated, onset_evidence, metric`,
onde `onset_evidence` guarda a frase exata (ou "not found" e as seções
verificadas). Isso vira material do repositório e sustenta a tabela caso um
revisor questione alguma classificação.
