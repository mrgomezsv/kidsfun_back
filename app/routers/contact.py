from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..database import get_db
from ..models.contact import Contact
from ..models.user import User
from ..schemas.contact import ContactCreate, ContactUpdate, ContactResponse, ContactList
from ..routers.auth import get_current_user
from ..config import settings

router = APIRouter()

def send_contact_email(contact: Contact) -> bool:
    """
    Enviar email de notificación cuando se recibe un formulario de contacto
    """
    try:
        # Configurar el mensaje
        msg = MIMEMultipart()
        msg['From'] = settings.smtp_user
        msg['To'] = settings.smtp_user  # Enviar a la misma dirección configurada
        msg['Subject'] = f"Nuevo formulario de contacto - {contact.first_name} {contact.last_name}"

        # Cuerpo del email
        body = f"""
        Se ha recibido un nuevo formulario de contacto:

        **Información del Contacto:**
        - Nombre: {contact.first_name} {contact.last_name}
        - Email: {contact.email}
        - Teléfono: {contact.contact_number}
        - Fecha: {contact.created_at.strftime('%Y-%m-%d %H:%M:%S')}

        **Mensaje:**
        {contact.reason}

        ---
        Este mensaje fue enviado automáticamente desde el formulario de contacto de KidsFun.
        """

        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # Enviar email
        server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        text = msg.as_string()
        server.sendmail(settings.smtp_user, settings.smtp_user, text)
        server.quit()

        return True

    except Exception as e:
        print(f"Error enviando email de contacto: {str(e)}")
        return False

@router.post("/", response_model=ContactResponse)
async def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo formulario de contacto
    """
    try:
        # Crear el contacto
        db_contact = Contact(**contact.dict())
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)

        # Enviar email de notificación
        email_sent = send_contact_email(db_contact)

        return {
            "id": db_contact.id,
            "first_name": db_contact.first_name,
            "last_name": db_contact.last_name,
            "contact_number": db_contact.contact_number,
            "email": db_contact.email,
            "reason": db_contact.reason,
            "created_at": db_contact.created_at,
            "is_read": db_contact.is_read,
            "is_responded": db_contact.is_responded
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear contacto: {str(e)}"
        )

@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_read: Optional[bool] = None,
    is_responded: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener todos los formularios de contacto (requiere autenticación)
    """
    query = db.query(Contact)
    
    if is_read is not None:
        query = query.filter(Contact.is_read == is_read)
    
    if is_responded is not None:
        query = query.filter(Contact.is_responded == is_responded)
    
    contacts = query.order_by(Contact.created_at.desc()).offset(skip).limit(limit).all()
    
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener un formulario de contacto específico (requiere autenticación)
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    contact_update: ContactUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar un formulario de contacto (requiere autenticación)
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    
    update_data = contact_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contact, field, value)
    
    db.commit()
    db.refresh(contact)
    
    return contact

@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar un formulario de contacto (requiere autenticación)
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    
    db.delete(contact)
    db.commit()
    
    return {"message": "Contacto eliminado exitosamente"}

@router.get("/stats/summary")
async def get_contact_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener estadísticas de formularios de contacto (requiere autenticación)
    """
    total_contacts = db.query(Contact).count()
    unread_contacts = db.query(Contact).filter(Contact.is_read == False).count()
    responded_contacts = db.query(Contact).filter(Contact.is_responded == True).count()
    
    return {
        "total_contacts": total_contacts,
        "unread_contacts": unread_contacts,
        "responded_contacts": responded_contacts,
        "pending_contacts": total_contacts - responded_contacts
    } 