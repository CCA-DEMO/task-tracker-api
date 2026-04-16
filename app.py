from flask import Flask, jsonify
from models import db, Task


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/health")
    def health():
        return {"status": "ok"}

    @app.route("/tasks")
    def get_tasks():
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
