# backend/routes/site.py
from flask import Blueprint, jsonify
from utils.db import get_db_connection

site_bp = Blueprint('site', __name__)

@site_bp.route('/', methods=['GET'])
def get_sites():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, latitude, longitude, parentOrgId FROM site')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Convert list of tuples to list of dictionaries
    sites = [
        {"id": row[0], "name": row[1], "latitude": row[2], "longitude": row[3], "parentOrgId": row[4]}
    for row in rows]
    
    return jsonify(sites)