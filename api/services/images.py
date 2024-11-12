import os
import time
from secrets import token_hex
from typing import Optional

from fastapi import UploadFile
from starlette.responses import FileResponse

from api.db.models import Image
from api.services.base import BaseService
from config import settings


class ImageService:
    model = Image

    async def create(self, file: UploadFile) -> dict:
        extension = file.filename.split('.')[-1]
        path = f'{settings.image_dir}/{token_hex(8)}_{time.strftime("%Y%m%d%H%M")}.{extension}'
        with open(path, 'wb') as f:
            f.write(await file.read())
        image = await BaseService().create(self.model, path=path, filename=file.filename, extension=extension)
        return {
            'status': 'ok',
            'image_id': image.id,
        }

    @staticmethod
    async def generate_url(image: Image) -> Optional[str]:
        if not image:
            return
        return f'{settings.api_link}/api/images/get?id={image.id}'

    async def get(self, id: int) -> [FileResponse, dict]:
        image: Image = await BaseService().get(self.model, id=id)
        if not image:
            return {
                'status': 'error',
                'description': 'Image not found'
            }
        if not os.path.exists(image.path):
            return {
                'status': 'error',
                'description': 'File not found'
            }
        return FileResponse(
            path=image.path,
        )

    async def delete(self, id: int) -> dict:
        image: Image = await BaseService().get(self.model, id=id)
        if not image:
            return {
                'status': 'error',
                'description': 'Image not found'
            }
        if os.path.exists(image.path):
            os.remove(image.path)
        await BaseService().delete(self.model, id_=id)

    async def generate_image_dict(self, image: Image) -> Optional[dict]:
        if not image:
            return
        return {
            'path': image.path,
            'filename': image.filename,
            'extension': image.extension,
            'url': await self.generate_url(image=image),
            'created': image.created.strftime(format=settings.date_time_format),
        }
