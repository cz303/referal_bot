import flask
from hashlib import md5

app = flask.Flask(__name__)
fk_ips = ['136.243.38.147', '136.243.38.149', '136.243.38.150', '136.243.38.151', '136.243.38.189', '88.198.88.98']
pay_sign = md5('SECRET'.encode('utf-8')).hexdigest()

@app.route('/', methods=['POST', 'GET'])
def process_request():
    print(check_pay(flask.request.access_route[0], flask.request.values['SIGN']))
    return 'YES'


def check_pay(ip, sign):
    return ip in fk_ips and sign == pay_sign

if __name__ == '__main__':
    app.threading = True
    app.run(host='185.252.213.57', debug=True)

