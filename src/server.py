from flask import Flask
from werkzeug.utils import find_modules, import_string

def create_app(config=None):
    app =  Flask(__name__)
    app.config.update(config or {})
    register_blueprints(app)
    #regiter_other_things(app
    return app


def register_blueprints(app):
    for name in find_modules('gt.blueprints'):
        mod = import_string('name')
        if hasattr(mod, 'blueprint'):
            app.register_blueprint(mod.blueprint)


class GainTraider(object):

    def __init__(self, config):
        self.flask_app = create_app(config)
        self.flask_app.gainTrader = self

    def __call__(self, environ, start_respnse):
        return self.flask_app(environ, start_respnse)

if __name__ == '__main__':
    config = {}
    print("Running :)")
    gainTrader = GainTraider(config)
