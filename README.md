
## qrcode-split.py

Small command line program written by ChatGPT 4o.

```
Write a python3 command line program to split any file (text or binary) into serials of QR code image files.

* This program should have -c, --chunk-size option to pass the chunk size of each split file,
* All generated files will be saved under the output/input_filename_basename sub-directory by default, the generated file will use input_filename_basename as the prefix
* Add a -C, --calc option to calculate the amount of QR code files to be generated, the output directory is not required when -C is used.
* Put "index / total_count" of files at the footer of each generated file, ensure the font size is visible, don't be too small to be visible.
```

## quick start

Install the required libraries:

```
python3 -m venv .venv
. .venv/bin/activate

pip install qrcode[pil] pillow
```

Running the script:

```
# To calculate the total number of QR code files needed:
python file_to_qr.py <path_to_input_file> -c <chunk_size_in_bytes> -C

# For example:
python file_to_qr.py input/input-1.mp4 -c 1900 -C

# To generate the QR code files:
python file_to_qr.py <path_to_input_file> -c <chunk_size_in_bytes>

# For example:
python file_to_qr.py input/input-1.mp4 -c 1900
```
