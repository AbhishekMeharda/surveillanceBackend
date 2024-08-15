# backend/routes/visit.py
from flask import Blueprint, jsonify
from utils.db import get_db_connection

visit_bp = Blueprint('visit', __name__)

@visit_bp.route('/', methods=['GET'])
def get_visit_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, diseases, date, parentSiteId FROM visit')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert list of tuples to list of dictionaries
    visits = [
        {"id": row[0], "diseases": row[1], "date": row[2], "parentSiteId": row[3]}
    for row in rows]

    return jsonify(visits)