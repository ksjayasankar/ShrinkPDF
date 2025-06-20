import sys
import subprocess
import os
import argparse

PRESETS = {
    'screen': {
        'desc': 'Lowest quality, smallest size (72 dpi).',
        'params': ['-dPDFSETTINGS=/screen']
    },
    'ebook': {
        'desc': 'Medium quality, medium size (150 dpi).',
        'params': ['-dPDFSETTINGS=/ebook']
    },
    'printer': {
        'desc': 'High quality (300 dpi).',
        'params': ['-dPDFSETTINGS=/printer']
    },
    'prepress': {
        'desc': 'Highest quality, for professional printing (300 dpi).',
        'params': ['-dPDFSETTINGS=/prepress']
    },
    'default': {
        'desc': 'A good balance between size and quality.',
        'params': ['-dPDFSETTINGS=/default']
    },
    'custom': {
        'desc': 'Custom settings for advanced users.',
        'params': [
            '-dCompatibilityLevel=1.7',
            '-dDownsampleColorImages=true',
            '-dDownsampleGrayImages=true',
            '-dDownsampleMonoImages=true',
            '-dColorImageResolution=150',
            '-dGrayImageResolution=150',
            '-dMonoImageResolution=300',
            '-dSubsetFonts=true',
            '-dCompressFonts=true',
            '-dConvertCMYKImagesToRGB=true',
            '-c', '.setdistillerparams << /ColorImageDict << /QFactor 1.5 /Blend 1 >> >> setdistillerparams'
        ]
    }
}

def compress_pdf(input_path, output_path, quality='ebook'):
    """
    Uses Ghostscript to compress a PDF file.
    """
    gs_command = 'gswin64c' if sys.platform == 'win32' else 'gs'
    
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        return

    if quality not in PRESETS:
        print(f"Error: Invalid quality preset '{quality}'.")
        print("Available presets:", ", ".join(PRESETS.keys()))
        return

    print(f"Starting compression for '{input_path}'...")
    print(f"Using quality preset: '{quality}' - {PRESETS[quality]['desc']}")

    try:
        command = [
            gs_command,
            '-sDEVICE=pdfwrite',
            '-dNOPAUSE',
            '-dBATCH',
            '-dQUIET',
            *PRESETS[quality]['params'],
            f'-sOutputFile={output_path}',
            input_path
        ]

        subprocess.run(command, check=True)
        
        original_size = os.path.getsize(input_path) / (1024 * 1024)
        compressed_size = os.path.getsize(output_path) / (1024 * 1024)
        reduction = (1 - compressed_size / original_size) * 100

        print("\n--- Compression Complete ---")
        print(f"Original file size: {original_size:.2f} MB")
        print(f"Compressed file size: {compressed_size:.2f} MB")
        print(f"Reduction: {reduction:.2f}%")
        print("--------------------------")

    except FileNotFoundError:
        print(f"Error: '{gs_command}' not found.")
        print("Please ensure Ghostscript is installed and in your system's PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Ghostscript failed with error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A Python wrapper for Ghostscript to compress PDF files.",
        formatter_class=argparse.RawTextHelpFormatter # To format help text nicely
    )
    
    parser.add_argument("input", help="Path to the input PDF file.")
    parser.add_argument("output", help="Path for the compressed output PDF file.")
    
    # Generate help text for presets dynamically
    preset_help_text = "Compression quality preset.\n\n"
    for name, data in PRESETS.items():
        preset_help_text += f"'{name}': {data['desc']}\n"

    parser.add_argument(
        "-q", "--quality", 
        choices=PRESETS.keys(), 
        default='ebook', 
        help=preset_help_text
    )

    args = parser.parse_args()
    
    compress_pdf(args.input, args.output, args.quality)