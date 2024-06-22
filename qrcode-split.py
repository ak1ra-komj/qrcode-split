# coding: utf-8

import argparse
import os
import base64
import math
import qrcode
from PIL import ImageDraw, ImageFont
from multiprocessing import Pool, cpu_count


def split_file_to_chunks(file_path, chunk_size):
    with open(file_path, 'rb') as f:
        index = 1
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield (chunk, index)
            index += 1


def encode_chunk_to_base64(chunk):
    return base64.b64encode(chunk).decode('utf-8')


def generate_qr_code(data_info):
    data, index, total_count, output_dir, prefix = data_info
    qr = qrcode.QRCode(
        version=40,  # Version 40 is the largest, can store up to 2953 bytes in binary mode
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white').convert('RGB')

    # Add footer with index/total_count_of_files
    draw = ImageDraw.Draw(img)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 20)
    text = f'{index}/{total_count}'
    textbbox = draw.textbbox((0, 0), text, font=font)
    textwidth = textbbox[2] - textbbox[0]
    textheight = textbbox[3] - textbbox[1]
    width, height = img.size
    text_x = (width - textwidth) / 2
    text_y = height - textheight - 10  # Adjust the Y position

    draw.text((text_x, text_y), text, font=font, fill='black')

    img_path = os.path.join(output_dir, f'{prefix}_{index}.png')
    img.save(img_path)
    print(f'Saved QR code {index} to {img_path}')


def calculate_total_chunks(file_size, chunk_size):
    return math.ceil(file_size / chunk_size)


def get_existing_indices(output_dir, prefix):
    existing_files = os.listdir(output_dir)
    indices = []
    for file in existing_files:
        if file.startswith(prefix) and file.endswith('.png'):
            try:
                index = int(file[len(prefix)+1:-4])
                indices.append(index)
            except ValueError:
                continue
    return sorted(indices)


def main():
    parser = argparse.ArgumentParser(
        description="Split a file into a series of QR code images.")
    parser.add_argument(
        "file", help="Path to the input file (text or binary).")
    parser.add_argument(
        "-o", "--output-dir", help="Directory to save the QR code images.", default=None)
    parser.add_argument("-c", "--chunk-size", type=int, default=1900,
                        help="Size of each chunk in bytes (default: 1900).")
    parser.add_argument("-C", "--calc", action='store_true',
                        help="Calculate and print the count of QR code files needed without generating QR codes.")
    parser.add_argument("-p", "--processes", type=int, default=cpu_count(),
                        help="Number of processes to use (default: number of CPU cores).")
    parser.add_argument("-r", "--resume", action='store_true',
                        help="Resume generating QR codes from where it left off.")

    args = parser.parse_args()

    file_name = os.path.basename(args.file)
    file_base_name = os.path.splitext(file_name)[0]

    chunk_size = args.chunk_size
    file_size = os.path.getsize(args.file)
    total_chunks = calculate_total_chunks(file_size, chunk_size)

    if args.calc:
        print(f'Total QR code files needed: {total_chunks}')
        return

    output_dir = args.output_dir or os.path.join("output", file_base_name)
    os.makedirs(output_dir, exist_ok=True)
    print(f'Splitting {args.file} into {total_chunks} QR codes.')

    if args.resume:
        existing_indices = get_existing_indices(output_dir, file_base_name)
    else:
        existing_indices = []

    last_index = existing_indices[-1] if existing_indices else 0

    pool = Pool(processes=args.processes)

    for chunk, index in split_file_to_chunks(args.file, chunk_size):
        if index <= last_index:
            continue
        encoded_chunk = encode_chunk_to_base64(chunk)
        pool.apply_async(generate_qr_code, ((
            encoded_chunk, index, total_chunks, output_dir, file_base_name),))

    pool.close()
    pool.join()


if __name__ == "__main__":
    main()
