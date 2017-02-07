import pycurl
from urllib.parse import urlencode

base_url = 'http://54.152.49.226:7000/api/v1/'
c = pycurl.Curl()

def post():
    c.setopt(c.URL, base_url + 'register')
    post_data = {'username' : 'technovendors',
                 'password' : 'helloworld',
                 'fullname' : 'Hello World'}
    # Form data must be provided already urlencoded.
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()
    # HTTP response code, e.g. 200.
    print('Status: %d' % c.getinfo(c.RESPONSE_CODE))

post()
c.close()
