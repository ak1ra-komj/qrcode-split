
## qrcode-split.py

Small command line program written by ChatGPT 4o.

```
Write a python3 command line program to split any file (text or binary) into serials of QR code image files.

* This program should have -c, --chunk-size option to pass the chunk size of each split file,
* All generated QR code image files will be saved under the output/ directory, with basename of input file as sub-directory and filename prefix by default,
* Add a -C, --calc option to calculate the amount of QR code image files to be generated, the output directory is not required when -C is given,
* Put "${index} / ${total_files}" at the footer of each generated files, ensure the font size is not too small to visible.
* Add a -r, --resume option to resume generating QR codes from where it left off,
* Add multiprocessing if it is possible,
```

## quick start

Install the required libraries:

```ShellSession
python3 -m venv .venv
. .venv/bin/activate

pip3 install -r requirements.txt
```

Running the script:

```ShellSession
# To calculate the total number of QR code files needed:
python qrcode-split.py input/input-1.mp4 -C

# To generate the QR code files:
python qrcode-split.py input/input-1.mp4

# Resume generating QR codes from where it left off:
python qrcode-split.py input/input-1.mp4 -r
```

Use `-h` or `--help` to checkout program help,

```ShellSession
$ python qrcode-split.py -h
usage: qrcode-split.py [-h] [-o OUTPUT_DIR] [-c CHUNK_SIZE] [-C] [-p PROCESSES] [-r] file

Split a file into a series of QR code images.

positional arguments:
  file                  Path to the input file (text or binary).

options:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Directory to save the QR code images.
  -c CHUNK_SIZE, --chunk-size CHUNK_SIZE
                        Size of each chunk in bytes (default: 1900).
  -C, --calc            Calculate and print the count of QR code files needed without generating QR codes.
  -p PROCESSES, --processes PROCESSES
                        Number of processes to use (default: number of CPU cores).
  -r, --resume          Resume generating QR codes from where it left off.
```
