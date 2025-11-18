#!/usr/bin/env python3
"""
Sample Medical Imaging Dataset Downloader
Downloads small example files for testing CHAZON Medical Imaging SCADA

Usage:
    python download-samples.py [--all] [--xray] [--ct] [--mri]
"""

import os
import sys
import urllib.request
import argparse

# Small open-source sample images (publicly accessible)
SAMPLE_DATASETS = {
    'xray': [
        {
            'name': 'chest_xray_sample.jpg',
            'url': 'https://github.com/ieee8023/covid-chestxray-dataset/raw/master/images/01E392EE-69F9-4E33-BFCE-E5C968654078.jpeg',
            'description': 'COVID-19 chest X-ray sample'
        }
    ],
    'dicom': [
        {
            'name': 'sample_dicom.dcm',
            'url': 'https://barre.dev/medical/samples/sample_dicom.dcm',
            'description': 'Sample DICOM file for testing'
        }
    ]
}

def download_file(url, dest_path, description):
    """Download a file from URL to destination path"""
    print(f"Downloading: {description}")
    print(f"  URL: {url}")
    print(f"  Destination: {dest_path}")

    try:
        urllib.request.urlretrieve(url, dest_path)
        file_size = os.path.getsize(dest_path)
        print(f"  ✓ Downloaded ({file_size:,} bytes)\n")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}\n")
        return False

def download_samples(modalities=['all']):
    """Download sample datasets for specified modalities"""
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if 'all' in modalities:
        modalities = list(SAMPLE_DATASETS.keys())

    total_downloaded = 0
    total_failed = 0

    for modality in modalities:
        if modality not in SAMPLE_DATASETS:
            print(f"Unknown modality: {modality}")
            continue

        modality_dir = os.path.join(base_dir, modality)
        os.makedirs(modality_dir, exist_ok=True)

        print(f"\n{'='*60}")
        print(f"Downloading {modality.upper()} samples")
        print(f"{'='*60}\n")

        for sample in SAMPLE_DATASETS[modality]:
            dest_path = os.path.join(modality_dir, sample['name'])

            # Skip if already exists
            if os.path.exists(dest_path):
                print(f"Skipping: {sample['description']} (already exists)\n")
                continue

            success = download_file(sample['url'], dest_path, sample['description'])
            if success:
                total_downloaded += 1
            else:
                total_failed += 1

    print(f"\n{'='*60}")
    print(f"Download Summary")
    print(f"{'='*60}")
    print(f"✓ Successfully downloaded: {total_downloaded}")
    print(f"✗ Failed: {total_failed}")
    print(f"\nSamples saved to: {base_dir}")
    print("\nFor more datasets, see README.md")

def main():
    parser = argparse.ArgumentParser(
        description='Download sample medical imaging datasets'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Download all available samples'
    )
    parser.add_argument(
        '--xray',
        action='store_true',
        help='Download X-ray samples'
    )
    parser.add_argument(
        '--ct',
        action='store_true',
        help='Download CT scan samples'
    )
    parser.add_argument(
        '--mri',
        action='store_true',
        help='Download MRI samples'
    )
    parser.add_argument(
        '--dicom',
        action='store_true',
        help='Download DICOM samples'
    )

    args = parser.parse_args()

    # Determine which modalities to download
    modalities = []
    if args.all or not any([args.xray, args.ct, args.mri, args.dicom]):
        modalities = ['all']
    else:
        if args.xray:
            modalities.append('xray')
        if args.ct:
            modalities.append('ct')
        if args.mri:
            modalities.append('mri')
        if args.dicom:
            modalities.append('dicom')

    print("\nCHAZON Medical Imaging - Sample Dataset Downloader")
    print("="*60)
    print("\nNote: These are small example files for testing purposes.")
    print("For full datasets, refer to README.md for links to:")
    print("  - MIMIC-CXR (377k chest X-rays)")
    print("  - NIH Chest X-Ray (112k images)")
    print("  - TCIA (cancer imaging archive)")
    print("  - OASIS (brain MRI)")
    print("  - And many more...\n")

    download_samples(modalities)

if __name__ == '__main__':
    main()
