# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

class text:
    def __init__(self, message, number):
        self.message = message
        self.number = number

    def main(self):
        # Your Account Sid and Auth Token from twilio.com/console
        # DANGER! This is insecure. See http://twil.io/secure
        account_sid = 'ACea8786990058ddc73047b144e7e3b5df'
        auth_token = '60730010a28a1cabaf43081b83c7b67c'
        client = Client(account_sid, auth_token)
        m = client.messages.create(
        body='{}'.format(self.message),
        from_='[+][1][4792501916]',
        to='[+][1][{}]'.format(self.number)
        )
        return(m.sid)

