# WP1A — Detailed Fault-Level Analysis

## Scope

Input: `/home/clarimar/Dropbox/aulas/ppgeiia/MEI0028/ProjetoA_TEP/results/wp1a_tables/table_04_class_level_performance.csv`

Primary metric: **f1_score**

- Models: **6**
- Faults/classes: **21**
- Model-fault observations: **126**

Class **0** is reported as **Normal Operation**, following the class convention used in this WP1A dataset.

## Main findings

The hardest fault/class was **0** (Normal Operation), with mean f1_score
equal to **0.1570**. The easiest was
**7**, with mean score **0.8365**.

The greatest disagreement among classifiers occurred for
**14**, whose standard deviation was
**0.3650**.

## Hardest faults

```
difficulty_rank fault n_models mean_f1_score median_f1_score std_f1_score min_f1_score max_f1_score range_f1_score cv_f1_score           best_model best_score         worst_model worst_score
         1.0000     0   6.0000        0.1570          0.1752       0.0664       0.0723       0.2319         0.1596      0.4230 HistGradientBoosting     0.2319 Logistic Regression      0.0723
         2.0000    15   6.0000        0.1740          0.1961       0.0825       0.0678       0.2638         0.1960      0.4741          Extra Trees     0.2638 Logistic Regression      0.0678
         3.0000     9   6.0000        0.1877          0.1951       0.0561       0.0854       0.2394         0.1540      0.2988          Extra Trees     0.2394 Logistic Regression      0.0854
         4.0000     3   6.0000        0.2106          0.1935       0.1191       0.0674       0.4030         0.3356      0.5655 HistGradientBoosting     0.4030 Logistic Regression      0.0674
         5.0000    10   6.0000        0.4666          0.6341       0.3186       0.0429       0.7078         0.6649      0.6828        Random Forest     0.7078          Linear SVM      0.0429
         6.0000    16   6.0000        0.4677          0.6168       0.2746       0.0861       0.6853         0.5992      0.5870 HistGradientBoosting     0.6853 Logistic Regression      0.0861
         7.0000    11   6.0000        0.4724          0.6473       0.3067       0.0405       0.7051         0.6646      0.6493 HistGradientBoosting     0.7051          Linear SVM      0.0405
         8.0000    19   6.0000        0.4959          0.6552       0.3350       0.0693       0.7705         0.7012      0.6755          Extra Trees     0.7705          Linear SVM      0.0693
         9.0000    12   6.0000        0.5406          0.6913       0.2959       0.0796       0.7636         0.6840      0.5474        Random Forest     0.7636          Linear SVM      0.0796
        10.0000    14   6.0000        0.5785          0.8088       0.3650       0.0301       0.8146         0.7845      0.6310 HistGradientBoosting     0.8146 Logistic Regression      0.0301
```

## Easiest faults

```
difficulty_rank fault n_models mean_f1_score median_f1_score std_f1_score min_f1_score max_f1_score range_f1_score cv_f1_score           best_model best_score          worst_model worst_score
        21.0000     7   6.0000        0.8365          0.8368       0.0011       0.8344       0.8372         0.0028      0.0013           Linear SVM     0.8372 HistGradientBoosting      0.8344
        20.0000     1   6.0000        0.8262          0.8274       0.0037       0.8208       0.8307         0.0099      0.0044          Extra Trees     0.8307 HistGradientBoosting      0.8208
        19.0000     2   6.0000        0.8243          0.8252       0.0028       0.8198       0.8269         0.0071      0.0034          Extra Trees     0.8269 HistGradientBoosting      0.8198
        18.0000     4   6.0000        0.8234          0.8289       0.0213       0.7822       0.8403         0.0581      0.0258           Linear SVM     0.8403        Decision Tree      0.7822
        17.0000     6   6.0000        0.8187          0.8288       0.0261       0.7701       0.8369         0.0668      0.0319        Random Forest     0.8369           Linear SVM      0.7701
        16.0000     5   6.0000        0.8123          0.8205       0.0281       0.7576       0.8352         0.0776      0.0345           Linear SVM     0.8352        Decision Tree      0.7576
        15.0000    18   6.0000        0.7410          0.7393       0.0158       0.7238       0.7623         0.0385      0.0213 HistGradientBoosting     0.7623           Linear SVM      0.7238
        14.0000    17   6.0000        0.7286          0.7629       0.0772       0.5861       0.7826         0.1965      0.1059          Extra Trees     0.7826           Linear SVM      0.5861
        13.0000    20   6.0000        0.6447          0.6491       0.0504       0.5525       0.6911         0.1386      0.0783  Logistic Regression     0.6911        Decision Tree      0.5525
        12.0000     8   6.0000        0.6402          0.7180       0.1733       0.4197       0.7817         0.3620      0.2707        Random Forest     0.7817           Linear SVM      0.4197
```

## Model summary

```
overall_position                model mean_f1_score median_f1_score std_f1_score min_f1_score max_f1_score worst_fault worst_fault_score best_fault best_fault_score
          1.0000 HistGradientBoosting        0.6715          0.7575       0.2152       0.1766       0.8344           9            0.1766          7           0.8344
          2.0000        Random Forest        0.6654          0.7551       0.2194       0.2063       0.8369           0            0.2063          6           0.8369
          3.0000          Extra Trees        0.6596          0.7456       0.2285       0.1614       0.8369           0            0.1614          7           0.8369
          4.0000        Decision Tree        0.6099          0.6693       0.2311       0.1764       0.8371           3            0.1764          7           0.8371
          5.0000  Logistic Regression        0.4246          0.4248       0.3420       0.0301       0.8368          14            0.0301          7           0.8368
          6.0000           Linear SVM        0.4202          0.4197       0.3293       0.0405       0.8403          11            0.0405          4           0.8403
```

## Warnings

- Wide input interpreted as f1_score; model columns=['HistGradientBoosting', 'Random Forest', 'Extra Trees', 'Decision Tree', 'Logistic Regression', 'Linear SVM']
- Validated the six expected WP1A classifiers.
