import qrcode
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Generator v2.0")
        self.root.geometry("450x550")
        self.qr_image = None
        self.setup_ui()
    
    def setup_ui(self):
        tk.Label(self.root, text="QR Генератор", font=("Arial", 18, "bold")).pack(pady=20)
        
        tk.Label(self.root, text="Текст/URL:").pack()
        self.text_entry = tk.Entry(self.root, width=40, font=("Arial", 11))
        self.text_entry.pack(pady=10)
        
        tk.Button(self.root, text="Создать QR", command=self.create_qr, 
                 bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
        
        self.canvas_label = tk.Label(self.root, text="QR появится тут", bg="lightgray")
        self.canvas_label.pack(expand=True, fill="both", pady=20)
    
    def create_qr(self,size=12):
        text = self.text_entry.get()
        if not text:
            messagebox.showwarning("Ошибка", "Введи текст!")
            return
        
        qr = qrcode.QRCode(version=1, box_size=size, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.thumbnail((250, 250))
        photo = ImageTk.PhotoImage(img)
        
        self.canvas_label.configure(image=photo, text="")
        self.qr_image = photo
        
        messagebox.showinfo("Готово", "QR создан!")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()

