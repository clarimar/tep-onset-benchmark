# WP1A — Critical Difference Analysis

- Split: `test`
- Metric: `trajectory_accuracy`
- Models: 6
- Common trajectories: 10500
- Friedman statistic: 15455.653920
- Friedman p-value: 0.000000e+00
- Kendall's W: 0.294393
- Critical difference: 0.073579
- Nemenyi significant comparisons: 13/15

## Average ranks

| Position | Model | Average rank |
|---:|---|---:|
| 1 | HistGradientBoosting | 2.706857 |
| 2 | Random Forest | 2.758143 |
| 3 | Extra Trees | 2.839857 |
| 4 | Decision Tree | 3.702429 |
| 5 | Logistic Regression | 4.492762 |
| 6 | Linear SVM | 4.499952 |

## Maximal nonsignificant groups

| Group | Models | Rank span |
|---:|---|---:|
| 1 | HistGradientBoosting | Random Forest | 0.051286 |
| 2 | Logistic Regression | Linear SVM | 0.007190 |

## Interpretation note

The Friedman test evaluates the global null hypothesis of equal model performance across paired trajectories. The Nemenyi procedure then compares average ranks while controlling the family-wise error rate for all pairwise comparisons. A rank difference greater than the critical difference indicates significance at the selected alpha.

The previously generated Holm-corrected Wilcoxon analysis remains the primary pairwise effect-oriented analysis. Nemenyi is included here mainly to support the conventional critical-difference visualization.