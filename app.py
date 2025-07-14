import streamlit as st
import pandas as pd
from PIL import Image
import io
import json
from datetime import datetime
from utils.data_manager import DataManager
from utils.pdf_generator import PDFGenerator
from utils.conflict_detector import ConflictDetector

# Initialize data manager
data_manager = DataManager()

# Page configuration
st.set_page_config(
    page_title="Faculty Scheduling System",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'faculty_data' not in st.session_state:
    st.session_state.faculty_data = data_manager.load_faculty_data()
if 'room_data' not in st.session_state:
    st.session_state.room_data = data_manager.load_room_data()
if 'time_data' not in st.session_state:
    st.session_state.time_data = data_manager.load_time_data()
if 'subject_data' not in st.session_state:
    st.session_state.subject_data = data_manager.load_subject_data()
if 'schedule_data' not in st.session_state:
    st.session_state.schedule_data = data_manager.load_schedule_data()

# Sidebar navigation
st.sidebar.title("🎓 Faculty Scheduling System")
page = st.sidebar.selectbox(
    "Navigate to:",
    ["📅 Schedule View", "👨‍🏫 Faculty Management", "🏢 Room Management", "⏰ Time Periods", "📚 Subject Management"]
)

def faculty_management():
    st.header("👨‍🏫 Faculty Management")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Faculty")
        faculty_name = st.text_input("Faculty Name", placeholder="e.g., Dr. John Smith")
        department = st.text_input("Department", placeholder="e.g., Computer Science")
        email = st.text_input("Email", placeholder="e.g., john.smith@university.edu")
        phone = st.text_input("Phone", placeholder="e.g., +1-234-567-8900")
        
        uploaded_photo = st.file_uploader("Upload Faculty Photo", type=['png', 'jpg', 'jpeg'])
        
        if st.button("Add Faculty", type="primary"):
            if faculty_name:
                photo_data = None
                if uploaded_photo:
                    photo_data = uploaded_photo.read()
                
                # Generate a unique ID based on name and timestamp
                import time
                faculty_id = f"FAC_{int(time.time())}"
                
                new_faculty = {
                    'id': faculty_id,
                    'name': faculty_name,
                    'department': department,
                    'email': email,
                    'phone': phone,
                    'photo': photo_data
                }
                
                st.session_state.faculty_data.append(new_faculty)
                data_manager.save_faculty_data(st.session_state.faculty_data)
                st.success("Faculty added successfully!")
                st.rerun()
            else:
                st.error("Please fill in faculty name")
    
    with col2:
        st.subheader("Existing Faculty")
        if st.session_state.faculty_data:
            for faculty in st.session_state.faculty_data:
                with st.expander(f"{faculty['name']}"):
                    col_info, col_photo = st.columns([2, 1])
                    
                    with col_info:
                        st.write(f"**Department:** {faculty.get('department', 'N/A')}")
                        st.write(f"**Email:** {faculty.get('email', 'N/A')}")
                        st.write(f"**Phone:** {faculty.get('phone', 'N/A')}")
                    
                    with col_photo:
                        if faculty.get('photo'):
                            try:
                                image = Image.open(io.BytesIO(faculty['photo']))
                                st.image(image, width=100)
                            except:
                                st.write("Photo unavailable")
                        else:
                            st.write("No photo")
                    
                    if st.button(f"Delete {faculty['name']}", key=f"del_fac_{faculty['id']}"):
                        st.session_state.faculty_data = [f for f in st.session_state.faculty_data if f['id'] != faculty['id']]
                        data_manager.save_faculty_data(st.session_state.faculty_data)
                        st.success("Faculty deleted successfully!")
                        st.rerun()
        else:
            st.info("No faculty members added yet.")

def room_management():
    st.header("🏢 Room Management")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Room")
        room_number = st.text_input("Room Number", placeholder="e.g., 101")
        capacity = st.number_input("Capacity", min_value=1, value=30)
        room_type = st.selectbox("Room Type", ["Lecture Hall", "Laboratory", "Seminar Room", "Conference Room"])
        facilities = st.text_area("Facilities", placeholder="e.g., Projector, AC, Whiteboard")
        
        if st.button("Add Room", type="primary"):
            if room_number:
                new_room = {
                    'number': room_number,
                    'capacity': capacity,
                    'type': room_type,
                    'facilities': facilities
                }
                
                if room_number not in [r['number'] for r in st.session_state.room_data]:
                    st.session_state.room_data.append(new_room)
                    data_manager.save_room_data(st.session_state.room_data)
                    st.success("Room added successfully!")
                    st.rerun()
                else:
                    st.error("Room number already exists!")
            else:
                st.error("Please enter a room number")
    
    with col2:
        st.subheader("Existing Rooms")
        if st.session_state.room_data:
            for room in st.session_state.room_data:
                with st.expander(f"Room {room['number']}"):
                    st.write(f"**Capacity:** {room['capacity']} students")
                    st.write(f"**Type:** {room['type']}")
                    st.write(f"**Facilities:** {room.get('facilities', 'N/A')}")
                    
                    if st.button(f"Delete Room {room['number']}", key=f"del_room_{room['number']}"):
                        st.session_state.room_data = [r for r in st.session_state.room_data if r['number'] != room['number']]
                        data_manager.save_room_data(st.session_state.room_data)
                        st.success("Room deleted successfully!")
                        st.rerun()
        else:
            st.info("No rooms added yet.")

def time_management():
    st.header("⏰ Time Period Management")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Time Period")
        
        # Day selection
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        selected_days = st.multiselect("Select Days", days_of_week, default=['Monday'])
        
        start_time = st.time_input("Start Time")
        end_time = st.time_input("End Time")
        
        if st.button("Add Time Period", type="primary"):
            if start_time < end_time and selected_days:
                time_slot = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
                
                # Check if this time slot with these days already exists
                existing_slots = [t for t in st.session_state.time_data 
                                if t['slot'] == time_slot and set(t['days']) == set(selected_days)]
                
                if not existing_slots:
                    new_time = {
                        'slot': time_slot,
                        'start': start_time.strftime('%H:%M'),
                        'end': end_time.strftime('%H:%M'),
                        'days': selected_days
                    }
                    st.session_state.time_data.append(new_time)
                    data_manager.save_time_data(st.session_state.time_data)
                    st.success("Time period added successfully!")
                    st.rerun()
                else:
                    st.error("Time period with these days already exists!")
            elif not selected_days:
                st.error("Please select at least one day")
            else:
                st.error("End time must be after start time")
    
    with col2:
        st.subheader("Existing Time Periods")
        if st.session_state.time_data:
            for time_slot in st.session_state.time_data:
                days_str = ', '.join(time_slot.get('days', ['N/A']))
                with st.expander(f"Time: {time_slot['slot']} ({days_str})"):
                    st.write(f"**Start:** {time_slot['start']}")
                    st.write(f"**End:** {time_slot['end']}")
                    st.write(f"**Days:** {days_str}")
                    
                    unique_key = f"{time_slot['slot']}_{hash(tuple(time_slot.get('days', [])))}"
                    if st.button(f"Delete {time_slot['slot']}", key=f"del_time_{unique_key}"):
                        st.session_state.time_data = [t for t in st.session_state.time_data if not (
                            t['slot'] == time_slot['slot'] and 
                            set(t.get('days', [])) == set(time_slot.get('days', []))
                        )]
                        data_manager.save_time_data(st.session_state.time_data)
                        st.success("Time period deleted successfully!")
                        st.rerun()
        else:
            st.info("No time periods added yet.")

def subject_management():
    st.header("📚 Subject Management")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Subject")
        subject_code = st.text_input("Subject Code", placeholder="e.g., CS101")
        subject_name = st.text_input("Subject Name", placeholder="e.g., Introduction to Programming")
        department = st.text_input("Department", placeholder="e.g., Computer Science")
        
        if st.button("Add Subject", type="primary"):
            if subject_code and subject_name:
                new_subject = {
                    'code': subject_code,
                    'name': subject_name,
                    'department': department
                }
                
                if subject_code not in [s['code'] for s in st.session_state.subject_data]:
                    st.session_state.subject_data.append(new_subject)
                    data_manager.save_subject_data(st.session_state.subject_data)
                    st.success("Subject added successfully!")
                    st.rerun()
                else:
                    st.error("Subject code already exists!")
            else:
                st.error("Please fill in required fields (Subject Code and Name)")
    
    with col2:
        st.subheader("Existing Subjects")
        if st.session_state.subject_data:
            for subject in st.session_state.subject_data:
                with st.expander(f"{subject['name']} ({subject['code']})"):
                    st.write(f"**Department:** {subject.get('department', 'N/A')}")
                    
                    if st.button(f"Delete {subject['code']}", key=f"del_subj_{subject['code']}"):
                        st.session_state.subject_data = [s for s in st.session_state.subject_data if s['code'] != subject['code']]
                        data_manager.save_subject_data(st.session_state.subject_data)
                        st.success("Subject deleted successfully!")
                        st.rerun()
        else:
            st.info("No subjects added yet.")

def schedule_view():
    st.header("📅 Schedule Management")
    
    # Control buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 Reset Schedule", type="secondary"):
            st.session_state.schedule_data = {}
            data_manager.save_schedule_data(st.session_state.schedule_data)
            st.success("Schedule reset successfully!")
            st.rerun()
    
    with col2:
        if st.button("📄 Export to PDF", type="primary"):
            if st.session_state.schedule_data:
                pdf_generator = PDFGenerator()
                pdf_buffer = pdf_generator.generate_schedule_pdf(
                    st.session_state.schedule_data,
                    st.session_state.faculty_data,
                    st.session_state.subject_data,
                    st.session_state.room_data,
                    st.session_state.time_data
                )
                
                st.download_button(
                    label="Download PDF",
                    data=pdf_buffer,
                    file_name=f"schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
            else:
                st.warning("No schedule data to export!")
    
    with col3:
        st.write("")  # Spacer
    
    # Schedule Grid
    if st.session_state.room_data and st.session_state.time_data:
        st.subheader("📋 Schedule Grid")
        
        # Day selection for viewing
        all_days = set()
        for time_slot in st.session_state.time_data:
            all_days.update(time_slot.get('days', ['Monday']))
        
        selected_day_view = st.selectbox("Select Day to View", sorted(all_days), key="day_view")
        
        # Create grid layout
        rooms = sorted(st.session_state.room_data, key=lambda x: x['number'])
        time_slots = sorted([t for t in st.session_state.time_data if selected_day_view in t.get('days', ['Monday'])], key=lambda x: x['start'])
        
        # Header row
        header_cols = st.columns([1.5] + [2] * len(rooms))
        with header_cols[0]:
            st.write("**Time / Room**")
        
        for i, room in enumerate(rooms):
            with header_cols[i + 1]:
                st.write(f"**{room['number']}**")
        
        # Time slot rows for selected day
        for time_slot in time_slots:
            row_cols = st.columns([1.5] + [2] * len(rooms))
            
            with row_cols[0]:
                st.write(f"**{time_slot['slot']}**")
                st.write(f"*{selected_day_view}*")
            
            for i, room in enumerate(rooms):
                with row_cols[i + 1]:
                    slot_key = f"{time_slot['slot']}_{room['number']}"
                    day_slot_key = f"{time_slot['slot']}_{room['number']}_{selected_day_view}"
                    
                    if day_slot_key in st.session_state.schedule_data:
                        # Show booked slot
                        booking = st.session_state.schedule_data[day_slot_key]
                        faculty = next((f for f in st.session_state.faculty_data if f['id'] == booking['faculty_id']), None)
                        subject = next((s for s in st.session_state.subject_data if s['code'] == booking['subject_code']), None)
                        
                        if faculty and subject:
                            # Display faculty photo if available
                            if faculty.get('photo'):
                                try:
                                    image = Image.open(io.BytesIO(faculty['photo']))
                                    st.image(image, width=60)
                                except:
                                    st.write("📷")
                            else:
                                st.write("👤")
                            
                            st.write(f"**{faculty['name']}**")
                            st.write(f"{subject['name']}")
                            st.write(f"*{booking['day']}*")
                            
                            if st.button("❌", key=f"remove_{day_slot_key}"):
                                del st.session_state.schedule_data[day_slot_key]
                                data_manager.save_schedule_data(st.session_state.schedule_data)
                                st.rerun()
                    else:
                        # Show available slot
                        st.write("📅")
                        st.write("**Available**")
                        st.write("Click to book")
                        
                        if st.button("📝 Book", key=f"book_{slot_key}"):
                            st.session_state.booking_slot = slot_key
                            st.session_state.show_booking_form = True
                            st.rerun()
        
        # Booking form
        if st.session_state.get('show_booking_form', False):
            st.subheader("📝 Book Schedule Slot")
            
            slot_key = st.session_state.get('booking_slot')
            time_slot, room_number = slot_key.split('_')
            
            # Find the time period data for this slot
            time_period = next((t for t in st.session_state.time_data if t['slot'] == time_slot), None)
            available_days = time_period.get('days', ['Monday']) if time_period else ['Monday']
            
            st.write(f"**Booking for:** {time_slot} in Room {room_number}")
            st.write(f"**Available Days:** {', '.join(available_days)}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                selected_day = st.selectbox("Select Day", available_days)
            
            with col2:
                faculty_options = [(f['id'], f['name']) for f in st.session_state.faculty_data]
                selected_faculty = st.selectbox(
                    "Select Faculty",
                    options=[f[0] for f in faculty_options],
                    format_func=lambda x: next(f[1] for f in faculty_options if f[0] == x)
                )
            
            with col3:
                subject_options = [(s['code'], s['name']) for s in st.session_state.subject_data]
                selected_subject = st.selectbox(
                    "Select Subject",
                    options=[s[0] for s in subject_options],
                    format_func=lambda x: next(s[1] for s in subject_options if s[0] == x)
                )
            
            col_book, col_cancel = st.columns(2)
            
            with col_book:
                if st.button("✅ Confirm Booking", type="primary"):
                    conflict_detector = ConflictDetector()
                    conflicts = conflict_detector.check_conflicts(
                        time_slot, room_number, selected_faculty, selected_subject,
                        st.session_state.schedule_data, selected_day
                    )
                    
                    if conflicts:
                        st.error(f"⚠️ Booking conflict detected: {conflicts}")
                    else:
                        # Create a unique key that includes the day
                        day_slot_key = f"{time_slot}_{room_number}_{selected_day}"
                        st.session_state.schedule_data[day_slot_key] = {
                            'faculty_id': selected_faculty,
                            'subject_code': selected_subject,
                            'time_slot': time_slot,
                            'room_number': room_number,
                            'day': selected_day
                        }
                        data_manager.save_schedule_data(st.session_state.schedule_data)
                        st.session_state.show_booking_form = False
                        st.success("Booking confirmed successfully!")
                        st.rerun()
            
            with col_cancel:
                if st.button("❌ Cancel", type="secondary"):
                    st.session_state.show_booking_form = False
                    st.rerun()
    
    else:
        st.warning("Please add rooms and time periods first to create the schedule grid.")

# Main app logic
if page == "📅 Schedule View":
    schedule_view()
elif page == "👨‍🏫 Faculty Management":
    faculty_management()
elif page == "🏢 Room Management":
    room_management()
elif page == "⏰ Time Periods":
    time_management()
elif page == "📚 Subject Management":
    subject_management()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("🎓 **Faculty Scheduling System**")
st.sidebar.markdown("Built with Streamlit")
