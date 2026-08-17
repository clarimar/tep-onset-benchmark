# WP1A Statistical Analysis

- Primary split: `test`
- Primary metric: `trajectory_accuracy`
- Alpha: `0.05`
- Experimental unit: `(faultNumber, simulationRun)` trajectory

## Descriptive statistics

| split   | model                  | metric              |   n_trajectories |     mean |      std |   median |        q1 |       q3 |   minimum |   maximum |   mean_ci_low |   mean_ci_high |   median_ci_low |   median_ci_high |
|:--------|:-----------------------|:--------------------|-----------------:|---------:|---------:|---------:|----------:|---------:|----------:|----------:|--------------:|---------------:|----------------:|-----------------:|
| test    | decision_tree          | trajectory_accuracy |            10500 | 0.609901 | 0.248839 | 0.68     | 0.481111  | 0.8      |         0 |         1 |      0.605219 |       0.614589 |        0.666667 |         0.681818 |
| test    | extra_trees            | trajectory_accuracy |            10500 | 0.659639 | 0.245363 | 0.73913  | 0.571429  | 0.833333 |         0 |         1 |      0.655069 |       0.664368 |        0.736842 |         0.75     |
| test    | hist_gradient_boosting | trajectory_accuracy |            10500 | 0.671459 | 0.23349  | 0.75     | 0.6       | 0.833333 |         0 |         1 |      0.666943 |       0.675967 |      nan        |       nan        |
| test    | linear_svm             | trajectory_accuracy |            10500 | 0.420226 | 0.335829 | 0.347826 | 0.0952381 | 0.769231 |         0 |         1 |      0.413674 |       0.426686 |      nan        |       nan        |
| test    | logistic_regression    | trajectory_accuracy |            10500 | 0.424601 | 0.347059 | 0.375    | 0.0769231 | 0.782609 |         0 |         1 |      0.418177 |       0.431332 |      nan        |       nan        |
| test    | random_forest          | trajectory_accuracy |            10500 | 0.665401 | 0.236911 | 0.73913  | 0.583333  | 0.833333 |         0 |         1 |      0.660562 |       0.669755 |        0.736842 |         0.75     |

## Friedman test

```json
{
  "applicable": true,
  "statistic": 15455.653919591054,
  "p_value": 0.0,
  "alpha": 0.05,
  "significant": true,
  "kendalls_w": 0.29439340799221053,
  "n_models": 6,
  "n_trajectories": 10500
}
```

## Average model ranking

|   overall_position | model                  |   average_rank |   rank_std |   first_place_count |   first_place_rate |   mean_metric |   median_metric |
|-------------------:|:-----------------------|---------------:|-----------:|--------------------:|-------------------:|--------------:|----------------:|
|                  1 | hist_gradient_boosting |        2.70686 |    1.19416 |                1459 |          0.138952  |      0.671459 |        0.75     |
|                  2 | random_forest          |        2.75814 |    1.02765 |                 665 |          0.0633333 |      0.665401 |        0.73913  |
|                  3 | extra_trees            |        2.83986 |    1.06707 |                 741 |          0.0705714 |      0.659639 |        0.73913  |
|                  4 | decision_tree          |        3.70243 |    1.24179 |                 422 |          0.0401905 |      0.609901 |        0.68     |
|                  5 | logistic_regression    |        4.49276 |    1.3047  |                 138 |          0.0131429 |      0.424601 |        0.375    |
|                  6 | linear_svm             |        4.49995 |    1.36538 |                 202 |          0.0192381 |      0.420226 |        0.347826 |

## Pairwise Wilcoxon tests with Holm correction

| model_a                | model_b                |   n_pairs |   mean_a |   mean_b |   mean_difference_a_minus_b |   median_difference_a_minus_b |   wilcoxon_statistic |   p_value_raw |   rank_biserial_a_vs_b | effect_magnitude   | better_model_by_mean   |   p_value_holm | significant_holm   |   alpha |
|:-----------------------|:-----------------------|----------:|---------:|---------:|----------------------------:|------------------------------:|---------------------:|--------------:|-----------------------:|:-------------------|:-----------------------|---------------:|:-------------------|--------:|
| decision_tree          | extra_trees            |     10500 | 0.609901 | 0.659639 |                 -0.0497376  |                     0         |          9.32772e+06 |   0           |             -0.657028  | large              | extra_trees            |    0           | True               |    0.05 |
| decision_tree          | hist_gradient_boosting |     10500 | 0.609901 | 0.671459 |                 -0.0615581  |                    -0.0434783 |          7.77076e+06 |   0           |             -0.733531  | large              | hist_gradient_boosting |    0           | True               |    0.05 |
| decision_tree          | linear_svm             |     10500 | 0.609901 | 0.420226 |                  0.189675   |                     0.0869565 |          8.6262e+06  |   0           |              0.767139  | large              | decision_tree          |    0           | True               |    0.05 |
| decision_tree          | logistic_regression    |     10500 | 0.609901 | 0.424601 |                  0.1853     |                     0.0833333 |          8.13951e+06 |   0           |              0.7803    | large              | decision_tree          |    0           | True               |    0.05 |
| decision_tree          | random_forest          |     10500 | 0.609901 | 0.665401 |                 -0.0555003  |                    -0.0416667 |          6.97798e+06 |   0           |             -0.750984  | large              | random_forest          |    0           | True               |    0.05 |
| extra_trees            | linear_svm             |     10500 | 0.659639 | 0.420226 |                  0.239413   |                     0.130435  |          4.11127e+06 |   0           |              0.919787  | large              | extra_trees            |    0           | True               |    0.05 |
| extra_trees            | logistic_regression    |     10500 | 0.659639 | 0.424601 |                  0.235038   |                     0.12      |          3.41072e+06 |   0           |              0.933732  | large              | extra_trees            |    0           | True               |    0.05 |
| hist_gradient_boosting | linear_svm             |     10500 | 0.671459 | 0.420226 |                  0.251233   |                     0.153846  |          4.05068e+06 |   0           |              0.924155  | large              | hist_gradient_boosting |    0           | True               |    0.05 |
| hist_gradient_boosting | logistic_regression    |     10500 | 0.671459 | 0.424601 |                  0.246858   |                     0.136364  |          3.40135e+06 |   0           |              0.943598  | large              | hist_gradient_boosting |    0           | True               |    0.05 |
| linear_svm             | random_forest          |     10500 | 0.420226 | 0.665401 |                 -0.245176   |                    -0.142857  |          3.93968e+06 |   0           |             -0.926857  | large              | random_forest          |    0           | True               |    0.05 |
| logistic_regression    | random_forest          |     10500 | 0.424601 | 0.665401 |                 -0.2408     |                    -0.136364  |          3.53101e+06 |   0           |             -0.936497  | large              | random_forest          |    0           | True               |    0.05 |
| extra_trees            | hist_gradient_boosting |     10500 | 0.659639 | 0.671459 |                 -0.0118205  |                     0         |          1.78627e+07 |   3.20503e-24 |             -0.194968  | small              | hist_gradient_boosting |    1.28201e-23 | True               |    0.05 |
| extra_trees            | random_forest          |     10500 | 0.659639 | 0.665401 |                 -0.0057627  |                     0         |          1.54262e+07 |   9.62287e-13 |             -0.14798   | small              | random_forest          |    2.88686e-12 | True               |    0.05 |
| hist_gradient_boosting | random_forest          |     10500 | 0.671459 | 0.665401 |                  0.00605782 |                     0         |          1.80219e+07 |   4.13127e-12 |              0.124752  | small              | hist_gradient_boosting |    8.26253e-12 | True               |    0.05 |
| linear_svm             | logistic_regression    |     10500 | 0.420226 | 0.424601 |                 -0.00437522 |                     0         |          2.11994e+07 |   2.70396e-07 |             -0.0598526 | negligible         | logistic_regression    |    2.70396e-07 | True               |    0.05 |