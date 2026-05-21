import qrcode
import base64
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader

# ---------------------------------------------------
# 1. QR CODE GENERATOR (HTML Template-ka v v imp)
# ---------------------------------------------------
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H, 
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode()

# ---------------------------------------------------
# 2. ID CARD PDF GENERATOR (AF-SOOMAALI + PLAN B)
# ---------------------------------------------------
def generate_id_card_pdf(user_profile, password=None):
    """
    Wuxuu dhalinayaa ID Card Af-Soomaali ah.
    Password-ka wuxuu ka soo qaadanayaa 'manual_password'-ka foomka.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --- Cabirka Kaarka ---
    card_width = 380
    card_height = 240
    x = (width - card_width) / 2
    y = height - 350

    # 1. Background-ka Kaarka (Midab Madow oo Buluug xiga)
    p.setFillColor(HexColor("#1a1a2e")) 
    p.roundRect(x, y, card_width, card_height, 15, fill=1)

    # 2. Header-ka Sare (Guduud/Purple mix)
    p.setFillColor(HexColor("#4834d4")) 
    p.roundRect(x, y + card_height - 50, card_width, 50, 15, fill=1)
    
    p.setFillColor(white)
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(x + card_width/2, y + card_height - 35, "KAARKA AQOONSIGA")

    # 3. Xogta Qofka
    p.setFont("Helvetica", 11)
    p.setFillColor(HexColor("#dff9fb"))
    
    text_x = x + 30
    y_start = y + card_height - 80

    # Magaca
    p.drawString(text_x, y_start, "MAGACA OO DHAMAYSTIRAN:")
    p.setFillColor(white)
    p.setFont("Helvetica-Bold", 13)
    full_name = f"{user_profile.first_name} {user_profile.father_name} {user_profile.grandfather_name}"
    p.drawString(text_x, y_start - 20, full_name.upper())

    # ID Code
    p.setFillColor(HexColor("#dff9fb"))
    p.setFont("Helvetica", 11)
    p.drawString(text_x, y_start - 55, "KOODKA AQOONSIGA:")
    p.setFillColor(HexColor("#f9ca24")) # Midab dahabi ah
    p.setFont("Helvetica-Bold", 16)
    p.drawString(text_x, y_start - 75, f"{user_profile.user_id_code}")

    # 4. QAYBTA PASSWORD-KA (PLAN B)
    # Wuxuu soo baxayaa kaliya haddii password-ka la soo geliyo
    if password and password != "Lama hayo":
        p.setFillColor(HexColor("#ff7979")) # Midab casaan khafif ah
        p.setFont("Helvetica-Bold", 11)
        p.drawString(text_x, y_start - 110, "SIRTA GALITAANKA (PASSWORD):")
        
        p.setFillColor(white)
        p.setFont("Courier-Bold", 14) 
        p.drawString(text_x, y_start - 130, f"{password}")

    # 5. QR Code-ka (Dhex-galka PDF)
    qr_img = qrcode.make(user_profile.user_id_code)
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    
    qr_reader = ImageReader(qr_buffer)
    p.drawImage(qr_reader, x + card_width - 100, y + 25, width=80, height=80)

    # 6. Footer Note
    p.setFillColor(HexColor("#95afc0"))
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(text_x, y + 15, "Kaarkan waxaa dhaliyay nidaamka, waana mid sax ah.")

    # --- DHAMMAAD ---
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer