#!/usr/bin/env python

print("[INFO] Importing modules...")
import qsm_forward
import json
import shutil
import glob
import os
import numpy as np

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

print("[INFO] Collecting outputs...")
os.makedirs("t2starw-mag", exist_ok=True)
os.makedirs("t2starw-phase", exist_ok=True)

mag_images = glob.glob("bids/sub-1/anat/*mag*nii")
phs_images = glob.glob("bids/sub-1/anat/*phase*nii")
mag_jsons = glob.glob("bids/sub-1/anat/*mag*json")
phs_jsons = glob.glob("bids/sub-1/anat/*phase*json")

if len(mag_images) != 1: raise RuntimeError(f"One magnitude file expected! Found {len(mag_images)} ({mag_images})")
if len(phs_images) != 1: raise RuntimeError(f"One phase file expected! Found {len(phs_images)} ({phs_images})")
if len(mag_jsons) != 1: raise RuntimeError(f"One magnitude sidecar expected! Found {len(mag_jsons)} ({mag_jsons})")
if len(phs_jsons) != 1: raise RuntimeError(f"One phase sidecar expected! Found {len(phs_jsons)} ({phs_jsons})")

shutil.copy2(mag_images[0], "t2starw-mag/t2starw.nii")
shutil.copy2(phs_images[0], "t2starw-phase/t2starw.nii")
shutil.copy2(mag_jsons[0], "t2starw-phase/t2starw.json")
shutil.copy2(phs_jsons[0], "t2starw-phase/t2starw.json")

os.makedirs("chimap", exist_ok=True)
shutil.copy2("bids/derivatives/qsm-forward/sub-1/anat/sub-1_Chimap.nii", "chimap/qsm.nii")
shutil.copy2(phs_jsons[0], "chimap/qsm.json")

