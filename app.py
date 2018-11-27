from flask import Flask
from flask import jsonify
from flask import request
from lib.Suggester import Suggester

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

suggester = Suggester()


@app.route("/")
def suggest():
    user_input = request.args.get('q')
    s = set()
    if user_input:
        num_words = request.args.get('n') if request.args.get('n') else 250
        s = suggester.suggest_for(user_input, num_words)
    return jsonify({'total': len(s), 'suggestions': s})


if __name__ == '__main__':
    app.run()
