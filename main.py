#!/usr/bin/env python

print("[INFO] Importing modules...")

import qsm_forward
import json
import shutil
import glob
import os
import numpy as np
import nibabel as nib

print("[INFO] Loading configuration...")
with open('config.json') as config_json_file_handle:
	config_json = json.load(config_json_file_handle)

print("[INFO] Preparing reconstruction parameters...")
recon_params = qsm_forward.ReconParams(
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
        small_cylinder_vals=[0.05, 0.1, 0.2, 0.5]
    )
)

print("[INFO] Generating BIDS dataset...")
qsm_forward.generate_bids(tissue_params, recon_params, "bids")

print("[INFO] Moving outputs...")
os.makedirs("t2starw-mag", exist_ok=True)
os.makedirs("t2starw-phase", exist_ok=True)

# Get a list of all echo image paths
mag_images = glob.glob("bids/sub-1/anat/*echo-*mag*nii")
phase_images = glob.glob("bids/sub-1/anat/*echo-*phase*nii")
mag_jsons = glob.glob("bids/sub-1/anat/*echo-*mag*json")
phase_jsons = glob.glob("bids/sub-1/anat/*echo-*phase*json")

if len(mag_images) > 0: raise RuntimeError(f"One magnitude file expected! Found {len(mag_images)} ({mag_images})")
if len(phase_images) > 0: raise RuntimeError(f"One magnitude file expected! Found {len(phase_images)} ({phase_images})")
if len(mag_jsons) > 0: raise RuntimeError(f"One magnitude file expected! Found {len(mag_jsons)} ({mag_jsons})")
if len(phase_jsons) > 0: raise RuntimeError(f"One magnitude file expected! Found {len(phase_jsons)} ({phase_jsons})")

# Save the new images to a temporary location
nib.save(mag_images[0], "t2starw-mag/t2starw.nii")
nib.save(phase_images[0], "t2starw-phase/t2starw.nii")
nib.save(mag_jsons[0], "t2starw-phase/t2starw.json")
nib.save(phase_jsons[0], "t2starw-phase/t2starw.json")

print("[INFO] Moving ground truth to chimap/...")
os.makedirs("chimap", exist_ok=True)
shutil.move("bids/derivatives/qsm-forward/sub-1/anat/sub-1_Chimap.nii", "chimap/qsm.nii")
nib.save(phase_jsons[0], "chimap/qsm.json")

