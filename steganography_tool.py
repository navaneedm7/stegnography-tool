import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import stepic


image_path = None


def select_image():
    global image_path
    image_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.bmp")]
    )
    if image_path:
        status_label.config(text="Image selected: " + image_path)


def hide_message():
    global image_path

    if not image_path:
        messagebox.showerror("Error", "Please select an image first")
        return

    message = text_box.get("1.0", tk.END).strip()

    if message == "":
        messagebox.showerror("Error", "Enter a message to hide")
        return

    try:
        img = Image.open(image_path)
        encoded_img = stepic.encode(img, message.encode())

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")]
        )

        if save_path:
            encoded_img.save(save_path)
            status_label.config(text="Message hidden successfully!")
            messagebox.showinfo("Success", "Message hidden in image")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def extract_message():
    global image_path

    if not image_path:
        messagebox.showerror("Error", "Please select an encoded image")
        return

    try:
        img = Image.open(image_path)
        message = stepic.decode(img)

        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, message)

        status_label.config(text="Message extracted successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Steganography Tool")
root.geometry("500x400")

title_label = tk.Label(root, text="Steganography Tool", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

select_button = tk.Button(root, text="Select Image", command=select_image)
select_button.pack(pady=5)

text_box = tk.Text(root, height=10, width=50)
text_box.pack(pady=10)

hide_button = tk.Button(root, text="Hide Message", command=hide_message)
hide_button.pack(pady=5)

extract_button = tk.Button(root, text="Extract Message", command=extract_message)
extract_button.pack(pady=5)

status_label = tk.Label(root, text="Status: Waiting for action")
status_label.pack(pady=10)

root.mainloop()