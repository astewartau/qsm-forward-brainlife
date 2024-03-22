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
	TEs=np.array([float(x) for x in str(config_json['TEs']).split(",")]),
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

print("[INFO] Moving outputs to magphase/...")
os.makedirs("magphase", exist_ok=True)

# Get a list of all echo image paths
mag_image_paths = sorted(glob.glob("bids/sub-1/anat/*echo-*mag*nii"))
phase_image_paths = sorted(glob.glob("bids/sub-1/anat/*echo-*phase*nii"))

# Concatenate the images along the 4th dimension
concat_mag = nib.concat_images(mag_image_paths)
concat_phase = nib.concat_images(phase_image_paths)

print(concat_mag.get_fdata().shape)
print(concat_mag.shape)

# Save the new images to a temporary location
nib.save(concat_mag, "magphase/mag.nii")
nib.save(concat_phase, "magphase/phase.nii")

def combine_json_files(in_paths, out_path):
    combined_data = {"echoes": []}

    for file_path in in_paths:
        # Open and load the JSON data from each file
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            # Append the data to the 'echoes' list
            combined_data["echoes"].append(data)

    with open(out_path, 'w') as json_file:
        json_file.write(json.dumps(combined_data))

mag_json_files = sorted(glob.glob("bids/sub-1/anat/*mag*.json"))
phase_json_files = sorted(glob.glob("bids/sub-1/anat/*phase*.json"))

combine_json_files(mag_json_files, "magphase/mag.json")
combine_json_files(phase_json_files, "magphase/phase.json")

print("[INFO] Moving ground truth to chimap/...")
os.makedirs("chimap", exist_ok=True)
shutil.move("bids/derivatives/qsm-forward/sub-1/anat/sub-1_Chimap.nii", "chimap/qsm.nii")

