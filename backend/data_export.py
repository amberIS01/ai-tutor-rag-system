"""
Data Export Module
Export data in various formats
"""

import json
import csv
from typing import List, Dict, Any
from io import StringIO, BytesIO
from logger import logger


class DataExporter:
    """Export data in various formats"""
    
    @staticmethod
    def to_json(data: Any, indent: int = 2) -> str:
        """Export data as JSON"""
        try:
            return json.dumps(data, indent=indent, default=str)
        except Exception as e:
            logger.error(f"Failed to export JSON: {str(e)}")
            return ""
    
    @staticmethod
    def to_csv(data: List[Dict[str, Any]]) -> str:
        """Export data as CSV"""
        if not data:
            return ""
        
        try:
            output = StringIO()
            fieldnames = list(data[0].keys())
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(data)
            
            return output.getvalue()
        except Exception as e:
            logger.error(f"Failed to export CSV: {str(e)}")
            return ""
    
    @staticmethod
    def to_txt(data: List[str]) -> str:
        """Export data as plain text"""
        try:
            return "\n".join(data)
        except Exception as e:
            logger.error(f"Failed to export text: {str(e)}")
            return ""
    
    @staticmethod
    def to_markdown(data: List[Dict[str, Any]]) -> str:
        """Export data as Markdown table"""
        if not data:
            return ""
        
        try:
            lines = []
            keys = list(data[0].keys())
            
            # Header
            lines.append("| " + " | ".join(keys) + " |")
            lines.append("|" + "|".join(["---"] * len(keys)) + "|")
            
            # Rows
            for row in data:
                values = [str(row.get(k, "")) for k in keys]
                lines.append("| " + " | ".join(values) + " |")
            
            return "\n".join(lines)
        except Exception as e:
            logger.error(f"Failed to export Markdown: {str(e)}")
            return ""


class ReportGenerator:
    """Generate reports from data"""
    
    @staticmethod
    def generate_summary_report(data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics"""
        if not data:
            return {}
        
        return {
            "total_records": len(data),
            "generated_at": str(__import__('datetime').datetime.now()),
            "data": data
        }
