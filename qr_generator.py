import qrcode


def create_qr(text):
    """Генерирует QR-код из текста"""
    qr = qrcode.QRCode(
        version=1,          # размер
        box_size=15,        # пиксели квадрата
        border=4            # рамка
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr_code.png")
    print("✅ QR-код сохранен: qr_code.png")


if __name__ == "__main__":
    print("=== QR Генератор =====")
    url = input("Введите текст или URL: ")
    create_qr(url)
    input("\nНажмите Enter для выхода...")
