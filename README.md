<h1 align="center">QSM Data Generator</h1>

<p align="center">
  Simulates T2*-weighted magnitude and phase images and a ground-truth susceptibility map from a synthetic cylinder phantom with qsm-forward, for testing QSM pipelines such as QSMxT.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.820"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.820-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-see_LICENSE-lightgrey.svg" alt="License"></a>
</p>

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Simulates T2*-weighted magnitude and phase images and a ground-truth susceptibility map from a synthetic cylinder phantom with qsm-forward, for testing QSM pipelines such as QSMxT.**

Generates a susceptibility phantom (a large cylinder with four smaller cylinders of different susceptibility) at the chosen matrix size and voxel size, runs the qsm-forward forward model with the given TR, TE, flip angle, field strength and field direction, and exports the simulated magnitude and phase images, the ground-truth chi map, a segmentation and a mask. Use it to create test data with known ground truth for QSM methods; it takes no input data. The README is the unmodified python App template, and the code fixes the peak SNR at 100.

| | |
|---|---|
| **Outputs** | `neuro/anat/t2starw` ×2 · `neuro/qsm` · `neuro/parcellation/volume` · `neuro/mask` |
| **Container** | `python:3.8-bookworm` |
| **Resources** | 16 GB memory · 1 h walltime |
| **Run it** | [doi.org/10.25663/brainlife.app.820](https://doi.org/10.25663/brainlife.app.820) |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `t2starw-mag` | `neuro/anat/t2starw` | T2*-weighted magnitude images. |
| `t2starw-phase` | `neuro/anat/t2starw` | T2*-weighted phase images. |
| `chimap` | `neuro/qsm` | Ground truth susceptibility map (Chi or χ). |
| `segmentation` | `neuro/parcellation/volume` | Segmentation of anatomical ROIs. |
| `mask` | `neuro/mask` | Mask of the internal ROI. |

<details>
<summary><b>Parameters</b> (15)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `subject` | string | `1` | Subject identifier |
| `resolution-0` | number | `100` | Phantom matrix size (voxels) along the first axis. |
| `resolution-1` | number | `100` | Phantom matrix size (voxels) along the second axis. |
| `resolution-2` | number | `100` | Phantom matrix size (voxels) along the third axis. |
| `TR` | number | `0.05` | Repetition time passed to the qsm-forward simulation. |
| `TE` | number | `0.004` | Echo time passed to the qsm-forward simulation (single echo). |
| `flip-angle` | number | `15` | Flip angle passed to the qsm-forward simulation. |
| `B0` | number | `7` | Main magnetic field strength passed to the simulation. |
| `B0-dir-0` | number | `0` | First component of the B0 field direction vector. |
| `B0-dir-1` | number | `0` | Second component of the B0 field direction vector. |
| `B0-dir-2` | number | `1` | Third component of the B0 field direction vector. |
| `voxel-size-0` | number | `1` | Voxel size along the first axis. |
| `voxel-size-1` | number | `1` | Voxel size along the second axis. |
| `voxel-size-2` | number | `1` | Voxel size along the third axis. |
| `peak-snr` | number |  | Not applied: the code reads the key 'peak_snr' and then always sets the peak SNR to 100. |

</details>

<!-- brainlife-app:end -->

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.820](https://doi.org/10.25663/brainlife.app.820), choose the input datasets from your project, set the parameters and press **Execute**. The results are saved to your project as `neuro/anat/t2starw`, `neuro/anat/t2starw`, `neuro/qsm`, `neuro/parcellation/volume`, `neuro/mask`.

### Locally

You need [Singularity/Apptainer](https://apptainer.org/) (the App runs in `python:3.8-bookworm`), [`jq`](https://jqlang.github.io/jq/).

1. Clone this repository.
2. Create `config.json` with the paths to your inputs and the parameters:

   ```json
   {
       "subject": "1",
       "resolution-0": 100,
       "resolution-1": 100,
       "resolution-2": 100,
       "TR": 0.05,
       "TE": 0.004,
       "flip-angle": 15,
       "B0": 7,
       "B0-dir-0": 0,
       "B0-dir-1": 0,
       "B0-dir-2": 1,
       "voxel-size-0": 1,
       "voxel-size-1": 1,
       "voxel-size-2": 1,
       "peak-snr": "<number>"
   }
   ```

3. Run `./main`.

## Troubleshooting

- **One magnitude file expected!**: The simulation produced an unexpected number of magnitude images; check the TE parameter (a single echo is expected).

## app-example-documentation

This is an example of how to write documentation (readme.md and license.md for Apps on brainlife.io)

Write the following here...

1) What the App does, and how it does it at the basic level.
2) Briefly explain what 1) means for novice users in a language that 1st year psychology student can understand it.
3) Briefly description of input / output files.

## Sample Datasets

If you don't have your own input file, you can download sample datasets from Brainlife.io, or you can use [Brainlife CLI](https://github.com/brainlife/cli).

```
npm install -g brainlife
bl login
mkdir input
bl dataset download 5a0f0fad2c214c9ba8624376#5a050966eec2b300611abff2 && mv 5a0f0fad2c214c9ba8624376#5a050966eec2b300611abff2 .
```

## Citing

If you use this App, please cite it, the software it builds on and brainlife.io:

- QSM Data Generator. brainlife.io App. [doi:10.25663/brainlife.app.820](https://doi.org/10.25663/brainlife.app.820)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

- Franco Pestilli

**Contributors**

- Franco Pestilli

#### Copyright (c) 2022 brainlife.io The University of Texas at Austin

## Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io, which runs this App, is publicly funded by Wellcome, the U.S. National Institutes of Health and the U.S. National Science Foundation; acknowledging that support helps keep it running.</sub>

## License

See [LICENSE](LICENSE).
