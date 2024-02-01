import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from fastapi import HTTPException
from fpdf import FPDF


# Function to generate a PDF invoice

async def generate_invoice(customer_name, items):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()

    # Add PNG image to the PDF at the right side, top
    image_width = 110
    pdf.image("images/car.jpg", x=pdf.w - image_width - 20, y=30, w=image_width)

    # Add invoice title
    pdf.set_font('Courier', 'B', size=30)  # 'B' stands for bold
    pdf.cell(0, 20, "Invoice", ln=True, align='L')
    pdf.ln(30)

    # Customer details
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Customer Name: {}".format(customer_name), ln=True, align='L')
    pdf.cell(0, 10, "Phone: Your Phone Number", ln=True, align='L')
    pdf.cell(0, 10, "Email: Your Email", ln=True, align='L')

    pdf.ln(-20)
    pdf.cell(0, 10, "Invoice ID: 12345", ln=True, align='R')
    pdf.cell(0, 10, "Date: {}".format(datetime.datetime.now().strftime("%Y-%m-%d")), ln=True, align='R')
    pdf.ln(10)
 
    # Table Header
    pdf.set_fill_color(200, 220, 255)
   

    pdf.cell(50, 10, txt="Description", align='C', fill=True)
    pdf.cell(70, 10, txt="Dates", align='C', fill=True)
    pdf.cell(30, 10, txt="Total Days",align='C', fill=True)
    pdf.cell(40, 10, txt="Price", align='C', fill=True)
    pdf.ln(10)

# Draw vertical lines after filling cells with color
    pdf.line(pdf.get_x() + 50, pdf.get_y() - 10, pdf.get_x() + 50, pdf.get_y())  # Vertical line after "Description"
    pdf.line(pdf.get_x() + 120, pdf.get_y() - 10, pdf.get_x() + 120, pdf.get_y())  # Vertical line after "Dates"
    pdf.line(pdf.get_x() + 150, pdf.get_y() - 10, pdf.get_x() + 150, pdf.get_y())  # Vertical line after "Total Days"
    
# Table Content
    for item in items:
        pdf.cell(50, 10, txt=item['Description'], align='C')
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x(), pdf.get_y() + 10)  # Vertical line
        pdf.cell(70, 10, txt=item['Dates'], align='C')
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x(), pdf.get_y() + 10)  # Vertical line
        pdf.cell(30, 10, txt=str(item['totalDates']), align='C')
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x(), pdf.get_y() + 10)  # Vertical line
        pdf.cell(40, 10, txt=item['price'], align='C')
        pdf.ln(10)
    tax=None
    pdf.cell(120, 10, txt="  ", align='C', border=0)
    pdf.cell(30, 10, txt="Tax", align='C', border=0)
    pdf.cell(40, 10, txt=tax, align='C', border=0)
    pdf.cell(120, 10, txt="  ", align='C', border=0)
    pdf.cell(30, 10, txt="Total ", align='C', border=0)
    pdf.cell(40, 10, txt="${:.2f}".format(sum(float(item['price']) for item in items)), align='C', border=0)
    pdf.ln(50)

    # Payment Seal
    pdf.cell(0, 20, "Payment Seal", ln=True, align='R')

    # Save the PDF to a byte string and return
    return pdf.output(dest='S').encode('latin1')

# Function to send an email with the invoice attached
async def send_invoice_email(subject,receiver_email, pdf_content):
    #subject = "Invoice for Your reservation"
    sender_email = "hrit1527@gmail.com"
    password = "kpju rzkp elgk ovyb"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the PDF content to the email
    message.attach(MIMEText("Please find your invoice attached.", "plain"))
    pdf_attachment = MIMEText(pdf_content, "pdf", "latin1")
    pdf_attachment.add_header('Content-Disposition', 'attachment; filename="invoice.pdf"')
    message.attach(pdf_attachment)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


async def send_invoice(email: str,items:list,customer_name):
    try:
        pdf_content =await generate_invoice(customer_name, items)
        await send_invoice_email(email, pdf_content)
        return "Invoice sent successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
