"""
Report Generator: Creates neat, formatted PDF reports from scan results.
"""
import json
import time
from pathlib import Path
from datetime import datetime
from core.utils import ensure_dir

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
    from reportlab.lib import colors
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


class ReportGenerator:
    """Generate professional PDF reports from command outputs and scan results."""

    def __init__(self, workspace="./reports"):
        self.workspace = Path(workspace)
        ensure_dir(self.workspace)
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def create_pdf_report(self, title, content, target=None, findings=None, metadata=None):
        """
        Create a formatted PDF report.
        
        Args:
            title: Report title
            content: Main report content (text or dict)
            target: Target host/domain (optional)
            findings: List of findings/vulnerabilities
            metadata: Additional metadata (user, date, tool, etc.)
        
        Returns:
            Path to generated PDF, or None if reportlab unavailable
        """
        if not HAS_REPORTLAB:
            return self._fallback_report(title, content, target, findings, metadata)

        filename = f"{self.workspace}/report_{self.timestamp}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=20,
            fontName='Helvetica-Bold'
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#0066cc'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )

        # Title
        story.append(Paragraph(f"SecShell PRO Report - {title}", title_style))
        story.append(Spacer(1, 0.3 * inch))

        # Metadata header
        if metadata or target:
            meta_data = []
            if target:
                meta_data.append(["Target", target])
            if metadata:
                if isinstance(metadata, dict):
                    for key, val in metadata.items():
                        meta_data.append([key, str(val)])
            meta_data.append(["Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

            meta_table = Table(meta_data, colWidths=[2 * inch, 4 * inch])
            meta_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e6f2ff')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            story.append(meta_table)
            story.append(Spacer(1, 0.3 * inch))

        # Main content
        if isinstance(content, str):
            story.append(Paragraph("Scan Output", heading_style))
            # Split large content into chunks to avoid overflow
            lines = content.split('\n')
            for line in lines[:100]:  # Limit to first 100 lines
                if line.strip():
                    story.append(Paragraph(f"<font face='Courier' size='9'>{line}</font>", styles['Normal']))
            if len(lines) > 100:
                story.append(Paragraph(f"<i>[... {len(lines) - 100} more lines omitted ...]</i>", styles['Normal']))

        elif isinstance(content, dict):
            for section, data in content.items():
                story.append(Paragraph(section, heading_style))
                if isinstance(data, list):
                    for item in data[:20]:
                        story.append(Paragraph(f"• {item}", styles['Normal']))
                else:
                    story.append(Paragraph(str(data), styles['Normal']))
                story.append(Spacer(1, 0.1 * inch))

        # Findings section
        if findings:
            story.append(PageBreak())
            story.append(Paragraph("Findings & Vulnerabilities", heading_style))

            findings_data = [["Severity", "Finding", "Description"]]
            for finding in findings[:15]:  # Limit to 15 findings per report
                if isinstance(finding, dict):
                    severity = finding.get("severity", "Unknown")
                    title_f = finding.get("title", "")
                    desc = finding.get("description", "")[:100]
                    findings_data.append([severity, title_f, desc])
                else:
                    findings_data.append(["INFO", str(finding), ""])

            findings_table = Table(findings_data, colWidths=[1 * inch, 2 * inch, 2.5 * inch])
            findings_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(findings_table)

        # Footer
        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph(
            f"<i>Report generated by SecShell PRO on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
            styles['Normal']
        ))

        # Build PDF
        try:
            doc.build(story)
            return filename
        except Exception as e:
            print(f"[error] Failed to build PDF: {e}")
            return None

    def _fallback_report(self, title, content, target, findings, metadata):
        """Generate a text-based report if reportlab is unavailable."""
        filename = f"{self.workspace}/report_{self.timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(f"{'='*80}\n")
            f.write(f"SecShell PRO Report - {title}\n")
            f.write(f"{'='*80}\n\n")

            if metadata or target:
                f.write("[METADATA]\n")
                if target:
                    f.write(f"Target: {target}\n")
                if metadata and isinstance(metadata, dict):
                    for key, val in metadata.items():
                        f.write(f"{key}: {val}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("[CONTENT]\n")
            if isinstance(content, str):
                f.write(content[:5000])
            elif isinstance(content, dict):
                for section, data in content.items():
                    f.write(f"\n{section}:\n")
                    f.write(str(data)[:1000] + "\n")

            if findings:
                f.write(f"\n\n[FINDINGS]\n")
                for i, finding in enumerate(findings[:20], 1):
                    if isinstance(finding, dict):
                        f.write(f"\n{i}. {finding.get('title', 'Finding')}\n")
                        f.write(f"   Severity: {finding.get('severity', 'Unknown')}\n")
                        f.write(f"   {finding.get('description', '')}\n")
                    else:
                        f.write(f"{i}. {finding}\n")

            f.write(f"\n{'='*80}\n")
            f.write(f"End of Report\n")

        return filename

    def ask_generate_report(self, cmd_output, target=None, metadata=None):
        """
        Interactive prompt to ask user if they want to generate a report.
        
        Returns:
            Path to report if generated, None otherwise
        """
        print("\n[report] Would you like to generate a report? (y/n): ", end="", flush=True)
        try:
            response = input().strip().lower()
            if response in ('y', 'yes'):
                title = f"Scan Results - {target or 'Target'}"
                report_path = self.create_pdf_report(
                    title=title,
                    content=cmd_output,
                    target=target,
                    metadata=metadata
                )
                if report_path:
                    print(f"[✓] Report generated: {report_path}")
                    return report_path
                else:
                    print("[✗] Failed to generate report")
                    return None
        except (KeyboardInterrupt, EOFError):
            pass

        return None

    def list_reports(self):
        """List all generated reports."""
        reports = sorted(self.workspace.glob("report_*.pdf")) + sorted(self.workspace.glob("report_*.txt"))
        return reports
