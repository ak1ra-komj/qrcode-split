# coding: utf-8

import argparse
import os
import base64
import math
import qrcode


def split_file_to_chunks(file_path, chunk_size):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


def encode_chunk_to_base64(chunk):
    return base64.b64encode(chunk).decode('utf-8')


def generate_qr_code(data, index, output_dir):
    qr = qrcode.QRCode(
        version=40,  # Version 40 is the largest, can store up to 2953 bytes in binary mode
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_path = os.path.join(output_dir, f'qr_code_{index}.png')
    img.save(img_path)
    print(f'Saved QR code {index} to {img_path}')


def main():
    parser = argparse.ArgumentParser(
        description="Split a file into a series of QR code images.")
    parser.add_argument(
        "file", help="Path to the input file (text or binary).")
    parser.add_argument(
        "output_dir", help="Directory to save the QR code images.")
    parser.add_argument("-c", "--chunk_size", type=int, default=1900,
                        help="Size of each chunk in bytes (default: 1900).")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    chunk_size = args.chunk_size
    file_size = os.path.getsize(args.file)
    total_chunks = math.ceil(file_size / chunk_size)

    print(f'Splitting {args.file} into {total_chunks} QR codes.')

    for i, chunk in enumerate(split_file_to_chunks(args.file, chunk_size)):
        encoded_chunk = encode_chunk_to_base64(chunk)
        generate_qr_code(encoded_chunk, i, args.output_dir)


if __name__ == "__main__":
    main()
