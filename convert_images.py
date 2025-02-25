import os
import pillow_heif
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def convert_images():
    # Ask user to select images
    file_paths = filedialog.askopenfilenames(
        title="Select images to convert",
        filetypes=[
            ("All Image Files", "*.jpg;*.jpeg;*.png;*.webp;*.heic;*.bmp;*.tiff"),
            ("JPEG Files", "*.jpg;*.jpeg"),
            ("PNG Files", "*.png"),
            ("WebP Files", "*.webp"),
            ("HEIC Files", "*.heic"),
            ("BMP Files", "*.bmp"),
            ("TIFF Files", "*.tiff"),
        ]
    )

    if not file_paths:
        messagebox.showinfo("No Files Selected", "No files were selected. Exiting.")
        return

    # Ask user where to save the converted images
    output_dir = filedialog.askdirectory(title="Select output folder")
    if not output_dir:
        messagebox.showinfo("No Folder Selected", "No output folder was selected. Exiting.")
        return

    # Get selected output format
    output_format = format_var.get()
    
    # **Fix**: Map "JPG" to "JPEG" because Pillow requires "JPEG"
    format_mapping = {"JPG": "JPEG", "PNG": "PNG", "WEBP": "WEBP", "BMP": "BMP", "TIFF": "TIFF"}
    output_format = format_mapping[output_format]

    # Get quality (only relevant for JPEG and WEBP)
    quality = quality_var.get() if output_format in ["JPEG", "WEBP"] else None

    # Process each selected file
    for file_path in file_paths:
        try:
            # Open the image (convert HEIC if needed)
            if file_path.lower().endswith(".heic"):
                heif_file = pillow_heif.read_heif(file_path)
                image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
            else:
                image = Image.open(file_path)

            # Convert to RGB if necessary (JPG does not support transparency)
            if output_format == "JPEG" and image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            # Create output file path
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_file = os.path.join(output_dir, f"{base_name}.{output_format.lower()}")

            # Save image with the chosen format and quality
            if quality:
                image.save(output_file, output_format, quality=quality)
            else:
                image.save(output_file, output_format)

            print(f"Converted: {file_path} -> {output_file}")

        except Exception as e:
            print(f"Error converting {file_path}: {e}")

    messagebox.showinfo("Conversion Complete", "All selected images have been converted successfully.")


# Initialize Tkinter window
root = tk.Tk()
root.title("Image Converter")

# Output format selection
tk.Label(root, text="Select Output Format:").pack(pady=5)
format_var = tk.StringVar(value="JPG")
format_options = ["JPG", "PNG", "WEBP", "BMP", "TIFF"]
format_menu = ttk.Combobox(root, textvariable=format_var, values=format_options, state="readonly")
format_menu.pack(pady=5)

# Quality selection (only for JPG & WEBP)
tk.Label(root, text="Select Quality (Only for JPG & WEBP):").pack(pady=5)
quality_var = tk.IntVar(value=95)
quality_slider = tk.Scale(root, from_=1, to=100, orient="horizontal", variable=quality_var)
quality_slider.pack(pady=5)

# Convert button
convert_button = tk.Button(root, text="Select Images & Convert", command=convert_images)
convert_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
