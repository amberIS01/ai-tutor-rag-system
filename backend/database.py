"""
Database Connection Module
Handles database connections and operations
"""

import sqlite3
from typing import Any, List, Dict, Optional
from contextlib import contextmanager


class DatabaseConnection:
    """SQLite database connection manager"""
    
    def __init__(self, db_path: str = "app_data.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # PDF metadata table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pdf_metadata (
                    id INTEGER PRIMARY KEY,
                    filename TEXT UNIQUE NOT NULL,
                    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    file_size INTEGER,
                    page_count INTEGER,
                    status TEXT DEFAULT 'processing'
                )
            ''')
            
            # Text chunks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS text_chunks (
                    id INTEGER PRIMARY KEY,
                    chunk_id TEXT UNIQUE NOT NULL,
                    pdf_filename TEXT NOT NULL,
                    page_number INTEGER,
                    content TEXT NOT NULL,
                    FOREIGN KEY (pdf_filename) REFERENCES pdf_metadata(filename)
                )
            ''')
            
            # Images table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY,
                    image_id TEXT UNIQUE NOT NULL,
                    pdf_filename TEXT NOT NULL,
                    page_number INTEGER,
                    image_path TEXT NOT NULL,
                    FOREIGN KEY (pdf_filename) REFERENCES pdf_metadata(filename)
                )
            ''')
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Get database connection context manager"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Any]:
        """Execute SELECT query"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute INSERT/UPDATE/DELETE query"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
