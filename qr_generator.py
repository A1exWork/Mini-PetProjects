import qrcode
import tkinter as tk
from tkinter import messagebox, colorchooser
from PIL import Image, ImageTk
from datetime import datetime
import base64
from io import BytesIO

class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Generator v6.5 📏✨")
        self.root.geometry("450x740")
        self.qr_img = None
        self.history = []
        self.dark_mode = False
        self.preview_photo = None
        self.qr_photo = None
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="QR Генератор v6.5 📏✨",
                 font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(self.root, text="Текст/URL:").pack()
        self.text_entry = tk.Entry(self.root, width=40, font=("Arial", 11))
        self.text_entry.pack(pady=10)
        self.text_entry.bind("<KeyRelease>", self.on_text_change)

        # ✅ Новый инфо-лейбл
        self.info_label = tk.Label(self.root, text="0 символов | QR: пусто",
                                   font=("Arial", 9))
        self.info_label.pack(pady=(0, 5))

        tk.Button(self.root, text="🎨 Создать QR", command=self.create_qr,
                  bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

        tk.Button(self.root, text="🌈 Цвета QR", command=self.choose_colors,
                  bg="#FF5722", fg="white", font=("Arial", 11)).pack(pady=5)
        
        tk.Button(self.root, text="📋 Копировать", command=self.copy_text,
                  bg="#FFC107", fg="black", font=("Arial", 11)).pack(pady=5)
        tk.Button(self.root, text="📱 Поделиться", command=self.share_qr,
                  bg="#00BCD4", fg="white", font=("Arial", 11)).pack(pady=5)
        tk.Button(self.root, text="💾 Сохранить", command=self.save_qr,
                  bg="#2196F3", fg="white").pack(pady=5)
        tk.Button(self.root, text="🧹 Очистить", command=self.clear_all,
                  bg="#FF9800", fg="white").pack(pady=5)
        tk.Button(self.root, text="📝 История", command=self.show_history,
                  bg="#9C27B0", fg="white").pack(pady=5)
        tk.Button(self.root, text="⚙ Пример", command=self.fill_example,
                  bg="#607D8B", fg="white", font=("Arial", 10)).pack(pady=5)

        tk.Label(self.root, text="Размер QR:").pack(pady=(10, 0))
        self.size_var = tk.IntVar(value=10)
        size_scale = tk.Scale(self.root, from_=5, to=20, orient=tk.HORIZONTAL,
                              variable=self.size_var, length=200)
        size_scale.pack(pady=5)
        size_scale.bind("<Motion>", self.on_size_change)

        self.theme_check = tk.Checkbutton(self.root, text="🌙 Тёмная тема",
                                          command=self.toggle_theme, font=("Arial", 10))
        self.theme_check.pack(pady=10)

        self.canvas_label = tk.Label(self.root, text="QR появится тут",
                                     bg="lightgray", wraplength=300)
        self.canvas_label.pack(expand=True, fill="both", pady=20)

    def on_text_change(self, event=None):
        text = self.text_entry.get()
        length = len(text)

        if length == 0:
            status = "пусто"
        elif length <= 50:
            status = "малый"
        elif length <= 150:
            status = "средний"
        else:
            status = "крупный"

        self.info_label.config(text=f"{length} символов | QR: {status}")

        if length > 2:
            self.create_qr_preview()

    def on_size_change(self, event=None):
        if self.text_entry.get().strip():
            self.create_qr_preview()

    def create_qr_preview(self):
        try:
            text = self.text_entry.get()
            size = min(self.size_var.get(), 8)

            qr = qrcode.QRCode(version=1, box_size=size, border=2)
            qr.add_data(text)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.thumbnail((80, 80))
            self.preview_photo = ImageTk.PhotoImage(img)

            self.canvas_label.configure(image=self.preview_photo, text="")
        except:
            pass

    def create_qr(self):
        text = self.text_entry.get()
        size = self.size_var.get()
        if not text:
            messagebox.showwarning("Ошибка", "Введи текст!")
            return

        qr = qrcode.QRCode(version=1, box_size=size, border=4)
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        self.qr_img = img
        img.thumbnail((250, 250))
        self.qr_photo = ImageTk.PhotoImage(img)

        self.canvas_label.configure(image=self.qr_photo, text="")
        self.canvas_label.image = self.qr_photo
        self.history.append(
            f"QR: {text[:30]}... ({size}px) - {datetime.now().strftime('%H:%M')}")
        messagebox.showinfo("Готово", f"QR создан! Размер: {size}px")

    def choose_colors(self):
        if not self.text_entry.get().strip():
            messagebox.showwarning("⚠️", "Сначала введи текст!")
            return
        
        fill_color = colorchooser.askcolor(title="Цвет QR (fill)")[1] or "black"
        back_color = colorchooser.askcolor(title="Фон QR (back)")[1] or "white"
        
        size = self.size_var.get()
        text = self.text_entry.get()
        
        qr = qrcode.QRCode(version=1, box_size=size, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        self.qr_img = img
        img.thumbnail((250, 250))
        self.qr_photo = ImageTk.PhotoImage(img)
        
        self.canvas_label.configure(image=self.qr_photo, text="")
        self.canvas_label.image = self.qr_photo
        
        self.history.append(
            f"QR: {text[:30]}... ({size}px, цвета) - {datetime.now().strftime('%H:%M')}")
        messagebox.showinfo("🎨", f"QR с цветами: {fill_color} на {back_color}")

    def share_qr(self):
        if self.qr_img:
            buffer = BytesIO()
            self.qr_img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            share_text = f"📱 QR код:\ndata:image/png;base64,{img_str}"
            
            self.root.clipboard_clear()
            self.root.clipboard_append(share_text)
            messagebox.showinfo("📱", "QR скопирован как картинка! Вставь в чат (Ctrl+V)")
        else:
            messagebox.showwarning("⚠️", "Сначала создай QR!")

    def save_qr(self):
        if self.qr_img:
            text = self.text_entry.get().strip() or "qr"
            safe_text = (
                text[:20]
                .replace(" ", "_")
                .replace("/", "_")
                .replace(":", "_")
            )

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qr_{safe_text}_{timestamp}.png"
            self.qr_img.save(filename)
            messagebox.showinfo("✅", f"Сохранено: {filename}")
        else:
            messagebox.showwarning("⚠️", "Сначала создай QR!")

    def clear_all(self):
        self.text_entry.delete(0, tk.END)
        self.canvas_label.configure(image="", text="QR появится тут")
        self.qr_img = None
        self.preview_photo = None
        self.qr_photo = None
        self.info_label.config(text="0 символов | QR: пусто")

    def show_history(self):
        if self.history:
            hist_text = "\n".join(self.history[-10:])
            messagebox.showinfo("📝 История QR (последние 10)", hist_text)
        else:
            messagebox.showinfo("📝 История", "Пока пусто!")

    def copy_text(self):
        text = self.text_entry.get()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("📋", "Текст скопирован!")
        else:
            messagebox.showwarning("⚠️", "Сначала введи текст!")

    def fill_example(self):
        example = "https://github.com/A1exWork"
        self.text_entry.delete(0, tk.END)
        self.text_entry.insert(0, example)
        self.on_text_change()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.root.configure(bg="#2b2b2b")
            self.canvas_label.configure(bg="#404040", fg="white")
        else:
            self.root.configure(bg="white")
            self.canvas_label.configure(bg="lightgray", fg="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()
