import threading
from PIL import Image
import numpy as np
import time, os

LAYOUT_PATH = "M:/vOptimus/layout.sys"
lock = threading.Lock()

def set_dynamic_layout(key_index, layout_path):
    key_index = int(key_index)
    with open(layout_path, 'r+b') as file:
        layout_data = bytearray(file.read())
        if key_index >= len(layout_data):
            raise IndexError("Key index is out of the bounds of the layout file.")
        layout_data[key_index-1] = 0x01
        file.seek(0)
        file.write(layout_data)
        print(f"Updated layout.sys for key index {key_index} to dynamic.")

def convert_frame_to_rgb565(frame):
    if frame.mode != 'RGB':
        frame = frame.convert('RGB')
    data = np.array(frame)
    r = (data[:,:,0] >> 3).astype(np.uint16)
    g = (data[:,:,1] >> 2).astype(np.uint16)
    b = (data[:,:,2] >> 3).astype(np.uint16)
    rgb565 = (r << 11) | (g << 5) | b
    rgb565_bytes = rgb565.byteswap().tobytes()
    return rgb565_bytes

def process_gif(image_path, output_path):
    with Image.open(image_path) as img:
        if img.format != 'GIF':
            raise ValueError("The image must be a GIF.")
        frame_number = 0
        while True:
            try:
                img.seek(frame_number)
                frame_duration = img.info.get('duration', 100) / 1000.0
                rgb565_bytes = convert_frame_to_rgb565(img)
                with lock:
                    with open(output_path, 'wb') as f:
                        f.write(rgb565_bytes)
                time.sleep(frame_duration)
                frame_number += 1
            except EOFError:
                frame_number = 0

def animate_key(key_index):
    set_dynamic_layout(key_index, LAYOUT_PATH)
    process_gif(f"./keys/{key_index}.gif", f"M:/vOptimus/dynamic/{key_index}.sys")

def main():
    keys_to_animate = [os.path.splitext(f)[0] for f in os.listdir("./keys/") if f.endswith('.gif')]
    threads = []
    for key in keys_to_animate:
        thread = threading.Thread(target=animate_key, args=(key,))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
