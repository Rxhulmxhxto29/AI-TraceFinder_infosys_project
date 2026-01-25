from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from config import Config
from modules.image_processor import ImageProcessor
from modules.scanner_detector import ScannerDetector
from modules.report_generator import ReportGenerator
from modules.image_comparator import ImageComparator
from modules.tampering_detector import TamperingDetector
from modules.visualizer import FingerprintVisualizer
from modules.history import AnalysisHistory
from modules.pdf_report import PDFReportGenerator

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Initialize modules
image_processor = ImageProcessor()
scanner_detector = ScannerDetector()
report_generator = ReportGenerator()
image_comparator = ImageComparator()
tampering_detector = TamperingDetector()
visualizer = FingerprintVisualizer()
history = AnalysisHistory()
pdf_generator = PDFReportGenerator()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """Render about page"""
    return render_template('about.html')

@app.route('/history_page')
def history_page():
    """Render history page"""
    return render_template('history.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and analysis"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, TIFF, PDF'}), 400
        
        # Save file securely
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Process image
        try:
            processed_image = image_processor.load_and_preprocess(filepath)
            
            if processed_image is None:
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'error': 'Failed to process image. Please ensure it is a valid image file.'}), 400
            
            # Analyze and detect scanner
            analysis_results = scanner_detector.analyze(filepath)
            
            # Save to history
            history.add_scanner_analysis(filename, file.content_length or 0, analysis_results)
            
        except Exception as e:
            print(f"Error processing image: {e}")
            import traceback
            traceback.print_exc()
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Image processing failed: {str(e)}'}), 500
        
        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            'success': True,
            'results': analysis_results,
            'filename': filename,
            'timestamp': timestamp
        })
    
    except Exception as e:
        print(f"Upload error: {e}")
        import traceback
        traceback.print_exc()
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    """Perform detailed forensic analysis"""
    try:
        data = request.get_json()
        if not data or 'image_path' not in data:
            return jsonify({'error': 'No image path provided'}), 400
        
        # Perform comprehensive analysis
        results = scanner_detector.full_analysis(data['image_path'])
        
        return jsonify({
            'success': True,
            'analysis': results
        })
    
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/generate_report', methods=['POST'])
def generate_report():
    """Generate PDF report of analysis"""
    try:
        data = request.get_json()
        
        # Generate report using new PDF generator
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f'reports/TraceFinder_Report_{timestamp}.pdf'
        
        result = pdf_generator.generate_report(data, output_path)
        
        if result['success']:
            return send_file(
                result['report_path'],
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'TraceFinder_Report_{timestamp}.pdf'
            )
        else:
            return jsonify({'error': result['error']}), 500
    
    except Exception as e:
        return jsonify({'error': f'Report generation failed: {str(e)}'}), 500

@app.route('/download_pdf/<int:analysis_id>', methods=['GET'])
def download_pdf(analysis_id):
    """Download PDF report for a specific analysis from history"""
    try:
        # Get analysis from history
        conn = history._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT filename, results_json FROM scanner_analysis WHERE id = ?
        ''', (analysis_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'error': 'Analysis not found'}), 404
        
        # Parse results
        import json
        results = json.loads(row[1])
        results['filename'] = row[0]
        results['case_id'] = f'CASE-{analysis_id}'
        
        # Generate PDF
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f'reports/TraceFinder_Report_{analysis_id}_{timestamp}.pdf'
        
        result = pdf_generator.generate_report(results, output_path)
        
        if result['success']:
            return send_file(
                result['report_path'],
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'TraceFinder_Report_{analysis_id}.pdf'
            )
        else:
            return jsonify({'error': result['error']}), 500
    
    except Exception as e:
        return jsonify({'error': f'PDF generation failed: {str(e)}'}), 500

@app.route('/compare', methods=['POST'])
def compare_images():
    """Compare two images to check if from same scanner"""
    try:
        if 'image1' not in request.files or 'image2' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Two images required for comparison'
            }), 400
        
        file1 = request.files['image1']
        file2 = request.files['image2']
        
        if file1.filename == '' or file2.filename == '':
            return jsonify({
                'success': False,
                'error': 'Both files must be selected'
            }), 400
        
        if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
            return jsonify({
                'success': False,
                'error': 'Invalid file type'
            }), 400
        
        # Save both files
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], 'compare_' + filename1)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], 'compare_' + filename2)
        
        file1.save(filepath1)
        file2.save(filepath2)
        
        # Perform comparison
        result = image_comparator.compare_images(filepath1, filepath2)
        
        # Save to history
        if result.get('success'):
            history.add_comparison(filename1, filename2, result)
        
        # Clean up
        try:
            os.remove(filepath1)
            os.remove(filepath2)
        except:
            pass
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Comparison error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Comparison failed: {str(e)}'
        }), 500

@app.route('/detect_tampering', methods=['POST'])
def detect_tampering():
    """Detect image tampering"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type'
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'tamper_' + filename)
        file.save(filepath)
        
        # Detect tampering
        result = tampering_detector.detect_tampering(filepath)
        
        # Clean up
        try:
            os.remove(filepath)
        except:
            pass
        
        # Save to history
        history.add_tampering_check(file.filename, result)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Tampering detection error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Tampering detection failed: {str(e)}'
        }), 500

@app.route('/visualize', methods=['POST'])
def visualize_fingerprint():
    """Generate visual fingerprints"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type'
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'viz_' + filename)
        file.save(filepath)
        
        # Generate visualizations
        result = visualizer.generate_visualizations(filepath)
        
        # Clean up
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Visualization error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Visualization failed: {str(e)}'
        }), 500

@app.route('/history')
def get_history():
    """Get analysis history"""
    try:
        history_type = request.args.get('type', 'all')
        limit_param = request.args.get('limit', '10')
        
        # Handle 'all' or convert to int
        if limit_param == 'all':
            limit = 9999  # Large number to get all records
        else:
            limit = int(limit_param)
        
        data = {}
        
        if history_type in ['all', 'scanner']:
            data['analyses'] = history.get_recent_analyses(limit)
        
        if history_type in ['all', 'comparison']:
            data['comparisons'] = history.get_recent_comparisons(limit)
        
        if history_type in ['all', 'tampering']:
            data['tampering_checks'] = history.get_recent_tampering_checks(limit)
        
        if history_type == 'all':
            data['statistics'] = history.get_statistics()
        
        return jsonify({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        print(f"Error in get_history: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/history/delete/<int:record_id>', methods=['DELETE'])
def delete_history_record(record_id):
    """Delete a specific history record"""
    try:
        analysis_type = request.args.get('type', 'scanner')
        success = history.delete_analysis(record_id, analysis_type)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Record deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Record not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/history/clear', methods=['DELETE'])
def clear_history():
    """Clear all history records"""
    try:
        analysis_type = request.args.get('type', None)
        success = history.clear_all_history(analysis_type)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'History cleared successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to clear history'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/history/notes/<int:analysis_id>', methods=['PUT', 'GET'])
def manage_notes(analysis_id):
    """Get or update notes for an analysis"""
    try:
        analysis_type = request.args.get('type', 'scanner')
        
        if request.method == 'GET':
            notes = history.get_notes(analysis_id, analysis_type)
            return jsonify({
                'success': True,
                'notes': notes or ''
            })
        
        elif request.method == 'PUT':
            data = request.get_json()
            notes = data.get('notes', '')
            
            success = history.update_notes(analysis_id, analysis_type, notes)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Notes updated successfully'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Failed to update notes'
                }), 500
                
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/batch_upload', methods=['POST'])
def batch_upload():
    """Handle batch file upload"""
    try:
        if 'files' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No files provided'
            }), 400
        
        files = request.files.getlist('files')
        
        if not files or files[0].filename == '':
            return jsonify({
                'success': False,
                'error': 'No files selected'
            }), 400
        
        results = []
        temp_files = []
        
        # Analyze all files
        for file in files:
            if file and allowed_file(file.filename):
                try:
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f'batch_{timestamp}_{filename}')
                    file.save(filepath)
                    temp_files.append(filepath)
                    
                    # Analyze
                    analysis_result = scanner_detector.analyze(filepath)
                    
                    # Save to history
                    history.add_scanner_analysis(filename, file.content_length or 0, analysis_result)
                    
                    results.append({
                        'filename': filename,
                        'success': True,
                        'result': analysis_result
                    })
                        
                except Exception as e:
                    results.append({
                        'filename': file.filename,
                        'success': False,
                        'error': str(e)
                    })
        
        # Group results by scanner
        scanner_groups = {}
        for result in results:
            if result['success']:
                scanner_key = f"{result['result'].get('scanner_brand', 'Unknown')} {result['result'].get('scanner_model', 'Unknown')}"
                if scanner_key not in scanner_groups:
                    scanner_groups[scanner_key] = []
                scanner_groups[scanner_key].append(result['filename'])
        
        # Clean up temp files
        for filepath in temp_files:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except:
                pass
        
        return jsonify({
            'success': True,
            'total': len(files),
            'processed': len(results),
            'results': results,
            'scanner_groups': scanner_groups,
            'summary': {
                'unique_scanners': len(scanner_groups),
                'groups': [{'scanner': k, 'count': len(v), 'files': v} for k, v in scanner_groups.items()]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("TraceFinder - Forensic Scanner Identification System")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("Press CTRL+C to quit")
    print("=" * 60)
    
    # Get port from environment variable (for deployment platforms)
    port = int(os.environ.get('PORT', 5000))
    
    # Run in production mode if PORT is set (deployment)
    if 'PORT' in os.environ:
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        app.run(debug=True, host='0.0.0.0', port=port)
