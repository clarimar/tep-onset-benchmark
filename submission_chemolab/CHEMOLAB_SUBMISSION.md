# Chemometrics and Intelligent Laboratory Systems — submission package

Confirmed against the journal's guide for authors (18 Nov 2026):

| Requirement | Journal | Ours | Status |
|---|---|---|---|
| Peer review | **single anonymized** | authors named in the PDF | OK — no blinding needed |
| Abstract | ≤ 250 words | 216 | OK |
| Keywords | 1–7, no "and"/"of" | 6, none | OK |
| Highlights | 3–5 bullets, ≤ 85 chars | 5 bullets, max 76 | OK |
| Layout | single column for Word; **double column allowed for LaTeX** | LaTeX, two columns, 15 pp | OK |
| Length | no limit for full articles | 15 pp | OK |
| Title page | required (authors, affiliations, corresponding e-mail) | in the PDF + separate file | OK |

**Single anonymized review is the important finding.** The manuscript keeps the
author block, so `article/main.pdf` is the file to upload. Do not run
`make_elsarticle.py` — that generator strips the authors for double-anonymized
venues and is not needed here.

## Files to upload in Editorial Manager

| Editorial Manager item | File |
|---|---|
| Cover Letter | `cover_letter_chemolab.txt` (paste into the box) |
| Manuscript | `article/main.pdf` |
| LaTeX source | `article/main.tex` + `article/figures/` |
| Highlights | `highlights_chemolab.txt` (name must contain "highlights") |
| Graphical Abstract | `graphical_abstract.pdf` |
| Title Page | `title_page_chemolab.txt` |
| Declaration of Interest | `declaration_of_competing_interests.docx` |

## Assemble the package in the repository

```bash
cd ~/repos/tep-onset-benchmark
mkdir -p submission_chemolab

cp ~/Downloads/main_revised.tex            article/main.tex
cp ~/Downloads/cover_letter_chemolab.txt   submission_chemolab/
cp ~/Downloads/highlights_chemolab.txt     submission_chemolab/
cp ~/Downloads/title_page_chemolab.txt     submission_chemolab/
cp ~/Downloads/abstract_chemolab.txt       submission_chemolab/
cp ~/Downloads/CHEMOLAB_SUBMISSION.md      submission_chemolab/

cd article && pdflatex main.tex && pdflatex main.tex && cd ..
cp article/main.pdf submission_chemolab/main.pdf
pdfinfo submission_chemolab/main.pdf | grep Pages     # expect 15

git add article/main.tex submission_chemolab
git commit -m "Chemolab submission: direct abstract, cover letter, highlights"
git push
```

## In the submission form

- Article type: **Research Paper**
- Declaration of generative AI: the text is in `title_page_chemolab.txt` and in
  the manuscript before the reference list
- Data availability: "Data will be made available on request" is wrong here —
  choose the option that lets you give the repository link, and paste
  `https://github.com/clarimar/tep-onset-benchmark`
- Suggested reviewers: if asked, people who work on TEP benchmarking rather than
  on chemometric calibration

## Honest caveat

Chemolab is a chemometrics journal. The paper uses tree ensembles and linear
baselines, not PCA/PLS. The argument for fit is that the bound is a property of
the data and the scoring rule, so it constrains latent-variable methods on this
benchmark exactly as it constrains ours — and that the journal published the
foundational TEP comparisons (Chiang/Russell/Braatz 2000, both cited). The cover
letter makes that argument explicitly. It is a real argument, not a stretch, but
it is the point an editor may push back on.
