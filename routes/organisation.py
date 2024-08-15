# backend/routes/organisation.py
from flask import Blueprint, jsonify
from utils.db import get_db_connection

organisation_bp = Blueprint('organisation', __name__)

@organisation_bp.route('/', methods=['GET'])
def get_organisations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, shortcode FROM organisation')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert list of tuples to list of dictionaries
    organisations = [
        {"id": row[0], "name": row[1], "shortcode": row[2]}
    for row in rows]

    return jsonify(organisations)