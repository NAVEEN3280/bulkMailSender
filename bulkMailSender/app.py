from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os

app = Flask(__name__)

# Your email credentials
my_email = "murugesannaveen357@gmail.com"
password = "zlti cekg ncyu ufdj"

# Route to display the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the form submission and sending emails
@app.route('/send_email', methods=['POST'])
def send_email():
    # Get data from the form
    emails = request.form['emails'].split(',')  # Get emails from the form
    subject = request.form['subject']  # Get custom subject from the form
    headline = request.form['headline']  # Get custom headline from the form
    message = request.form['message']  # Get custom message from the form
    image_file = request.files['image_file']

    # Save image temporarily
    image_path = os.path.join('image.jpg')
    image_file.save(image_path)

    # Prepare email message with custom subject, headline, and message
    msg = MIMEMultipart("related")
    msg['From'] = my_email
    msg['Subject'] = subject  # Use the custom subject entered by the user

    # Create HTML content for the email with custom headline and message
    html_body = f"""
    <html>
    <body>
        <h1>{headline}</h1>  <!-- Use the custom headline -->
        <p>{message}</p>  <!-- Use the custom message -->
        <img src="cid:image1" alt="Motivation Image">
    </body>
    </html>
    """
    html_part = MIMEText(html_body, 'html', 'utf-8')
    msg.attach(html_part)

    # Attach the image to the email
    with open(image_path, "rb") as img_file:
        img = MIMEImage(img_file.read())
        img.add_header('Content-ID', '<image1>')
        img.add_header('Content-Disposition', 'inline', filename="image.jpg")
        msg.attach(img)

    # Sending email to all recipients
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(from_addr=my_email, to_addrs=emails, msg=msg.as_string())


    return "Emails and WhatsApp message sent successfully!"

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
