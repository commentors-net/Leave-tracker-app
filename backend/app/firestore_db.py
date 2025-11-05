# Firestore Database Connection and Helper Functions
import os
from google.cloud import firestore
from typing import Optional, List, Dict, Any
from datetime import datetime, date

class FirestoreDB:
    """Firestore database helper class"""
    
    def __init__(self):
        # Initialize Firestore client
        # Will use GOOGLE_APPLICATION_CREDENTIALS env var for auth
        self.db = firestore.Client()
        
        # Collection names
        self.USERS = "users"
        self.AI_INSTRUCTIONS = "ai_instructions"
        self.ABSENCES = "absences"
        self.PEOPLE = "people"
        self.TYPES = "types"
    
    # ==================== USERS ====================
    
    def create_user(self, username: str, password: str, otp_secret: str) -> Dict[str, Any]:
        """Create a new user"""
        user_ref = self.db.collection(self.USERS).document()
        user_data = {
            "username": username,
            "password": password,
            "otp_secret": otp_secret,
            "created_at": datetime.now().isoformat()
        }
        user_ref.set(user_data)
        return {"id": user_ref.id, **user_data}
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        users = self.db.collection(self.USERS).where("username", "==", username).limit(1).stream()
        for user in users:
            return {"id": user.id, **user.to_dict()}
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        user_ref = self.db.collection(self.USERS).document(user_id)
        user = user_ref.get()
        if user.exists:
            return {"id": user.id, **user.to_dict()}
        return None
    
    def update_user_password(self, user_id: str, new_password: str):
        """Update user password"""
        user_ref = self.db.collection(self.USERS).document(user_id)
        user_ref.update({"password": new_password})
    
    # ==================== AI INSTRUCTIONS ====================
    
    def get_ai_instructions(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get the latest AI instructions for a user"""
        instructions = self.db.collection(self.AI_INSTRUCTIONS)\
            .where("user_id", "==", user_id)\
            .order_by("updated_at", direction=firestore.Query.DESCENDING)\
            .limit(1)\
            .stream()
        for instruction in instructions:
            return {"id": instruction.id, **instruction.to_dict()}
        return None
    
    def create_ai_instructions(self, user_id: str, instructions: str) -> Dict[str, Any]:
        """Create new AI instructions for a user"""
        now = datetime.now().isoformat()
        instruction_ref = self.db.collection(self.AI_INSTRUCTIONS).document()
        instruction_data = {
            "user_id": user_id,
            "instructions": instructions,
            "created_at": now,
            "updated_at": now
        }
        instruction_ref.set(instruction_data)
        return {"id": instruction_ref.id, **instruction_data}
    
    def update_ai_instructions(self, instruction_id: str, user_id: str, instructions: str) -> Dict[str, Any]:
        """Update existing AI instructions (with user_id check for security)"""
        instruction_ref = self.db.collection(self.AI_INSTRUCTIONS).document(instruction_id)
        # Verify ownership
        instruction = instruction_ref.get()
        if instruction.exists and instruction.to_dict().get("user_id") == user_id:
            instruction_data = {
                "instructions": instructions,
                "updated_at": datetime.now().isoformat()
            }
            instruction_ref.update(instruction_data)
            instruction = instruction_ref.get()
            return {"id": instruction.id, **instruction.to_dict()}
        return None
    
    # ==================== PEOPLE ====================
    
    def create_person(self, user_id: str, name: str) -> Dict[str, Any]:
        """Create a new person for a user"""
        person_ref = self.db.collection(self.PEOPLE).document()
        person_data = {"user_id": user_id, "name": name}
        person_ref.set(person_data)
        return {"id": person_ref.id, **person_data}
    
    def get_all_people(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all people for a user"""
        people = self.db.collection(self.PEOPLE)\
            .where("user_id", "==", user_id)\
            .order_by("name")\
            .stream()
        return [{"id": person.id, **person.to_dict()} for person in people]
    
    def get_person_by_id(self, person_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get person by ID (with user_id check for security)"""
        person_ref = self.db.collection(self.PEOPLE).document(person_id)
        person = person_ref.get()
        if person.exists and person.to_dict().get("user_id") == user_id:
            return {"id": person.id, **person.to_dict()}
        return None
    
    def get_person_by_name(self, name: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get person by name for a user"""
        people = self.db.collection(self.PEOPLE)\
            .where("user_id", "==", user_id)\
            .where("name", "==", name)\
            .limit(1)\
            .stream()
        for person in people:
            return {"id": person.id, **person.to_dict()}
        return None
    
    def update_person(self, person_id: str, user_id: str, name: str) -> Dict[str, Any]:
        """Update person (with user_id check for security)"""
        person_ref = self.db.collection(self.PEOPLE).document(person_id)
        person = person_ref.get()
        if person.exists and person.to_dict().get("user_id") == user_id:
            person_ref.update({"name": name})
            person = person_ref.get()
            return {"id": person.id, **person.to_dict()}
        return None
    
    def delete_person(self, person_id: str, user_id: str) -> bool:
        """Delete person (with user_id check for security)"""
        self.db.collection(self.PEOPLE).document(person_id).delete()
        return True
    
    # ==================== TYPES ====================
    
    def create_type(self, user_id: str, name: str) -> Dict[str, Any]:
        """Create a new leave type for a user"""
        type_ref = self.db.collection(self.TYPES).document()
        type_data = {"user_id": user_id, "name": name}
        type_ref.set(type_data)
        return {"id": type_ref.id, **type_data}
    
    def get_all_types(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all leave types for a user"""
        types = self.db.collection(self.TYPES)\
            .where("user_id", "==", user_id)\
            .order_by("name")\
            .stream()
        return [{"id": t.id, **t.to_dict()} for t in types]
    
    def get_type_by_id(self, type_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get type by ID (with user_id check for security)"""
        type_ref = self.db.collection(self.TYPES).document(type_id)
        type_doc = type_ref.get()
        if type_doc.exists and type_doc.to_dict().get("user_id") == user_id:
            return {"id": type_doc.id, **type_doc.to_dict()}
        return None
    
    def get_type_by_name(self, name: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get type by name for a user"""
        types = self.db.collection(self.TYPES)\
            .where("user_id", "==", user_id)\
            .where("name", "==", name)\
            .limit(1)\
            .stream()
        for type_doc in types:
            return {"id": type_doc.id, **type_doc.to_dict()}
        return None
    
    def update_type(self, type_id: str, user_id: str, name: str) -> Dict[str, Any]:
        """Update leave type (with user_id check for security)"""
        type_ref = self.db.collection(self.TYPES).document(type_id)
        type_doc = type_ref.get()
        if type_doc.exists and type_doc.to_dict().get("user_id") == user_id:
            type_ref.update({"name": name})
            type_doc = type_ref.get()
            return {"id": type_doc.id, **type_doc.to_dict()}
        return None
    
    def delete_type(self, type_id: str, user_id: str) -> bool:
        """Delete leave type (with user_id check for security)"""
        type_ref = self.db.collection(self.TYPES).document(type_id)
        type_doc = type_ref.get()
        if type_doc.exists and type_doc.to_dict().get("user_id") == user_id:
            type_ref.delete()
            return True
        return False
    
    # ==================== ABSENCES ====================
    
    def create_absence(self, user_id: str, date_val: date, duration: str, reason: str, 
                      type_id: str, person_id: str, applied: int = 0) -> Dict[str, Any]:
        """Create a new absence for a user"""
        absence_ref = self.db.collection(self.ABSENCES).document()
        absence_data = {
            "user_id": user_id,
            "date": date_val.isoformat() if isinstance(date_val, date) else date_val,  # Store as ISO string
            "duration": duration,
            "reason": reason,
            "type_id": type_id,
            "person_id": person_id,
            "applied": applied,
            "created_at": datetime.now().isoformat()
        }
        absence_ref.set(absence_data)
        return {"id": absence_ref.id, **absence_data}
    
    def get_all_absences(self, user_id: str, person_id: Optional[str] = None, 
                         type_id: Optional[str] = None,
                         date_from: Optional[date] = None,
                         date_to: Optional[date] = None) -> List[Dict[str, Any]]:
        """Get all absences for a user with optional filters"""
        query = self.db.collection(self.ABSENCES).where("user_id", "==", user_id)
        
        # Apply filters
        if person_id:
            query = query.where("person_id", "==", person_id)
        if type_id:
            query = query.where("type_id", "==", type_id)
        if date_from:
            query = query.where("date", ">=", date_from.isoformat())
        if date_to:
            query = query.where("date", "<=", date_to.isoformat())
        
        # Order by date descending
        query = query.order_by("date", direction=firestore.Query.DESCENDING)
        
        absences = query.stream()
        result = []
        for absence in absences:
            data = absence.to_dict()
            # Convert date string back to date object
            if "date" in data and isinstance(data["date"], str):
                try:
                    data["date"] = datetime.fromisoformat(data["date"]).date()
                except:
                    pass  # Keep as string if conversion fails
            result.append({"id": absence.id, **data})
        return result
    
    def get_absence_by_id(self, absence_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get absence by ID (with user_id check for security)"""
        absence_ref = self.db.collection(self.ABSENCES).document(absence_id)
        absence = absence_ref.get()
        if absence.exists and absence.to_dict().get("user_id") == user_id:
            data = absence.to_dict()
            # Convert date string back to date object
            if "date" in data and isinstance(data["date"], str):
                try:
                    data["date"] = datetime.fromisoformat(data["date"]).date()
                except:
                    pass  # Keep as string if conversion fails
            return {"id": absence.id, **data}
        return None
    
    def update_absence(self, absence_id: str, user_id: str, applied: int) -> Dict[str, Any]:
        """Update absence (user_id check for security)"""
        absence_ref = self.db.collection(self.ABSENCES).document(absence_id)
        absence = absence_ref.get()
        
        if absence.exists and absence.to_dict().get("user_id") == user_id:
            absence_ref.update({"applied": applied})
            absence = absence_ref.get()
            data = absence.to_dict()
            
            # Convert date string back to date object
            if "date" in data and isinstance(data["date"], str):
                try:
                    data["date"] = datetime.fromisoformat(data["date"]).date()
                except:
                    pass
            
            return {"id": absence.id, **data}
        return None
    
    def delete_absence(self, absence_id: str, user_id: str) -> bool:
        """Delete absence (with user_id check for security)"""
        absence_ref = self.db.collection(self.ABSENCES).document(absence_id)
        absence = absence_ref.get()
        if absence.exists and absence.to_dict().get("user_id") == user_id:
            absence_ref.delete()
            return True
        return False
    
    def bulk_delete_absences(self, absence_ids: List[str], user_id: str) -> int:
        """Delete multiple absences (with user_id check for security)"""
        batch = self.db.batch()
        deleted_count = 0
        for absence_id in absence_ids:
            absence_ref = self.db.collection(self.ABSENCES).document(absence_id)
            absence = absence_ref.get()
            if absence.exists and absence.to_dict().get("user_id") == user_id:
                batch.delete(absence_ref)
                deleted_count += 1
        batch.commit()
        return deleted_count
    
    def bulk_update_applied(self, absence_ids: List[str], user_id: str, applied: int) -> int:
        """Update applied status for multiple absences (with user_id check for security)"""
        batch = self.db.batch()
        updated_count = 0
        for absence_id in absence_ids:
            absence_ref = self.db.collection(self.ABSENCES).document(absence_id)
            absence = absence_ref.get()
            if absence.exists and absence.to_dict().get("user_id") == user_id:
                batch.update(absence_ref, {"applied": applied})
                updated_count += 1
        batch.commit()
        return updated_count


# Global instance
firestore_db = FirestoreDB()
