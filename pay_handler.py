import flask
from bot_time import get_time, month
from core import pay_success, menu_f, write_to_bot_2_f
from airtabledb import set_first_pay_date, set_pay_date
import bot_time

import db

app = flask.Flask(__name__)
fk_ips = ['136.243.38.147', '136.243.38.149', '136.243.38.150', '136.243.38.151', '136.243.38.189', '88.198.88.98']


@app.route('/', methods=['POST', 'GET'])
def process_request():
    if flask.request.access_route[0] not in fk_ips:
        flask.abort(403)
    user_id = db.get_user_by_pay_sign(flask.request.values['SIGN'])
    if user_id is None:
        flask.abort(422)
    if db.is_first_pay(user_id):
        pay_success(user_id, True)
        db.set_expire(user_id, get_time() + month)
        write_to_bot_2_f(id=user_id)
        set_first_pay_date(db.get_at_id(user_id), bot_time.get_isoformat_date())
    else:
        pay_success(user_id, False)
        db.set_expire(user_id, db.get_expiration_time(user_id) + month)
        menu_f(id=user_id)
        set_pay_date(db.get_at_id(user_id), bot_time.get_isoformat_date())
    return 'YES'


def payment_handler_loop():
    app.threading = True
    app.run(host='185.252.213.57')
