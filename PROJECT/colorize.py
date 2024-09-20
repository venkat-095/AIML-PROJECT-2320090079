import numpy as np
import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import time

# Paths to load the model
DIR = r"D:\AIML PROJECT\Colorizing-black-and-white-images-using-Python-master"
PROTOTXT = os.path.join(DIR, r"model/colorization_deploy_v2.prototxt")
POINTS = os.path.join(DIR, r"model/pts_in_hull.npy")
MODEL = os.path.join(DIR, r"model/colorization_release_v2.caffemodel")

# Load the Model
print("Load model")
net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
pts = np.load(POINTS)

# Load centers for ab channel quantization used for rebalancing.
class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

def colorize_image(image_path):
    # Load the input image with Pillow
    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        raise ValueError(f"Could not open image: {e}")

    # Convert image to numpy array for OpenCV processing
    image_cv = np.array(image)
    
    # Check if the image is loaded properly
    if image_cv is None or image_cv.size == 0:
        raise ValueError("The image file could not be read or is empty.")
    
    scaled = image_cv.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_RGB2Lab)
    
    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50
    
    print("Colorizing the image")
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    
    ab = cv2.resize(ab, (image_cv.shape[1], image_cv.shape[0]))
    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    
    colorized = cv2.cvtColor(colorized, cv2.COLOR_Lab2RGB)
    colorized = np.clip(colorized, 0, 1)
    
    colorized = (255 * colorized).astype("uint8")
    
    return image_cv, colorized

def resize_image(image, base_width):
    width, height = image.size
    aspect_ratio = height / width
    new_width = base_width
    new_height = int(aspect_ratio * new_width)
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def select_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("All Image Files", "*.*")]
    )
    if file_path:
        global original_image, colorized_image
        try:
            original, colorized = colorize_image(file_path)
            original_image = Image.fromarray(original)
            colorized_image = Image.fromarray(colorized)
            show_images(original_image, colorized_image)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showinfo("No File Selected", "No image file was selected.")

def show_images(original_image, colorized_image):
    display_window = tk.Toplevel()
    display_window.title("Image Colorization")
    display_window.configure(bg='#f0f0f0')

    frame = tk.Frame(display_window, bg='#f0f0f0')
    frame.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)

    base_width = 800
    original_image = resize_image(original_image, base_width)
    colorized_image = resize_image(colorized_image, base_width)

    original_photo = ImageTk.PhotoImage(image=original_image)
    colorized_photo = ImageTk.PhotoImage(image=colorized_image)

    original_label = tk.Label(frame, image=original_photo, bg='#f0f0f0', borderwidth=2, relief="flat")
    original_label.image = original_photo
    original_label.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    colorized_label = tk.Label(frame, image=colorized_photo, bg='#f0f0f0', borderwidth=2, relief="flat")
    colorized_label.image = colorized_photo
    colorized_label.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    save_button = tk.Button(display_window, text="Save Colorized Image", command=lambda: save_image(colorized_image),
                           font=('Helvetica', 12), bg='#4CAF50', fg='white', padx=15, pady=5, relief="raised", borderwidth=0)
    save_button.pack(pady=10)

    fade_in_effect(original_label)
    fade_in_effect(colorized_label)

    display_window.update_idletasks()
    display_window.geometry(f"{base_width*2 + 60}x{max(original_image.height, colorized_image.height) + 100}")

def fade_in_effect(label):
    for i in range(0, 101, 10):
        label.configure(bg=f'#00{hex(i*2)[2:].zfill(2)}ff')
        root.update()
        time.sleep(0.05)

def save_image(image):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")]
    )
    if file_path:
        image.save(file_path)
        messagebox.showinfo("Save Successful", f"Image saved as {file_path}")

def main():
    global root
    root = tk.Tk()
    root.title("Colorization App")
    root.geometry("500x300")
    root.configure(bg='#f0f0f0')

    header = tk.Label(root, text="Black & White Image Colorization", font=('Helvetica', 18, 'bold'), bg='#f0f0f0')
    header.pack(pady=20)

    frame = tk.Frame(root, bg='#f0f0f0')
    frame.pack(pady=50)

    btn_select_image = tk.Button(frame, text="Select Image", command=select_image, font=('Helvetica', 14),
                                 bg='#2196F3', fg='white', padx=20, pady=10, relief="raised", borderwidth=0)
    btn_select_image.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
