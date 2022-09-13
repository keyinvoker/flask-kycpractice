import re

regex_name = r'([A-Za-z]*\s?)*'
regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class RegisterSchemaValidator(object):
    def __init__(self, response={}):
        self.response = response

    def isTrue(self):
        error_messages = []

        try:
            name = self.response.get('name')
            if name is None or not re.fullmatch(regex_name, name):
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Name is required and cannot be special characters!')
            
        try:
            email = self.response.get('email')
            if email is None or not re.fullmatch(regex_email, email):
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Email has to be a valid email!')
        
        try:
            phone = self.response.get('phone', None)
            if phone is None or len(phone)<10 or len(phone)>13 or phone.isnumeric()==False:
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Phone has to be a valid phone number (10-13 digits)!')
        
        try:
            address = self.response.get('address')
            if address is None or len(address)<=1:
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Address is required!')
        
        try:
            salary = int(self.response.get('salary'))
            if salary is None or salary==0:
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Salary field is required!')
        
        try:
            ktp = self.response.get('ktp')
            if ktp is None or len(ktp)!=16 or ktp.isnumeric()==False:
                raise Exception('Error')
        except Exception as e:
            error_messages.append('KTP has to be 16 digits!')
        
        try:
            npwp = self.response.get('npwp')
            if npwp is None or len(npwp)!=16 or npwp.isnumeric()==False:
                raise Exception('Error')
        except Exception as e:
            error_messages.append('NPWP has to be 16 digits!')

        return error_messages

class UpdateSchemaValidator(object):
    def __init__(self, response={}):
        self.response = response

    def isTrue(self):
        error_messages = []

        try:
            name = self.response.get('name')
            if not name is None and not re.fullmatch(regex_name, name):
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Name cannot be special characters!')
            
        try:
            email = self.response.get('email')
            if not email is None and not re.fullmatch(regex_email, email):
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Email has to be a valid email!')
        
        try:
            phone = self.response.get('phone', None)
            if not phone is None and (len(phone)<10 or len(phone)>13 or phone.isnumeric()==False):
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Phone has to be a valid phone number (10-13 digits)!')
        
        try:
            address = self.response.get('address')
            if not address is None and len(address)<=1:
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Address is required!')
        
        try:
            salary = self.response.get('salary')
            if not salary is None and salary<=0:
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Salary has to be a positive value!')
        
        try:
            ktp = self.response.get('ktp')
            if not ktp is None and (len(ktp)!=16 or ktp.isnumeric()==False):
                raise Exception('Error')
        except Exception as e:
            error_messages.append('KTP has to be 16 digits!')
        
        try:
            npwp = self.response.get('npwp')
            if not npwp is None and (len(npwp)!=16 or npwp.isnumeric()==False):
                raise Exception('Error')
        except Exception as e:
            error_messages.append('NPWP has to be 16 digits!')

        return error_messages