import sendgrid
import os
from sendgrid.helpers.mail import *
from python_http_client.exceptions import UnauthorizedError


class SendGrid():
    def __init__(self, to_email_addr):
        self.to_email_addr = to_email_addr
        self.send_grid_api = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        self.from_email = Email(os.environ.get('FROM_EMAIL_ADDR', 'test@test.com'))

    def _send_basetext_email(self, subject_txt, content_txt):
        """
        Uses SendGrid API to send a text email with given content and subject
        :param subject_txt: <string>
        :param content_txt: <string>
        :return: <int> status_code
        """

        to_email = Email(self.to_email_addr)
        subject = subject_txt
        content = Content("text/plain", content_txt)
        mail = Mail(self.from_email, subject, to_email, content)

        try:
            response = self.send_grid_api.client.mail.send.post(request_body=mail.get())
        except UnauthorizedError as error:
            raise Exception('If you do not wish to send email to users, '
                            'then set RedshiftUserManagement(send_mail=False). '
                            'Otherwise, set the correct environmental variables.', error)

        if response >= 300:
            print('Failed to send email')

        return response.status_code

    def send_usercreated_mail(self, user, password):
        """
        Send email to a user informing credentials and password.
        :param user: <string>
        :param password: <string>
        :return: <int> status_code
        """
        subject = 'Credentials for account - {} Redshift'.format(os.environ.get('COMPANY_NAME', 'My Company'))

        content = open('utils/templates/user_created.txt', encoding='utf-8').read()
        content = content.format(os.environ.get('COMPANY_NAME', 'My Company'),
                                 os.environ.get('HOST', 'localhost'),
                                 os.environ.get('PORT', 5439),
                                 os.environ.get('DBNAME', 'database'),
                                 user,
                                 password)

        return self._send_basetext_email(subject, content)
