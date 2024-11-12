from api.db.models import Message, User, Ticket
from api.db.models.messages import MessageSender
from api.services.base import BaseService
from api.services.ticket import TicketService
from config import settings


class MessageService:
    model = Message

    async def create(self, user: User, ticket_id: int, content: str) -> dict:
        if not content:
            return {
                'status': 'error',
                'description': f'Content not found',
            }
        ticket = await BaseService().get(Ticket, user_id=user.id, id=ticket_id)
        if not ticket:
            return {
                'status': 'error',
                'description': f'Ticket #{ticket_id} not found',
            }
        await BaseService().create(self.model, ticket_id=ticket.id, sender=MessageSender.USER, content=content)
        return {
            'status': 'ok',
            'messages': [
                await self.generate_message_dict(message=message)
                for message in await BaseService().get_all(self.model, ticket_id=ticket.id)
            ],
        }

    async def get_all(self, user: User, ticket_id: int):
        ticket = await BaseService().get(Ticket, user_id=user.id, id=ticket_id)
        if not ticket:
            return {
                'status': 'error',
                'description': f'Ticket #{ticket_id} not found',
            }
        return {
            'status': 'ok',
            'messages': [
                await self.generate_message_dict(message=message)
                for message in await BaseService().get_all(self.model, ticket_id=ticket.id)
            ],
        }

    @staticmethod
    async def generate_message_dict(message: Message) -> dict:
        if not message:
            return {}
        return {
            'id': message.id,
            'ticket': await TicketService().generate_ticket_dict(ticket=message.ticket),
            'sender': message.sender,
            'content': message.content,
            'date': message.created_at.strftime('%d.%m.%Y'),
            'time': message.created_at.strftime('%H:%M'),
            'created': message.created_at.strftime(format=settings.date_time_format),
        }
