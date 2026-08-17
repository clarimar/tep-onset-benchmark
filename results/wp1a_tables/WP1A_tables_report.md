# WP1A Final Tables

The statistical unit is the complete trajectory `(faultNumber, simulationRun)`.

## Global test performance

|   position | model                |   accuracy |   balanced_accuracy |   precision_macro |   recall_macro |   f1_macro |   f1_weighted |    mcc |   cohen_kappa |   log_loss |   training_time_seconds |   inference_time_seconds |   inference_ms_per_sample |   overall_position |   average_rank |   first_place_rate |
|-----------:|:---------------------|-----------:|--------------------:|------------------:|---------------:|-----------:|--------------:|-------:|--------------:|-----------:|------------------------:|-------------------------:|--------------------------:|-------------------:|---------------:|-------------------:|
|          1 | HistGradientBoosting |     0.6702 |              0.6702 |            0.7746 |         0.6702 |     0.7128 |        0.7128 | 0.6561 |        0.6537 |     1.2739 |                 14.8909 |                   1.5801 |                    0.0075 |                  1 |         2.7069 |             0.139  |
|          2 | Random Forest        |     0.6641 |              0.6641 |            0.7704 |         0.6641 |     0.7081 |        0.7081 | 0.6492 |        0.6473 |     1.8021 |                100.738  |                   3.2537 |                    0.0155 |                  2 |         2.7581 |             0.0633 |
|          3 | Extra Trees          |     0.6585 |              0.6585 |            0.7504 |         0.6585 |     0.6965 |        0.6965 | 0.6432 |        0.6415 |     1.6204 |                 51.2751 |                   4.0496 |                    0.0193 |                  3 |         2.8399 |             0.0706 |
|          4 | Decision Tree        |     0.6086 |              0.6086 |            0.6632 |         0.6086 |     0.633  |        0.633  | 0.5896 |        0.589  |    14.036  |                 53.7633 |                   0.0599 |                    0.0003 |                  4 |         3.7024 |             0.0402 |
|          5 | Logistic Regression  |     0.4237 |              0.4237 |            0.4427 |         0.4237 |     0.4283 |        0.4283 | 0.3961 |        0.3949 |     1.9296 |                 67.8947 |                   0.0284 |                    0.0001 |                  5 |         4.4928 |             0.0131 |
|          6 | Linear SVM           |     0.4193 |              0.4193 |            0.4372 |         0.4193 |     0.4207 |        0.4207 | 0.3919 |        0.3903 |   nan      |                  3.8804 |                   0.0291 |                    0.0001 |                  6 |         4.5    |             0.0192 |

## Average model ranking

|   overall_position | model                |   average_rank |   rank_std |   first_place_count |   first_place_rate |   mean_metric |   median_metric |
|-------------------:|:---------------------|---------------:|-----------:|--------------------:|-------------------:|--------------:|----------------:|
|                  1 | HistGradientBoosting |         2.7069 |     1.1942 |                1459 |             0.139  |        0.6715 |          0.75   |
|                  2 | Random Forest        |         2.7581 |     1.0276 |                 665 |             0.0633 |        0.6654 |          0.7391 |
|                  3 | Extra Trees          |         2.8399 |     1.0671 |                 741 |             0.0706 |        0.6596 |          0.7391 |
|                  4 | Decision Tree        |         3.7024 |     1.2418 |                 422 |             0.0402 |        0.6099 |          0.68   |
|                  5 | Logistic Regression  |         4.4928 |     1.3047 |                 138 |             0.0131 |        0.4246 |          0.375  |
|                  6 | Linear SVM           |         4.5    |     1.3654 |                 202 |             0.0192 |        0.4202 |          0.3478 |

## Pairwise Wilcoxon tests with Holm correction

| model_a              | model_b              |   n_pairs |   mean_a |   mean_b |   mean_difference_a_minus_b |   median_difference_a_minus_b |   wilcoxon_statistic |   p_value_raw |   p_value_holm | significant_holm   |   rank_biserial_a_vs_b | effect_magnitude   | better_model_by_mean   |
|:---------------------|:---------------------|----------:|---------:|---------:|----------------------------:|------------------------------:|---------------------:|--------------:|---------------:|:-------------------|-----------------------:|:-------------------|:-----------------------|
| Decision Tree        | Extra Trees          |     10500 |   0.6099 |   0.6596 |                     -0.0497 |                        0      |          9.32772e+06 |             0 |              0 | True               |                -0.657  | large              | Extra Trees            |
| Decision Tree        | HistGradientBoosting |     10500 |   0.6099 |   0.6715 |                     -0.0616 |                       -0.0435 |          7.77076e+06 |             0 |              0 | True               |                -0.7335 | large              | HistGradientBoosting   |
| Decision Tree        | Linear SVM           |     10500 |   0.6099 |   0.4202 |                      0.1897 |                        0.087  |          8.6262e+06  |             0 |              0 | True               |                 0.7671 | large              | Decision Tree          |
| Decision Tree        | Logistic Regression  |     10500 |   0.6099 |   0.4246 |                      0.1853 |                        0.0833 |          8.13951e+06 |             0 |              0 | True               |                 0.7803 | large              | Decision Tree          |
| Decision Tree        | Random Forest        |     10500 |   0.6099 |   0.6654 |                     -0.0555 |                       -0.0417 |          6.97798e+06 |             0 |              0 | True               |                -0.751  | large              | Random Forest          |
| Extra Trees          | Linear SVM           |     10500 |   0.6596 |   0.4202 |                      0.2394 |                        0.1304 |          4.11127e+06 |             0 |              0 | True               |                 0.9198 | large              | Extra Trees            |
| Extra Trees          | Logistic Regression  |     10500 |   0.6596 |   0.4246 |                      0.235  |                        0.12   |          3.41072e+06 |             0 |              0 | True               |                 0.9337 | large              | Extra Trees            |
| HistGradientBoosting | Linear SVM           |     10500 |   0.6715 |   0.4202 |                      0.2512 |                        0.1538 |          4.05068e+06 |             0 |              0 | True               |                 0.9242 | large              | HistGradientBoosting   |
| HistGradientBoosting | Logistic Regression  |     10500 |   0.6715 |   0.4246 |                      0.2469 |                        0.1364 |          3.40135e+06 |             0 |              0 | True               |                 0.9436 | large              | HistGradientBoosting   |
| Linear SVM           | Random Forest        |     10500 |   0.4202 |   0.6654 |                     -0.2452 |                       -0.1429 |          3.93968e+06 |             0 |              0 | True               |                -0.9269 | large              | Random Forest          |
| Logistic Regression  | Random Forest        |     10500 |   0.4246 |   0.6654 |                     -0.2408 |                       -0.1364 |          3.53101e+06 |             0 |              0 | True               |                -0.9365 | large              | Random Forest          |
| Extra Trees          | HistGradientBoosting |     10500 |   0.6596 |   0.6715 |                     -0.0118 |                        0      |          1.78627e+07 |             0 |              0 | True               |                -0.195  | small              | HistGradientBoosting   |
| Extra Trees          | Random Forest        |     10500 |   0.6596 |   0.6654 |                     -0.0058 |                        0      |          1.54262e+07 |             0 |              0 | True               |                -0.148  | small              | Random Forest          |
| HistGradientBoosting | Random Forest        |     10500 |   0.6715 |   0.6654 |                      0.0061 |                        0      |          1.80219e+07 |             0 |              0 | True               |                 0.1248 | small              | HistGradientBoosting   |
| Linear SVM           | Logistic Regression  |     10500 |   0.4202 |   0.4246 |                     -0.0044 |                        0      |          2.11994e+07 |             0 |              0 | True               |                -0.0599 | negligible         | Logistic Regression    |

## Class-level performance

|   fault_class |   HistGradientBoosting |   Random Forest |   Extra Trees |   Decision Tree |   Logistic Regression |   Linear SVM | best_model           |   best_score |   worst_score |   performance_range |
|--------------:|-----------------------:|----------------:|--------------:|----------------:|----------------------:|-------------:|:---------------------|-------------:|--------------:|--------------------:|
|             0 |                 0.2319 |          0.2063 |        0.1614 |          0.1889 |                0.0723 |       0.0809 | HistGradientBoosting |       0.2319 |        0.0723 |              0.1596 |
|             1 |                 0.8208 |          0.8278 |        0.8307 |          0.823  |                0.8282 |       0.8269 | Extra Trees          |       0.8307 |        0.8208 |              0.0099 |
|             2 |                 0.8198 |          0.8265 |        0.8269 |          0.8222 |                0.8245 |       0.8259 | Extra Trees          |       0.8269 |        0.8198 |              0.007  |
|             3 |                 0.403  |          0.2808 |        0.2105 |          0.1764 |                0.0674 |       0.1253 | HistGradientBoosting |       0.403  |        0.0674 |              0.3356 |
|             4 |                 0.8237 |          0.8241 |        0.8337 |          0.7822 |                0.8364 |       0.8403 | Linear SVM           |       0.8403 |        0.7822 |              0.0581 |
|             5 |                 0.8252 |          0.812  |        0.8157 |          0.7576 |                0.8278 |       0.8352 | Linear SVM           |       0.8352 |        0.7576 |              0.0776 |
|             6 |                 0.8212 |          0.8369 |        0.8368 |          0.8364 |                0.8107 |       0.7701 | Random Forest        |       0.8369 |        0.7701 |              0.0668 |
|             7 |                 0.8344 |          0.8368 |        0.8369 |          0.8371 |                0.8368 |       0.8372 | Linear SVM           |       0.8372 |        0.8344 |              0.0027 |
|             8 |                 0.7615 |          0.7817 |        0.779  |          0.6745 |                0.4248 |       0.4197 | Random Forest        |       0.7817 |        0.4197 |              0.362  |
|             9 |                 0.1766 |          0.2348 |        0.2394 |          0.1865 |                0.0854 |       0.2036 | Extra Trees          |       0.2394 |        0.0854 |              0.154  |
|            10 |                 0.6945 |          0.7078 |        0.7023 |          0.5736 |                0.0783 |       0.0429 | Random Forest        |       0.7078 |        0.0429 |              0.6648 |
|            11 |                 0.7051 |          0.677  |        0.6585 |          0.6362 |                0.117  |       0.0405 | HistGradientBoosting |       0.7051 |        0.0405 |              0.6645 |
|            12 |                 0.7575 |          0.7636 |        0.7397 |          0.6429 |                0.2605 |       0.0796 | Random Forest        |       0.7636 |        0.0796 |              0.6841 |
|            13 |                 0.7305 |          0.7419 |        0.7417 |          0.6693 |                0.473  |       0.4382 | Random Forest        |       0.7419 |        0.4382 |              0.3037 |
|            14 |                 0.8146 |          0.8144 |        0.8038 |          0.8138 |                0.0301 |       0.194  | HistGradientBoosting |       0.8146 |        0.0301 |              0.7846 |
|            15 |                 0.2152 |          0.2396 |        0.2638 |          0.177  |                0.0678 |       0.0808 | Extra Trees          |       0.2638 |        0.0678 |              0.1961 |
|            16 |                 0.6853 |          0.6556 |        0.6333 |          0.6003 |                0.0861 |       0.1458 | HistGradientBoosting |       0.6853 |        0.0861 |              0.5992 |
|            17 |                 0.7812 |          0.7763 |        0.7826 |          0.7495 |                0.6959 |       0.5861 | Extra Trees          |       0.7826 |        0.5861 |              0.1964 |
|            18 |                 0.7623 |          0.7551 |        0.7456 |          0.733  |                0.7263 |       0.7238 | HistGradientBoosting |       0.7623 |        0.7238 |              0.0385 |
|            19 |                 0.749  |          0.7355 |        0.7705 |          0.5749 |                0.0763 |       0.0693 | Extra Trees          |       0.7705 |        0.0693 |              0.7013 |
|            20 |                 0.6873 |          0.6389 |        0.6395 |          0.5525 |                0.6911 |       0.6587 | Logistic Regression  |       0.6911 |        0.5525 |              0.1386 |

## Validation versus test

| model                |   n_common_trajectories |   validation_mean |   test_mean |   mean_difference_validation_minus_test |   wilcoxon_statistic |   p_value_raw |   p_value_holm | significant_holm   |   rank_biserial_validation_vs_test | effect_magnitude   |
|:---------------------|------------------------:|------------------:|------------:|----------------------------------------:|---------------------:|--------------:|---------------:|:-------------------|-----------------------------------:|:-------------------|
| Decision Tree        |                    2100 |            0.6794 |      0.609  |                                  0.0704 |               483752 |             0 |              0 | True               |                             0.5627 | large              |
| Extra Trees          |                    2100 |            0.7277 |      0.6581 |                                  0.0696 |               481738 |             0 |              0 | True               |                             0.5641 | large              |
| HistGradientBoosting |                    2100 |            0.7543 |      0.6698 |                                  0.0845 |               370464 |             0 |              0 | True               |                             0.6655 | large              |
| Linear SVM           |                    2100 |            0.4722 |      0.4204 |                                  0.0518 |               609510 |             0 |              0 | True               |                             0.4505 | medium             |
| Logistic Regression  |                    2100 |            0.4741 |      0.4242 |                                  0.0498 |               624338 |             0 |              0 | True               |                             0.4366 | medium             |
| Random Forest        |                    2100 |            0.7365 |      0.6644 |                                  0.0721 |               475272 |             0 |              0 | True               |                             0.57   | large              |

## Statistical summary

| item                             | value                |
|:---------------------------------|:---------------------|
| Analysis status                  | PASS                 |
| Primary split                    | test                 |
| Primary metric                   | trajectory_accuracy  |
| Number of models                 | 6                    |
| Common trajectories              | 10500                |
| Best model by average rank       | HistGradientBoosting |
| Best average rank                | 2.706857142857143    |
| Friedman applicable              | True                 |
| Friedman statistic               | 15455.653919591054   |
| Friedman p-value                 | 0.0                  |
| Friedman significant             | True                 |
| Kendall's W                      | 0.29439340799221053  |
| Alpha                            | 0.05                 |
| Significant pairwise comparisons | 15                   |
| Total pairwise comparisons       | 15                   |
