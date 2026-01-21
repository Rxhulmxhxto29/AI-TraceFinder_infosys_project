import sqlite3
import json
from datetime import datetime
import os

class AnalysisHistory:
    """Manage analysis history database"""
    
    def __init__(self, db_path='data/analysis_history.db'):
        self.db_path = db_path
        self._ensure_db_directory()
        self._initialize_database()
    
    def _ensure_db_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _initialize_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scanner_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_size INTEGER,
                analysis_type TEXT NOT NULL,
                detected_brand TEXT,
                detected_model TEXT,
                confidence REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                results_json TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comparisons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file1_name TEXT NOT NULL,
                file2_name TEXT NOT NULL,
                similarity_score REAL,
                match_status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                results_json TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tampering_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                tampering_detected BOOLEAN,
                confidence REAL,
                risk_level TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                results_json TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_scanner_analysis(self, filename, file_size, results):
        """Add scanner analysis record"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO scanner_analysis 
                (filename, file_size, analysis_type, detected_brand, detected_model, 
                 confidence, results_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                filename,
                file_size,
                'scanner_detection',
                results.get('scanner', {}).get('brand', 'Unknown'),
                results.get('scanner', {}).get('model', 'Unknown'),
                results.get('confidence', 0.0),
                json.dumps(results)
            ))
            
            conn.commit()
            record_id = cursor.lastrowid
            conn.close()
            
            return record_id
            
        except Exception as e:
            print(f"Error saving analysis: {e}")
            return None
    
    def add_comparison(self, file1, file2, results):
        """Add comparison record"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO comparisons 
                (file1_name, file2_name, similarity_score, match_status, results_json)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                file1,
                file2,
                results.get('overall_similarity', 0.0),
                results.get('match_status', 'Unknown'),
                json.dumps(results)
            ))
            
            conn.commit()
            record_id = cursor.lastrowid
            conn.close()
            
            return record_id
            
        except Exception as e:
            print(f"Error saving comparison: {e}")
            return None
    
    def add_tampering_check(self, filename, results):
        """Add tampering check record"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO tampering_checks 
                (filename, tampering_detected, confidence, risk_level, results_json)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                filename,
                results.get('tampering_detected', False),
                results.get('confidence', 0.0),
                results.get('risk_level', 'Low'),
                json.dumps(results)
            ))
            
            conn.commit()
            record_id = cursor.lastrowid
            conn.close()
            
            return record_id
            
        except Exception as e:
            print(f"Error saving tampering check: {e}")
            return None
    
    def get_recent_analyses(self, limit=10):
        """Get recent scanner analyses"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, filename, detected_brand, detected_model, 
                       confidence, timestamp
                FROM scanner_analysis
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [{
                'id': row[0],
                'filename': row[1],
                'brand': row[2],
                'model': row[3],
                'confidence': row[4],
                'timestamp': row[5]
            } for row in rows]
            
        except Exception as e:
            print(f"Error fetching analyses: {e}")
            return []
    
    def get_recent_comparisons(self, limit=10):
        """Get recent comparisons"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, file1_name, file2_name, similarity_score, 
                       match_status, timestamp
                FROM comparisons
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [{
                'id': row[0],
                'file1': row[1],
                'file2': row[2],
                'similarity': row[3],
                'status': row[4],
                'timestamp': row[5]
            } for row in rows]
            
        except Exception as e:
            print(f"Error fetching comparisons: {e}")
            return []
    
    def get_recent_tampering_checks(self, limit=10):
        """Get recent tampering checks"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, filename, tampering_detected, confidence, 
                       risk_level, timestamp
                FROM tampering_checks
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [{
                'id': row[0],
                'filename': row[1],
                'tampering_detected': bool(row[2]),
                'confidence': row[3],
                'risk_level': row[4],
                'timestamp': row[5]
            } for row in rows]
            
        except Exception as e:
            print(f"Error fetching tampering checks: {e}")
            return []
    
    def get_statistics(self):
        """Get overall statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total analyses
            cursor.execute('SELECT COUNT(*) FROM scanner_analysis')
            total_analyses = cursor.fetchone()[0]
            
            # Total comparisons
            cursor.execute('SELECT COUNT(*) FROM comparisons')
            total_comparisons = cursor.fetchone()[0]
            
            # Total tampering checks
            cursor.execute('SELECT COUNT(*) FROM tampering_checks')
            total_tampering = cursor.fetchone()[0]
            
            # Most common brands
            cursor.execute('''
                SELECT detected_brand, COUNT(*) as count 
                FROM scanner_analysis 
                GROUP BY detected_brand 
                ORDER BY count DESC 
                LIMIT 5
            ''')
            top_brands = [{'brand': row[0], 'count': row[1]} for row in cursor.fetchall()]
            
            # Tampering rate
            cursor.execute('SELECT COUNT(*) FROM tampering_checks WHERE tampering_detected = 1')
            tampered_count = cursor.fetchone()[0]
            tampering_rate = (tampered_count / total_tampering * 100) if total_tampering > 0 else 0
            
            conn.close()
            
            return {
                'total_analyses': total_analyses,
                'total_comparisons': total_comparisons,
                'total_tampering_checks': total_tampering,
                'top_brands': top_brands,
                'tampering_rate': round(tampering_rate, 2)
            }
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return None
    
    def search_by_filename(self, filename_pattern):
        """Search analyses by filename"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, filename, detected_brand, detected_model, 
                       confidence, timestamp
                FROM scanner_analysis
                WHERE filename LIKE ?
                ORDER BY timestamp DESC
            ''', (f'%{filename_pattern}%',))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [{
                'id': row[0],
                'filename': row[1],
                'brand': row[2],
                'model': row[3],
                'confidence': row[4],
                'timestamp': row[5]
            } for row in rows]
            
        except Exception as e:
            print(f"Error searching: {e}")
            return []
