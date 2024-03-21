#!/usr/bin/env python

print("[INFO] Importing modules...")
import qsm_forward
import json
import shutil
import glob
import os

print("[INFO] Loading configuration...")
with open('config.json') as config_json_file_handle:
	config_json = json.load(config_json_file_handle)

print("[INFO] Preparing reconstruction parameters...")
recon_params = qsm_forward.ReconParams()
recon_params.peak_snr = 100
tissue_params = qsm_forward.TissueParams(
    chi=qsm_forward.generate_susceptibility_phantom(
        resolution=[100, 100, 100],
        background=0,
        large_cylinder_val=0.005,
        small_cylinder_radii=[4, 4, 4, 7],
        small_cylinder_vals=[0.05, 0.1, 0.2, 0.5]
    )
)

print("[INFO] Generating BIDS dataset...")
qsm_forward.generate_bids(tissue_params, recon_params, "bids")

print("[INFO] Moving outputs to magphase/...")
os.makedirs("magphase", exist_ok=True)
shutil.move(glob.glob("bids/sub-1/anat/*echo-1*mag*nii")[0], "magphase/mag.nii")
shutil.move(glob.glob("bids/sub-1/anat/*echo-1*phase*nii")[0], "magphase/phase.nii")
shutil.move(glob.glob("bids/sub-1/anat/*echo-1*mag*json")[0], "magphase/mag.json")
shutil.move(glob.glob("bids/sub-1/anat/*echo-1*phase*json")[0], "magphase/phase.json")

print("[INFO] Moving ground truth to chimap/...")
os.makedirs("chimap", exist_ok=True)
shutil.move("bids/derivatives/qsm-forward/sub-1/anat/sub-1_Chimap.nii", "chimap/qsm.nii")

