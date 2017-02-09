import pycurl
from io import BytesIO
from urllib.parse import urlencode

base_url = 'http://54.152.49.226:7000/'

def post(url, postfields, headers = {}):
    headers = ["%s: %s" % (key, val) for key, val in headers.items()]
    buffer = BytesIO()

    c = pycurl.Curl()
    c.setopt(c.HTTPHEADER, headers)
    c.setopt(c.URL, base_url + url)
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
    c.close()
    return buffer
    

def get(url, token):
    headers = ["x-access-token: " + token]
    buffer = BytesIO()
    
    c = pycurl.Curl()
    c.setopt(c.HTTPHEADER, headers)
    c.setopt(c.URL, base_url + url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
    c.close()
    print(buffer.getvalue().decode('iso-8859-1'))
    

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
    data = body.decode('iso-8859-1').split(',')[-1].split(':')[1][1:-2]
    return data

#token = login('bond007', 'spectre')
#get('me', token)
