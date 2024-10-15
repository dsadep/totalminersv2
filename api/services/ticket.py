from fastapi import UploadFile
from typing import Optional

from api.db.models import Ticket, Message, User, Image
from api.db.models.messages import MessageSender
from api.services.base import BaseService
from api.services.user import UserService
from config import settings


class TicketService:
    model = Ticket

    async def create(self, user: User, title: str, content: str, file: Optional[UploadFile] = None) -> dict:
        from api.services.messages import MessageService
        from api.services.images import ImageService
        if not content:
            return {
                'status': 'error',
                'description': f'Content not found',
            }
        ticket = await BaseService().create(self.model, title=title, user_id=user.id)
        if file:
            image = await ImageService().create(file=file)
            message = await BaseService().create(Message, ticket_id=ticket.id, sender=MessageSender.USER, content=content, image_id=image['image_id'])
        else:
            message = await BaseService().create(Message, ticket_id=ticket.id, sender=MessageSender.USER, content=content)
        return {
            'status': 'ok',
            'ticket': await self.generate_ticket_dict(ticket=ticket),
            'message': await MessageService.generate_message_dict(message=message),
        }

    async def get(self, user: User, id: int):
        ticket = await BaseService().get(self.model, user_id=user.id, id=id)
        if not ticket:
            return {
                'status': 'error',
                'description': f'Ticket #{id} not found'
            }
        return {
            'status': 'ok',
            'ticket': await self.generate_ticket_dict(ticket=ticket),
        }

    async def get_all(self, user: User):
        return {
            'status': 'ok',
            'tickets': [
                await self.generate_ticket_dict(ticket=ticket)
                for ticket in await BaseService().get_all(self.model, user_id=user.id)
            ],
        }

    async def close(self, user: User, id: int) -> dict:
        ticket = await BaseService().get(self.model, user_id=user.id, id=id)
        if not ticket:
            return {
                'status': 'error',
                'description': f'Ticket #{id} not found'
            }
        await BaseService().update(ticket, is_open=False)
        return {
            'status': 'ok',
            'ticket': await self.generate_ticket_dict(ticket=ticket),
        }

    @staticmethod
    async def generate_ticket_dict(ticket: Ticket) -> dict:
        if not ticket:
            return {}
        return {
            'id': ticket.id,
            'title': ticket.title,
            'user': await UserService().generate_user_dict(user=ticket.user),
            'is_open': ticket.is_open,
            'date': ticket.created_at.strftime('%d.%m.%Y'),
            'time': ticket.created_at.strftime('%H:%M'),
            'created': ticket.created_at.strftime(format=settings.date_time_format),
        }
