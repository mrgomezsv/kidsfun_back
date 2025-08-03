from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
import json

from ..database import get_db
from ..models.chat import ChatRoom, ChatMessage, ChatAdministrator
from ..models.user import User
from ..schemas.chat import (
    ChatRoomCreate, ChatRoomResponse, ChatMessageCreate, 
    ChatMessageResponse, ChatAdministratorCreate, ChatAdministratorResponse
)
from ..routers.auth import get_current_user
from ..config import settings

router = APIRouter()

# Almacenamiento en memoria para WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}  # chat_id -> list of connections

    async def connect(self, websocket: WebSocket, chat_id: int):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, websocket: WebSocket, chat_id: int):
        if chat_id in self.active_connections:
            self.active_connections[chat_id].remove(websocket)
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_chat(self, message: str, chat_id: int):
        if chat_id in self.active_connections:
            for connection in self.active_connections[chat_id]:
                try:
                    await connection.send_text(message)
                except:
                    # Remover conexiones muertas
                    self.active_connections[chat_id].remove(connection)

manager = ConnectionManager()

@router.get("/", response_model=List[ChatRoomResponse])
async def get_chat_rooms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener todas las salas de chat del usuario"""
    try:
        # Verificar si el usuario es administrador
        is_admin = db.query(ChatAdministrator).filter(
            ChatAdministrator.user_id == current_user.id,
            ChatAdministrator.is_active == True
        ).first()

        if is_admin:
            # Administrador ve todas las salas activas
            rooms = db.query(ChatRoom).filter(
                ChatRoom.is_active == True
            ).order_by(ChatRoom.last_message_at.desc()).all()
        else:
            # Usuario normal ve solo sus salas
            rooms = db.query(ChatRoom).filter(
                ChatRoom.user_id == current_user.id,
                ChatRoom.is_active == True
            ).order_by(ChatRoom.last_message_at.desc()).all()

        return [
            {
                "id": room.id,
                "user_id": room.user_id,
                "created_at": room.created_at,
                "is_active": room.is_active,
                "last_message_at": room.last_message_at,
                "user_name": room.user.username if room.user else "Usuario"
            }
            for room in rooms
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener salas de chat: {str(e)}"
        )

@router.post("/", response_model=ChatRoomResponse)
async def create_chat_room(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear una nueva sala de chat"""
    try:
        # Verificar si ya existe una sala activa para este usuario
        existing_room = db.query(ChatRoom).filter(
            ChatRoom.user_id == current_user.id,
            ChatRoom.is_active == True
        ).first()

        if existing_room:
            return {
                "id": existing_room.id,
                "user_id": existing_room.user_id,
                "created_at": existing_room.created_at,
                "is_active": existing_room.is_active,
                "last_message_at": existing_room.last_message_at,
                "user_name": existing_room.user.username if existing_room.user else "Usuario"
            }

        # Crear nueva sala
        new_room = ChatRoom(
            user_id=current_user.id
        )
        db.add(new_room)
        db.commit()
        db.refresh(new_room)

        # Crear mensaje de bienvenida
        welcome_message = ChatMessage(
            chat_room_id=new_room.id,
            sender_id=current_user.id,
            content="¡Hola! Bienvenido al chat de KidsFun. ¿En qué podemos ayudarte?"
        )
        db.add(welcome_message)
        db.commit()

        return {
            "id": new_room.id,
            "user_id": new_room.user_id,
            "created_at": new_room.created_at,
            "is_active": new_room.is_active,
            "last_message_at": new_room.last_message_at,
            "user_name": new_room.user.username if new_room.user else "Usuario"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear sala de chat: {str(e)}"
        )

@router.get("/{room_id}", response_model=ChatRoomResponse)
async def get_chat_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener una sala de chat específica"""
    try:
        # Verificar acceso a la sala
        room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sala de chat no encontrada"
            )

        # Verificar si el usuario tiene acceso
        is_admin = db.query(ChatAdministrator).filter(
            ChatAdministrator.user_id == current_user.id,
            ChatAdministrator.is_active == True
        ).first()

        if not is_admin and room.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a esta sala de chat"
            )

        return {
            "id": room.id,
            "user_id": room.user_id,
            "created_at": room.created_at,
            "is_active": room.is_active,
            "last_message_at": room.last_message_at,
            "user_name": room.user.username if room.user else "Usuario"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener sala de chat: {str(e)}"
        )

@router.get("/rooms", response_model=List[ChatRoomResponse])
async def get_chat_rooms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener todas las salas de chat del usuario"""
    try:
        # Verificar si el usuario es administrador
        is_admin = db.query(ChatAdministrator).filter(
            ChatAdministrator.user_id == current_user.id,
            ChatAdministrator.is_active == True
        ).first()

        if is_admin:
            # Administrador ve todas las salas activas
            rooms = db.query(ChatRoom).filter(
                ChatRoom.is_active == True
            ).order_by(ChatRoom.last_message_at.desc()).all()
        else:
            # Usuario normal ve solo sus salas
            rooms = db.query(ChatRoom).filter(
                ChatRoom.user_id == current_user.id,
                ChatRoom.is_active == True
            ).order_by(ChatRoom.last_message_at.desc()).all()

        return [
            {
                "id": room.id,
                "user_id": room.user_id,
                "created_at": room.created_at,
                "is_active": room.is_active,
                "last_message_at": room.last_message_at,
                "user_name": room.user.username if room.user else "Usuario"
            }
            for room in rooms
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener salas de chat: {str(e)}"
        )

@router.post("/rooms", response_model=ChatRoomResponse)
async def create_chat_room(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear una nueva sala de chat"""
    try:
        # Verificar si ya existe una sala activa para este usuario
        existing_room = db.query(ChatRoom).filter(
            ChatRoom.user_id == current_user.id,
            ChatRoom.is_active == True
        ).first()

        if existing_room:
            return {
                "id": existing_room.id,
                "user_id": existing_room.user_id,
                "created_at": existing_room.created_at,
                "is_active": existing_room.is_active,
                "last_message_at": existing_room.last_message_at,
                "user_name": existing_room.user.username if existing_room.user else "Usuario"
            }

        # Crear nueva sala
        new_room = ChatRoom(
            user_id=current_user.id
        )
        db.add(new_room)
        db.commit()
        db.refresh(new_room)

        # Crear mensaje de bienvenida
        welcome_message = ChatMessage(
            chat_room_id=new_room.id,
            sender_id=current_user.id,
            content="¡Hola! Bienvenido al chat de KidsFun. ¿En qué podemos ayudarte?"
        )
        db.add(welcome_message)
        db.commit()

        return {
            "id": new_room.id,
            "user_id": new_room.user_id,
            "created_at": new_room.created_at,
            "is_active": new_room.is_active,
            "last_message_at": new_room.last_message_at,
            "user_name": new_room.user.username if new_room.user else "Usuario"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear sala de chat: {str(e)}"
        )

@router.get("/rooms/{room_id}/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener mensajes de una sala de chat"""
    try:
        # Verificar acceso a la sala
        room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sala de chat no encontrada"
            )

        # Verificar si el usuario tiene acceso
        is_admin = db.query(ChatAdministrator).filter(
            ChatAdministrator.user_id == current_user.id,
            ChatAdministrator.is_active == True
        ).first()

        if not is_admin and room.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a esta sala de chat"
            )

        # Obtener mensajes
        messages = db.query(ChatMessage).filter(
            ChatMessage.chat_room_id == room_id
        ).order_by(ChatMessage.timestamp.asc()).all()

        return [
            {
                "id": msg.id,
                "chat_room_id": msg.chat_room_id,
                "sender_id": msg.sender_id,
                "content": msg.content,
                "timestamp": msg.timestamp,
                "is_read": msg.is_read,
                "sender_name": msg.sender.username if msg.sender else "Usuario"
            }
            for msg in messages
        ]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener mensajes: {str(e)}"
        )

@router.post("/rooms/{room_id}/messages", response_model=ChatMessageResponse)
async def send_message(
    room_id: int,
    message: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enviar un mensaje a una sala de chat"""
    try:
        # Verificar acceso a la sala
        room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sala de chat no encontrada"
            )

        # Verificar si el usuario tiene acceso
        is_admin = db.query(ChatAdministrator).filter(
            ChatAdministrator.user_id == current_user.id,
            ChatAdministrator.is_active == True
        ).first()

        if not is_admin and room.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a esta sala de chat"
            )

        # Crear mensaje
        new_message = ChatMessage(
            chat_room_id=room_id,
            sender_id=current_user.id,
            content=message.content
        )
        db.add(new_message)

        # Actualizar último mensaje de la sala
        room.last_message_at = datetime.now()
        db.commit()
        db.refresh(new_message)

        # Enviar mensaje por WebSocket si hay conexiones activas
        message_data = {
            "id": new_message.id,
            "chat_room_id": new_message.chat_room_id,
            "sender_id": new_message.sender_id,
            "content": new_message.content,
            "timestamp": new_message.timestamp.isoformat(),
            "is_read": new_message.is_read,
            "sender_name": new_message.sender.username if new_message.sender else "Usuario"
        }
        
        await manager.broadcast_to_chat(json.dumps(message_data), room_id)

        return {
            "id": new_message.id,
            "chat_room_id": new_message.chat_room_id,
            "sender_id": new_message.sender_id,
            "content": new_message.content,
            "timestamp": new_message.timestamp,
            "is_read": new_message.is_read,
            "sender_name": new_message.sender.username if new_message.sender else "Usuario"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al enviar mensaje: {str(e)}"
        )

@router.post("/admin/administrators", response_model=ChatAdministratorResponse)
async def create_chat_administrator(
    admin: ChatAdministratorCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear un nuevo administrador de chat (solo super admin)"""
    try:
        # Verificar si el usuario actual es super admin (puedes ajustar esta lógica)
        is_super_admin = current_user.is_superuser if hasattr(current_user, 'is_superuser') else False
        
        if not is_super_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo los super administradores pueden crear administradores de chat"
            )

        # Verificar si el email ya existe
        existing_admin = db.query(ChatAdministrator).filter(
            ChatAdministrator.email == admin.email
        ).first()

        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un administrador con este email"
            )

        # Buscar usuario por email
        user = db.query(User).filter(User.email == admin.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado con este email"
            )

        # Crear administrador
        new_admin = ChatAdministrator(
            user_id=user.id,
            email=admin.email
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

        return {
            "id": new_admin.id,
            "user_id": new_admin.user_id,
            "email": new_admin.email,
            "is_active": new_admin.is_active,
            "created_at": new_admin.created_at
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear administrador: {str(e)}"
        )

@router.get("/admin/administrators", response_model=List[ChatAdministratorResponse])
async def get_chat_administrators(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener lista de administradores de chat"""
    try:
        # Verificar si el usuario actual es super admin
        is_super_admin = current_user.is_superuser if hasattr(current_user, 'is_superuser') else False
        
        if not is_super_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo los super administradores pueden ver la lista de administradores"
            )

        administrators = db.query(ChatAdministrator).order_by(ChatAdministrator.created_at.desc()).all()

        return [
            {
                "id": admin.id,
                "user_id": admin.user_id,
                "email": admin.email,
                "is_active": admin.is_active,
                "created_at": admin.created_at
            }
            for admin in administrators
        ]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener administradores: {str(e)}"
        )

@router.put("/admin/administrators/{admin_id}/toggle")
async def toggle_chat_administrator(
    admin_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Activar/desactivar un administrador de chat"""
    try:
        # Verificar si el usuario actual es super admin
        is_super_admin = current_user.is_superuser if hasattr(current_user, 'is_superuser') else False
        
        if not is_super_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo los super administradores pueden modificar administradores"
            )

        admin = db.query(ChatAdministrator).filter(ChatAdministrator.id == admin_id).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrador no encontrado"
            )

        # Toggle estado
        admin.is_active = not admin.is_active
        db.commit()

        return {
            "message": f"Administrador {'activado' if admin.is_active else 'desactivado'} exitosamente",
            "admin_id": admin.id,
            "is_active": admin.is_active
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al modificar administrador: {str(e)}"
        )

# WebSocket endpoint para chat en tiempo real
@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, db: Session = Depends(get_db)):
    await manager.connect(websocket, chat_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Procesar mensaje recibido si es necesario
            await manager.broadcast_to_chat(data, chat_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id) 