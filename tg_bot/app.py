from flask import Flask, jsonify

from bot_main import generate_daily_password

app = Flask(__name__)


@app.route('/daily-password', methods=['GET'])
def get_daily_password():
    daily_password = generate_daily_password()
    return jsonify({'password': daily_password})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
