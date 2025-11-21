from fpdf import FPDF
import os
import re

class PDFGenerator(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'Global Travel Planner Itinerary', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Helvetica', 'B', 14)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 10, label, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Helvetica', '', 11)
        # Basic Markdown Parsing
        lines = body.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                self.ln(2)
                continue
            
            # Header detection (## or ###)
            if line.startswith('##') or line.startswith('###'):
                clean_line = line.replace('#', '').strip()
                self.set_font('Helvetica', 'B', 12)
                self.cell(0, 8, clean_line, 0, 1)
                self.set_font('Helvetica', '', 11)
            # Bullet points
            elif line.startswith('- ') or line.startswith('* '):
                clean_line = line[2:].strip()
                # Handle bolding within line (simple regex for **text**)
                self.write_formatted_line(clean_line, is_bullet=True)
            else:
                self.write_formatted_line(line)
        self.ln()

    def write_formatted_line(self, text, is_bullet=False):
        # Simple bold parser: splits by ** and alternates font
        parts = re.split(r'(\*\*.*?\*\*)', text)
        
        if is_bullet:
            self.cell(5, 6, chr(149), 0, 0) # Bullet char
        
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                self.set_font('Helvetica', 'B', 11)
                clean_part = part[2:-2]
                # Encode to latin-1 to handle special chars, replace errors
                clean_part = clean_part.encode('latin-1', 'replace').decode('latin-1')
                self.write(6, clean_part)
            else:
                self.set_font('Helvetica', '', 11)
                # Encode to latin-1
                part = part.encode('latin-1', 'replace').decode('latin-1')
                self.write(6, part)
        
        self.ln()

def generate_pdf(content: str, filename: str = "itinerary.pdf", return_bytes: bool = False):
    pdf = PDFGenerator()
    pdf.add_page()
    
    # Split content by main headers (# Header) if possible, or just treat as one block
    # For simplicity, let's process line by line in chapter_body
    pdf.chapter_body(content)
    
    if return_bytes:
        # 'S' returns a string, we need to encode it to latin-1 to get the binary PDF content
        return pdf.output(dest='S').encode('latin-1')
    
    output_path = os.path.join(os.getcwd(), filename)
    pdf.output(output_path)
    return output_path
