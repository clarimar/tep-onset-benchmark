# WP1A definitivo

O pipeline tem duas barreiras. `tune` usa somente treino e validação; nem sequer
aceita um caminho de teste. `finalize` repete os modelos selecionados em cinco
sementes e só acessa o teste quando `--test` é informado explicitamente.

## 1. Verificação rápida

```bash
python -m wp1a.tune \
  --train ../upload/train.parquet \
  --validation ../upload/validation.parquet \
  --output results/wp1a_definitive/smoke_test \
  --quick-check
```

## 2. Ajuste definitivo

```bash
python -m wp1a.tune \
  --train ../upload/train.parquet \
  --validation ../upload/validation.parquet
```

Os melhores hiperparâmetros por algoritmo ficam em
`results/wp1a_definitive/tuning/selected_hyperparameters.csv`.

## 3. Repetições sem teste

```bash
python -m wp1a.finalize \
  --train ../upload/train.parquet \
  --validation ../upload/validation.parquet \
  --selected results/wp1a_definitive/tuning/selected_hyperparameters.csv
```

Na fase final do artigo, repita o comando acrescentando
`--test /caminho/local/test.parquet` e use uma nova pasta em `--output`. Nunca
sobrescreva uma execução anterior.
