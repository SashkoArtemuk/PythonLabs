from flask import Flask
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route('/api/v1/hello-world-<id>')
def hello_world(id):
    return 'Hello World - '+str(id)


http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
