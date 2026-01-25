"""
Professional PDF Report Generator for TraceFinder
Generates comprehensive forensic analysis reports
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.platypus import KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import os

class PDFReportGenerator:
    """Generate professional PDF forensic reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=14,
            alignment=TA_JUSTIFY
        ))
        
        # Highlight style
        self.styles.add(ParagraphStyle(
            name='Highlight',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#e74c3c'),
            fontName='Helvetica-Bold'
        ))
    
    def generate_report(self, analysis_data, output_path='reports/forensic_report.pdf'):
        """Generate comprehensive PDF report"""
        try:
            # Ensure reports directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build content
            story = []
            
            # Header
            story.extend(self._create_header(analysis_data))
            story.append(Spacer(1, 0.3*inch))
            
            # Executive Summary
            story.extend(self._create_executive_summary(analysis_data))
            story.append(Spacer(1, 0.2*inch))
            
            # Scanner Detection Results
            story.extend(self._create_detection_section(analysis_data))
            story.append(Spacer(1, 0.2*inch))
            
            # Confidence Analysis
            story.extend(self._create_confidence_section(analysis_data))
            story.append(Spacer(1, 0.2*inch))
            
            # Technical Details
            story.extend(self._create_technical_section(analysis_data))
            story.append(Spacer(1, 0.2*inch))
            
            # Metadata Analysis
            if analysis_data.get('metadata'):
                story.extend(self._create_metadata_section(analysis_data))
                story.append(Spacer(1, 0.2*inch))
            
            # Conclusion
            story.extend(self._create_conclusion(analysis_data))
            
            # Footer
            story.append(Spacer(1, 0.3*inch))
            story.extend(self._create_footer())
            
            # Build PDF
            doc.build(story)
            
            return {
                'success': True,
                'report_path': output_path,
                'file_size': os.path.getsize(output_path)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_header(self, data):
        """Create report header"""
        elements = []
        
        # Title
        title = Paragraph("TRACEFINDER FORENSIC ANALYSIS REPORT", self.styles['CustomTitle'])
        elements.append(title)
        
        # Case information table
        case_data = [
            ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Document Analyzed:', data.get('filename', 'Unknown')],
            ['Case ID:', data.get('case_id', datetime.now().strftime('CASE-%Y%m%d-%H%M%S'))],
            ['Analysis Type:', 'Scanner Identification']
        ]
        
        case_table = Table(case_data, colWidths=[2*inch, 4*inch])
        case_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(case_table)
        
        return elements
    
    def _create_executive_summary(self, data):
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.styles['CustomSubtitle']))
        
        # Key findings
        brand = data.get('scanner_brand', 'Unknown')
        model = data.get('scanner_model', 'Unknown')
        confidence = data.get('confidence', 0) * 100
        confidence_level = data.get('confidence_level', 'Unknown')
        
        summary_text = f"""
        This forensic analysis report presents the findings from the examination of the submitted 
        document. Using advanced digital forensics techniques and machine learning algorithms, 
        TraceFinder has identified the scanner device responsible for creating this document.
        <br/><br/>
        <b>Primary Finding:</b> The document was scanned using a <b>{brand} {model}</b> scanner 
        with a confidence level of <b>{confidence:.1f}% ({confidence_level})</b>.
        """
        
        elements.append(Paragraph(summary_text, self.styles['CustomBody']))
        
        return elements
    
    def _create_detection_section(self, data):
        """Create scanner detection results section"""
        elements = []
        
        elements.append(Paragraph("SCANNER DETECTION RESULTS", self.styles['CustomSubtitle']))
        
        # Detection results table
        brand = data.get('scanner_brand', 'Unknown')
        model = data.get('scanner_model', 'Unknown')
        confidence = data.get('confidence', 0) * 100
        confidence_level = data.get('confidence_level', 'Unknown')
        
        detection_data = [
            ['Parameter', 'Value'],
            ['Scanner Brand', brand],
            ['Scanner Model', model],
            ['Confidence Score', f'{confidence:.2f}%'],
            ['Confidence Level', confidence_level],
            ['Detection Method', data.get('detection_method', 'Multi-Factor Analysis')]
        ]
        
        detection_table = Table(detection_data, colWidths=[2.5*inch, 3.5*inch])
        detection_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(detection_table)
        
        return elements
    
    def _create_confidence_section(self, data):
        """Create confidence analysis section"""
        elements = []
        
        elements.append(Paragraph("CONFIDENCE ANALYSIS", self.styles['CustomSubtitle']))
        
        confidence = data.get('confidence', 0) * 100
        
        # Confidence interpretation
        if confidence >= 90:
            interpretation = "Very High - Results are highly reliable for forensic purposes"
            color_hex = '#27ae60'
        elif confidence >= 75:
            interpretation = "High - Results are reliable with strong supporting evidence"
            color_hex = '#2ecc71'
        elif confidence >= 60:
            interpretation = "Moderate - Results are probable but require additional verification"
            color_hex = '#f39c12'
        elif confidence >= 40:
            interpretation = "Low - Results are tentative and require further investigation"
            color_hex = '#e67e22'
        else:
            interpretation = "Very Low - Results are uncertain and should not be relied upon"
            color_hex = '#e74c3c'
        
        conf_text = f"""
        <b>Confidence Score:</b> {confidence:.2f}%<br/>
        <b>Interpretation:</b> <font color="{color_hex}">{interpretation}</font>
        """
        
        elements.append(Paragraph(conf_text, self.styles['CustomBody']))
        
        # Confidence factors
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph("Contributing Factors:", self.styles['SectionHeader']))
        
        factors = self._get_confidence_factors(data)
        for factor in factors:
            bullet = Paragraph(f"• {factor}", self.styles['CustomBody'])
            elements.append(bullet)
        
        return elements
    
    def _get_confidence_factors(self, data):
        """Extract confidence contributing factors"""
        factors = []
        
        # Check metadata
        if data.get('metadata', {}).get('exif_data'):
            factors.append("EXIF metadata present and analyzed")
        
        # Check detection method
        detailed = data.get('detailed_analysis', {})
        if detailed:
            primary = detailed.get('primary_indicators', [])
            factors.extend(primary[:3])  # Top 3 indicators
        
        # ML model usage
        if data.get('using_trained_model'):
            factors.append("Machine learning model prediction")
        
        # Feature analysis
        if data.get('features_summary'):
            factors.append("Digital fingerprint analysis completed")
        
        if not factors:
            factors.append("Standard forensic analysis performed")
        
        return factors
    
    def _create_technical_section(self, data):
        """Create technical details section"""
        elements = []
        
        elements.append(Paragraph("TECHNICAL ANALYSIS", self.styles['CustomSubtitle']))
        
        # Primary indicators
        detailed = data.get('detailed_analysis', {})
        if detailed:
            primary = detailed.get('primary_indicators', [])
            if primary:
                elements.append(Paragraph("Primary Indicators:", self.styles['SectionHeader']))
                for indicator in primary:
                    elements.append(Paragraph(f"• {indicator}", self.styles['CustomBody']))
                elements.append(Spacer(1, 0.1*inch))
            
            # Secondary indicators
            secondary = detailed.get('secondary_indicators', [])
            if secondary:
                elements.append(Paragraph("Secondary Indicators:", self.styles['SectionHeader']))
                for indicator in secondary:
                    elements.append(Paragraph(f"• {indicator}", self.styles['CustomBody']))
                elements.append(Spacer(1, 0.1*inch))
            
            # Anomalies
            anomalies = detailed.get('anomalies', [])
            if anomalies:
                elements.append(Paragraph("Observed Anomalies:", self.styles['SectionHeader']))
                for anomaly in anomalies:
                    elements.append(Paragraph(f"• {anomaly}", self.styles['CustomBody']))
        
        return elements
    
    def _create_metadata_section(self, data):
        """Create metadata analysis section"""
        elements = []
        
        elements.append(Paragraph("METADATA ANALYSIS", self.styles['CustomSubtitle']))
        
        metadata = data.get('metadata', {})
        exif_data = metadata.get('exif_data', {})
        
        if exif_data:
            # Key metadata fields
            key_fields = [
                'Image Make', 'Image Model', 'Image DateTime',
                'Image Software', 'Image XResolution', 'Image YResolution'
            ]
            
            metadata_rows = [['Field', 'Value']]
            for field in key_fields:
                if field in exif_data:
                    metadata_rows.append([field.replace('Image ', ''), str(exif_data[field])[:50]])
            
            if len(metadata_rows) > 1:
                meta_table = Table(metadata_rows, colWidths=[2*inch, 4*inch])
                meta_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#95a5a6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
                ]))
                elements.append(meta_table)
        else:
            elements.append(Paragraph("No EXIF metadata found in the document.", self.styles['CustomBody']))
        
        return elements
    
    def _create_conclusion(self, data):
        """Create conclusion section"""
        elements = []
        
        elements.append(Paragraph("CONCLUSION", self.styles['CustomSubtitle']))
        
        brand = data.get('scanner_brand', 'Unknown')
        model = data.get('scanner_model', 'Unknown')
        confidence = data.get('confidence', 0) * 100
        
        conclusion_text = f"""
        Based on comprehensive forensic analysis using TraceFinder's advanced detection algorithms, 
        this document was scanned using a <b>{brand} {model}</b> scanner. The analysis achieved 
        a confidence score of <b>{confidence:.1f}%</b>, indicating {self._get_reliability_statement(confidence)}.
        <br/><br/>
        This analysis employed multiple forensic techniques including metadata extraction, digital 
        fingerprint analysis, and machine learning-based pattern recognition to ensure accurate 
        scanner identification.
        """
        
        elements.append(Paragraph(conclusion_text, self.styles['CustomBody']))
        
        return elements
    
    def _get_reliability_statement(self, confidence):
        """Get reliability statement based on confidence"""
        if confidence >= 90:
            return "a very high level of reliability suitable for forensic evidence"
        elif confidence >= 75:
            return "a high level of reliability with strong supporting evidence"
        elif confidence >= 60:
            return "a moderate level of reliability requiring additional verification"
        else:
            return "a low level of reliability requiring further investigation"
    
    def _create_footer(self):
        """Create report footer"""
        elements = []
        
        footer_style = ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        
        footer_text = """
        <br/><br/>
        ───────────────────────────────────────────────────────<br/>
        Generated by TraceFinder - Forensic Scanner Identification System<br/>
        This report is generated using automated forensic analysis tools.<br/>
        For legal purposes, results should be verified by certified forensic experts.<br/>
        © 2026 TraceFinder. All rights reserved.
        """
        
        elements.append(Paragraph(footer_text, footer_style))
        
        return elements
