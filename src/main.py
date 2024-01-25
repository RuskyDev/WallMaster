import os
import requests
import ctypes
from io import BytesIO
from PIL import Image, ImageTk
import tempfile
import tkinter as tk
from tkinter import ttk, Entry, Button, Label, messagebox
from datetime import datetime

class WallMaster:
    def __init__(self, master):
        self.master = master
        master.title("WallMaster")

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        master.iconbitmap(icon_path)

        master.resizable(False, False)
        master.geometry("500x300")

        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))

        self.label = ttk.Label(master, text="Enter the image URL:")
        self.label.pack(pady=10)

        self.entry = Entry(master, font=("Helvetica", 12), width=30)
        self.entry.pack(pady=10)

        self.set_button = ttk.Button(master, text="Set Wallpaper", command=self.set_wallpaper)
        self.set_button.pack(pady=10)

        self.clear_button = ttk.Button(master, text="Clear Wallpaper", command=self.clear_wallpaper)
        self.clear_button.pack(pady=10)

        self.note_label = ttk.Label(master, text="Note: Ensure that your image is in HD, or it may appear blurry when set.", font=("Helvetica", 10), foreground="gray")
        self.note_label.pack(pady=10)

        self.log_file_path = os.path.join(os.getenv('APPDATA'), 'WallMaster', 'logs.txt')
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
        with open(self.log_file_path, 'a'):
            pass

    def log_message(self, message):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(f"{timestamp} {message}\n")

    def set_wallpaper(self):
        try:
            temp_folder = tempfile.gettempdir()
            image_url = self.entry.get()
            response = requests.get(image_url)

            if response.status_code == 200:
                image_name = os.path.join(temp_folder, os.path.basename(image_url))

                with open(image_name, "wb") as img_file:
                    img_file.write(response.content)

                ctypes.windll.user32.SystemParametersInfoW(20, 0, image_name, 3)
                messagebox.showinfo("Success", "Wallpaper set successfully!")
            else:
                self.log_message(f"Failed to download image from URL: {image_url}")
                messagebox.showerror("Error", "Failed to download image. Please check the URL.")
        except Exception as e:
            self.log_message(f"An error occurred: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_wallpaper(self):
        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, "", 3)
            messagebox.showinfo("Success", "Wallpaper cleared successfully!")
        except Exception as e:
            self.log_message(f"An error occurred while clearing wallpaper: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WallMaster(root)
    root.mainloop()
