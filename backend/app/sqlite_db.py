# SQLite Database Wrapper (matches Firestore interface)
import os
import sqlite3
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import json

class SQLiteDB:
    """SQLite database helper class with Firestore-compatible interface"""
    
    def __init__(self, db_path: str = None):
        # Use absolute path to avoid working directory issues
        if db_path is None:
            # Get the directory where this file is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to backend directory
            backend_dir = os.path.dirname(current_dir)
            db_path = os.path.join(backend_dir, "database.db")
        
        self.db_path = db_path
        self._create_tables()
    
    def _get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def _create_tables(self):
        """Create tables if they don't exist"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                otp_secret TEXT NOT NULL
            )
        ''')
        
        # AI Instructions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_instructions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                instructions TEXT NOT NULL,
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # People table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS people (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Types table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS types (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Absences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS absences (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                person_id TEXT NOT NULL,
                type_id TEXT NOT NULL,
                date TEXT NOT NULL,
                duration TEXT NOT NULL,
                reason TEXT,
                applied INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (person_id) REFERENCES people (id),
                FOREIGN KEY (type_id) REFERENCES types (id)
            )
        ''')
        
        # Create indexes for user_id columns for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ai_instructions_user_id ON ai_instructions(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_people_user_id ON people(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_types_user_id ON types(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_absences_user_id ON absences(user_id)')
        
        conn.commit()
        conn.close()
    
    # ==================== USERS ====================
    
    def create_user(self, username: str, password: str, otp_secret: str) -> Dict[str, Any]:
        """Create a new user"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Generate ID
        import uuid
        user_id = str(uuid.uuid4())
        
        cursor.execute(
            "INSERT INTO users (id, username, password, otp_secret) VALUES (?, ?, ?, ?)",
            (user_id, username, password, otp_secret)
        )
        conn.commit()
        conn.close()
        
        return {
            "id": user_id,
            "username": username,
            "password": password,
            "otp_secret": otp_secret
        }
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def update_user_password(self, user_id: str, new_password: str):
        """Update user password"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (new_password, user_id)
        )
        conn.commit()
        conn.close()
    
    # ==================== AI INSTRUCTIONS ====================
    
    def get_ai_instructions(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get AI instructions for a specific user"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM ai_instructions WHERE user_id = ? LIMIT 1", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def create_ai_instructions(self, user_id: str, instructions: str) -> Dict[str, Any]:
        """Create AI instructions for a user"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        import uuid
        doc_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        cursor.execute(
            "INSERT INTO ai_instructions (id, user_id, instructions, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (doc_id, user_id, instructions, now, now)
        )
        conn.commit()
        conn.close()
        
        return {
            "id": doc_id,
            "user_id": user_id,
            "instructions": instructions,
            "created_at": now,
            "updated_at": now
        }
    
    def update_ai_instructions(self, instruction_id: str, user_id: str, instructions: str) -> Dict[str, Any]:
        """Update AI instructions by ID (user_id check for security)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        
        cursor.execute(
            "UPDATE ai_instructions SET instructions = ?, updated_at = ? WHERE id = ? AND user_id = ?",
            (instructions, now, instruction_id, user_id)
        )
        conn.commit()
        
        # Fetch the updated record to get created_at
        cursor.execute("SELECT * FROM ai_instructions WHERE id = ? AND user_id = ?", (instruction_id, user_id))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        
        # Fallback if not found (shouldn't happen)
        return {
            "id": instruction_id,
            "user_id": user_id,
            "instructions": instructions,
            "updated_at": now,
            "created_at": now
        }
    
    # ==================== PEOPLE ====================
    
    def get_all_people(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all people for a specific user"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM people WHERE user_id = ? ORDER BY name", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_person_by_id(self, person_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get person by ID (with user_id check for security)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM people WHERE id = ? AND user_id = ?", (person_id, user_id))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def create_person(self, user_id: str, name: str) -> Dict[str, Any]:
        """Create a new person for a user"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        import uuid
        person_id = str(uuid.uuid4())
        
        cursor.execute(
            "INSERT INTO people (id, user_id, name) VALUES (?, ?, ?)",
            (person_id, user_id, name)
        )
        conn.commit()
        conn.close()
        
        return {"id": person_id, "user_id": user_id, "name": name}
    
    def update_person(self, person_id: str, user_id: str, name: str) -> Dict[str, Any]:
        """Update a person (with user_id check for security)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE people SET name = ? WHERE id = ? AND user_id = ?",
            (name, person_id, user_id)
        )
        conn.commit()
        conn.close()
        
        return {"id": person_id, "user_id": user_id, "name": name}
    
    def delete_person(self, person_id: str, user_id: str):
        """Delete a person (with user_id check for security)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM people WHERE id = ? AND user_id = ?", (person_id, user_id))
        conn.commit()
        conn.close()
    
    # ==================== TYPES ====================
    
    def get_all_types(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all leave types for a specific user"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM types WHERE user_id = ? ORDER BY name", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_type_by_id(self, type_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get leave type by ID (with user_id check for security)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM types WHERE id = ? AND user_id = ?", (type_id, user_id))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def create_type(self, user_id: str, name: str) -> Dict[str, Any]:
        """Create a new leave type for a user"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        import uuid
        type_id = str(uuid.uuid4())
        
        cursor.execute(
            "INSERT INTO types (id, user_id, name) VALUES (?, ?, ?)",
            (type_id, user_id, name)
        )
        conn.commit()
        conn.close()
        
        return {"id": type_id, "user_id": user_id, "name": name}
    
    def update_type(self, type_id: str, user_id: str, name: str) -> Dict[str, Any]:
        """Update a leave type (with user_id check for security)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE types SET name = ? WHERE id = ? AND user_id = ?",
            (name, type_id, user_id)
        )
        conn.commit()
        conn.close()
        
        return {"id": type_id, "user_id": user_id, "name": name}
    
    def delete_type(self, type_id: str, user_id: str):
        """Delete a leave type (with user_id check for security)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM types WHERE id = ? AND user_id = ?", (type_id, user_id))
        conn.commit()
        conn.close()
    
    # ==================== ABSENCES ====================
    
    def get_all_absences(self, user_id: str, person_id: Optional[str] = None, 
                        type_id: Optional[str] = None,
                        date_from: Optional[date] = None,
                        date_to: Optional[date] = None) -> List[Dict[str, Any]]:
        """Get all absences for a user with optional filters"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM absences WHERE user_id = ?"
        params = [user_id]
        
        if person_id:
            query += " AND person_id = ?"
            params.append(person_id)
        
        if type_id:
            query += " AND type_id = ?"
            params.append(type_id)
        
        if date_from:
            query += " AND date >= ?"
            params.append(date_from.isoformat())
        
        if date_to:
            query += " AND date <= ?"
            params.append(date_to.isoformat())
        
        query += " ORDER BY date DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_absence_by_id(self, absence_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get absence by ID (with user_id check for security)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM absences WHERE id = ? AND user_id = ?", (absence_id, user_id))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def create_absence(self, user_id: str, person_id: str, type_id: str, date_val: str, 
                      duration: str, reason: str = "", applied: int = 0) -> Dict[str, Any]:
        """Create a new absence for a user"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        import uuid
        absence_id = str(uuid.uuid4())
        
        cursor.execute(
            "INSERT INTO absences (id, user_id, person_id, type_id, date, duration, reason, applied) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (absence_id, user_id, person_id, type_id, date_val, duration, reason, applied)
        )
        conn.commit()
        conn.close()
        
        return {
            "id": absence_id,
            "user_id": user_id,
            "person_id": person_id,
            "type_id": type_id,
            "date": date_val,
            "duration": duration,
            "reason": reason,
            "applied": applied
        }
    
    def update_absence(self, absence_id: str, user_id: str, applied: int) -> Dict[str, Any]:
        """Update an absence (user_id check for security)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Update only the applied field
        cursor.execute(
            "UPDATE absences SET applied = ? WHERE id = ? AND user_id = ?",
            (applied, absence_id, user_id)
        )
        conn.commit()
        
        # Fetch updated record
        cursor.execute("SELECT * FROM absences WHERE id = ? AND user_id = ?", (absence_id, user_id))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        
        # Return minimal data if not found
        return {
            "id": absence_id,
            "user_id": user_id,
            "applied": applied
        }
    
    def delete_absence(self, absence_id: str, user_id: str):
        """Delete an absence (with user_id check for security)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM absences WHERE id = ? AND user_id = ?", (absence_id, user_id))
        conn.commit()
        conn.close()
    
    def bulk_delete_absences(self, absence_ids: List[str], user_id: str) -> int:
        """Delete multiple absences (with user_id check for security)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        placeholders = ",".join(["?" for _ in absence_ids])
        cursor.execute(
            f"DELETE FROM absences WHERE user_id = ? AND id IN ({placeholders})", 
            [user_id] + absence_ids
        )
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def bulk_update_applied(self, absence_ids: List[str], user_id: str, applied: int) -> int:
        """Update applied status for multiple absences (with user_id check for security)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        placeholders = ",".join(["?" for _ in absence_ids])
        cursor.execute(
            f"UPDATE absences SET applied = ? WHERE user_id = ? AND id IN ({placeholders})", 
            [applied, user_id] + absence_ids
        )
        updated_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return updated_count

# Create singleton instance
sqlite_db = SQLiteDB()
