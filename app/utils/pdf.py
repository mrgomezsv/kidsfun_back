from io import BytesIO
from typing import List
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime

def create_waiver_pdf(
    user_name: str,
    user_email: str,
    relatives: List[dict]
) -> BytesIO:
    """
    Crear PDF del waiver con la información del usuario y familiares
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Crear estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Centrado
        textColor=colors.darkblue
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        textColor=colors.darkblue
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12
    )
    
    # Contenido del PDF
    story = []
    
    # Título principal
    story.append(Paragraph("WAIVER DE RESPONSABILIDAD", title_style))
    story.append(Spacer(1, 20))
    
    # Información del usuario
    story.append(Paragraph("Información del Usuario", subtitle_style))
    story.append(Paragraph(f"<b>Nombre:</b> {user_name}", normal_style))
    story.append(Paragraph(f"<b>Email:</b> {user_email}", normal_style))
    story.append(Paragraph(f"<b>Fecha de creación:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    story.append(Spacer(1, 20))
    
    # Familiares
    story.append(Paragraph("Familiares Registrados", subtitle_style))
    
    if relatives:
        # Crear tabla de familiares
        data = [['Nombre', 'Edad']]
        for relative in relatives:
            data.append([relative['name'], str(relative['age'])])
        
        table = Table(data, colWidths=[3*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
    else:
        story.append(Paragraph("No hay familiares registrados", normal_style))
    
    story.append(Spacer(1, 30))
    
    # Términos y condiciones
    story.append(Paragraph("Términos y Condiciones", subtitle_style))
    
    terms = [
        "1. Este waiver es válido por 24 horas desde su creación.",
        "2. Debe presentar este documento al llegar a KidsFun.",
        "3. El código QR será escaneado para validar su entrada.",
        "4. Es responsabilidad del usuario mantener este documento seguro.",
        "5. KidsFun no se hace responsable por pérdida o daño del documento.",
        "6. Este waiver es personal e intransferible.",
        "7. En caso de dudas, contacte al personal de KidsFun."
    ]
    
    for term in terms:
        story.append(Paragraph(term, normal_style))
    
    story.append(Spacer(1, 30))
    
    # Pie de página
    story.append(Paragraph("KidsFun - Fiestas Infantiles", subtitle_style))
    story.append(Paragraph("Documento generado automáticamente", normal_style))
    
    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    
    return buffer 