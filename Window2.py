import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("MRI Image Viewer")
        self.root.geometry("1200x800")  # Az ablak méretének beállítása

        self.image_list = []  # Képek listája
        self.current_image_index = 0  # Jelenleg megjelenített kép indexe
        self.target_size = (800, 600)  # Képek célmérete

        # Felület elemek létrehozása
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.LEFT, fill=tk.Y)

        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = Listbox(self.frame, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.config(command=self.listbox.yview)

        self.image_label = tk.Label(root)
        self.image_label.pack(side=tk.RIGHT, expand=True)
        self.image_label.bind("<Button-1>", self.open_image_in_new_window)

        # Menü létrehozása
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Folder", command=self.load_directory)

        # Események kezelése
        self.listbox.bind('<<ListboxSelect>>', self.show_image)
        root.bind('<Left>', self.previous_image)
        root.bind('<Right>', self.next_image)

    def load_directory(self):
        # Könyvtár kiválasztása és képek betöltése
        directory = filedialog.askdirectory()
        if directory:
            # Képek listájának összeállítása
            self.image_list = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            if not self.image_list:
                messagebox.showinfo("Információ", "Nem található kép a kiválasztott mappában.")
                return

            # Listbox frissítése képekkel
            self.listbox.delete(0, tk.END)
            for image in self.image_list:
                self.listbox.insert(tk.END, os.path.basename(image))

            self.current_image_index = 0
            self.show_image()

    def show_image(self, event=None):
        # Kép megjelenítése a listából
        if not self.image_list:
            return

        if event:
            self.current_image_index = self.listbox.curselection()[0]

        image_path = self.image_list[self.current_image_index]
        image = Image.open(image_path)

        # Kép átméretezése az arányok megtartásával
        image = self.resize_image(image, self.target_size)
        photo = ImageTk.PhotoImage(image)

        self.image_label.config(image=photo)
        self.image_label.image = photo
        self.root.title(f"MRI Image Viewer - {os.path.basename(image_path)}")

    def resize_image(self, image, target_size):
        # Kép átméretezése az arányok megtartásával
        original_width, original_height = image.size
        target_width, target_height = target_size

        # Új méret kiszámítása az arányok megtartásával
        ratio = min(target_width / original_width, target_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)

        return image.resize((new_width, new_height), Image.LANCZOS)

    def open_image_in_new_window(self, event):
        # Kép megnyitása új ablakban
        if not self.image_list:
            return

        image_path = self.image_list[self.current_image_index]
        image = Image.open(image_path)

        new_window = tk.Toplevel(self.root)
        new_window.title(f"Enlarged Image - {os.path.basename(image_path)}")
        new_window.geometry("1200x800")

        # Kép átméretezése az új ablak méretéhez
        def resize_image_to_window(event):
            window_width, window_height = event.width, event.height
            ratio = min(window_width / image.width, window_height / image.height)
            new_width = int(image.width * ratio)
            new_height = int(image.height * ratio)
            resized_image = image.resize((new_width, new_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)
            label.config(image=photo)
            label.image = photo

        # Eredeti kép megjelenítése és átméretezés kezelése
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(new_window, image=photo)
        label.image = photo
        label.pack(expand=True, fill=tk.BOTH)
        new_window.bind("<Configure>", resize_image_to_window)

    def previous_image(self, event):
        # Előző kép megjelenítése
        if self.image_list:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_list)
            self.listbox.select_set(self.current_image_index)
            self.listbox.event_generate("<<ListboxSelect>>")

    def next_image(self, event):
        # Következő kép megjelenítése
        if self.image_list:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
            self.listbox.select_set(self.current_image_index)
            self.listbox.event_generate("<<ListboxSelect>>")

if __name__ == "__main__":
    root = tk.Tk()
    viewer = ImageViewer(root)
    root.mainloop()
