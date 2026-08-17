# Relatório de controle de qualidade — WP1A

**Situação geral:** `PASS`

## Configuração identificada

- Coluna de classe: `faultNumber`
- Coluna de execução: `simulationRun`
- Coluna temporal: `sample`
- Número de atributos: **52**
- Classes esperadas: **21**

## Partições

| split      | file                                                                                        |   size_mb |     rows |   columns |   features |   classes |   missing_labels |   sampled_rows |
|:-----------|:--------------------------------------------------------------------------------------------|----------:|---------:|----------:|-----------:|----------:|-----------------:|---------------:|
| train      | /home/clarimar/Dropbox/aulas/ppgeiia/MEI0028/ProjetoA_TEP/data/processed/train.parquet      |   411.349 |  4200000 |        56 |         52 |        21 |                0 |         300000 |
| validation | /home/clarimar/Dropbox/aulas/ppgeiia/MEI0028/ProjetoA_TEP/data/processed/validation.parquet |   125.521 |  1050000 |        56 |         52 |        21 |                0 |         300000 |
| test       | /home/clarimar/Dropbox/aulas/ppgeiia/MEI0028/ProjetoA_TEP/data/processed/test.parquet       |   921.726 | 10080000 |        56 |         52 |        21 |                0 |         300000 |

## Resultado das verificações

| status   | severity   | split              | check                            | value                                                                   | threshold   | message                                                                                                                                                                                                        |
|:---------|:-----------|:-------------------|:---------------------------------|:------------------------------------------------------------------------|:------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PASS     | critical   | validation         | schema_columns                   | 56                                                                      | 56          | Esquema idêntico ao treino.                                                                                                                                                                                    |
| PASS     | critical   | test               | schema_columns                   | 56                                                                      | 56          | Esquema idêntico ao treino.                                                                                                                                                                                    |
| PASS     | critical   | train              | non_empty_split                  | 4200000                                                                 | > 0         | Partição contém observações.                                                                                                                                                                                   |
| PASS     | critical   | train              | missing_labels                   | 0                                                                       | 0           | Nenhum rótulo ausente.                                                                                                                                                                                         |
| PASS     | warning    | train              | number_of_classes                | 21                                                                      | 21          | Número de classes conforme o esperado.                                                                                                                                                                         |
| PASS     | critical   | train              | missing_feature_values           | 0                                                                       | 0           | Nenhum valor ausente nos atributos amostrados.                                                                                                                                                                 |
| PASS     | critical   | train              | infinite_feature_values          | 0                                                                       | 0           | Nenhum valor infinito nos atributos amostrados.                                                                                                                                                                |
| PASS     | warning    | train              | constant_features                | 0                                                                       | 0           | Nenhuma variável constante.                                                                                                                                                                                    |
| PASS     | warning    | train              | exact_duplicates_sample          | 0 (0.000000%)                                                           | 0           | Nenhuma duplicata exata na amostra.                                                                                                                                                                            |
| PASS     | critical   | validation         | non_empty_split                  | 1050000                                                                 | > 0         | Partição contém observações.                                                                                                                                                                                   |
| PASS     | critical   | validation         | missing_labels                   | 0                                                                       | 0           | Nenhum rótulo ausente.                                                                                                                                                                                         |
| PASS     | warning    | validation         | number_of_classes                | 21                                                                      | 21          | Número de classes conforme o esperado.                                                                                                                                                                         |
| PASS     | critical   | validation         | missing_feature_values           | 0                                                                       | 0           | Nenhum valor ausente nos atributos amostrados.                                                                                                                                                                 |
| PASS     | critical   | validation         | infinite_feature_values          | 0                                                                       | 0           | Nenhum valor infinito nos atributos amostrados.                                                                                                                                                                |
| PASS     | warning    | validation         | constant_features                | 0                                                                       | 0           | Nenhuma variável constante.                                                                                                                                                                                    |
| PASS     | warning    | validation         | exact_duplicates_sample          | 0 (0.000000%)                                                           | 0           | Nenhuma duplicata exata na amostra.                                                                                                                                                                            |
| PASS     | critical   | test               | non_empty_split                  | 10080000                                                                | > 0         | Partição contém observações.                                                                                                                                                                                   |
| PASS     | critical   | test               | missing_labels                   | 0                                                                       | 0           | Nenhum rótulo ausente.                                                                                                                                                                                         |
| PASS     | warning    | test               | number_of_classes                | 21                                                                      | 21          | Número de classes conforme o esperado.                                                                                                                                                                         |
| PASS     | critical   | test               | missing_feature_values           | 0                                                                       | 0           | Nenhum valor ausente nos atributos amostrados.                                                                                                                                                                 |
| PASS     | critical   | test               | infinite_feature_values          | 0                                                                       | 0           | Nenhum valor infinito nos atributos amostrados.                                                                                                                                                                |
| PASS     | warning    | test               | constant_features                | 0                                                                       | 0           | Nenhuma variável constante.                                                                                                                                                                                    |
| PASS     | warning    | test               | exact_duplicates_sample          | 0 (0.000000%)                                                           | 0           | Nenhuma duplicata exata na amostra.                                                                                                                                                                            |
| PASS     | warning    | train              | trajectory_original_order        | 0                                                                       | 0           | Todas as trajetórias estão ordenadas no arquivo.                                                                                                                                                               |
| PASS     | critical   | train              | trajectory_duplicate_time_points | 0                                                                       | 0           | Não há pares duplicados de classe, execução e tempo.                                                                                                                                                           |
| PASS     | critical   | train              | trajectory_missing_time          | 0                                                                       | 0           | Não há valores temporais ausentes.                                                                                                                                                                             |
| PASS     | warning    | train              | trajectory_gaps                  | 0                                                                       | 0           | Não foram detectadas lacunas temporais.                                                                                                                                                                        |
| PASS     | info       | train              | trajectory_length_summary        | {"runs": 8400, "min": 500, "median": 500.0, "mean": 500.0, "max": 500}  | descriptive | Resumo descritivo do comprimento das trajetórias.                                                                                                                                                              |
| PASS     | warning    | validation         | trajectory_original_order        | 0                                                                       | 0           | Todas as trajetórias estão ordenadas no arquivo.                                                                                                                                                               |
| PASS     | critical   | validation         | trajectory_duplicate_time_points | 0                                                                       | 0           | Não há pares duplicados de classe, execução e tempo.                                                                                                                                                           |
| PASS     | critical   | validation         | trajectory_missing_time          | 0                                                                       | 0           | Não há valores temporais ausentes.                                                                                                                                                                             |
| PASS     | warning    | validation         | trajectory_gaps                  | 0                                                                       | 0           | Não foram detectadas lacunas temporais.                                                                                                                                                                        |
| PASS     | info       | validation         | trajectory_length_summary        | {"runs": 2100, "min": 500, "median": 500.0, "mean": 500.0, "max": 500}  | descriptive | Resumo descritivo do comprimento das trajetórias.                                                                                                                                                              |
| PASS     | warning    | test               | trajectory_original_order        | 0                                                                       | 0           | Todas as trajetórias estão ordenadas no arquivo.                                                                                                                                                               |
| PASS     | critical   | test               | trajectory_duplicate_time_points | 0                                                                       | 0           | Não há pares duplicados de classe, execução e tempo.                                                                                                                                                           |
| PASS     | critical   | test               | trajectory_missing_time          | 0                                                                       | 0           | Não há valores temporais ausentes.                                                                                                                                                                             |
| PASS     | warning    | test               | trajectory_gaps                  | 0                                                                       | 0           | Não foram detectadas lacunas temporais.                                                                                                                                                                        |
| PASS     | info       | test               | trajectory_length_summary        | {"runs": 10500, "min": 960, "median": 960.0, "mean": 960.0, "max": 960} | descriptive | Resumo descritivo do comprimento das trajetórias.                                                                                                                                                              |
| PASS     | info       | train x validation | run_id_overlap                   | 491                                                                     | 0           | Há números de execução repetidos entre as partições. No TEP isso é esperado porque simulationRun é um identificador local e pode ser reiniciado. A repetição foi registrada apenas como informação contextual. |
| PASS     | info       | train x test       | run_id_overlap                   | 500                                                                     | 0           | Há números de execução repetidos entre as partições. No TEP isso é esperado porque simulationRun é um identificador local e pode ser reiniciado. A repetição foi registrada apenas como informação contextual. |
| PASS     | info       | validation x test  | run_id_overlap                   | 491                                                                     | 0           | Há números de execução repetidos entre as partições. No TEP isso é esperado porque simulationRun é um identificador local e pode ser reiniciado. A repetição foi registrada apenas como informação contextual. |
| PASS     | warning    | train x validation | row_hash_overlap_sample          | 0                                                                       | 0           | Nenhuma linha idêntica encontrada nas amostras cruzadas.                                                                                                                                                       |
| PASS     | warning    | train x test       | row_hash_overlap_sample          | 0                                                                       | 0           | Nenhuma linha idêntica encontrada nas amostras cruzadas.                                                                                                                                                       |
| PASS     | warning    | validation x test  | row_hash_overlap_sample          | 0                                                                       | 0           | Nenhuma linha idêntica encontrada nas amostras cruzadas.                                                                                                                                                       |
| PASS     | warning    | train              | training_standardization_sample  | 0                                                                       | 0           | As variáveis de treino parecem padronizadas.                                                                                                                                                                   |

## Distribuição das classes

| split      |   class |   count |   proportion |
|:-----------|--------:|--------:|-------------:|
| train      |       0 |  200000 |     0.047619 |
| train      |       1 |  200000 |     0.047619 |
| train      |       2 |  200000 |     0.047619 |
| train      |       3 |  200000 |     0.047619 |
| train      |       4 |  200000 |     0.047619 |
| train      |       5 |  200000 |     0.047619 |
| train      |       6 |  200000 |     0.047619 |
| train      |       7 |  200000 |     0.047619 |
| train      |       8 |  200000 |     0.047619 |
| train      |       9 |  200000 |     0.047619 |
| train      |      10 |  200000 |     0.047619 |
| train      |      11 |  200000 |     0.047619 |
| train      |      12 |  200000 |     0.047619 |
| train      |      13 |  200000 |     0.047619 |
| train      |      14 |  200000 |     0.047619 |
| train      |      15 |  200000 |     0.047619 |
| train      |      16 |  200000 |     0.047619 |
| train      |      17 |  200000 |     0.047619 |
| train      |      18 |  200000 |     0.047619 |
| train      |      19 |  200000 |     0.047619 |
| train      |      20 |  200000 |     0.047619 |
| validation |       0 |   50000 |     0.047619 |
| validation |       1 |   50000 |     0.047619 |
| validation |       2 |   50000 |     0.047619 |
| validation |       3 |   50000 |     0.047619 |
| validation |       4 |   50000 |     0.047619 |
| validation |       5 |   50000 |     0.047619 |
| validation |       6 |   50000 |     0.047619 |
| validation |       7 |   50000 |     0.047619 |
| validation |       8 |   50000 |     0.047619 |
| validation |       9 |   50000 |     0.047619 |
| validation |      10 |   50000 |     0.047619 |
| validation |      11 |   50000 |     0.047619 |
| validation |      12 |   50000 |     0.047619 |
| validation |      13 |   50000 |     0.047619 |
| validation |      14 |   50000 |     0.047619 |
| validation |      15 |   50000 |     0.047619 |
| validation |      16 |   50000 |     0.047619 |
| validation |      17 |   50000 |     0.047619 |
| validation |      18 |   50000 |     0.047619 |
| validation |      19 |   50000 |     0.047619 |
| validation |      20 |   50000 |     0.047619 |
| test       |       0 |  480000 |     0.047619 |
| test       |       1 |  480000 |     0.047619 |
| test       |       2 |  480000 |     0.047619 |
| test       |       3 |  480000 |     0.047619 |
| test       |       4 |  480000 |     0.047619 |
| test       |       5 |  480000 |     0.047619 |
| test       |       6 |  480000 |     0.047619 |
| test       |       7 |  480000 |     0.047619 |
| test       |       8 |  480000 |     0.047619 |
| test       |       9 |  480000 |     0.047619 |
| test       |      10 |  480000 |     0.047619 |
| test       |      11 |  480000 |     0.047619 |
| test       |      12 |  480000 |     0.047619 |
| test       |      13 |  480000 |     0.047619 |
| test       |      14 |  480000 |     0.047619 |
| test       |      15 |  480000 |     0.047619 |
| test       |      16 |  480000 |     0.047619 |
| test       |      17 |  480000 |     0.047619 |
| test       |      18 |  480000 |     0.047619 |
| test       |      19 |  480000 |     0.047619 |
| test       |      20 |  480000 |     0.047619 |

## Integridade das trajetórias

| split      |   trajectories |   min_length |   median_length |   mean_length |   max_length |   duplicated_time_points |   runs_with_gaps |
|:-----------|---------------:|-------------:|----------------:|--------------:|-------------:|-------------------------:|-----------------:|
| test       |          10500 |          960 |             960 |           960 |          960 |                        0 |                0 |
| train      |           8400 |          500 |             500 |           500 |          500 |                        0 |                0 |
| validation |           2100 |          500 |             500 |           500 |          500 |                        0 |                0 |

## Estatísticas das variáveis

| split      | feature   | dtype   |   missing |   positive_inf |   negative_inf |   finite_count |         mean |      std |       min |      max |   nunique |
|:-----------|:----------|:--------|----------:|---------------:|---------------:|---------------:|-------------:|---------:|----------:|---------:|----------:|
| train      | xmeas_1   | float32 |         0 |              0 |              0 |         300000 | -0.00234893  | 0.994059 |  -1.81778 |  5.16513 |     56621 |
| train      | xmeas_2   | float32 |         0 |              0 |              0 |         300000 |  0.00093187  | 0.995419 |  -7.15465 |  4.80024 |      3361 |
| train      | xmeas_3   | float32 |         0 |              0 |              0 |         300000 | -0.00280977  | 0.996382 |  -8.4998  |  5.57645 |      8745 |
| train      | xmeas_4   | float32 |         0 |              0 |              0 |         300000 |  0.000144117 | 0.994094 |  -7.41696 |  8.112   |     18683 |
| train      | xmeas_5   | float32 |         0 |              0 |              0 |         300000 |  0.000826428 | 1.00016  |  -6.38688 |  6.2812  |      2213 |
| train      | xmeas_6   | float32 |         0 |              0 |              0 |         300000 | -0.00295265  | 0.997454 |  -7.10694 |  7.01512 |      2987 |
| train      | xmeas_7   | float32 |         0 |              0 |              0 |         300000 | -0.00204317  | 0.996978 |  -3.87182 |  3.75134 |      4584 |
| train      | xmeas_8   | float32 |         0 |              0 |              0 |         300000 | -0.000198881 | 0.998383 |  -9.92673 |  9.24682 |     11573 |
| train      | xmeas_9   | float32 |         0 |              0 |              0 |         300000 | -0.00032725  | 0.998039 | -10.5209  |  7.85193 |       131 |
| train      | xmeas_10  | float32 |         0 |              0 |              0 |         300000 | -0.00305965  | 0.990485 |  -3.83265 |  5.6282  |     30277 |
| train      | xmeas_11  | float32 |         0 |              0 |              0 |         300000 |  0.0013304   | 0.997622 |  -6.35529 |  4.05465 |     10349 |
| train      | xmeas_12  | float32 |         0 |              0 |              0 |         300000 | -0.00275905  | 1.00068  |  -4.75169 |  4.66027 |      6472 |
| train      | xmeas_13  | float32 |         0 |              0 |              0 |         300000 | -0.00200553  | 0.996623 |  -4.15113 |  3.95418 |      4754 |
| train      | xmeas_14  | float32 |         0 |              0 |              0 |         300000 |  0.00103359  | 0.997634 |  -4.93849 |  6.08666 |      7111 |
| train      | xmeas_15  | float32 |         0 |              0 |              0 |         300000 |  0.000655577 | 0.999069 |  -4.88442 |  5.01813 |      6623 |
| train      | xmeas_16  | float32 |         0 |              0 |              0 |         300000 | -0.0016655   | 0.998494 |  -2.93209 |  4.29688 |      4552 |
| train      | xmeas_17  | float32 |         0 |              0 |              0 |         300000 |  0.00109477  | 0.999496 |  -4.9492  |  6.02131 |      4506 |
| train      | xmeas_18  | float32 |         0 |              0 |              0 |         300000 | -0.000796814 | 0.992452 |  -6.7979  |  4.6357  |     14309 |
| train      | xmeas_19  | float32 |         0 |              0 |              0 |         300000 | -0.000802319 | 0.995276 |  -3.65562 |  3.24746 |     32867 |
| train      | xmeas_20  | float32 |         0 |              0 |              0 |         300000 | -0.00122979  | 0.997089 |  -9.75714 |  5.49739 |      8436 |
| train      | xmeas_21  | float32 |         0 |              0 |              0 |         300000 |  0.00090507  | 0.996561 | -11.2934  |  4.1339  |      9891 |
| train      | xmeas_22  | float32 |         0 |              0 |              0 |         300000 | -0.000315817 | 0.999692 |  -9.8939  |  4.59135 |      9951 |
| train      | xmeas_23  | float32 |         0 |              0 |              0 |         300000 | -0.00115719  | 0.998688 |  -4.97669 |  4.50424 |     11306 |
| train      | xmeas_24  | float32 |         0 |              0 |              0 |         300000 |  0.000318653 | 0.996422 |  -6.15864 |  6.01348 |     17347 |
| train      | xmeas_25  | float32 |         0 |              0 |              0 |         300000 | -0.00103943  | 0.99993  |  -4.16897 |  4.9671  |     11350 |
| train      | xmeas_26  | float32 |         0 |              0 |              0 |         300000 |  0.00099571  | 0.997264 |  -6.64997 |  6.64658 |     10053 |
| train      | xmeas_27  | float32 |         0 |              0 |              0 |         300000 |  0.00195026  | 0.992436 |  -6.7974  |  7.58389 |      9013 |
| train      | xmeas_28  | float32 |         0 |              0 |              0 |         300000 |  0.00496548  | 0.987856 |  -5.6966  |  4.10445 |      9463 |
| train      | xmeas_29  | float32 |         0 |              0 |              0 |         300000 | -0.00103898  | 0.998885 |  -4.67684 |  4.35392 |     15022 |
| train      | xmeas_30  | float32 |         0 |              0 |              0 |         300000 |  0.00198221  | 0.995702 |  -6.04076 |  6.09452 |      3007 |
| train      | xmeas_31  | float32 |         0 |              0 |              0 |         300000 | -0.000995199 | 1.00027  |  -4.00601 |  4.877   |     14882 |
| train      | xmeas_32  | float32 |         0 |              0 |              0 |         300000 |  0.00176515  | 0.997131 |  -6.55724 |  9.10268 |     16613 |
| train      | xmeas_33  | float32 |         0 |              0 |              0 |         300000 |  0.00291485  | 0.992005 |  -6.42759 |  7.98168 |     11333 |
| train      | xmeas_34  | float32 |         0 |              0 |              0 |         300000 |  0.00538511  | 0.9888   |  -5.44611 |  4.3745  |     10517 |
| train      | xmeas_35  | float32 |         0 |              0 |              0 |         300000 |  0.00165039  | 0.997459 |  -5.01049 |  4.48054 |     20458 |
| train      | xmeas_36  | float32 |         0 |              0 |              0 |         300000 |  0.000932925 | 0.997442 |  -5.00196 |  4.24557 |     12688 |
| train      | xmeas_37  | float32 |         0 |              0 |              0 |         300000 |  0.000440648 | 1.00089  |  -4.51954 |  4.80627 |     76216 |
| train      | xmeas_38  | float32 |         0 |              0 |              0 |         300000 |  0.00176443  | 0.995321 |  -4.95596 |  8.10367 |     36333 |
| train      | xmeas_39  | float32 |         0 |              0 |              0 |         300000 |  0.00450897  | 0.999539 |  -5.3715  |  5.39579 |     37537 |
| train      | xmeas_40  | float32 |         0 |              0 |              0 |         300000 |  0.000424023 | 0.99848  |  -6.40782 |  5.5803  |      4341 |
| train      | xmeas_41  | float32 |         0 |              0 |              0 |         300000 | -0.00291061  | 0.998339 |  -5.35553 |  5.55926 |      4617 |
| train      | xmv_1     | float32 |         0 |              0 |              0 |         300000 | -0.00187234  | 0.996281 |  -6.06575 | 11.3434  |     12727 |
| train      | xmv_2     | float32 |         0 |              0 |              0 |         300000 | -0.00318502  | 0.990538 |  -4.06987 |  9.0132  |     17109 |
| train      | xmv_3     | float32 |         0 |              0 |              0 |         300000 | -0.00148707  | 0.997737 |  -1.51676 |  3.49307 |     54138 |
| train      | xmv_4     | float32 |         0 |              0 |              0 |         300000 | -0.00204031  | 0.996402 |  -8.76365 |  5.11917 |     28560 |
| train      | xmv_5     | float32 |         0 |              0 |              0 |         300000 | -0.0015362   | 0.992765 |  -2.13469 |  7.16242 |     21238 |
| train      | xmv_6     | float32 |         0 |              0 |              0 |         300000 | -0.00193745  | 0.992537 |  -3.16727 |  4.49358 |     44048 |
| train      | xmv_7     | float32 |         0 |              0 |              0 |         300000 | -0.00275861  | 1.00068  |  -4.75224 |  4.66041 |     17038 |
| train      | xmv_8     | float32 |         0 |              0 |              0 |         300000 |  0.000655982 | 0.999069 |  -4.88452 |  5.01869 |     13997 |
| train      | xmv_9     | float32 |         0 |              0 |              0 |         300000 |  0.000159394 | 0.994432 |  -2.95852 |  2.90464 |     57358 |
| train      | xmv_10    | float32 |         0 |              0 |              0 |         300000 |  0.000954244 | 0.999356 |  -4.32797 |  5.99165 |     26224 |
| train      | xmv_11    | float32 |         0 |              0 |              0 |         300000 |  0.000797482 | 1.00057  |  -3.67882 | 15.8613  |     20380 |
| validation | xmeas_1   | float32 |         0 |              0 |              0 |         300000 | -0.0045623   | 0.99366  |  -1.81346 |  5.16034 |     56281 |
| validation | xmeas_2   | float32 |         0 |              0 |              0 |         300000 |  0.000747395 | 1.0083   |  -6.85466 |  5.07679 |      3350 |
| validation | xmeas_3   | float32 |         0 |              0 |              0 |         300000 |  0.00508743  | 0.989913 |  -7.68412 |  5.68128 |      8671 |
| validation | xmeas_4   | float32 |         0 |              0 |              0 |         300000 |  0.00812537  | 1.02041  |  -6.97993 |  7.8634  |     18490 |
| validation | xmeas_5   | float32 |         0 |              0 |              0 |         300000 | -0.00131552  | 0.997696 |  -5.78962 |  6.69669 |      2211 |
| validation | xmeas_6   | float32 |         0 |              0 |              0 |         300000 |  0.00683101  | 1.01231  |  -7.17104 |  7.31641 |      2837 |
| validation | xmeas_7   | float32 |         0 |              0 |              0 |         300000 | -0.00462064  | 0.998476 |  -3.60607 |  3.75269 |      4590 |
| validation | xmeas_8   | float32 |         0 |              0 |              0 |         300000 | -0.00730113  | 1.00499  |  -9.16189 |  8.45224 |     11390 |
| validation | xmeas_9   | float32 |         0 |              0 |              0 |         300000 |  0.00136791  | 0.999018 | -10.8014  |  7.43118 |       131 |
| validation | xmeas_10  | float32 |         0 |              0 |              0 |         300000 | -0.002346    | 0.992612 |  -3.54178 |  5.57926 |     30150 |
| validation | xmeas_11  | float32 |         0 |              0 |              0 |         300000 |  0.00437917  | 0.993165 |  -5.9128  |  4.10072 |     10070 |
| validation | xmeas_12  | float32 |         0 |              0 |              0 |         300000 | -0.00124301  | 1.00122  |  -4.28673 |  4.65229 |      6469 |
| validation | xmeas_13  | float32 |         0 |              0 |              0 |         300000 | -0.00420128  | 0.999155 |  -3.8432  |  3.94882 |      4729 |
| validation | xmeas_14  | float32 |         0 |              0 |              0 |         300000 |  0.00465475  | 0.99084  |  -4.648   |  6.48972 |      7085 |
| validation | xmeas_15  | float32 |         0 |              0 |              0 |         300000 | -0.000524833 | 1.00171  |  -4.51839 |  4.9465  |      6596 |
| validation | xmeas_16  | float32 |         0 |              0 |              0 |         300000 | -0.00568615  | 0.995361 |  -2.89828 |  4.30728 |      4530 |
| validation | xmeas_17  | float32 |         0 |              0 |              0 |         300000 |  0.00269029  | 0.99438  |  -4.79032 |  5.69892 |      4494 |
| validation | xmeas_18  | float32 |         0 |              0 |              0 |         300000 | -0.00387655  | 0.996054 |  -6.53648 |  4.71825 |     14464 |
| validation | xmeas_19  | float32 |         0 |              0 |              0 |         300000 | -0.00576008  | 0.994174 |  -3.65627 |  3.25571 |     32655 |
| validation | xmeas_20  | float32 |         0 |              0 |              0 |         300000 |  0.00808606  | 1.00387  |  -8.25365 |  4.8641  |      8145 |
| validation | xmeas_21  | float32 |         0 |              0 |              0 |         300000 | -0.00445857  | 1.00593  | -11.381   |  4.17967 |      9788 |
| validation | xmeas_22  | float32 |         0 |              0 |              0 |         300000 |  0.0149153   | 0.96418  |  -9.87308 |  4.0155  |      9612 |
| validation | xmeas_23  | float32 |         0 |              0 |              0 |         300000 |  0.00823576  | 0.998691 |  -4.92827 |  3.94511 |     11065 |
| validation | xmeas_24  | float32 |         0 |              0 |              0 |         300000 | -0.00342333  | 1.00572  |  -6.135   |  5.69972 |     16802 |
| validation | xmeas_25  | float32 |         0 |              0 |              0 |         300000 | -0.00619631  | 0.992255 |  -4.13408 |  4.96918 |     11000 |
| validation | xmeas_26  | float32 |         0 |              0 |              0 |         300000 | -0.00213802  | 1.00549  |  -6.29841 |  6.93463 |      9848 |
| validation | xmeas_27  | float32 |         0 |              0 |              0 |         300000 | -0.00662166  | 1.01423  |  -6.85206 |  7.62569 |      8692 |
| validation | xmeas_28  | float32 |         0 |              0 |              0 |         300000 |  0.0063621   | 0.996738 |  -5.70158 |  4.10766 |      9241 |
| validation | xmeas_29  | float32 |         0 |              0 |              0 |         300000 |  0.00914216  | 0.998491 |  -4.75511 |  3.95025 |     14672 |
| validation | xmeas_30  | float32 |         0 |              0 |              0 |         300000 | -0.0018032   | 1.00239  |  -5.95665 |  6.10152 |      2991 |
| validation | xmeas_31  | float32 |         0 |              0 |              0 |         300000 | -0.00659431  | 0.991088 |  -4.0662  |  4.89053 |     14434 |
| validation | xmeas_32  | float32 |         0 |              0 |              0 |         300000 |  0.000121942 | 1.00738  |  -6.285   |  8.32741 |     15733 |
| validation | xmeas_33  | float32 |         0 |              0 |              0 |         300000 | -0.00681105  | 1.01228  |  -6.41994 |  7.78202 |     10968 |
| validation | xmeas_34  | float32 |         0 |              0 |              0 |         300000 |  0.0069449   | 0.99629  |  -5.49374 |  4.26867 |     10400 |
| validation | xmeas_35  | float32 |         0 |              0 |              0 |         300000 |  0.00394645  | 0.994905 |  -4.48975 |  4.56366 |     20027 |
| validation | xmeas_36  | float32 |         0 |              0 |              0 |         300000 |  0.00619272  | 0.995597 |  -4.96071 |  4.41004 |     12577 |
| validation | xmeas_37  | float32 |         0 |              0 |              0 |         300000 |  0.00301097  | 0.998601 |  -4.08191 |  4.16824 |     60564 |
| validation | xmeas_38  | float32 |         0 |              0 |              0 |         300000 | -0.00644765  | 1.00561  |  -4.70147 |  9.66552 |     30615 |
| validation | xmeas_39  | float32 |         0 |              0 |              0 |         300000 |  0.00220946  | 1.00013  |  -5.25818 |  4.85752 |     32977 |
| validation | xmeas_40  | float32 |         0 |              0 |              0 |         300000 | -0.0100463   | 1.00115  |  -5.44526 |  5.08094 |      4125 |
| validation | xmeas_41  | float32 |         0 |              0 |              0 |         300000 |  0.00747306  | 0.999274 |  -5.26655 |  4.94958 |      4413 |
| validation | xmv_1     | float32 |         0 |              0 |              0 |         300000 |  0.00576852  | 1.06346  |  -4.76566 | 11.3434  |     11932 |
| validation | xmv_2     | float32 |         0 |              0 |              0 |         300000 |  0.010408    | 1.04049  |  -4.51411 |  9.0132  |     16432 |
| validation | xmv_3     | float32 |         0 |              0 |              0 |         300000 | -0.00811088  | 0.992336 |  -1.51376 |  3.49257 |     54027 |
| validation | xmv_4     | float32 |         0 |              0 |              0 |         300000 |  0.0056878   | 1.00902  |  -4.55017 |  5.11917 |     28075 |
| validation | xmv_5     | float32 |         0 |              0 |              0 |         300000 | -0.00201751  | 0.997509 |  -2.13524 |  7.15964 |     20773 |
| validation | xmv_6     | float32 |         0 |              0 |              0 |         300000 | -0.00277709  | 0.996191 |  -3.16727 |  4.47971 |     42969 |
| validation | xmv_7     | float32 |         0 |              0 |              0 |         300000 | -0.0012444   | 1.00122  |  -4.28672 |  4.65193 |     17074 |
| validation | xmv_8     | float32 |         0 |              0 |              0 |         300000 | -0.000522544 | 1.00171  |  -4.51773 |  4.94618 |     13991 |
| validation | xmv_9     | float32 |         0 |              0 |              0 |         300000 | -0.0124364   | 0.993465 |  -2.95893 |  2.90755 |     56515 |
| validation | xmv_10    | float32 |         0 |              0 |              0 |         300000 |  0.00490629  | 0.994963 |  -4.31848 |  5.99986 |     26382 |
| validation | xmv_11    | float32 |         0 |              0 |              0 |         300000 | -0.0156232   | 0.938609 |  -3.67867 | 15.8594  |     19542 |
| test       | xmeas_1   | float32 |         0 |              0 |              0 |         300000 | -0.0303652   | 0.94517  |  -1.82078 |  5.16582 |     49315 |
| test       | xmeas_2   | float32 |         0 |              0 |              0 |         300000 |  0.029636    | 1.00521  |  -6.66483 |  4.89633 |      3259 |
| test       | xmeas_3   | float32 |         0 |              0 |              0 |         300000 |  0.0331111   | 0.973563 |  -8.26162 |  5.62426 |      8322 |
| test       | xmeas_4   | float32 |         0 |              0 |              0 |         300000 |  0.0532224   | 1.04587  |  -7.10762 |  7.9877  |     17631 |
| test       | xmeas_5   | float32 |         0 |              0 |              0 |         300000 | -0.00101606  | 0.983007 |  -5.96274 |  6.35045 |      2183 |
| test       | xmeas_6   | float32 |         0 |              0 |              0 |         300000 |  0.0363658   | 1.01723  |  -6.87296 |  6.50549 |      2863 |
| test       | xmeas_7   | float32 |         0 |              0 |              0 |         300000 |  0.0267049   | 1.04317  |  -3.63844 |  3.75134 |      4364 |
| test       | xmeas_8   | float32 |         0 |              0 |              0 |         300000 | -0.0217714   | 0.957706 |  -9.32202 |  9.00128 |     10714 |
| test       | xmeas_9   | float32 |         0 |              0 |              0 |         300000 | -4.90862e-05 | 0.935901 | -10.5209  |  7.57143 |       128 |
| test       | xmeas_10  | float32 |         0 |              0 |              0 |         300000 | -0.0242737   | 0.941561 |  -3.50267 |  5.57962 |     27488 |
| test       | xmeas_11  | float32 |         0 |              0 |              0 |         300000 | -0.0214039   | 1.01174  |  -5.9037  |  4.24405 |      9965 |
| test       | xmeas_12  | float32 |         0 |              0 |              0 |         300000 | -0.00479216  | 0.995676 |  -4.2548  |  4.35196 |      6440 |
| test       | xmeas_13  | float32 |         0 |              0 |              0 |         300000 |  0.0300183   | 1.04905  |  -3.89675 |  3.95418 |      4561 |
| test       | xmeas_14  | float32 |         0 |              0 |              0 |         300000 | -0.0184464   | 1.00619  |  -4.68885 |  5.7072  |      7026 |
| test       | xmeas_15  | float32 |         0 |              0 |              0 |         300000 | -0.00638104  | 0.994015 |  -5.54387 |  4.7414  |      6516 |
| test       | xmeas_16  | float32 |         0 |              0 |              0 |         300000 |  0.0156537   | 1.01517  |  -2.93729 |  4.32028 |      4374 |
| test       | xmeas_17  | float32 |         0 |              0 |              0 |         300000 | -0.00687989  | 0.998471 |  -5.26233 |  5.2161  |      4424 |
| test       | xmeas_18  | float32 |         0 |              0 |              0 |         300000 |  0.00145246  | 0.921394 |  -6.79405 |  4.58617 |     13762 |
| test       | xmeas_19  | float32 |         0 |              0 |              0 |         300000 |  0.0103075   | 0.981748 |  -3.64846 |  3.25085 |     30635 |
| test       | xmeas_20  | float32 |         0 |              0 |              0 |         300000 |  0.0582146   | 1.0167   |  -8.20262 |  5.12015 |      8124 |
| test       | xmeas_21  | float32 |         0 |              0 |              0 |         300000 | -0.00839939  | 0.959869 | -11.2548  |  3.92715 |      9342 |
| test       | xmeas_22  | float32 |         0 |              0 |              0 |         300000 |  0.0285438   | 0.91196  |  -9.74887 |  4.10238 |      8718 |
| test       | xmeas_23  | float32 |         0 |              0 |              0 |         300000 |  0.0444139   | 1.00312  |  -4.86487 |  4.59877 |     11175 |
| test       | xmeas_24  | float32 |         0 |              0 |              0 |         300000 | -0.0615056   | 1.03338  |  -6.27642 |  5.89525 |     17291 |
| test       | xmeas_25  | float32 |         0 |              0 |              0 |         300000 | -0.000144101 | 0.971661 |  -4.19084 |  4.98793 |     10640 |
| test       | xmeas_26  | float32 |         0 |              0 |              0 |         300000 | -0.0341502   | 1.02731  |  -6.4723  |  5.91095 |     10374 |
| test       | xmeas_27  | float32 |         0 |              0 |              0 |         300000 | -0.0574859   | 1.09017  |  -6.72665 |  7.55387 |      8848 |
| test       | xmeas_28  | float32 |         0 |              0 |              0 |         300000 | -0.00199813  | 1.02995  |  -5.81576 |  4.24095 |     10063 |
| test       | xmeas_29  | float32 |         0 |              0 |              0 |         300000 |  0.0444128   | 1.00634  |  -4.84721 |  4.90187 |     15084 |
| test       | xmeas_30  | float32 |         0 |              0 |              0 |         300000 | -0.0585533   | 1.01702  |  -6.5699  |  7.08622 |      2990 |
| test       | xmeas_31  | float32 |         0 |              0 |              0 |         300000 | -0.00233082  | 0.968372 |  -4.03813 |  4.88478 |     13983 |
| test       | xmeas_32  | float32 |         0 |              0 |              0 |         300000 | -0.049787    | 1.03781  |  -6.20031 |  8.56908 |     18482 |
| test       | xmeas_33  | float32 |         0 |              0 |              0 |         300000 | -0.0574986   | 1.0912   |  -6.40388 |  7.89064 |     11138 |
| test       | xmeas_34  | float32 |         0 |              0 |              0 |         300000 | -0.00021029  | 1.02708  |  -5.56958 |  3.9647  |      9886 |
| test       | xmeas_35  | float32 |         0 |              0 |              0 |         300000 | -0.0237898   | 1.01041  |  -4.58491 |  4.63474 |     20276 |
| test       | xmeas_36  | float32 |         0 |              0 |              0 |         300000 | -0.0128482   | 0.999758 |  -4.9354  |  4.24667 |     12758 |
| test       | xmeas_37  | float32 |         0 |              0 |              0 |         300000 | -0.013701    | 1.00328  |  -4.28053 |  4.81049 |     77174 |
| test       | xmeas_38  | float32 |         0 |              0 |              0 |         300000 | -0.0488922   | 1.02124  |  -4.95785 |  9.12676 |     36477 |
| test       | xmeas_39  | float32 |         0 |              0 |              0 |         300000 | -0.00618371  | 1.00663  |  -5.44521 |  5.1826  |     38632 |
| test       | xmeas_40  | float32 |         0 |              0 |              0 |         300000 | -0.0388188   | 1.00988  |  -5.81892 |  5.384   |      4455 |
| test       | xmeas_41  | float32 |         0 |              0 |              0 |         300000 |  0.0259641   | 1.01181  |  -5.23689 |  5.71909 |      4741 |
| test       | xmv_1     | float32 |         0 |              0 |              0 |         300000 |  0.171233    | 1.6577   | -10.7681  | 11.3434  |     14935 |
| test       | xmv_2     | float32 |         0 |              0 |              0 |         300000 |  0.079007    | 1.4648   |  -8.98376 |  9.0132  |     18551 |
| test       | xmv_3     | float32 |         0 |              0 |              0 |         300000 | -0.0498322   | 0.950929 |  -1.51509 |  3.49607 |     48329 |
| test       | xmv_4     | float32 |         0 |              0 |              0 |         300000 |  0.0669236   | 1.20328  |  -8.7637  |  5.11917 |     25253 |
| test       | xmv_5     | float32 |         0 |              0 |              0 |         300000 |  0.0264574   | 1.15075  |  -2.13593 |  7.16057 |     19618 |
| test       | xmv_6     | float32 |         0 |              0 |              0 |         300000 | -0.0511622   | 1.02012  |  -3.16727 |  4.43665 |     41768 |
| test       | xmv_7     | float32 |         0 |              0 |              0 |         300000 | -0.00479215  | 0.995677 |  -4.25519 |  4.35221 |     16897 |
| test       | xmv_8     | float32 |         0 |              0 |              0 |         300000 | -0.00638212  | 0.994015 |  -5.54346 |  4.7418  |     13839 |
| test       | xmv_9     | float32 |         0 |              0 |              0 |         300000 | -0.053544    | 0.994611 |  -2.97874 |  2.91163 |     56140 |
| test       | xmv_10    | float32 |         0 |              0 |              0 |         300000 |  0.0106828   | 1.1876   |  -4.35107 |  6.02142 |     26680 |
| test       | xmv_11    | float32 |         0 |              0 |              0 |         300000 |  0.0969632   | 1.67191  |  -3.6791  | 15.8613  |     21445 |

## Critério de liberação

- `PASS`: nenhuma falha crítica foi detectada.
- `WARN`: o benchmark pode prosseguir, mas a advertência deve ser analisada.
- `FAIL`: o benchmark não deve ser executado antes da correção.
