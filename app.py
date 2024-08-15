from flask import Flask
from flask_cors import CORS
from routes.organisation import organisation_bp
from routes.site import site_bp
from routes.sample import sample_bp
from routes.visit import visit_bp
from utils.db import create_tables, insert_data

app = Flask(__name__)
CORS(app)

# Create tables and insert data
create_tables()
insert_data()

app.register_blueprint(organisation_bp, url_prefix='/api/organisation')
app.register_blueprint(site_bp, url_prefix='/api/site')
app.register_blueprint(sample_bp, url_prefix='/api/sample')
app.register_blueprint(visit_bp, url_prefix='/api/visit')

if __name__ == '__main__':
    app.run(debug=True)