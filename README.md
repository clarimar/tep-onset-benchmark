# Fault-Onset Labeling and Classical ML Benchmarking in the Tennessee Eastman Process

Code, results, and manuscript for a leakage-controlled benchmark of six
classical machine-learning methods for 21-class fault diagnosis in the
Tennessee Eastman Process (TEP), together with an analysis showing that the
fault-onset labeling convention accounts for a large and predictable share of
the reported error.

---

## Main result

Frozen XGBoost, complete official test partition (10,080,000 observations).
The two columns differ **only** in whether the pre-onset segment of each faulty
run is scored. No model is refitted between them.

| Metric | Literal labels (L) | Post-onset labels (P) |
|---|---|---|
| Accuracy | 0.6754 | 0.7949 |
| Balanced accuracy | 0.6754 | 0.8006 |
| Macro-F1 | 0.7200 | 0.8054 |
| MCC | 0.6621 | 0.7852 |

The effect is not specific to this model. Across seven classifiers spanning a
single decision tree, four ensembles, and two linear baselines, the relative
accuracy gain falls between 0.142 and 0.150, against a structural upper bound
of 0.1587.

The apparent validation-to-test generalization gap of +0.0483 in macro-F1
becomes −0.0125 once both partitions are scored under the same convention.

---

## Why the labeling matters

In the expanded TEP data, faults are injected after a fixed warm-up interval:

| Partition | Run length | Fault active from | Mislabeled fraction |
|---|---|---|---|
| Development | 500 samples | sample 21 | 4.0% |
| Official test | 960 samples | sample 161 | 16.7% |

Observations before injection carry a fault label while describing nominal
operation. Under literal labeling this caps the recall of every fault class at
800/960 = 0.8333. Faults 6 and 7 attain 0.8333 and 0.8332 — the ceiling itself.

Because the mislabeled fraction differs between partitions, a metric computed
on development and on test data is not measuring the same quantity.

**Any observation-level result on this dataset should state how the onset
window was treated.**

---

## Data

Not distributed here. Obtain from the original sources:

- Rieth, Amsel, Tran & Cook (2017), Harvard Dataverse,
  [doi:10.7910/DVN/6C3JR1](https://doi.org/10.7910/DVN/6C3JR1)
- CSV conversion:
  [kaggle.com/datasets/afrniomelo/tep-csv](https://www.kaggle.com/datasets/afrniomelo/tep-csv)

Place the four CSV files in `data/raw/` and verify against the SHA-256 hashes
in `data/metadata/tep_download_manifest.json`.

---

## Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Reference environment: Python 3.12.13, scikit-learn 1.9.0, XGBoost 3.4.0, Linux.
Per-run environment records are in the `*_environment.json` files under
`results/`.

---

## Pipeline

See `wp1a/README.md` for the invocation options of each stage.

```bash
# 1. audit the source files and record hashes
python3 scripts/01_audit_data.py

# 2. run-level split manifest (fixed seed)
python3 scripts/02_build_manifest.py

# 3. protocol assertions (test partition must remain untouched)
python3 scripts/03_validate_protocol.py

# 4. hyperparameter tuning: 3 candidates x 6 families
python3 -m wp1a.tune --n-jobs <N>

# 5. repeated validation over seeds 2026-2030
python3 -m wp1a.repeat --n-jobs <N>

# 6. frozen final evaluation on the official test partition
python3 -m wp1a.final_test --n-jobs <N>
```

Record the value of `--n-jobs`: timings are not comparable across stages
without it.

### Onset analysis (no refitting)

Rescores saved predictions under both labeling protocols.

```bash
# test partition (onset at sample 161, the default)
python3 scripts/postonset_analysis.py \
    results/wp1a_definitive/final_test_v2/final_test_predictions.parquet \
    --cols faultNumber,simulationRun,sample,predicted_class \
    --out results/wp1a_onset_analysis

# validation partition (note --onset 21: development runs are 500 samples)
python3 scripts/generate_validation_predictions.py \
    --model results/wp1a_definitive/tuning_v2/candidates/xgboost_1.joblib \
    --data  data/processed/validation.parquet \
    --out   results/wp1a_onset_validation/validation_predictions.parquet
python3 scripts/postonset_analysis.py \
    results/wp1a_onset_validation/validation_predictions.parquet \
    --cols faultNumber,simulationRun,sample,predicted_class \
    --onset 21 --out results/wp1a_onset_validation
```

---

## Layout

```
article/            manuscript (LaTeX + figures + PDF)
wp1a/               pipeline package: tune, repeat, final_test, core, finalize
scripts/            data audit, split manifest, protocol checks, onset analysis
data/
  metadata/         download manifest with SHA-256 hashes
  processed/        split_manifest.csv, preprocessing config
results/
  wp1a_definitive/          tuning, repeated validation, frozen final test
  wp1a_onset_analysis/      post-onset rescoring, test partition
  wp1a_onset_validation/    post-onset rescoring, validation partition
  wp1a_quality_control/     schema, duplicates, trajectory integrity
  wp1a_statistics/          see PROVENANCE.md
  wp1a_cd_diagram/          see PROVENANCE.md
  wp1a_tables/              see PROVENANCE.md
```

Large artifacts are not in git: raw data (5.5 GB), prediction parquets, and the
tuning candidate models (the random forests reach 8.7 GB). The frozen XGBoost
model, 6.8 MB, is included.

**`results/wp1a_statistics/`, `wp1a_cd_diagram/` and `wp1a_tables/` come from an
earlier exploratory experiment, not from the benchmark reported in the
manuscript.** They include an extra-trees model, omit XGBoost, and use test
trajectories as blocks. See the `PROVENANCE.md` file in each. The statistics
reported in the article are computed over the five repeated-validation seeds.

---

## Leakage control

The independent unit is the complete simulation run, never the observation.
8,400 training runs, 2,100 validation runs, 10,500 official test runs; no run
appears in more than one partition. Standardization is fitted on training data
only. The tuning and repeated-validation programs assert at runtime that the
test partition was not read.

---

## Citation

```bibtex
@software{coelho_tep_onset_benchmark,
  author    = {Coelho, Clarimar Jos\'e},
  title     = {Fault-Onset Labeling and Classical ML Benchmarking in the
               Tennessee Eastman Process},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {PLACEHOLDER}
}
```

Cite the concept DOI (all versions), not a version-specific one.

---

## License

Code: MIT. Results and figures: CC BY 4.0. The TEP data are distributed by
their original authors under their own terms.
