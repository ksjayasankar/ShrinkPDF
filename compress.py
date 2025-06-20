import sys
import subprocess
import os
import argparse

# Define quality presets based on Ghostscript's capabilities.
# We include standard presets and our own advanced, custom ones.
PRESETS = {
    'screen': {
        'desc': 'Lowest quality, smallest size (72 dpi). Good for screen viewing.',
        'params': ['-dPDFSETTINGS=/screen']
    },
    'ebook': {
        'desc': 'Medium quality, medium size (150 dpi). A good balance.',
        'params': ['-dPDFSETTINGS=/ebook']
    },
    'printer': {
        'desc': 'High quality for printing (300 dpi). Larger file size.',
        'params': ['-dPDFSETTINGS=/printer']
    },
    'prepress': {
        'desc': 'Highest quality, for professional printing, color preservation.',
        'params': ['-dPDFSETTINGS=/prepress']
    },
    'architectural': {
        'desc': 'Highly optimized for hybrid files like architectural plans. Aggressively compresses images while preserving vector quality.',
        'params': [
            # ==> GENERAL & PRE-PROCESSING PARAMETERS
            '-dCompatibilityLevel=1.6',
            '-dDetectDuplicateImages=true',
            '-dCompressFonts=true',
            '-dSubsetFonts=true',
            '-sColorConversionStrategy=sRGB',
            '-dProcessColorModel=/DeviceRGB',
            
            # ==> RASTER IMAGE DOWNSAMPLING
            '-dDownsampleColorImages=true',
            '-dDownsampleGrayImages=true',
            '-dDownsampleMonoImages=true',
            '-dColorImageResolution=150',
            '-dGrayImageResolution=150',
            '-dMonoImageResolution=300',
            
            # ==> ALGORITHM SEGREGATION AND APPLICATION
            # This is a single, multi-line argument passed to Ghostscript's -c option
            (
                '-c', 
                ".setdistillerparams << "
                "/ColorImageDict << /QFactor 2.0 /Blend 1 /HSamples [2 1 1 2] /VSamples [2 1 1 2] /ImageType 1 /DCTEncode >> "
                "/GrayImageDict << /QFactor 2.0 /Blend 1 /HSamples [2 1 1 2] /VSamples [2 1 1 2] /ImageType 1 /DCTEncode >> "
                "/MonoImageDict << /K -1 /ImageType 3 /JBIG2Encode >> "
                ">> setdistillerparams"
            )
        ]
    }
}

def compress_pdf(input_path, output_path, quality='ebook'):
    """
    Uses Ghostscript to compress a PDF file based on a selected quality preset.
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
        # Build the command list
        command = [
            gs_command,
            '-sDEVICE=pdfwrite',
            '-dNOPAUSE',
            '-dBATCH',
            '-dQUIET',
            f'-sOutputFile={output_path}',
        ]
        
        # Add preset parameters. Note the special handling for the tuple in 'architectural'
        preset_params = PRESETS[quality]['params']
        for param in preset_params:
            if isinstance(param, tuple):
                command.extend(param)
            else:
                command.append(param)
        
        command.append(input_path)

        # Execute the command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print("--- Ghostscript Error ---")
            print("STDOUT:", stdout.decode(errors='ignore'))
            print("STDERR:", stderr.decode(errors='ignore'))
            print("-------------------------")
            return
        
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