# Revised primary dataset: full public sepsis release

The revised main study uses all **40,336** public PhysioNet/CinC 2019 patient files: 20,336 from hospital A and 20,000 from hospital B, totaling 1,552,210 hourly rows. The full release is redistributed in `data/raw/sepsis-public/sepsis-public-full.zip` under the original **CC BY 4.0** license. Source: Reyna et al., [v1.0.0](https://physionet.org/content/challenge-2019/1.0.0/), DOI 10.13026/v64v-d857. File-level source/checksum records are in `full_manifest.json` and `configs/sepsis_full_selection.json`.

Public patient identifiers are benchmark IDs, not newly collected identifiers. SepsisLabel begins six hours before inferred onset. The paper defines incident eligibility, exclusions, retrospective stopping and patient-wise splits explicitly. Consent and reviewer states are simulated and must not be interpreted as observed attributes. No credentialed MIMIC-IV result is included.

The following original data-card text documents the archived initial study and its smaller inputs.

---

# Data access, provenance and limitations

## Inputs used

**PhysioNet/CinC 2019 — REAL OPEN DATA.** Reyna et al., DOI 10.13026/v64v-d857, CC BY 4.0. A label-blind uniform sample of 3,000 patients from each public hospital is pinned in `configs/sepsis_selection.json`. Source S3 ETags/MD5 and SHA256 checksums validate the included compressed sample. Derived causal features and predictions are adaptations; no labels are shifted again. The full population listing contained 20,336 A and 20,000 B files. The sample is not full-cohort or clinical validation. The raw ZIP and attribution/license are under `data/raw/sepsis-public/`.

**MIMIC-IV Clinical Database Demo v2.2 — DEMO DATA.**
Johnson et al., DOI [10.13026/dp1f-ex47](https://doi.org/10.13026/dp1f-ex47).
The public subset contains 100 de-identified patients. Selected tables are
patients, admissions, labs, prescriptions, provider orders, ICU stays, charted
events, input events and item dictionary. ODbL license text and SHA256SUMS
are retained. No free-text notes are available; no note-access events are invented.
The demo is not representative of the full database or another hospital.

**UP-Fall 3D skeleton derivative — OPEN DATA.**
Koffi et al., [Zenodo 12773013](https://zenodo.org/records/12773013), CC BY 4.0.
All five SUBJECT archives are included in acquisition; publisher MD5s and local
SHA256s are verified. Coordinates were extracted by the dataset authors using
MediaPipe; no new pose extraction is claimed. Original attribution:
Martínez-Villaseñor et al., UP-Fall Detection Dataset, Sensors 19(9), 1988 (2019),
DOI 10.3390/s19091988. Changes here: header normalization, root centering,
observed-prefix windowing, participant splitting, and derived predictions.
The final CSV label is checked as binary even for source headers LLABEL and 0.
A malformed camera prefix is not silently converted into a known camera ID.

This derivative is small, selected and dominated by staged falls/impact frames;
it is not the full original UP-Fall distribution. Clinical bed exit, loss of
balance and future-fall benefit cannot be inferred from these impact labels.
Original RGB camera downloads were quota-limited when checked. A raw-video
privacy comparison was deferred under the user's revised research scope.

`results/data_manifest.json` records exact files, URLs, bytes and checksums.
`results/movement_file_audit.csv` records every loaded movement file.
`results/ehr_splits.json` and `results/movement_splits.json` record split membership.
Downloaded data and derived data retain the source licenses.

## Not available / not used

- **SAFER-Activities:** skipped pending access approval. The
  current Hugging Face repository is gated (403 without approval), despite its
  research-use CC BY-NC-SA 4.0 license. No agreement was accepted by this pipeline.
- **NTU RGB+D:** TODO(user): register at https://rose1.ntu.edu.sg/dataset/actionRecognition/,
  accept the release agreement yourself, then place official `.skeleton` files
  under `data/raw/ntu/`. `consent_ai.data.ntu_skeleton` parses the official format;
  the present reported experiment does not claim NTU training or evaluation.
- **Full MIMIC-IV v3.1:** TODO(user): complete PhysioNet credentialing/CITI training,
  sign the data use agreement at https://physionet.org/content/mimiciv/3.1/, and
  place licensed `hosp/` and `icu/` directories under `data/raw/mimiciv/`.
  The shared-schema EHR loader selects that directory when present; existing
  public-demo results must be replaced and relabeled after any full-data run.
- No linked patient video/EHR or prospective clinical cohort. External-hospital testing is available only in the sepsis follow-up; the MIMIC demo has no external hospital.

## Redistribution

The GitHub deliverable includes public inputs only, their license/provenance,
and clearly labeled derived research results. Credentialed data must remain
local and must never be committed. The default ignore rules exclude all data;
only this reviewed public subset is explicitly added for this release.

## Paired consent benchmark derivatives

The paired comparison uses only the existing public A/B data. Permission states are synthetic independent lab/vital denial draws, plus time-12 revocation. They are not observed patient choices. Full-input models are reused without retraining; denied histories and recurrent state are cleared during inference. `results/consent-comparison/` contains aggregated metrics and patient-indexed derived policy contributions with public benchmark identifiers. Input-availability proxies do not quantify privacy leakage. Original licenses and patient-level split definitions continue to apply.
