"""
PDF Report Generator for TraceFinder
Generates professional forensic analysis reports
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime
import os

class PDFReportGenerator:
    """Generate professional PDF reports for forensic analysis"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()
    
    def _add_custom_styles(self):
        """Add custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_LEFT
        ))
    
    def generate_scanner_report(self, result_data, output_path=None):
        """
        Generate a PDF report for scanner detection analysis
        
        Args:
            result_data: Dictionary containing analysis results
            output_path: Path to save PDF (if None, returns BytesIO buffer)
        
        Returns:
            BytesIO buffer if output_path is None, else None
        """
        buffer = BytesIO() if output_path is None else None
        pdf_target = buffer if buffer else output_path
        
        doc = SimpleDocTemplate(pdf_target, pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        story = []
        
        # Header
        story.append(Paragraph("FORENSIC ANALYSIS REPORT", self.styles['CustomTitle']))
        story.append(Paragraph("Scanner Device Identification", self.styles['CustomHeading']))
        story.append(Spacer(1, 12))
        
        # Report metadata
        report_info = [
            ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Analysis Type:', 'Scanner Detection'],
            ['System:', 'TraceFinder v1.0'],
            ['Case ID:', result_data.get('case_id', 'N/A')]
        ]
        
        t = Table(report_info, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#64748b')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
        ]))
        story.append(t)
        story.append(Spacer(1, 20))
        
        # Scanner Detection Results
        story.append(Paragraph("SCANNER IDENTIFICATION", self.styles['CustomHeading']))
        
        scanner_data = [
            ['Scanner Brand:', result_data.get('scanner', {}).get('brand', 'Unknown')],
            ['Scanner Model:', result_data.get('scanner', {}).get('model', 'Unknown')],
            ['Confidence Score:', f"{result_data.get('confidence', 0):.1f}%"],
            ['Detection Method:', result_data.get('method', 'Machine Learning')]
        ]
        
        t2 = Table(scanner_data, colWidths=[2.5*inch, 3.5*inch])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
        ]))
        story.append(t2)
        story.append(Spacer(1, 20))
        
        # Feature Analysis
        if 'features' in result_data:
            story.append(Paragraph("FEATURE ANALYSIS", self.styles['CustomHeading']))
            
            features = result_data['features']
            feature_data = [
                ['Feature', 'Value', 'Status']
            ]
            
            for key, value in features.items():
                status = '✓' if value > 0.5 else '○'
                feature_data.append([
                    key.replace('_', ' ').title(),
                    f"{value:.4f}",
                    status
                ])
            
            t3 = Table(feature_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
            t3.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
            ]))
            story.append(t3)
            story.append(Spacer(1, 20))
        
        # Metadata
        if 'metadata' in result_data:
            story.append(Paragraph("IMAGE METADATA", self.styles['CustomHeading']))
            metadata = result_data['metadata']
            
            meta_data = []
            for key, value in metadata.items():
                if value:
                    meta_data.append([key.replace('_', ' ').title() + ':', str(value)])
            
            if meta_data:
                t4 = Table(meta_data, colWidths=[2*inch, 4*inch])
                t4.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
                ]))
                story.append(t4)
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph(
            "<i>This report was generated by TraceFinder - Forensic Scanner Identification System.<br/>"
            "For educational, research, and forensic purposes only.</i>",
            self.styles['CustomBody']
        ))
        
        # Build PDF
        doc.build(story)
        
        if buffer:
            buffer.seek(0)
            return buffer
        return None
    
    def generate_comparison_report(self, result_data, output_path=None):
        """Generate PDF report for image comparison analysis"""
        buffer = BytesIO() if output_path is None else None
        pdf_target = buffer if buffer else output_path
        
        doc = SimpleDocTemplate(pdf_target, pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        story = []
        
        # Header
        story.append(Paragraph("FORENSIC ANALYSIS REPORT", self.styles['CustomTitle']))
        story.append(Paragraph("Image Comparison Analysis", self.styles['CustomHeading']))
        story.append(Spacer(1, 12))
        
        # Report metadata
        report_info = [
            ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Analysis Type:', 'Image Comparison'],
            ['System:', 'TraceFinder v1.0']
        ]
        
        t = Table(report_info, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
        ]))
        story.append(t)
        story.append(Spacer(1, 20))
        
        # Comparison Results
        story.append(Paragraph("COMPARISON RESULTS", self.styles['CustomHeading']))
        
        match_status = result_data.get('match', False)
        similarity_score = result_data.get('similarity_score', 0)
        
        comparison_data = [
            ['Match Status:', 'MATCH FOUND' if match_status else 'NO MATCH'],
            ['Similarity Score:', f"{similarity_score:.2f}%"],
            ['Confidence Level:', result_data.get('confidence_level', 'Medium')],
            ['Same Scanner:', 'Yes' if match_status else 'No']
        ]
        
        t2 = Table(comparison_data, colWidths=[2.5*inch, 3.5*inch])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981' if match_status else '#ef4444')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
        ]))
        story.append(t2)
        story.append(Spacer(1, 20))
        
        # Build PDF
        doc.build(story)
        
        if buffer:
            buffer.seek(0)
            return buffer
        return None
    
    def generate_tampering_report(self, result_data, output_path=None):
        """Generate PDF report for tampering detection analysis"""
        buffer = BytesIO() if output_path is None else None
        pdf_target = buffer if buffer else output_path
        
        doc = SimpleDocTemplate(pdf_target, pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        story = []
        
        # Header
        story.append(Paragraph("FORENSIC ANALYSIS REPORT", self.styles['CustomTitle']))
        story.append(Paragraph("Image Tampering Detection", self.styles['CustomHeading']))
        story.append(Spacer(1, 12))
        
        # Report metadata
        report_info = [
            ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Analysis Type:', 'Tampering Detection'],
            ['System:', 'TraceFinder v1.0']
        ]
        
        t = Table(report_info, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
        ]))
        story.append(t)
        story.append(Spacer(1, 20))
        
        # Tampering Results
        story.append(Paragraph("TAMPERING ANALYSIS", self.styles['CustomHeading']))
        
        is_tampered = result_data.get('is_tampered', False)
        confidence = result_data.get('confidence', 0)
        
        tampering_data = [
            ['Status:', 'TAMPERED' if is_tampered else 'AUTHENTIC'],
            ['Confidence:', f"{confidence:.1f}%"],
            ['Risk Level:', result_data.get('risk_level', 'Low')]
        ]
        
        t2 = Table(tampering_data, colWidths=[2.5*inch, 3.5*inch])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ef4444' if is_tampered else '#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
        ]))
        story.append(t2)
        story.append(Spacer(1, 20))
        
        # Findings
        if 'findings' in result_data:
            story.append(Paragraph("DETECTED ANOMALIES", self.styles['CustomHeading']))
            findings_text = "<br/>".join([f"• {finding}" for finding in result_data['findings']])
            story.append(Paragraph(findings_text, self.styles['CustomBody']))
        
        # Build PDF
        doc.build(story)
        
        if buffer:
            buffer.seek(0)
            return buffer
        return None
