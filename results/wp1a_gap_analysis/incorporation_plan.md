# Prioritized Incorporation Plan

This plan is ordered by editorial priority.

## [CRITICAL] Friedman statistical test

- **Category:** statistics
- **Target section:** Results / Statistical analysis
- **Project evidence:** results/wp1a_tables/table_06_statistical_summary.csv; results/wp1a_tables/table_06_statistical_summary.tex; results/wp1a_tables/WP1A_tables_report.md; results/wp1a_tables/tables_manifest.csv; results/wp1a_cd_diagram/cd_analysis_report.md; results/wp1a_cd_diagram/cd_analysis_summary.json; results/wp1a_statistics/class_level_statistics.csv; results/wp1a_statistics/trajectory_metrics.parquet
- **Manuscript evidence:** Not detected
- **Required action:** Report the Friedman test, test statistic, p-value, number of trajectories, and interpretation.

## [CRITICAL] Nemenyi post-hoc comparison

- **Category:** statistics
- **Target section:** Results / Statistical analysis
- **Project evidence:** results/wp1a_tables/tables_manifest.csv; results/wp1a_tables/table_03_pairwise_statistics.tex; results/wp1a_tables/table_03_pairwise_statistics.csv; results/wp1a_cd_diagram/average_ranks_recomputed.csv; results/wp1a_cd_diagram/cd_analysis_report.md; results/wp1a_cd_diagram/nemenyi_significance_matrix.csv; results/wp1a_cd_diagram/nonsignificant_groups.csv; results/wp1a_cd_diagram/critical_difference_diagram.png
- **Manuscript evidence:** Not detected
- **Required action:** Add the Nemenyi post-hoc procedure, corrected pairwise results, critical difference, and significant comparison count.

## [MAJOR] Practical magnitude of model differences

- **Category:** discussion
- **Target section:** Discussion
- **Project evidence:** results/wp1a_tables/table_02_average_model_ranking.csv; results/wp1a_tables/table_01_global_test_performance.csv; results/wp1a_tables/table_01_global_test_performance.tex; results/wp1a_tables/tables_manifest.csv; results/wp1a_tables/table_02_average_model_ranking.tex; results/wp1a_figures/08_performance_vs_cost.png; results/wp1a_figures/figures_manifest.csv; results/wp1a_figures/08_performance_vs_cost.svg
- **Manuscript evidence:** Not detected
- **Required action:** Quantify the absolute and relative performance gaps between the best ensemble, simpler trees, and linear baselines.

## [MAJOR] Training and inference cost analysis

- **Category:** discussion
- **Target section:** Results and Discussion
- **Project evidence:** results/wp1a_benchmark_test/benchmark_summary.csv; results/wp1a_benchmark_test/benchmark_test_ranking.csv; results/wp1a_tables/table_01_global_test_performance.csv; results/wp1a_tables/WP1A_tables_report.md; results/wp1a_figures/07_training_time.svg; results/wp1a_figures/07_training_time.pdf; results/wp1a_figures/08_performance_vs_cost.png; results/wp1a_figures/figures_manifest.csv
- **Manuscript evidence:** Not detected
- **Required action:** Discuss the trade-off between predictive performance, training time, inference cost, and model complexity.

## [MAJOR] Critical Difference diagram

- **Category:** figures
- **Target section:** Results / Figures
- **Project evidence:** results/wp1a_cd_diagram/average_ranks_recomputed.csv; results/wp1a_cd_diagram/cd_analysis_report.md; results/wp1a_cd_diagram/nemenyi_significance_matrix.csv; results/wp1a_cd_diagram/nonsignificant_groups.csv; results/wp1a_cd_diagram/critical_difference_diagram.png; results/wp1a_cd_diagram/cd_analysis_summary.json; results/wp1a_cd_diagram/critical_difference_diagram.pdf; results/wp1a_cd_diagram/nemenyi_pairwise.csv
- **Manuscript evidence:** Not detected
- **Required action:** Include or cite the Critical Difference diagram and explain the groups of statistically indistinguishable models.

## [MAJOR] Class balance and stratified sampling

- **Category:** methodology
- **Target section:** Methods / Sampling
- **Project evidence:** results/wp1a_quality_control/qc_class_distribution.csv; results/audit/tep_class_distribution.csv; results/eda/figures/class_distribution.png; src/13_tcn_benchmark.py; src/13_tcn_benchmark_atualizado.py; src/04_baseline_classificacao_v2.py; src/11_cnn_attention.py; src/08_build_temporal_sequences_v2.py
- **Manuscript evidence:** Not detected
- **Required action:** Report the per-class sampling limits, resulting sample counts, and rationale for balanced macro-level comparison.

## [MAJOR] Data quality-control audit

- **Category:** methodology
- **Target section:** Methods / Data preparation
- **Project evidence:** results/wp1a_quality_control/qc_split_summary.csv; results/wp1a_quality_control/qc_feature_statistics.csv; results/wp1a_quality_control/qc_checks.csv; results/wp1a_quality_control/qc_class_distribution.csv; results/wp1a_quality_control/qc_trajectory_integrity.csv; results/wp1a_quality_control/benchmark_readiness.json; results/wp1a_quality_control/quality_control_summary.json; results/wp1a_quality_control/quality_control_report.md
- **Manuscript evidence:** Not detected
- **Required action:** Summarize the data-quality checks: schema consistency, missing values, duplicates, trajectory integrity, and class coverage.

## [MAJOR] Validation versus test comparison

- **Category:** methodology
- **Target section:** Methods / Experimental protocol
- **Project evidence:** results/wp1a_tables/table_05_validation_test_comparison.csv; results/wp1a_tables/table_05_validation_test_comparison.tex; results/wp1a_tables/tables_manifest.csv; results/wp1a_statistics/validation_test_comparison.csv; results/wp1a_final_package/final_report/wp1a_artifact_inventory.csv; results/wp1a_final_package/wp1a_reproducibility_package/documentation/checksums_sha256.txt; results/wp1a_final_package/wp1a_reproducibility_package/documentation/package_contents.txt; results/wp1a_final_package/wp1a_reproducibility_package/documentation/wp1a_artifact_inventory.csv
- **Manuscript evidence:** Not detected
- **Required action:** Explain how validation guided model selection and how the test partition remained isolated until final evaluation.

## [MAJOR] Code availability statement

- **Category:** reproducibility
- **Target section:** Code Availability Statement
- **Project evidence:** results/wp1a_fault_analysis/experiment_manifest.json; results/EERS_Sprint1/pyproject.toml; results/wp1a_scientific_audit/recommendations.md; results/wp1a_scientific_audit/checklist.tex; results/wp1a_scientific_audit/problems.csv; results/wp1a_scientific_audit/audit_manifest.json; results/wp1a_scientific_audit/checklist.csv; results/EERS_Sprint1/tests/test_latex_parser.py
- **Manuscript evidence:** Not detected
- **Required action:** Add a Code Availability Statement. Use a repository URL when public, or state that code will be released upon acceptance.

## [MAJOR] Data availability statement

- **Category:** reproducibility
- **Target section:** Data Availability Statement
- **Project evidence:** results/eda/dataset_summary.csv; results/eda/eda_report.md; results/eda/class_summary.csv; results/audit/tep_file_audit.csv; results/audit/tep_metadata.json; results/EERS_Sprint1/src/eers/parsers/latex_parser_v0_2.py; src/27_wp1_gap_analysis.py; src/01_auditar_base_tep.py
- **Manuscript evidence:** Not detected
- **Required action:** Add a formal statement identifying the public TEP data source and the exact files used.

## [MAJOR] Reproducibility package

- **Category:** reproducibility
- **Target section:** Data and Code Availability
- **Project evidence:** results/wp1a_final_package/wp1a_reproducibility_package.zip; results/wp1a_article/manuscript_manifest.json; results/wp1a_article_validation/build/manuscript_manifest.json; results/wp1a_final_package/final_report/wp1a_methods_results_draft.md; results/wp1a_final_package/final_report/wp1a_integrity_checks.csv; results/wp1a_final_package/final_report/wp1a_reproducibility_manifest.json; results/wp1a_final_package/final_report/wp1a_artifact_inventory.csv; results/wp1a_final_package/final_report/wp1a_final_scientific_report.md
- **Manuscript evidence:** Not detected
- **Required action:** State that the reproducibility package contains tables, figures, metadata, environment information, and checksums.

## [MAJOR] Software and library versions

- **Category:** reproducibility
- **Target section:** Methods / Computational environment
- **Project evidence:** results/wp1a_benchmark_test/benchmark_environment.json; results/wp1a_fault_analysis/experiment_manifest.json; results/wp1a_benchmark/benchmark_environment.json; results/wp1a_quality_control/quality_control_summary.json; results/EERS_Sprint1/README.md; results/EERS_Sprint1/pyproject.toml; results/wp1a_statistics/statistics_run_summary.json; results/wp1a_scientific_audit/recommendations.md
- **Manuscript evidence:** Not detected
- **Required action:** Report Python and core library versions used in the benchmark.

## [MINOR] Random seed and deterministic settings

- **Category:** reproducibility
- **Target section:** Methods / Reproducibility
- **Project evidence:** results/wp1a_benchmark_test/benchmark_summary.csv; results/wp1a_benchmark_test/benchmark_test_ranking.csv; results/wp1a_benchmark_test/benchmark_environment.json; results/wp1a_benchmark/benchmark_summary.csv; results/wp1a_benchmark/benchmark_test_ranking.csv; results/wp1a_benchmark/benchmark_environment.json; results/cnn1d_test/reports/environment.json; results/EERS_Sprint1/src/eers/parsers/.venv/lib/python3.14/site-packages/numpy/random/tests/test_generator_mt19937.py
- **Manuscript evidence:** Not detected
- **Required action:** Report random_state=42 and any deterministic execution settings.

