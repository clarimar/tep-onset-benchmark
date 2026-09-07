# ISA Transactions — submission package

Three files go to the system separately. Only the manuscript is blinded.

---

## 1. Highlights (anonymized — upload as a separate file)

Five items, each under 85 characters, as required.

```
TEP fault injection at sample 161 caps literal-label recall at 0.833 per fault class
Rescoring the frozen model post-onset raises macro-F1 from 0.720 to 0.805
The apparent validation-to-test gap of +0.048 becomes -0.013 under symmetric labeling
Seven classifiers gain 0.142-0.150 in relative accuracy, near a 0.159 structural bound
Faults 3, 9, 15 and normal operation remain confounded after the artifact is removed
```

Character counts: 84, 73, 85, 86, 84. The fourth is two over — if the system
rejects it, drop "structural": `Seven classifiers gain 0.142-0.150 in relative
accuracy, near a 0.159 bound` (75).

No author, institution or repository name appears in any item.

---

## 2. Title page (NOT blinded — separate file)

**Title**

Fault-Onset Labeling Bounds Reported Accuracy in the Tennessee Eastman
Benchmark: A Leakage-Controlled Study of Six Classical Classifiers

**Authors**

Alexandre Coelho ^a, Rodrigo de Souza Ruzzi ^a, Clarimar José Coelho ^b,*

^a Klug Automação, Av. Dep. José Alves dos Santos 2998, Jardim Petrópolis,
87083-250, Maringá, Paraná, Brazil
^b Scientific Computing Laboratory, School of Polytechnic and Arts,
Pontifical Catholic University of Goiás, Goiânia, Goiás, Brazil

\* Corresponding author.
E-mail: [preencher]
ORCID: 0000-0002-5163-2986 (C. J. Coelho)

> ORCIDs de Alexandre Coelho e Rodrigo de Souza Ruzzi ainda em branco.
> Confirme também se o endereço da Klug é o mesmo para os dois autores.

**Acknowledgments**

The authors acknowledge the students and researchers associated with the
MEI0028 Modeling and Simulation activities and the Scientific Computing
Laboratory at the Pontifical Catholic University of Goiás.

> Fill in the Klug Automação address, the ORCIDs of the first two authors, and
> the corresponding author's e-mail. I left them blank rather than guess.
> Confirm also that Clarimar is the corresponding author — as last author and
> submitter it is the natural choice, but it is your call.

---

## 3. Cover letter

> Dear Editor-in-Chief,
>
> We submit for your consideration the manuscript "Fault-Onset Labeling Bounds
> Reported Accuracy in the Tennessee Eastman Benchmark: A Leakage-Controlled
> Study of Six Classical Classifiers".
>
> The Tennessee Eastman Process is among the most widely used benchmarks for
> fault detection and diagnosis. In both the original distribution and the
> expanded simulation dataset, each fault is injected after a fixed warm-up
> interval: sample 21 of 500 in development runs, sample 161 of 960 in test
> runs. Observations preceding the injection therefore carry a fault label
> while describing nominal operation. We show that this convention bounds what
> any observation-level classifier can report, and that its treatment is not
> standardized across published work.
>
> Under literal labeling the recall of every fault class is capped at
> 800/960 = 0.8333; faults 6 and 7 attain 0.8333 and 0.8332, the ceiling
> itself. Rescoring a frozen XGBoost model over the complete official test
> partition of 10.08 million observations, with no refitting, raises macro-F1
> from 0.7200 to 0.8054, accuracy from 0.6754 to 0.7949 and MCC from 0.6621 to
> 0.7852. Applying the same protocol to the validation partition turns an
> apparent validation-to-test generalization gap of +0.0483 in macro-F1 into
> -0.0125, indicating that the reported gap reflects the difference in
> mislabeled fraction between the two partitions rather than a loss of
> generalization.
>
> The effect is a property of the labeling convention rather than of any
> estimator. Across seven classifiers spanning a single decision tree, four
> ensembles and two linear baselines, the relative accuracy gain falls between
> 0.142 and 0.150 against a structural bound of 0.1587 derived from the
> retained fraction of the partition. For calibration of its practical weight:
> quadrupling the training data from the size used in the frozen fit gains
> 0.0086 in post-onset macro-F1, while changing the labeling convention on a
> single fixed model changes it by 0.0854.
>
> We also document that three studies on the same simulator adopt three
> different conventions -- relabeling the pre-onset segment as normal,
> retaining it under the fault label, and not addressing it -- and we offer a
> structural explanation: in binary detection the pre-onset segment has a
> natural destination in the normal class, and the false-alarm rate is defined
> over precisely that segment, whereas in multiclass diagnosis the same move
> alters the prior of the normal condition and the distinction disappears
> without being posed as a choice.
>
> Faults 3, 9 and 15 and normal operation remain mutually confounded after the
> correction, consistent with their long-documented weak observability, which
> separates a genuine limitation of the measurements from an artifact of the
> labels.
>
> The benchmark underlying these results follows a leakage-controlled protocol:
> partitioning by complete simulation runs, standardization fitted on training
> data only, hyperparameter selection isolated from the test partition,
> five-seed repeated validation with Friedman and Nemenyi analysis, and a
> single frozen evaluation. All code, split manifests, frozen hyperparameters,
> predictions and metrics are deposited in a public archive; the repository URL
> and its DOI are withheld from the anonymized manuscript and can be released
> to the editorial office on request.
>
> We believe the work fits the scope of ISA Transactions in fault detection and
> diagnosis and in the evaluation of data-driven monitoring methods. Two of the
> authors work in industrial automation, and Section 5.3 addresses what the
> result means for practitioners who rely on benchmark figures when specifying
> diagnostic systems.
>
> The manuscript is original, has not been published elsewhere and is not under
> consideration by another journal. All authors have approved the submission
> and declare no competing interests.
>
> Sincerely,
>
> Clarimar José Coelho, on behalf of the authors
> [e-mail]

## 4. Before uploading

- [ ] Fill the two remaining `\TBD{}` markers: learning curve, anonymous DOI
- [ ] Create the **anonymous** Zenodo deposit for review (no author names);
      keep the GitHub repository for the accepted version
- [ ] Recompile so no red `[TBD: ...]` text survives in the PDF
- [ ] Check the PDF for any residual identifying string:
      `pdftotext main_isa_blind.pdf - | grep -iE "clarimar|goias|klug|puc|github"`
- [ ] Select the Associate Editor whose interests match fault detection and
      diagnosis; use the Editor-in-Chief if unsure
- [ ] Confirm CAPES–Elsevier eligibility for ISA Transactions and for your
      institution before the open-access step
