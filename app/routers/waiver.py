from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import os
import tempfile
from datetime import datetime, timedelta
import qrcode
from io import BytesIO
import base64

from ..database import get_db
from ..models.waiver import WaiverData, WaiverValidator, WaiverDataDB
from ..models.user import User
from ..schemas.waiver import (
    WaiverCreate, WaiverResponse, WaiverValidation, 
    WaiverDataCreate, WaiverValidatorCreate, WaiverValidatorResponse
)
from ..routers.auth import get_current_user
from ..config import settings
from ..utils.email import send_waiver_email
from ..utils.pdf import create_waiver_pdf

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_waivers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener todos los waivers del usuario actual"""
    try:
        waivers = db.query(WaiverValidator).filter(
            WaiverValidator.user_id == current_user.id
        ).order_by(WaiverValidator.created_at.desc()).all()

        waiver_list = []
        for waiver in waivers:
            relatives_data = db.query(WaiverData).filter(
                WaiverData.user_id == waiver.user_id
            ).all()

            relatives = []
            for relative in relatives_data:
                relatives.append({
                    "name": relative.relative_name,
                    "age": relative.relative_age
                })

            waiver_age = datetime.now() - waiver.created_at
            status = "ACTIVE" if waiver_age <= timedelta(hours=24) else "EXPIRED"

            waiver_list.append({
                "qr_code": waiver.email,
                "user_name": relatives_data[0].user_name if relatives_data else "Usuario",
                "user_email": waiver.email,
                "created_at": waiver.created_at,
                "status": status,
                "relatives": relatives
            })

        return waiver_list

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener waivers: {str(e)}"
        )

@router.post("/", response_model=WaiverResponse)
async def create_waiver(
    waiver: WaiverCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear un nuevo waiver con QR único"""
    try:
        # Verificar si ya existe un waiver activo para este usuario hoy
        today = datetime.now().date()
        existing_waiver = db.query(WaiverValidator).filter(
            WaiverValidator.user_id == waiver.user_id,
            func.date(WaiverValidator.created_at) == today
        ).first()

        if existing_waiver:
            return {
                "message": "Ya existe un waiver activo para hoy.",
                "waiver": {
                    "qr_code": existing_waiver.email,  # Usamos email como QR temporal
                    "user_name": waiver.user_name,
                    "user_email": existing_waiver.email,
                    "created_at": existing_waiver.created_at,
                    "status": "ACTIVE"
                },
                "is_new": False
            }

        # Crear nuevo waiver validator
        waiver_validator = WaiverValidator(
            user_id=waiver.user_id,
            email=waiver.user_email
        )
        db.add(waiver_validator)
        db.commit()
        db.refresh(waiver_validator)

        # Guardar datos de familiares
        for relative in waiver.relatives:
            waiver_data = WaiverData(
                user_id=waiver.user_id,
                user_name=waiver.user_name,
                relative_name=relative.name,
                relative_age=relative.age
            )
            db.add(waiver_data)

        # Crear QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(waiver_validator.email)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir QR a base64
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode()

        # Generar PDF
        pdf_buffer = create_waiver_pdf(
            user_name=waiver.user_name,
            user_email=waiver.user_email,
            relatives=waiver.relatives
        )

        # Enviar email con PDF
        email_sent = send_waiver_email(
            user_email=waiver.user_email,
            user_name=waiver.user_name,
            qr_code=waiver_validator.email,
            pdf_buffer=pdf_buffer,
            relatives=waiver.relatives
        )

        db.commit()

        return {
            "message": "Waiver creado exitosamente y correo enviado.",
            "waiver": {
                "qr_code": waiver_validator.email,
                "qr_image": qr_base64,
                "user_name": waiver.user_name,
                "user_email": waiver.user_email,
                "created_at": waiver_validator.created_at,
                "status": "ACTIVE"
            },
            "email_sent": email_sent,
            "is_new": True
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear waiver: {str(e)}"
        )

@router.post("/validate", response_model=dict)
async def validate_waiver(
    validation: WaiverValidation,
    db: Session = Depends(get_db)
):
    """Validar un waiver por QR code"""
    try:
        # Buscar waiver por email (que actúa como QR code)
        waiver = db.query(WaiverValidator).filter(
            WaiverValidator.email == validation.qr_code
        ).first()

        if not waiver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Waiver no encontrado"
            )

        # Verificar si el waiver está activo (menos de 24 horas)
        waiver_age = datetime.now() - waiver.created_at
        if waiver_age > timedelta(hours=24):
            return {
                "valid": False,
                "message": "Waiver expirado",
                "waiver": {
                    "qr_code": waiver.email,
                    "user_name": "Usuario",
                    "status": "EXPIRED"
                }
            }

        # Obtener datos de familiares
        relatives_data = db.query(WaiverData).filter(
            WaiverData.user_id == waiver.user_id
        ).all()

        relatives = []
        for relative in relatives_data:
            relatives.append({
                "name": relative.relative_name,
                "age": relative.relative_age
            })

        return {
            "valid": True,
            "message": "Waiver válido",
            "waiver": {
                "qr_code": waiver.email,
                "user_name": relatives_data[0].user_name if relatives_data else "Usuario",
                "user_email": waiver.email,
                "created_at": waiver.created_at,
                "status": "ACTIVE",
                "relatives": relatives
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al validar waiver: {str(e)}"
        )

@router.get("/{qr_code}", response_model=dict)
async def get_waiver_data(
    qr_code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener datos de un waiver por QR code"""
    try:
        waiver = db.query(WaiverValidator).filter(
            WaiverValidator.email == qr_code
        ).first()

        if not waiver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Waiver no encontrado"
            )

        relatives_data = db.query(WaiverData).filter(
            WaiverData.user_id == waiver.user_id
        ).all()

        relatives = []
        for relative in relatives_data:
            relatives.append({
                "name": relative.relative_name,
                "age": relative.relative_age
            })

        return {
            "waiver": {
                "qr_code": waiver.email,
                "user_name": relatives_data[0].user_name if relatives_data else "Usuario",
                "user_email": waiver.email,
                "created_at": waiver.created_at,
                "relatives": relatives
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener datos del waiver: {str(e)}"
        )

@router.get("/user/{user_id}", response_model=dict)
async def get_user_waivers(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Obtener todos los waivers de un usuario"""
    try:
        waivers = db.query(WaiverValidator).filter(
            WaiverValidator.user_id == user_id
        ).order_by(WaiverValidator.created_at.desc()).all()

        waiver_list = []
        for waiver in waivers:
            relatives_data = db.query(WaiverData).filter(
                WaiverData.user_id == waiver.user_id
            ).all()

            relatives = []
            for relative in relatives_data:
                relatives.append({
                    "name": relative.relative_name,
                    "age": relative.relative_age
                })

            waiver_age = datetime.now() - waiver.created_at
            status = "ACTIVE" if waiver_age <= timedelta(hours=24) else "EXPIRED"

            waiver_list.append({
                "qr_code": waiver.email,
                "user_name": relatives_data[0].user_name if relatives_data else "Usuario",
                "user_email": waiver.email,
                "created_at": waiver.created_at,
                "status": status,
                "relatives": relatives
            })

        return {
            "total_count": len(waiver_list),
            "waivers": waiver_list
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener waivers del usuario: {str(e)}"
        )

@router.post("/admin/validator", response_model=WaiverValidatorResponse)
async def create_waiver_validator(
    validator: WaiverValidatorCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear un nuevo validador de waivers (solo admin)"""
    try:
        # Verificar si el email ya existe
        existing_validator = db.query(WaiverValidator).filter(
            WaiverValidator.email == validator.email
        ).first()

        if existing_validator:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un validador con este email"
            )

        new_validator = WaiverValidator(
            user_id=current_user.id,
            email=validator.email
        )
        db.add(new_validator)
        db.commit()
        db.refresh(new_validator)

        return {
            "id": new_validator.id,
            "email": new_validator.email,
            "created_at": new_validator.created_at
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear validador: {str(e)}"
        ) 