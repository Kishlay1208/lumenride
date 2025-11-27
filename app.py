from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(message="LumenRide service online for CIE set 55")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
