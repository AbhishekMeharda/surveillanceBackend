# backend/routes/sample.py
from flask import Blueprint, jsonify
from utils.db import get_db_connection

sample_bp = Blueprint('sample', __name__)

@sample_bp.route('/', methods=['GET'])
def get_samples():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT type, subtype, barcode, visitId FROM sample')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert list of tuples to list of dictionaries
    samples = [
        {"type": row[0], "subtype": row[1], "barcode": row[2], "visitId": row[3]}
    for row in rows]

    return jsonify(samples)