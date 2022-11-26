from app import app
import os


SERVICE_PORT = os.environ['SERVICE_PORT']


if __name__ == "__main__":
    app.run(debug=True, port=SERVICE_PORT)
