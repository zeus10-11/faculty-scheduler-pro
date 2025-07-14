from typing import Dict, List, Optional

class ConflictDetector:
    """Detects scheduling conflicts for faculty and subjects"""
    
    def __init__(self):
        pass
    
    def check_conflicts(self, time_slot: str, room_number: str, faculty_id: str, 
                       subject_code: str, schedule_data: Dict[str, Dict]) -> Optional[str]:
        """
        Check for scheduling conflicts
        
        Args:
            time_slot: Time slot for the booking
            room_number: Room number for the booking
            faculty_id: Faculty ID for the booking
            subject_code: Subject code for the booking
            schedule_data: Current schedule data
            
        Returns:
            Conflict message if conflict exists, None otherwise
        """
        
        conflicts = []
        
        # Check for faculty double booking
        faculty_conflict = self.check_faculty_conflict(time_slot, faculty_id, schedule_data)
        if faculty_conflict:
            conflicts.append(faculty_conflict)
        
        # Check for subject double booking
        subject_conflict = self.check_subject_conflict(time_slot, subject_code, schedule_data)
        if subject_conflict:
            conflicts.append(subject_conflict)
        
        # Check for room double booking
        room_conflict = self.check_room_conflict(time_slot, room_number, schedule_data)
        if room_conflict:
            conflicts.append(room_conflict)
        
        if conflicts:
            return " | ".join(conflicts)
        
        return None
    
    def check_faculty_conflict(self, time_slot: str, faculty_id: str, 
                             schedule_data: Dict[str, Dict]) -> Optional[str]:
        """Check if faculty is already scheduled at the given time slot"""
        
        for slot_key, booking in schedule_data.items():
            if booking['faculty_id'] == faculty_id and booking['time_slot'] == time_slot:
                return f"Faculty is already scheduled at {time_slot} in room {booking['room_number']}"
        
        return None
    
    def check_subject_conflict(self, time_slot: str, subject_code: str, 
                             schedule_data: Dict[str, Dict]) -> Optional[str]:
        """Check if subject is already scheduled at the given time slot"""
        
        for slot_key, booking in schedule_data.items():
            if booking['subject_code'] == subject_code and booking['time_slot'] == time_slot:
                return f"Subject is already scheduled at {time_slot} in room {booking['room_number']}"
        
        return None
    
    def check_room_conflict(self, time_slot: str, room_number: str, 
                          schedule_data: Dict[str, Dict]) -> Optional[str]:
        """Check if room is already booked at the given time slot"""
        
        slot_key = f"{time_slot}_{room_number}"
        if slot_key in schedule_data:
            return f"Room {room_number} is already booked at {time_slot}"
        
        return None
    
    def get_faculty_schedule(self, faculty_id: str, 
                           schedule_data: Dict[str, Dict]) -> List[Dict]:
        """Get all scheduled slots for a specific faculty member"""
        
        faculty_schedule = []
        for slot_key, booking in schedule_data.items():
            if booking['faculty_id'] == faculty_id:
                faculty_schedule.append({
                    'time_slot': booking['time_slot'],
                    'room_number': booking['room_number'],
                    'subject_code': booking['subject_code']
                })
        
        return sorted(faculty_schedule, key=lambda x: x['time_slot'])
    
    def get_subject_schedule(self, subject_code: str, 
                           schedule_data: Dict[str, Dict]) -> List[Dict]:
        """Get all scheduled slots for a specific subject"""
        
        subject_schedule = []
        for slot_key, booking in schedule_data.items():
            if booking['subject_code'] == subject_code:
                subject_schedule.append({
                    'time_slot': booking['time_slot'],
                    'room_number': booking['room_number'],
                    'faculty_id': booking['faculty_id']
                })
        
        return sorted(subject_schedule, key=lambda x: x['time_slot'])
    
    def get_room_schedule(self, room_number: str, 
                        schedule_data: Dict[str, Dict]) -> List[Dict]:
        """Get all scheduled slots for a specific room"""
        
        room_schedule = []
        for slot_key, booking in schedule_data.items():
            if booking['room_number'] == room_number:
                room_schedule.append({
                    'time_slot': booking['time_slot'],
                    'faculty_id': booking['faculty_id'],
                    'subject_code': booking['subject_code']
                })
        
        return sorted(room_schedule, key=lambda x: x['time_slot'])
    
    def validate_schedule_integrity(self, schedule_data: Dict[str, Dict]) -> List[str]:
        """Validate the entire schedule for any integrity issues"""
        
        issues = []
        
        # Check for any remaining conflicts
        for slot_key, booking in schedule_data.items():
            time_slot = booking['time_slot']
            room_number = booking['room_number']
            faculty_id = booking['faculty_id']
            subject_code = booking['subject_code']
            
            # Create temporary schedule without current booking
            temp_schedule = {k: v for k, v in schedule_data.items() if k != slot_key}
            
            # Check for conflicts
            conflicts = self.check_conflicts(time_slot, room_number, faculty_id, 
                                           subject_code, temp_schedule)
            if conflicts:
                issues.append(f"Conflict in slot {slot_key}: {conflicts}")
        
        return issues
    
    def suggest_alternative_slots(self, faculty_id: str, subject_code: str, 
                                schedule_data: Dict[str, Dict], 
                                all_time_slots: List[str], 
                                all_rooms: List[str]) -> List[Dict]:
        """Suggest alternative available slots for booking"""
        
        available_slots = []
        
        for time_slot in all_time_slots:
            for room_number in all_rooms:
                conflicts = self.check_conflicts(time_slot, room_number, faculty_id, 
                                               subject_code, schedule_data)
                if not conflicts:
                    available_slots.append({
                        'time_slot': time_slot,
                        'room_number': room_number,
                        'status': 'available'
                    })
        
        return available_slots
