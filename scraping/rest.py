import pycurl
from io import BytesIO
from urllib.parse import urlencode

base_url = 'http://54.152.49.226:7000'

def register(username, password, fullname):
    c = pycurl.Curl()
    c.setopt(c.URL, base_url + '/auth/register')
    post_data = {'username' : username,
                 'password' : password,
                 'fullname' : fullname}
    # Form data must be provided already urlencoded.
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()
    # HTTP response code, e.g. 200.
    print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
    c.close()


def login(username, password):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, base_url + '/auth/login')
    post_data = {'username' : username,
                 'password' : password}
    postfields = urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
    c.close()

    body = buffer.getvalue()
    print(body.decode('iso-8859-1'))

#login('technovendors','helloworld')

