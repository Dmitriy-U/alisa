from flask import Flask, request, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST"])
def alisa_command_handler():
    print("-->", request.json)
    response = make_response(
        {
            "status": "ok"
        },
        200
    )
    return response
