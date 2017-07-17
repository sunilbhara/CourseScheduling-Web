from flask import Flask

from CourseScheduling.blueprints.page import page
from CourseScheduling.blueprints.schedule import schedule
from CourseScheduling.extensions import debug_toolbar, db, mongoInterface, admin

def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    app.register_blueprint(page)
    app.register_blueprint(schedule)
    extensions(app)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    debug_toolbar.init_app(app)
    db.init_app(app)
    admin.init_app(app)
    from CourseScheduling.blueprints.admin.views import CourseView, Course, Requirement, RequirementView
    admin.add_view(CourseView(Course))
    admin.add_view(RequirementView(Requirement))

    app.session_interface = mongoInterface
    return None
