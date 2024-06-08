from PIL import Image
import numpy as np
import time

def set_dynamic_layout(key_index, layout_path):
    # Open the existing layout.sys file in binary read/write mode
    with open(layout_path, 'r+b') as file:
        # Read the entire file
        layout_data = bytearray(file.read())
        
        # Check if the index is within the file size
        if key_index >= len(layout_data):
            raise IndexError("Key index is out of the bounds of the layout file.")
        
        # Set the bit at the corresponding key index to 1 for dynamic layout
        layout_data[key_index-1] = 0x01
        
        # Move the file pointer to the beginning of the file
        file.seek(0)
        
        # Write the updated data back to the file
        file.write(layout_data)
        print(f"Updated layout.sys for key index {key_index} to dynamic.")


def convert_frame_to_rgb565(frame):
    if frame.mode != 'RGB':
        frame = frame.convert('RGB')
            
    # Convert frame to numpy array
    data = np.array(frame)
    
    # Extracting color components
    r = (data[:,:,0] >> 3).astype(np.uint16)
    g = (data[:,:,1] >> 2).astype(np.uint16)
    b = (data[:,:,2] >> 3).astype(np.uint16)
    
    # Packing RGB565
    rgb565 = (r << 11) | (g << 5) | b
    
    # Ensuring correct byte order (big-endian)
    rgb565_bytes = rgb565.byteswap().tobytes()
    
    return rgb565_bytes

def process_gif(image_path, output_path):
    with Image.open(image_path) as img:
        # Check if it is indeed a GIF (optional)
        if img.format != 'GIF':
            raise ValueError("The image must be a GIF.")
        
        # Loop indefinitely
        while True:
            frame_number = 0
            # Iterate over each frame
            while True:
                # Get frame duration (in milliseconds), convert to seconds
                frame_duration = img.info.get('duration', 100) / 1000.0  # Default to 100ms if not provided
                
                # Convert current frame to RGB565 and write to file
                rgb565_bytes = convert_frame_to_rgb565(img)
                with open(output_path, 'wb') as f:
                    f.write(rgb565_bytes)
                
                # Wait according to the frame duration
                time.sleep(frame_duration)
                
                # Try to move to the next frame
                try:
                    img.seek(img.tell() + 1)
                    frame_number += 1
                except EOFError:
                    img.seek(0)
                    break  # Go to the first frame and continue

def main():
    input_image_path = "./keys/s.gif"
    output_sys_file = "M:/vOptimus/dynamic/076.sys"
    layout_path = "M:/vOptimus/layout.sys"
    key_index = 76  # Index of the key for which to set the layout to dynamic
    set_dynamic_layout(key_index, layout_path)
    # output_sys_file = "./076.sys"
    process_gif(input_image_path, output_sys_file)
    print("GIF processed and displayed successfully.")

if __name__ == "__main__":
    main()
