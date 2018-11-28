import time
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
    response = {
        "error": "Parameter missing",
        "message": "You've not added required query parameter *q* with the word",
        "allowed_params": {
            "q": {
                "type": "required",
                "value": "string",
                "desc": "word to auto complete"
            },
            "n": {
                "type": "optional",
                "value": "positive integer",
                "desc": "number of auto complete suggestions to return"
            }
        }
    }
    if user_input:
        try:
            start = time.time()
            num_words = int(request.args.get('n')) if request.args.get('n') else 25
            response = suggester.suggest_for(user_input, num_words)
            end = time.time()
            time_taken = (end - start) * 1000
            return jsonify({'time_taken': str(round(time_taken, 2)) + 'ms', 'total': len(response), 'suggestions': response}), 200
        except ValueError:
            return jsonify({"error": "Input is invalid"}), 422
    else:
        return jsonify(response), 400


if __name__ == '__main__':
    app.run()
