from flask import Blueprint

def register_routes(app):
    from .users import users_bp
    from .auth import auth_bp
    from .products.rackets import rackets_bp
    from .products.shoes import shoes_bp
    from .products.shuttlecocks import shuttlecocks_bp

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(rackets_bp, url_prefix='/rackets')
    app.register_blueprint(shoes_bp, url_prefix='/shoes')
    app.register_blueprint(shuttlecocks_bp, url_prefix='/shuttlecocks')
