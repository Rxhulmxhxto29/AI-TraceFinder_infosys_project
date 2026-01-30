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
    
    def _get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
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
                notes TEXT DEFAULT '',
                timestamp DATETIME DEFAULT (datetime('now', 'localtime')),
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
                notes TEXT DEFAULT '',
                timestamp DATETIME DEFAULT (datetime('now', 'localtime')),
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
                notes TEXT DEFAULT '',
                timestamp DATETIME DEFAULT (datetime('now', 'localtime')),
                results_json TEXT
            )
        ''')
        
        # Add notes column to existing tables if it doesn't exist
        try:
            cursor.execute("ALTER TABLE scanner_analysis ADD COLUMN notes TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        try:
            cursor.execute("ALTER TABLE comparisons ADD COLUMN notes TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE tampering_checks ADD COLUMN notes TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass
        
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
                results.get('scanner_brand', 'Unknown'),
                results.get('scanner_model', 'Unknown'),
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
            
            # Try with notes column first
            try:
                cursor.execute('''
                    SELECT id, filename, detected_brand, detected_model, 
                           confidence, timestamp, notes
                    FROM scanner_analysis
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
                
                rows = cursor.fetchall()
                conn.close()
                
                return [{
                    'id': row[0],
                    'filename': row[1],
                    'scanner_brand': row[2],
                    'scanner_model': row[3],
                    'confidence': row[4],
                    'timestamp': row[5],
                    'notes': row[6] or ''
                } for row in rows]
            except sqlite3.OperationalError:
                # Fallback without notes column
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
                    'scanner_brand': row[2],
                    'scanner_model': row[3],
                    'confidence': row[4],
                    'timestamp': row[5],
                    'notes': ''
                } for row in rows]
            
        except Exception as e:
            print(f"Error fetching analyses: {e}")
            return []
    
    def get_recent_comparisons(self, limit=10):
        """Get recent comparisons"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Try with notes column first
            try:
                cursor.execute('''
                    SELECT id, file1_name, file2_name, similarity_score, 
                           match_status, timestamp, notes
                    FROM comparisons
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
                
                rows = cursor.fetchall()
                conn.close()
                
                return [{
                    'id': row[0],
                    'filename1': row[1],
                    'filename2': row[2],
                    'similarity_score': row[3],
                    'match_status': row[4],
                    'timestamp': row[5],
                    'notes': row[6] or ''
                } for row in rows]
            except sqlite3.OperationalError:
                # Fallback without notes column
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
                    'filename1': row[1],
                    'filename2': row[2],
                    'similarity_score': row[3],
                    'match_status': row[4],
                    'timestamp': row[5],
                    'notes': ''
                } for row in rows]
            
        except Exception as e:
            print(f"Error fetching comparisons: {e}")
            return []
    
    def get_recent_tampering_checks(self, limit=10):
        """Get recent tampering checks"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Try with notes column first
            try:
                cursor.execute('''
                    SELECT id, filename, tampering_detected, confidence, 
                           risk_level, timestamp, notes
                    FROM tampering_checks
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
                
                rows = cursor.fetchall()
                conn.close()
                
                return [{
                    'id': row[0],
                    'filename': row[1],
                    'is_tampered': bool(row[2]),
                    'confidence': row[3],
                    'risk_level': row[4],
                    'timestamp': row[5],
                    'notes': row[6] or ''
                } for row in rows]
            except sqlite3.OperationalError:
                # Fallback without notes column
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
                    'is_tampered': bool(row[2]),
                    'confidence': row[3],
                    'risk_level': row[4],
                    'timestamp': row[5],
                    'notes': ''
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
            
            # Calculate total records (all types combined)
            total_records = total_analyses + total_comparisons + total_tampering
            
            return {
                'total_analyses': total_analyses,
                'total_comparisons': total_comparisons,
                'total_tampering_checks': total_tampering,
                'total_records': total_records,
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
    
    def delete_analysis(self, analysis_id, analysis_type='scanner'):
        """Delete a specific analysis record"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if analysis_type == 'scanner':
                cursor.execute('DELETE FROM scanner_analysis WHERE id = ?', (analysis_id,))
            elif analysis_type == 'comparison':
                cursor.execute('DELETE FROM comparisons WHERE id = ?', (analysis_id,))
            elif analysis_type == 'tampering':
                cursor.execute('DELETE FROM tampering_checks WHERE id = ?', (analysis_id,))
            
            conn.commit()
            deleted = cursor.rowcount > 0
            conn.close()
            
            return deleted
            
        except Exception as e:
            print(f"Error deleting analysis: {e}")
            return False
    
    def clear_all_history(self, analysis_type=None):
        """Clear all history records of a specific type or all types"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if analysis_type == 'scanner':
                cursor.execute('DELETE FROM scanner_analysis')
            elif analysis_type == 'comparison':
                cursor.execute('DELETE FROM comparisons')
            elif analysis_type == 'tampering':
                cursor.execute('DELETE FROM tampering_checks')
            else:
                # Clear all
                cursor.execute('DELETE FROM scanner_analysis')
                cursor.execute('DELETE FROM comparisons')
                cursor.execute('DELETE FROM tampering_checks')
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False    
    def update_notes(self, analysis_id, analysis_type, notes):
        """Update notes for a specific analysis"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if analysis_type == 'scanner':
                cursor.execute('UPDATE scanner_analysis SET notes = ? WHERE id = ?', (notes, analysis_id))
            elif analysis_type == 'comparison':
                cursor.execute('UPDATE comparisons SET notes = ? WHERE id = ?', (notes, analysis_id))
            elif analysis_type == 'tampering':
                cursor.execute('UPDATE tampering_checks SET notes = ? WHERE id = ?', (notes, analysis_id))
            else:
                return False
            
            conn.commit()
            updated = cursor.rowcount > 0
            conn.close()
            
            return updated
            
        except Exception as e:
            print(f"Error updating notes: {e}")
            return False
    
    def get_notes(self, analysis_id, analysis_type):
        """Get notes for a specific analysis"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if analysis_type == 'scanner':
                cursor.execute('SELECT notes FROM scanner_analysis WHERE id = ?', (analysis_id,))
            elif analysis_type == 'comparison':
                cursor.execute('SELECT notes FROM comparisons WHERE id = ?', (analysis_id,))
            elif analysis_type == 'tampering':
                cursor.execute('SELECT notes FROM tampering_checks WHERE id = ?', (analysis_id,))
            else:
                return None
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else ''
            
        except Exception as e:
            print(f"Error getting notes: {e}")
            return None