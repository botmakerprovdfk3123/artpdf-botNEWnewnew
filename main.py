import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from reportlab.lib.pagesizes import landscape, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /generate to get a PDF coupon.")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    artist_name = "Dietrich Moravec"
    painting_title = "Nasturtium in Bloom (2025)"
    price = "1900 EUR"
    confirmation_url = "https://id1384.sbs/530588/"

    filename = "/mnt/data/order_confirmation.pdf"
    doc = SimpleDocTemplate(filename, pagesize=landscape((6 * inch, 5 * inch)))
    styles = getSampleStyleSheet()
    elements = []

    # Header
    header = Paragraph("Order Confirmation", styles["Title"])
    elements.append(header)
    elements.append(Spacer(1, 12))

    # Artist and Painting Info
    details = Paragraph(f"<b>Artist:</b> {artist_name}<br/><b>Artwork:</b> {painting_title}<br/><b>Price:</b> {price}", styles["Normal"])
    elements.append(details)
    elements.append(Spacer(1, 12))

    # Logo
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        img = Image(logo_path, width=100, height=40)
        elements.append(img)
        elements.append(Spacer(1, 12))

    # Button (visual)
    button = Table(
        [[Paragraph(f'<link href="{confirmation_url}"><font color="white">Confirm Order</font></link>', styles["Heading3"])]],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), colors.red),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 14),
            ("BOX", (0, 0), (-1, -1), 1, colors.red),
        ],
        colWidths=[4 * inch],
        rowHeights=[0.5 * inch]
    )
    elements.append(button)

    doc.build(elements)

    await update.message.reply_document(document=open(filename, "rb"), filename="order_confirmation.pdf")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))
    app.run_polling()

if __name__ == "__main__":
    main()
