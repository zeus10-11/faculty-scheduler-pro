import streamlit as st
import json
import os
from typing import List, Dict, Any
import base64

class DataManager:
    """Manages data persistence using session state and local file storage simulation"""
    
    def __init__(self):
        self.data_dir = "data"
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_faculty_data(self, faculty_data: List[Dict[str, Any]]):
        """Save faculty data to local storage"""
        # Convert photos to base64 for JSON serialization
        serializable_data = []
        for faculty in faculty_data:
            faculty_copy = faculty.copy()
            if faculty_copy.get('photo'):
                faculty_copy['photo'] = base64.b64encode(faculty_copy['photo']).decode('utf-8')
            serializable_data.append(faculty_copy)
        
        with open(os.path.join(self.data_dir, 'faculty.json'), 'w') as f:
            json.dump(serializable_data, f, indent=2)
    
    def load_faculty_data(self) -> List[Dict[str, Any]]:
        """Load faculty data from local storage"""
        try:
            with open(os.path.join(self.data_dir, 'faculty.json'), 'r') as f:
                data = json.load(f)
                # Convert base64 photos back to bytes
                for faculty in data:
                    if faculty.get('photo'):
                        faculty['photo'] = base64.b64decode(faculty['photo'].encode('utf-8'))
                return data
        except FileNotFoundError:
            return []
    
    def save_room_data(self, room_data: List[Dict[str, Any]]):
        """Save room data to local storage"""
        with open(os.path.join(self.data_dir, 'rooms.json'), 'w') as f:
            json.dump(room_data, f, indent=2)
    
    def load_room_data(self) -> List[Dict[str, Any]]:
        """Load room data from local storage"""
        try:
            with open(os.path.join(self.data_dir, 'rooms.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_time_data(self, time_data: List[Dict[str, Any]]):
        """Save time period data to local storage"""
        with open(os.path.join(self.data_dir, 'time_periods.json'), 'w') as f:
            json.dump(time_data, f, indent=2)
    
    def load_time_data(self) -> List[Dict[str, Any]]:
        """Load time period data from local storage"""
        try:
            with open(os.path.join(self.data_dir, 'time_periods.json'), 'r') as f:
                data = json.load(f)
                # Migration: add 'days' field if it doesn't exist
                for time_period in data:
                    if 'days' not in time_period:
                        time_period['days'] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
                return data
        except FileNotFoundError:
            return []
    
    def save_subject_data(self, subject_data: List[Dict[str, Any]]):
        """Save subject data to local storage"""
        with open(os.path.join(self.data_dir, 'subjects.json'), 'w') as f:
            json.dump(subject_data, f, indent=2)
    
    def load_subject_data(self) -> List[Dict[str, Any]]:
        """Load subject data from local storage"""
        try:
            with open(os.path.join(self.data_dir, 'subjects.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_schedule_data(self, schedule_data: Dict[str, Any]):
        """Save schedule data to local storage"""
        with open(os.path.join(self.data_dir, 'schedule.json'), 'w') as f:
            json.dump(schedule_data, f, indent=2)
    
    def load_schedule_data(self) -> Dict[str, Any]:
        """Load schedule data from local storage"""
        try:
            with open(os.path.join(self.data_dir, 'schedule.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def export_all_data(self) -> Dict[str, Any]:
        """Export all data for backup purposes"""
        return {
            'faculty': self.load_faculty_data(),
            'rooms': self.load_room_data(),
            'time_periods': self.load_time_data(),
            'subjects': self.load_subject_data(),
            'schedule': self.load_schedule_data()
        }
    
    def import_all_data(self, data: Dict[str, Any]):
        """Import all data from backup"""
        if 'faculty' in data:
            self.save_faculty_data(data['faculty'])
        if 'rooms' in data:
            self.save_room_data(data['rooms'])
        if 'time_periods' in data:
            self.save_time_data(data['time_periods'])
        if 'subjects' in data:
            self.save_subject_data(data['subjects'])
        if 'schedule' in data:
            self.save_schedule_data(data['schedule'])
