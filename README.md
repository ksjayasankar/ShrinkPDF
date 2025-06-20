# ShrinkScribe 🖋️

A simple, powerful, and cross-platform command-line tool that leverages Ghostscript to offer best-in-class PDF compression. Say goodbye to privacy-invasive online tools!

## The Problem
You have a massive PDF file (1.5GB!) that you need to email or upload, but online compression tools are slow, compromise your privacy by uploading your data, or have restrictive file size limits.

## The Solution
`ShrinkScribe` uses the power of Ghostscript right on your own machine to safely and effectively compress your PDFs. You get full control over the quality and compression level.

## Features
-   **Cross-Platform:** Works on Windows, macOS, and Linux.
-   **Secure:** Your files never leave your computer.
-   **Powerful:** Uses the robust Ghostscript engine.
-   **Customizable:** Choose from simple presets or use advanced settings for maximum control.

## Prerequisites
You MUST have **Ghostscript** installed and accessible in your system's PATH.
-   **Windows:** [Download from ghostscript.com](https://www.ghostscript.com/releases/gsdnld.html)
-   **macOS:** `brew install ghostscript`
-   **Linux (Debian/Ubuntu):** `sudo apt-get install ghostscript`

## Installation
1.  Clone this repository:
    ```bash
    git clone [https://github.com/your-username/ShrinkScribe.git](https://github.com/your-username/ShrinkScribe.git)
    cd ShrinkScribe
    ```
2.  (Optional) It's good practice to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

## Usage
The script is simple to use. The basic syntax is:
`python compress.py <input.pdf> <output.pdf> --quality <preset>`

#### Basic Example
This will use the well-balanced `ebook` preset.
```bash
python compress.py my_giant_file.pdf compressed_file.pdf
```

#### High Compression Example
For maximum compression, use the `screen` preset. Quality will be lower.
```bash
python compress.py my_giant_file.pdf compressed_file.pdf --quality screen
```

#### Advanced Custom Compression
Use the `custom` preset for fine-tuned, high-ratio compression.
```bash
python compress.py my_giant_file.pdf compressed_file.pdf --quality custom
```

## How to Contribute
Contributions are welcome! If you have ideas for improvements, new features, or find a bug, please feel free to:
1.  Open an issue to discuss the change.
2.  Fork the repository and submit a pull request.

## License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.
