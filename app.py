from flask import Flask, jsonify, request
from models import db, Task


def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
    if config:
        app.config.update(config)
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

    @app.route("/tasks", methods=["POST"])
    def create_task():
        data = request.get_json()
        if not data or not data.get("title"):
            return jsonify({"error": "title is required"}), 400
        task = Task(
            title=data["title"],
            description=data.get("description", ""),
        )
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
