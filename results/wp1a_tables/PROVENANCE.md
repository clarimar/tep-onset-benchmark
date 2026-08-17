# Procedência

Estes resultados provêm do experimento exploratório `wp1a_benchmark`, **não**
do experimento `wp1a_definitive` reportado no artigo.

Diferenças relevantes:

- conjunto de modelos: inclui ExtraTrees e **não** inclui XGBoost
- unidade de bloco: 10.500 trajetórias da partição de teste
- métrica: acurácia por trajetória

O artigo reporta um teste de Friedman distinto, calculado sobre as cinco
sementes da validação repetida (`wp1a_definitive/repeated_validation_v1`),
com os seis modelos do benchmark. Ver Seção 4.1 do manuscrito:
chi2 = 24,54; p = 1,71e-4; Kendall W = 0,982; CD de Nemenyi = 3,372.

A partição oficial de teste **não** foi usada para comparação entre modelos no
protocolo do artigo. Estes arquivos são preservados como registro de trabalho
exploratório anterior.
