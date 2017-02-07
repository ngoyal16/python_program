import pycurl
from io import BytesIO
from urllib.parse import urlencode

base_url = 'http://54.152.49.226:7000/'

def post(url, postfields):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, base_url + url)
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
    c.close()
    return buffer
    

def register(username, password, fullname):
    post_data = {'username' : username,
                 'password' : password,
                 'fullname' : fullname}
    postfields = urlencode(post_data)

    post('auth/register', postfields)


def login(username, password):
    post_data = {'username' : username,
                 'password' : password}
    postfields = urlencode(post_data)
    body = post('auth/login', postfields).getvalue()
    print(body.decode('iso-8859-1'))

#login('technovendors','helloworld')

