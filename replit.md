# Faculty Scheduling System

## Overview

This is a Streamlit-based Faculty Scheduling System designed to manage faculty assignments, room bookings, and time periods for educational institutions. The system provides a web interface for scheduling classes, managing faculty data, and generating PDF reports with conflict detection capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

### December 2024
- Added day management to time periods (days of the week selection)
- Removed credits field from subject management for simplified interface
- Removed manual faculty ID input - now auto-generated for easier use
- Updated conflict detection to consider days when preventing double booking
- Enhanced schedule grid with day-specific view selection
- Simplified booking form by removing day selector (uses main schedule day selection)
- Updated PDF exports to only generate timetable for selected day
- Removed faculty details and subject list sections from PDF exports

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit (Python web framework)
- **User Interface**: Multi-page application with sidebar navigation
- **State Management**: Streamlit session state for maintaining application data
- **Layout**: Wide layout with column-based organization for optimal screen utilization

### Backend Architecture
- **Language**: Python
- **Architecture Pattern**: Utility-based modular design
- **Data Processing**: Pandas for data manipulation
- **File Operations**: JSON-based data persistence with base64 encoding for binary data

### Data Storage
- **Primary Storage**: Local JSON files in `/data` directory
- **Session Storage**: Streamlit session state for runtime data management
- **File Structure**: Separate JSON files for different data types (faculty, rooms, schedules, etc.)
- **Binary Data**: Base64 encoding for photo storage in JSON format

## Key Components

### Core Modules

1. **DataManager** (`utils/data_manager.py`)
   - Handles data persistence and retrieval
   - Manages JSON file operations with base64 encoding/decoding
   - Provides CRUD operations for all data types

2. **ConflictDetector** (`utils/conflict_detector.py`)
   - Detects scheduling conflicts for faculty, rooms, and subjects
   - Validates time slot availability
   - Prevents double bookings across multiple dimensions

3. **PDFGenerator** (`utils/pdf_generator.py`)
   - Generates PDF reports using ReportLab
   - Creates formatted schedule reports
   - Handles custom styling and layout

### Data Models
- **Faculty**: Auto-generated ID, name, department, email, phone, photo (optional)
- **Rooms**: Room number, capacity, equipment
- **Time Periods**: Time slots with associated days of the week
- **Subjects**: Subject codes, names, and departments
- **Schedule**: Time slot assignments linking faculty, rooms, subjects, and specific days

## Data Flow

1. **Initialization**: Application loads data from JSON files into session state
2. **User Interaction**: Users interact with Streamlit interface to modify data
3. **Conflict Detection**: System validates all scheduling changes for conflicts
4. **Data Persistence**: Changes are saved to JSON files via DataManager
5. **Report Generation**: PDF reports are generated on-demand from current data

## External Dependencies

### Core Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **PIL (Pillow)**: Image processing for faculty photos
- **ReportLab**: PDF generation library

### Standard Library Dependencies
- **json**: Data serialization
- **datetime**: Date and time handling
- **io**: Input/output operations
- **os**: Operating system interface
- **base64**: Binary data encoding
- **typing**: Type hints for better code documentation

## Deployment Strategy

### Local Development
- Run using `streamlit run app.py`
- Data stored in local `data/` directory
- No external database required

### Production Considerations
- File-based storage suitable for small to medium datasets
- May require database migration for larger deployments
- PDF generation handled server-side
- Image storage optimized through base64 encoding

### Scalability Notes
- Current architecture supports single-user or small team usage
- Database integration (like PostgreSQL with Drizzle) may be added for multi-user scenarios
- Session state management works well for individual user sessions