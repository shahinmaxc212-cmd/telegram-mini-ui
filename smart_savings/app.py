import os
from flask import Flask
from database.db import init_db
from routes.home    import home_bp
from routes.deposit import deposit_bp
from routes.support import support_bp
from routes.admin   import admin_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(deposit_bp)
app.register_blueprint(support_bp)
app.register_blueprint(admin_bp)

# Initialise database on startup
with app.app_context():
    init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
