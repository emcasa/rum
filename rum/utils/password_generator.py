import secrets
import string

special_char = '-_=.'


class Password:

    def __init__(self, length=20, minimal_length=15):
        self.minimal_length = minimal_length
        self.length = length
        self.str = self.generate()

    def is_length_valid(self, length):
        """
        Checks if the length of password is valid
        :param length: <int>
        :return: <bool>
        """
        if length < 5:
            raise ValueError('Password length must be at least 5 digits.')
        elif length < self.minimal_length:
            raise ValueError('Password length was defined to be at least {} digits.'.format(self.minimal_length))
        return True

    @staticmethod
    def is_characters_valid(password):
        """
        Get a password and chek if it has at least one lowercase,
        one uppercase, one digit and one special character.
        :param password: <string>
        :return: <bool>
        """
        if not any(c in password for c in special_char):
            return False
        if not any(c.isdigit() for c in password):
            return False
        if not any(c.islower() for c in password):
            return False
        if not any(c.isupper() for c in password):
            return False
        return True

    def generate(self):
        """
        Creates random password
        """

        alphabet = string.ascii_letters + string.digits + special_char
        password = ''
        while not self.is_characters_valid(password):
            password = ''.join(secrets.choice(alphabet) for idx in range(self.length))

        self.is_length_valid(len(password))

        return password

    def __str__(self):
        return self.generate()
