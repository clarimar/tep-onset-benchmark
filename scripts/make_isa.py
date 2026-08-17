#!/usr/bin/env python3
"""Produce the ISA Transactions blinded submission from main_revised.tex."""
import io, re, sys, shutil

src = "article/main.tex"
dst = "submission/main_isa_blind.tex"
shutil.copy(src, dst)
s = io.open(dst, encoding="utf-8").read()
done = []

def sub(old, new, label):
    global s
    if old not in s: print("!! NOT FOUND:", label); sys.exit(1)
    if s.count(old) != 1: print("!! NOT UNIQUE:", label); sys.exit(1)
    s = s.replace(old, new); done.append(label)

# ---- document class: single column, 12pt, Times ---------------------------
sub(r"""\documentclass[10pt,twocolumn,a4paper]{article}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[margin=1.8cm,columnsep=0.65cm]{geometry}""",
r"""% =========================================================================
% ISA Transactions -- BLINDED SUBMISSION
% Single file, 12 pt Times Roman, max 30 pages, double-anonymized.
% Author names, affiliations, acknowledgments and the identifying
% repository URL are removed from this file. They belong in the separate
% title page / cover letter.
% =========================================================================
\documentclass[12pt,a4paper]{article}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{mathptmx}          % Times Roman text and math
\usepackage[margin=2.5cm]{geometry}
\usepackage{setspace}
\onehalfspacing
\usepackage{lineno}
\linenumbers""",
"documentclass")

sub(r"""\usepackage[hidelinks]{hyperref}
\usepackage{balance}""",
r"""\usepackage[hidelinks]{hyperref}""",
"drop balance")

sub(r"""\balance
""", "", "drop balance call") if "\\balance\n" in s else done.append("no balance call")

# ---- table* / figure* have no meaning in one-column layout ----------------
s = s.replace(r"\begin{table*}", r"\begin{table}")
s = s.replace(r"\end{table*}", r"\end{table}")
s = s.replace(r"\begin{figure*}", r"\begin{figure}")
s = s.replace(r"\end{figure*}", r"\end{figure}")
done.append("starred floats -> plain (single column)")

# ---- title and blinded author block --------------------------------------
sub(r"""\title{\Large\textbf{A Reproducible Benchmark of Classical Machine Learning Methods\\
for Fault Diagnosis in the Tennessee Eastman Process}}

\author{Clarimar Jos\'e Coelho\\
\small Scientific Computing Laboratory, School of Polytechnic and Arts\\
\small Pontifical Catholic University of Goi\'as, Goi\^ania, Brazil\\
\small ORCID: 0000-0002-5163-2986}
\date{}""",
r"""\title{\textbf{Fault-Onset Labeling Bounds Reported Accuracy in the Tennessee
Eastman Benchmark: A Leakage-Controlled Study of Six Classical Classifiers}}

\author{}
\date{}""",
"blinded title block")

# ---- singular author -> plural -------------------------------------------
sub(r"""\section*{Acknowledgments}

The author acknowledges the students and researchers associated with the
MEI0028 Modeling and Simulation activities and the Scientific Computing
Laboratory at the Pontifical Catholic University of Goi\'as.

\section*{Conflict of Interest}

The author declares no conflict of interest.""",
r"""% Acknowledgments removed for double-anonymized review.
% Restore in the accepted version.

\section*{Declaration of Competing Interest}

The authors declare that they have no known competing financial interests or
personal relationships that could have appeared to influence the work reported
in this paper.

\section*{CRediT Authorship Contribution Statement}

\textbf{Author 1:} Conceptualization, Methodology, Software, Validation,
Formal analysis, Investigation, Data curation, Writing -- original draft,
Visualization.
\textbf{Author 2:} Methodology, Software, Validation, Investigation,
Writing -- review \& editing.
\textbf{Author 3:} Conceptualization, Methodology, Resources, Writing --
review \& editing, Supervision, Project administration.""",
"declarations + CRediT")

# ---- survey table: too wide for one column at 12 pt -----------------------
# tabela do levantamento: \resizebox no main.tex ja garante o ajuste


# ---- anonymize the repository ---------------------------------------------
sub(r"""\TBD{repository URL} and archived under \TBD{Zenodo DOI}.""",
r"""an anonymized public repository for peer review, \TBD{anonymous Zenodo DOI};
the non-anonymized repository will be cited in the accepted version.""",
"anonymize repository")

io.open(dst, "w", encoding="utf-8").write(s)
print("Wrote", dst)
for d in done: print("  -", d)
print("Remaining TBD:", s.count("\\TBD{") - 1)
