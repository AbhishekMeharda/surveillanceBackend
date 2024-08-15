import psycopg2
from config import config

def get_db_connection():
    conn = psycopg2.connect(
        host=config.DB_HOST,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )
    return conn

def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS organisation (
            id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(255),
            shortcode VARCHAR(10)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS site (
            id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(255),
            latitude FLOAT,
            longitude FLOAT,
            parentOrgId VARCHAR(10),
            FOREIGN KEY (parentOrgId) REFERENCES organisation(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS visit (
            id VARCHAR(10) PRIMARY KEY,
            diseases VARCHAR(255),
            date DATE,
            parentSiteId VARCHAR(10),
            FOREIGN KEY (parentSiteId) REFERENCES site(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS sample (
            type VARCHAR(50),
            subtype VARCHAR(50),
            barcode VARCHAR(50) PRIMARY KEY,
            visitId VARCHAR(10),
            FOREIGN KEY (visitId) REFERENCES visit(id)
        )
        """
    ]
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
        cursor.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_data():
    organisation_data = [
        ('ORG001', 'Gujarat Biotech Research Centre', 'GBRC'),
        ('ORG002', 'Centre for Ceullular and Molecular Biology', 'CCMB'),
        ('ORG003', 'National Chemical Laboratory', 'NCL'),
        ('ORG004', 'Pune Knowledge Cluster', 'PKC'),
        ('ORG005', 'AI & Robotics Technology Park', 'ARTPARK'),
        ('ORG006', 'Tata Institute for Genetics & Society', 'TIGS')
    ]
    site_data = [
        ('SIT001', 'Gopi Dairy Farms, Ranasan', 23.114034, 72.681215, 'ORG001'),
        ('SIT002', 'Makarba Poultry Farm Govt of Gujarat', 22.998293, 72.508676, 'ORG001')
    ]
    sample_data = [
        ('Clinical', 'Saliva', 'G-2407-C-F-01-01', 'VIS001'),
        ('Clinical', 'Urine', 'G-2407-C-F-01-02', 'VIS001'),
        ('Environmental', 'Dung', 'G-2407-E-F-01-01', 'VIS001'),
        ('Environmental', 'Feed', 'G-2407-E-F-01-02', 'VIS001'),
        ('Environmental', 'Slurry', 'G-2407-E-F-01-03', 'VIS001'),
        ('Environmental', 'Dung Pile', 'G-2407-E-F-01-04', 'VIS001'),
        ('Environmental', 'Fecal', 'G-2407-E-A-02-01', 'VIS002'),
        ('Environmental', 'Feather', 'G-2407-E-A-02-02', 'VIS002'),
        ('Environmental', 'Litre', 'G-2407-E-A-02-03', 'VIS002'),
        ('Environmental', 'Drinking Water', 'G-2407-E-A-02-04', 'VIS002'),
        ('Environmental', 'Feed', 'G-2407-E-A-02-05', 'VIS002')
    ]
    visit_data = [
        ('VIS001', 'FMDV, LSDV', '2024-07-30', 'SIT001'),
        ('VIS002', 'Avian Influenza', '2024-07-30', 'SIT002')
    ]
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO organisation (id, name, shortcode) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING", organisation_data)
        cursor.executemany("INSERT INTO site (id, name, latitude, longitude, parentOrgId) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING", site_data)
        cursor.executemany("INSERT INTO visit (id, diseases, date, parentSiteId) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING", visit_data)
        cursor.executemany("INSERT INTO sample (type, subtype, barcode, visitId) VALUES (%s, %s, %s, %s) ON CONFLICT (barcode) DO NOTHING", sample_data)
        cursor.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()