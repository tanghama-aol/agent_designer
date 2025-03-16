from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from controllers.component_controller import component_bp
from controllers.workflow_controller import workflow_bp
from controllers.settings_controller import settings_bp

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
CORS(app)
db.init_app(app)

# 注册蓝图
app.register_blueprint(component_bp, url_prefix='/api/components')
app.register_blueprint(workflow_bp, url_prefix='/api/workflows')
app.register_blueprint(settings_bp, url_prefix='/api/settings')

@app.route('/')
def index():
    return "Agent编辑器后台API服务"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)