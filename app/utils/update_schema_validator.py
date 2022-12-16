import re

regex_name = r'([A-Za-z]*\s?)*'
regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class UpdateSchemaValidator(object):
    def __init__(self, response={}):
        self.response = response

    def isTrue(self):
        error_messages = []

        try:
            name = self.response.get('name')
            if name is not None and not re.fullmatch(regex_name, name):
                raise Exception('Error')
        except Exception:
            error_messages.append('Name cannot be special characters!')

        try:
            email = self.response.get('email')
            if email is not None and not re.fullmatch(regex_email, email):
                raise Exception('Error')
        except Exception:
            error_messages.append('Email has to be a valid email!')

        try:
            phone = self.response.get('phone', None)
            if (
                phone is not None
                and (
                    len(phone) < 10
                    or len(phone) > 13
                    or not phone.isnumeric()
                )
            ):
                raise Exception('Error')
        except Exception:
            error_messages.append(
                'Phone has to be a valid phone number (10-13 digits)!'
            )

        try:
            address = self.response.get('address')
            if address is not None and len(address) <= 1:
                raise Exception('Error')
        except Exception:
            error_messages.append('Address is required!')

        try:
            salary = self.response.get('salary')
            if salary is not None and salary <= 0:
                raise Exception('Error')
        except Exception:
            error_messages.append('Salary has to be a positive value!')

        try:
            ktp = self.response.get('ktp')
            if ktp is not None and (len(ktp) != 16 or not ktp.isnumeric()):
                raise Exception('Error')
        except Exception:
            error_messages.append('KTP has to be 16 digits!')

        try:
            npwp = self.response.get('npwp')
            if npwp is not None and (len(npwp) != 16 or not npwp.isnumeric()):
                raise Exception('Error')
        except Exception:
            error_messages.append('NPWP has to be 16 digits!')

        return error_messages
