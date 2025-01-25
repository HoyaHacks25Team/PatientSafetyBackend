from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register blueprints from each module
    from ConflictionWarnings.routes import blueprint as conflict_blueprint
    from pillModel.routes import blueprint as pillModel
    #from PillRecognition.routes import blueprint as pill_recognition_blueprint
    #from ChatBot.routes import blueprint as chatbot_blueprint

    app.register_blueprint(conflict_blueprint, url_prefix='/conflict')
    #app.register_blueprint(pill_recognition_blueprint, url_prefix='/pill')
    #app.register_blueprint(chatbot_blueprint, url_prefix='/chatbot')

    app.register_blueprint(pillModel, url_prefix='/predict')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)