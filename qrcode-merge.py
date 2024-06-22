import argparse
import os
import base64
from PIL import Image
from pyzbar.pyzbar import decode
from multiprocessing import Pool, cpu_count


def decode_qr_code(file_path):
    img = Image.open(file_path)
    decoded_objects = decode(img)
    if decoded_objects:
        data = decoded_objects[0].data.decode("utf-8")
        index = int(os.path.splitext(
            os.path.basename(file_path))[0].split('_')[-1])
        return (index, data)
    else:
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Merge a directory of QR code images back into the original file.")
    parser.add_argument(
        "directory", help="Path to the directory containing the QR code images.")
    parser.add_argument("-o", "--output-file",
                        help="Path to save the merged file.", required=True)
    parser.add_argument("-p", "--processes", type=int, default=cpu_count(),
                        help="Number of processes to use (default: number of CPU cores).")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        raise ValueError(
            f"The specified directory does not exist: {args.directory}")

    qr_files = [os.path.join(args.directory, f)
                for f in os.listdir(args.directory) if f.endswith('.png')]
    qr_files.sort(key=lambda f: int(os.path.splitext(
        os.path.basename(f))[0].split('_')[-1]))  # Sort by index

    pool = Pool(processes=args.processes)
    decoded_chunks = pool.map(decode_qr_code, qr_files)
    pool.close()
    pool.join()

    decoded_chunks = [chunk for chunk in decoded_chunks if chunk is not None]
    decoded_chunks.sort(key=lambda x: x[0])  # Sort by index
    data_chunks = [base64.b64decode(chunk) for _, chunk in decoded_chunks]

    with open(args.output_file, 'wb') as f:
        for chunk in data_chunks:
            f.write(chunk)

    print(f"Merged file saved to {args.output_file}")


if __name__ == "__main__":
    main()
