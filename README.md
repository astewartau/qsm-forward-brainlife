[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.444-blue.svg)](https://doi.org/10.25663/bl.app.444)

# app-template-python

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Simulates T2*-weighted magnitude and phase images and a ground-truth susceptibility map from a synthetic cylinder phantom with qsm-forward, for testing QSM pipelines such as QSMxT.**

Generates a susceptibility phantom (a large cylinder with four smaller cylinders of different susceptibility) at the chosen matrix size and voxel size, runs the qsm-forward forward model with the given TR, TE, flip angle, field strength and field direction, and exports the simulated magnitude and phase images, the ground-truth chi map, a segmentation and a mask. Use it to create test data with known ground truth for QSM methods; it takes no input data. The README is the unmodified python App template, and the code fixes the peak SNR at 100.

| | |
|---|---|
| 📤 **Outputs** | `neuro/anat/t2starw` ×2 · `neuro/qsm` · `neuro/parcellation/volume` · `neuro/mask` |
| 🐳 **Container** | `python:3.8-bookworm` |
| ⚙️ **Resources** | 16 GB memory · 1 h walltime |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.820](https://doi.org/10.25663/brainlife.app.820) |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `t2starw-mag` | `neuro/anat/t2starw` | T2*-weighted magnitude images. |
| `t2starw-phase` | `neuro/anat/t2starw` | T2*-weighted phase images. |
| `chimap` | `neuro/qsm` | Ground truth susceptibility map (Chi or χ). |
| `segmentation` | `neuro/parcellation/volume` | Segmentation of anatomical ROIs. |
| `mask` | `neuro/mask` | Mask of the internal ROI. |

<details>
<summary><b>⚙️ Parameters</b> (15)</summary>

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

This is a template showing how to develop a python-based brainlife.io/app

# app-example-documentation
This is an example of how to write documentation (readme.md and license.md for Apps on brainlife.io)

Write the following here...

1) What the App does, and how it does it at the basic level.
2) Briefly explain what 1) means for novice users in a language that 1st year psychology student can understand it.
3) Briefly description of input / output files.

### Authors
- [Franco Pestilli](pestilli@utexas.edu)

### Contributors
- [Franco Pestilli](pestilli@utexas.edu)

#### Copyright (c) 2022 brainlife.io The University of Texas at Austin

### Funding Acknowledgement
brainlife.io is publicly funded and for the sustainability of the project it is helpful to Acknowledge the use of the platform. We kindly ask that you acknowledge the funding below in your code and publications. Copy and past the following lines into your repository when using this code.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)

### Citations
We ask that you the following articles when publishing papers that used data, code or other resources created by the brainlife.io community.

1. Avesani, P., McPherson, B., Hayashi, S. et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. Sci Data 6, 69 (2019). [https://doi.org/10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)


## Running the App 

### On Brainlife.io

You can submit this App online at [https://doi.org/10.25663/bl.app.444](https://doi.org/10.25663/bl.app.444) via the "Execute" tab.

### Running Locally (on your machine)

1. git clone this repo.
2. Inside the cloned directory, create `config.json` with something like the following content with paths to your input files.

```json
{
  "t1": "t1.nii.gz"
}
```

3. Launch the App by executing `main`

```bash
./main
```

### Sample Datasets

If you don't have your own input file, you can download sample datasets from Brainlife.io, or you can use [Brainlife CLI](https://github.com/brain-life/cli).

```
npm install -g brainlife
bl login
mkdir input
bl dataset download 5a0f0fad2c214c9ba8624376#5a050966eec2b300611abff2 && mv 5a0f0fad2c214c9ba8624376#5a050966eec2b300611abff2 .
```

## Output

All output file (a resampled T1w NIFTI-1 file) will be generated inside the current working directory (pwd), inside a specifc directory called:

```
out_dir
```

### Dependencies

This App only requires DIPY.org to run. 
