import qrcode
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Generator v4.0 🧹📝")
        self.root.geometry("450x600")
        self.qr_img = None
        self.history = []  # История QR
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="QR Генератор v4.0",
                 font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(self.root, text="Текст/URL:").pack()
        self.text_entry = tk.Entry(self.root, width=40, font=("Arial", 11))
        self.text_entry.pack(pady=10)

        tk.Button(self.root, text="Создать QR", command=self.create_qr,
                  bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
        tk.Button(self.root, text="💾 Сохранить", command=self.save_qr,
                  bg="#2196F3", fg="white").pack(pady=5)
        tk.Button(self.root, text="🧹 Очистить", command=self.clear_all,
                  bg="#FF9800", fg="white").pack(pady=5)
        tk.Button(self.root, text="📝 История", command=self.show_history,
                  bg="#9C27B0", fg="white").pack(pady=5)

        self.canvas_label = tk.Label(
            self.root, text="QR появится тут", bg="lightgray")
        self.canvas_label.pack(expand=True, fill="both", pady=20)

    def create_qr(self, size=12):
        text = self.text_entry.get()
        if not text:
            messagebox.showwarning("Ошибка", "Введи текст!")
            return

        qr = qrcode.QRCode(version=1, box_size=size, border=4)
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        self.qr_img = img
        img.thumbnail((250, 250))
        photo = ImageTk.PhotoImage(img)

        self.canvas_label.configure(image=photo, text="")
        self.history.append(f"QR: {text}")  # ✅ История!
        messagebox.showinfo("Готово", "QR создан!")

    def save_qr(self):
        if self.qr_img:
            text = self.text_entry.get()
            filename = f"qr_{text[:20].replace(' ', '_')}.png"
            self.qr_img.save(filename)
            messagebox.showinfo("✅", f"Сохранено: {filename}")
        else:
            messagebox.showwarning("⚠️", "Сначала создай QR!")

    def clear_all(self):
        self.text_entry.delete(0, tk.END)
        self.canvas_label.configure(image="", text="QR появится тут")
        self.qr_img = None

    def show_history(self):
        if self.history:
            hist_text = "\n".join(self.history[-5:])  # последние 5
            messagebox.showinfo("📝 История QR", hist_text)
        else:
            messagebox.showinfo("📝 История", "Пока пусто!")


if __name__ == "__main__":
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()
