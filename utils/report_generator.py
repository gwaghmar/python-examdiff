"""
Report Generator - HTML and PDF Report Generation
=================================================

Generates comparison reports in various formats.
"""

from typing import List, Optional
from datetime import datetime
import os

from core.myers_algorithm import DiffResult, DiffType


class ReportGenerator:
    """Generates comparison reports."""
    
    def __init__(self, title: str = "File Comparison Report"):
        """
        Initialize report generator.
        
        Args:
            title: Report title
        """
        self.title = title
        self.timestamp = datetime.now()
    
    def generate_html(self, file1: str, file2: str, 
                     lines1: List[str], lines2: List[str],
                     results: List[DiffResult],
                     output_path: str) -> None:
        """
        Generate HTML report.
        
        Args:
            file1: First file path
            file2: Second file path
            lines1: Lines from first file
            lines2: Lines from second file
            results: Diff results
            output_path: Output file path
        """
        html = self._build_html(file1, file2, lines1, lines2, results)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def _build_html(self, file1: str, file2: str,
                   lines1: List[str], lines2: List[str],
                   results: List[DiffResult]) -> str:
        """Build HTML content."""
        
        # Calculate statistics
        total_diffs = len([r for r in results if r.type != DiffType.EQUAL])
        added = sum(r.new_count for r in results if r.type == DiffType.INSERT)
        deleted = sum(r.old_count for r in results if r.type == DiffType.DELETE)
        modified = len([r for r in results if r.type == DiffType.REPLACE])
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            border-radius: 8px;
        }}
        
        .header {{
            background: #2c3e50;
            color: white;
            padding: 30px;
            border-radius: 8px 8px 0 0;
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            opacity: 0.9;
            font-size: 14px;
        }}
        
        .info {{
            padding: 20px 30px;
            background: #ecf0f1;
            border-bottom: 1px solid #bdc3c7;
        }}
        
        .info-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }}
        
        .stats {{
            padding: 20px 30px;
            display: flex;
            justify-content: space-around;
            background: #fff;
            border-bottom: 2px solid #3498db;
        }}
        
        .stat {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .stat-label {{
            font-size: 14px;
            color: #7f8c8d;
            margin-top: 5px;
        }}
        
        .comparison {{
            padding: 30px;
        }}
        
        .diff-container {{
            display: grid;
            grid-template-columns: 50px 1fr 50px 1fr;
            gap: 10px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            margin-bottom: 20px;
        }}
        
        .line-number {{
            text-align: right;
            padding: 5px;
            color: #95a5a6;
            background: #ecf0f1;
            border-radius: 3px;
            user-select: none;
        }}
        
        .line-content {{
            padding: 5px;
            white-space: pre-wrap;
            word-break: break-all;
            border-radius: 3px;
        }}
        
        .line-equal {{
            background: #fff;
        }}
        
        .line-added {{
            background: #d4edda;
            border-left: 3px solid #28a745;
        }}
        
        .line-deleted {{
            background: #f8d7da;
            border-left: 3px solid #dc3545;
        }}
        
        .line-modified {{
            background: #fff3cd;
            border-left: 3px solid #ffc107;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: bold;
            margin: 20px 0 10px 0;
            color: #2c3e50;
        }}
        
        .footer {{
            padding: 20px 30px;
            text-align: center;
            color: #7f8c8d;
            border-top: 1px solid #ecf0f1;
            font-size: 14px;
        }}
        
        @media print {{
            body {{
                padding: 0;
                background: white;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{self.title}</h1>
            <p>Generated on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="info">
            <div class="info-row">
                <strong>File 1:</strong>
                <span>{os.path.basename(file1)}</span>
            </div>
            <div class="info-row">
                <strong>File 2:</strong>
                <span>{os.path.basename(file2)}</span>
            </div>
            <div class="info-row">
                <strong>Lines:</strong>
                <span>{len(lines1)} vs {len(lines2)}</span>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{total_diffs}</div>
                <div class="stat-label">Total Differences</div>
            </div>
            <div class="stat">
                <div class="stat-value" style="color: #28a745;">{added}</div>
                <div class="stat-label">Lines Added</div>
            </div>
            <div class="stat">
                <div class="stat-value" style="color: #dc3545;">{deleted}</div>
                <div class="stat-label">Lines Deleted</div>
            </div>
            <div class="stat">
                <div class="stat-value" style="color: #ffc107;">{modified}</div>
                <div class="stat-label">Lines Modified</div>
            </div>
        </div>
        
        <div class="comparison">
            <h2 class="section-title">Comparison Details</h2>
"""
        
        # Add diff content
        for result in results:
            css_class = {
                DiffType.EQUAL: 'line-equal',
                DiffType.INSERT: 'line-added',
                DiffType.DELETE: 'line-deleted',
                DiffType.REPLACE: 'line-modified'
            }[result.type]
            
            if result.type == DiffType.EQUAL:
                # Show a few lines of equal content
                for i in range(min(3, len(result.old_lines))):
                    line_num = result.old_start + i + 1
                    html += f"""
            <div class="diff-container">
                <div class="line-number">{line_num}</div>
                <div class="line-content {css_class}">{self._escape_html(result.old_lines[i])}</div>
                <div class="line-number">{result.new_start + i + 1}</div>
                <div class="line-content {css_class}">{self._escape_html(result.new_lines[i])}</div>
            </div>
"""
            else:
                # Show differences
                max_lines = max(len(result.old_lines), len(result.new_lines))
                for i in range(max_lines):
                    old_line = result.old_lines[i] if i < len(result.old_lines) else ""
                    new_line = result.new_lines[i] if i < len(result.new_lines) else ""
                    old_num = result.old_start + i + 1 if i < len(result.old_lines) else ""
                    new_num = result.new_start + i + 1 if i < len(result.new_lines) else ""
                    
                    html += f"""
            <div class="diff-container">
                <div class="line-number">{old_num}</div>
                <div class="line-content {css_class}">{self._escape_html(old_line)}</div>
                <div class="line-number">{new_num}</div>
                <div class="line-content {css_class}">{self._escape_html(new_line)}</div>
            </div>
"""
        
        html += """
        </div>
        
        <div class="footer">
            <p>Generated by Python ExamDiff Pro - Professional File Comparison Tool</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))
    
    def generate_text_report(self, file1: str, file2: str,
                           results: List[DiffResult]) -> str:
        """
        Generate plain text report.
        
        Args:
            file1: First file path
            file2: Second file path
            results: Diff results
            
        Returns:
            Report as string
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"COMPARISON REPORT")
        lines.append("=" * 70)
        lines.append(f"Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"File 1: {file1}")
        lines.append(f"File 2: {file2}")
        lines.append("")
        
        # Statistics
        total_diffs = len([r for r in results if r.type != DiffType.EQUAL])
        lines.append(f"Total Differences: {total_diffs}")
        lines.append("")
        
        # Details
        for i, result in enumerate(results):
            if result.type != DiffType.EQUAL:
                lines.append(f"Difference #{i+1}: {result.type.value}")
                lines.append(f"  Location: Line {result.old_start+1}")
                if result.old_lines:
                    lines.append("  OLD: " + ", ".join(result.old_lines[:3]))
                if result.new_lines:
                    lines.append("  NEW: " + ", ".join(result.new_lines[:3]))
                lines.append("")
        
        return "\n".join(lines)


def create_html_report(file1: str, file2: str,
                      lines1: List[str], lines2: List[str],
                      results: List[DiffResult],
                      output_path: str) -> None:
    """
    Convenience function to create HTML report.
    
    Args:
        file1: First file path
        file2: Second file path
        lines1: Lines from first file
        lines2: Lines from second file
        results: Diff results
        output_path: Output file path
    """
    generator = ReportGenerator()
    generator.generate_html(file1, file2, lines1, lines2, results, output_path)
