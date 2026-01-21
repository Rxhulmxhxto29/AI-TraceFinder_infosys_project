from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from datetime import datetime
import os

class ReportGenerator:
    """Generate forensic analysis reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Check if styles already exist before adding
        if 'CustomTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=30,
                alignment=1  # Center
            ))
        
        if 'SectionHeader' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='SectionHeader',
                parent=self.styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=12,
                spaceBefore=12
            ))
        
        if 'CustomBodyText' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomBodyText',
                parent=self.styles['Normal'],
                fontSize=11,
                leading=14
            ))
    
    def create_pdf_report(self, analysis_data):
        """Generate PDF report from analysis data"""
        # Create filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'tracefinder_report_{timestamp}.pdf'
        filepath = os.path.join('static', 'uploads', filename)
        
        # Create document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build content
        story = []
        
        # Title
        story.append(Paragraph("TraceFinder Forensic Analysis Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        # Report metadata
        report_info = [
            ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Analysis ID:', timestamp],
            ['System Version:', '1.0.0']
        ]
        
        t = Table(report_info, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(t)
        story.append(Spacer(1, 20))
        
        # Analysis Results
        story.append(Paragraph("1. Scanner Identification Results", self.styles['SectionHeader']))
        
        if 'results' in analysis_data and analysis_data['results'].get('success'):
            results = analysis_data['results']
            
            result_data = [
                ['Scanner Brand:', results.get('scanner_brand', 'Unknown')],
                ['Scanner Model:', results.get('scanner_model', 'Unknown')],
                ['Confidence Score:', f"{results.get('confidence', 0)*100:.1f}%"],
                ['Confidence Level:', results.get('confidence_level', 'N/A')]
            ]
            
            t = Table(result_data, colWidths=[2*inch, 4*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#ecf0f1')),
                ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            story.append(t)
            story.append(Spacer(1, 15))
            
            # Features Summary
            if 'features_summary' in results:
                story.append(Paragraph("2. Feature Analysis Summary", self.styles['SectionHeader']))
                
                for feature, value in results['features_summary'].items():
                    story.append(Paragraph(f"<b>{feature}:</b> {value}", self.styles['CustomBodyText']))
                    story.append(Spacer(1, 6))
                
                story.append(Spacer(1, 15))
            
            # Detailed Analysis
            if 'detailed_analysis' in results:
                story.append(Paragraph("3. Detailed Forensic Analysis", self.styles['SectionHeader']))
                
                details = results['detailed_analysis']
                
                # Primary Indicators
                story.append(Paragraph("<b>Primary Indicators:</b>", self.styles['CustomBodyText']))
                for indicator in details.get('primary_indicators', []):
                    story.append(Paragraph(f"• {indicator}", self.styles['CustomBodyText']))
                story.append(Spacer(1, 10))
                
                # Secondary Indicators
                story.append(Paragraph("<b>Secondary Indicators:</b>", self.styles['CustomBodyText']))
                for indicator in details.get('secondary_indicators', []):
                    story.append(Paragraph(f"• {indicator}", self.styles['CustomBodyText']))
                story.append(Spacer(1, 10))
                
                # Anomalies
                story.append(Paragraph("<b>Anomalies Detected:</b>", self.styles['CustomBodyText']))
                for anomaly in details.get('anomalies', []):
                    story.append(Paragraph(f"• {anomaly}", self.styles['CustomBodyText']))
                story.append(Spacer(1, 15))
        
        else:
            story.append(Paragraph("Analysis failed or no results available", self.styles['CustomBodyText']))
        
        # Conclusion
        story.append(Paragraph("4. Conclusion", self.styles['SectionHeader']))
        story.append(Paragraph(
            "This forensic analysis was conducted using TraceFinder's advanced scanner "
            "identification algorithms. The results are based on multiple forensic techniques "
            "including PRNU analysis, texture analysis, frequency domain analysis, and metadata "
            "extraction.",
            self.styles['CustomBodyText']
        ))
        story.append(Spacer(1, 10))
        story.append(Paragraph(
            "<b>Disclaimer:</b> This report is generated for forensic and investigative purposes. "
            "The accuracy of results depends on image quality and availability of reference data.",
            self.styles['CustomBodyText']
        ))
        
        # Build PDF
        doc.build(story)
        
        return filepath
