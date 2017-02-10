from socketIO_client import SocketIO, BaseNamespace
import requests

key = 'key-d47971b31e4f183660b42cb709f788e4'
sandbox = 'sandbox922b9b0446fb4c688b1a284a8fa6b4c4.mailgun.org'


def sendmail(subject, message, recipient):
    request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(sandbox)
    request = requests.post(request_url, auth=('api', key), data={
        'from': "spark0396@gmail.com", #Can Be Any
        'to': recipient,
        'subject': subject,
        'text': message
    })
    print('Status: {0}'.format(request.status_code))
    print('Body:   {0}'.format(request.text))


#sendmail('Mail Function', 'Mail sent using Sendmail.', 'raghavpiet108@poornima.org')
#sendmail('Mail Function', 'Mail sent using Sendmail.', 'nitin.nitingoyal.goyal@gmail.com')

class Namespace(BaseNamespace):
	def on_connect(self):
		print('[Connected]')

	def on_reconnect(self):
		print('[Reconnected]')

	def on_disconnect(self):
		print('[Disconnected]')

def on_news_response(*args):
	sendmail('Mail Function', 'Mail sent using Sendmail.' + args, 'raghavpiet108@poornima.org')
	print('on_news_response', args)

socketIO = SocketIO('54.152.49.226', 7000, Namespace)
socketIO.on('news', on_news_response)
#socketIO.emit('news', {'xxx':'yyy'}, on_news_response)
socketIO.wait(seconds=100)
