from django.test import TestCase

import base64
import json


# Create your tests here.


paquete = {
    'firstname': 'William',
    'lastname': 'Rodriguez',
    'email': 'williamrodriguez@fcv.org'
}

bytesPaquete = bytes(json.dumps(paquete), 'utf-8')


#encode

encode = base64.urlsafe_b64encode(bytesPaquete)

# decode

decode = base64.urlsafe_b64decode(encode).decode('utf-8')
print(decode)


