from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    
    from ConflictionWarnings.routes import blueprint as conflict_blueprint
    from ChatBot.routes import blueprint as chatbot_blueprint

    app.register_blueprint(conflict_blueprint, url_prefix='/conflict')
    app.register_blueprint(chatbot_blueprint, url_prefix='/chatbot')

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)