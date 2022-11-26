from app.gerbil_wrapper_service import wrapper_service_bp
from flask import Flask 

configfile = "app.conf"

healthendpoint = "/health"
aboutendpoint = "/about"

app = Flask(__name__)
app.register_blueprint(wrapper_service_bp)

@app.route(healthendpoint, methods=["GET"])
def health():
    return "alive"

@app.route(aboutendpoint, methods=["GET"])
def about():
    return "about"

