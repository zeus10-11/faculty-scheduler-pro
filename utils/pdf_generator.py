from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
from datetime import datetime
from typing import Dict, List, Any

class PDFGenerator:
    """Generates PDF reports for the scheduling system"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for PDF generation"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.darkblue,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.darkgreen,
            alignment=TA_LEFT,
            spaceAfter=10
        )
    
    def generate_schedule_pdf(self, schedule_data: Dict[str, Any], faculty_data: List[Dict], 
                            subject_data: List[Dict], room_data: List[Dict], 
                            time_data: List[Dict]) -> bytes:
        """Generate PDF report of the current schedule"""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Build PDF content
        story = []
        
        # Title
        title = Paragraph("Faculty Schedule Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Generation info
        generation_info = Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
            self.styles['Normal']
        )
        story.append(generation_info)
        story.append(Spacer(1, 20))
        
        # Schedule summary
        summary_header = Paragraph("Schedule Summary", self.header_style)
        story.append(summary_header)
        
        total_bookings = len(schedule_data)
        unique_faculty = len(set(booking['faculty_id'] for booking in schedule_data.values()))
        unique_subjects = len(set(booking['subject_code'] for booking in schedule_data.values()))
        
        summary_text = f"""
        Total Bookings: {total_bookings}<br/>
        Faculty Involved: {unique_faculty}<br/>
        Subjects Scheduled: {unique_subjects}<br/>
        Rooms in Use: {len(set(booking['room_number'] for booking in schedule_data.values()))}
        """
        
        summary_para = Paragraph(summary_text, self.styles['Normal'])
        story.append(summary_para)
        story.append(Spacer(1, 20))
        
        # Schedule table
        if schedule_data:
            schedule_header = Paragraph("Detailed Schedule", self.header_style)
            story.append(schedule_header)
            
            # Create schedule table
            rooms = sorted(set(room['number'] for room in room_data))
            time_slots = sorted(set(time['slot'] for time in time_data), 
                              key=lambda x: x.split(' - ')[0])
            
            # Table headers
            table_data = [['Time / Room'] + rooms]
            
            # Fill table data
            for time_slot in time_slots:
                row = [time_slot]
                for room in rooms:
                    # Check for any booking in this time slot and room across all days
                    cell_content = "Available"
                    bookings_for_slot = []
                    
                    for slot_key, booking in schedule_data.items():
                        if booking['time_slot'] == time_slot and booking['room_number'] == room:
                            faculty = next((f for f in faculty_data if f['id'] == booking['faculty_id']), None)
                            subject = next((s for s in subject_data if s['code'] == booking['subject_code']), None)
                            
                            if faculty and subject:
                                day_info = f" ({booking.get('day', 'N/A')})" if booking.get('day') else ""
                                bookings_for_slot.append(f"{faculty['name']}\n{subject['name']}{day_info}")
                    
                    if bookings_for_slot:
                        cell_content = "\n---\n".join(bookings_for_slot)
                    
                    row.append(cell_content)
                table_data.append(row)
            
            # Create table
            table = Table(table_data, colWidths=[1.5*inch] + [1.2*inch] * len(rooms))
            
            # Style the table
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('WORDWRAP', (0, 0), (-1, -1), True),
            ]))
            
            story.append(table)
            story.append(Spacer(1, 20))
        
        # Faculty list
        if faculty_data:
            faculty_header = Paragraph("Faculty List", self.header_style)
            story.append(faculty_header)
            
            faculty_table_data = [['Faculty ID', 'Name', 'Department']]
            for faculty in faculty_data:
                faculty_table_data.append([
                    faculty['id'],
                    faculty['name'],
                    faculty.get('department', 'N/A')
                ])
            
            faculty_table = Table(faculty_table_data, colWidths=[1.5*inch, 2*inch, 2*inch])
            faculty_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            story.append(faculty_table)
            story.append(Spacer(1, 20))
        
        # Subject list
        if subject_data:
            subject_header = Paragraph("Subject List", self.header_style)
            story.append(subject_header)
            
            subject_table_data = [['Subject Code', 'Subject Name', 'Credits']]
            for subject in subject_data:
                subject_table_data.append([
                    subject['code'],
                    subject['name'],
                    str(subject['credits'])
                ])
            
            subject_table = Table(subject_table_data, colWidths=[1.5*inch, 3*inch, 1*inch])
            subject_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            story.append(subject_table)
        
        # Build PDF
        doc.build(story)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def generate_faculty_report(self, faculty_data: List[Dict], schedule_data: Dict[str, Any]) -> bytes:
        """Generate a detailed faculty report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        title = Paragraph("Faculty Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Faculty workload analysis
        faculty_workload = {}
        for slot_key, booking in schedule_data.items():
            faculty_id = booking['faculty_id']
            if faculty_id not in faculty_workload:
                faculty_workload[faculty_id] = 0
            faculty_workload[faculty_id] += 1
        
        workload_header = Paragraph("Faculty Workload Analysis", self.header_style)
        story.append(workload_header)
        
        workload_table_data = [['Faculty Name', 'Total Classes', 'Workload Status']]
        for faculty in faculty_data:
            faculty_id = faculty['id']
            total_classes = faculty_workload.get(faculty_id, 0)
            
            if total_classes == 0:
                status = "No classes assigned"
            elif total_classes <= 3:
                status = "Light workload"
            elif total_classes <= 6:
                status = "Moderate workload"
            else:
                status = "Heavy workload"
            
            workload_table_data.append([
                faculty['name'],
                str(total_classes),
                status
            ])
        
        workload_table = Table(workload_table_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
        workload_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(workload_table)
        
        # Build PDF
        doc.build(story)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
