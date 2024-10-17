#!/usr/bin/env python

print("[INFO] Importing modules...")

import qsm_forward
import json
import shutil
import glob
import os
import gzip
import numpy as np

print("[INFO] Loading configuration...")
with open('config.json') as config_json_file_handle:
	config_json = json.load(config_json_file_handle)

print("[INFO] Preparing reconstruction parameters...")
subject = config_json['subject']
recon_params = qsm_forward.ReconParams(
	subject=subject,
	TR=config_json['TR'],
	TEs=np.array([config_json['TE']]),
	flip_angle=config_json['flip-angle'],
    B0=config_json['B0'],
	B0_dir=np.array([config_json['B0-dir-0'], config_json['B0-dir-1'], config_json['B0-dir-2']]),
	voxel_size=np.array([config_json['voxel-size-0'], config_json['voxel-size-1'], config_json['voxel-size-2']]),
	peak_snr=config_json['peak_snr'] if 'peak_snr' in config_json else None
)
recon_params.peak_snr = 100
tissue_params = qsm_forward.TissueParams(
    chi=qsm_forward.generate_susceptibility_phantom(
        resolution=np.array([config_json['resolution-0'], config_json['resolution-1'], config_json['resolution-2']]),
        background=0,
        large_cylinder_val=0.005,
        small_cylinder_radii=[4, 4, 4, 7],
        small_cylinder_vals=[0.05, 0.1, 0.2, 0.5],
    ),
	voxel_size=np.array([config_json['voxel-size-0'], config_json['voxel-size-1'], config_json['voxel-size-2']])
)

print("[INFO] Generating BIDS dataset...")
qsm_forward.generate_bids(tissue_params, recon_params, "bids")

print("[INFO] Collecting outputs...")
os.makedirs("t2starw-mag", exist_ok=True)
os.makedirs("t2starw-phase", exist_ok=True)

mag_images = sorted(glob.glob(f"bids/sub-{subject}/anat/*mag*nii"))
phs_images = sorted(glob.glob(f"bids/sub-{subject}/anat/*phase*nii"))
mag_jsons = sorted(glob.glob(f"bids/sub-{subject}/anat/*mag*json"))
phs_jsons = sorted(glob.glob(f"bids/sub-{subject}/anat/*phase*json"))

if len(mag_images) != 1: raise RuntimeError(f"One magnitude file expected! Found {len(mag_images)} ({mag_images})")
if len(phs_images) != 1: raise RuntimeError(f"One phase file expected! Found {len(phs_images)} ({phs_images})")
if len(mag_jsons) != 1: raise RuntimeError(f"One magnitude sidecar expected! Found {len(mag_jsons)} ({mag_jsons})")
if len(phs_jsons) != 1: raise RuntimeError(f"One phase sidecar expected! Found {len(phs_jsons)} ({phs_jsons})")

shutil.copy2(mag_images[0], "t2starw-mag/t2starw.nii")
shutil.copy2(phs_images[0], "t2starw-phase/t2starw.nii")

# Add 'Subject' and save JSONs
with open(mag_jsons[0], 'r') as mag_json_file:
    mag_json_data = json.load(mag_json_file)
mag_json_data["Subject"] = subject
with open("t2starw-mag/t2starw.json", 'w') as mag_json_file:
    json.dump(mag_json_data, mag_json_file, indent=4)

with open(phs_jsons[0], 'r') as phs_json_file:
    phs_json_data = json.load(phs_json_file)
phs_json_data["Subject"] = subject
with open("t2starw-phase/t2starw.json", 'w') as phs_json_file:
    json.dump(phs_json_data, phs_json_file, indent=4)

os.makedirs("chimap", exist_ok=True)
os.makedirs("segmentation", exist_ok=True)
os.makedirs("mask", exist_ok=True)

shutil.copy2(f"bids/derivatives/qsm-forward/sub-{subject}/anat/sub-{subject}_Chimap.nii", "chimap/qsm.nii")
shutil.copy2("t2starw-phase/t2starw.json", "chimap/qsm.json")
shutil.copy2(f"bids/derivatives/qsm-forward/sub-{subject}/anat/sub-{subject}_dseg.nii", "segmentation/parc.nii")
shutil.copy2("t2starw-mag/t2starw.json", "segmentation/parc.json")

mask_file = f"bids/derivatives/qsm-forward/sub-{subject}/anat/sub-{subject}_mask.nii"
with open(mask_file, 'rb') as f_in:
    with gzip.open("mask/mask.nii.gz", 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
shutil.copy2("t2starw-mag/t2starw.json", "mask/mask.json")

