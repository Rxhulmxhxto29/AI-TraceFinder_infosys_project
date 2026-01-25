import sqlite3

conn = sqlite3.connect('data/analysis_history.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print('Tables:', tables)

if 'scanner_analysis' in tables:
    cursor.execute('SELECT COUNT(*) FROM scanner_analysis')
    print('Records in scanner_analysis:', cursor.fetchone()[0])
