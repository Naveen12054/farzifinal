from twilio.rest import Client

def send_sms(recipient_number, message):
    # Your Twilio credentials
    account_sid = 'ACdd73defbb24e5f653611d4906eafff25'
    auth_token = 'cf333437aa65df405dbbb2b9c4d6c719'

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    try:
        # Send SMS message
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body='Your Booking has been successful',
            to='whatsapp:+916282519724'
        )
        print("Message sent successfully:", message.sid)
        return True
    except Exception as e:
        print("Failed to send message:", str(e))
        return False