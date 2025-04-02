#!/usr/bin/env python3
"""
A simple utility to convert .caf (Core Audio Format) audio files to .mp3 format.
"""

import os
import sys
import argparse
import glob
from pathlib import Path
import ffmpeg
from tqdm import tqdm

def convert_caf_to_mp3(input_file, output_file):
    """
    Convert a .caf file to .mp3 using ffmpeg
    
    Args:
        input_file (str): Path to input .caf file
        output_file (str): Path to output .mp3 file
    
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    try:
        # Print debug info
        print(f"Converting {input_file} to {output_file}")
        
        # Use ffmpeg-python to convert the file
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.output(stream, output_file, acodec='libmp3lame', ab='192k')
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True, overwrite_output=True)
        
        # Verify the output file exists
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"Successfully converted to {output_file}")
            return True
        else:
            print("Conversion failed - output file not created")
            return False
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}")
        return False
    except Exception as e:
        print(f"Conversion error: {str(e)}")
        return False

def convert_directory(input_dir, output_dir=None):
    """
    Convert all .caf files in the input directory to .mp3 format.
    
    Args:
        input_dir (str): Path to the input directory containing .caf files
        output_dir (str, optional): Path to the output directory. If None, 
                                  mp3 files will be saved in the same directory as caf files.
    
    Returns:
        tuple: (number of successful conversions, total number of files)
    """
    # Find all .caf files in the input directory
    caf_files = glob.glob(os.path.join(input_dir, '*.caf'))
    
    if not caf_files:
        print(f"No .caf files found in {input_dir}")
        return 0, 0
    
    success_count = 0
    total_files = len(caf_files)
    
    print(f"Found {total_files} .caf files to convert.")
    
    for caf_file in tqdm(caf_files, desc="Converting files"):
        if output_dir:
            # Determine output file path
            file_name = os.path.basename(caf_file)
            base_name = os.path.splitext(file_name)[0]
            output_file = os.path.join(output_dir, base_name + '.mp3')
        else:
            output_file = None  # Will use same directory as input
        
        if convert_caf_to_mp3(caf_file, output_file):
            success_count += 1
    
    return success_count, total_files

def main():
    """Main function for the script."""
    parser = argparse.ArgumentParser(description='Convert .caf audio files to .mp3 format.')
    parser.add_argument('input_dir', nargs='?', default=os.getcwd(),
                        help='Directory containing .caf files (default: current directory)')
    parser.add_argument('output_dir', nargs='?', default=None,
                        help='Directory to save .mp3 files (default: same as input directory)')
    
    args = parser.parse_args()
    
    # Check if input directory exists
    if not os.path.isdir(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist.")
        return 1
    
    # Create output directory if it doesn't exist
    if args.output_dir and not os.path.exists(args.output_dir):
        try:
            os.makedirs(args.output_dir)
            print(f"Created output directory: {args.output_dir}")
        except Exception as e:
            print(f"Error creating output directory: {str(e)}")
            return 1
    
    success, total = convert_directory(args.input_dir, args.output_dir)
    
    print(f"\nConversion complete: {success} of {total} files successfully converted.")
    
    if success < total:
        print(f"Failed to convert {total - success} files. Check the output for details.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 