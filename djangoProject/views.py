from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

# Email server settings
smtp_server = 'smtp.gmail.com'  # Replace with your SMTP server address
smtp_port = 587  # Replace with your SMTP server port
smtp_username = 'platform.smartestprep@gmail.com'
smtp_password = 'zhjxijsfukihtwec'


@csrf_exempt
def send_emails(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email_address = data.get('email')
        mock_link = "https://chat.openai.com/?model=text-davinci-002-render-sha"

        if email_address:
            # Email content
            subject = 'Important Information'
            message_text = 'Dear Student, ' \
                           f'\nThis is the link to IELTS mock test with proctoring system: <a href="{mock_link}">Click start mock</a>' \
                           '\n The duration is 3 hours. You are allowed to have breaks. ' \
                           '\nSubmission deadline is Sunday 12am. \n' \
                           'Good luck, \n' \
                           'STP team'

            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = email_address
            msg['Subject'] = subject
            msg.attach(MIMEText(message_text, 'plain'))

            # Connect to the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Use TLS encryption

            # Log in to the SMTP server
            server.login(smtp_username, smtp_password)

            # Send the email
            server.sendmail(smtp_username, email_address, msg.as_string())

            # Disconnect from the SMTP server
            server.quit()

            return JsonResponse({'message': f'Email sent to {email_address}'}, status=200)
        else:
            return JsonResponse({'message': 'Email address not provided'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
