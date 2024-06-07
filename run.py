from PIL import Image
import numpy as np

def convert_image_to_rgb565(image_path, output_path):
    # Load an image
    img = Image.open(image_path)
    # Resize image to 48x48 pixels using LANCZOS resampling
    img = img.resize((48, 48), Image.Resampling.LANCZOS)
    
    # Convert image to RGB
    img = img.convert("RGB")
    data = np.array(img)
    
    # Extracting color components
    r = (data[:,:,0] >> 3).astype(np.uint16)
    g = (data[:,:,1] >> 2).astype(np.uint16)
    b = (data[:,:,2] >> 3).astype(np.uint16)
    
    # Packing RGB565
    rgb565 = (r << 11) | (g << 5) | b
    
    # Ensuring correct byte order (big-endian)
    # 'big' means the most significant byte is at the beginning of the byte array
    rgb565_bytes = rgb565.byteswap().tobytes()
    
    # Save to binary file
    with open(output_path, 'wb') as f:
        f.write(rgb565_bytes)

def main():
    input_image_path = "./keys/s.png"
    output_sys_file = "M:/vOptimus/normal/076.sys"
    convert_image_to_rgb565(input_image_path, output_sys_file)
    print("Image converted and written successfully.")

if __name__ == "__main__":
    main()
