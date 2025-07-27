import os
import enum
import random
from abc import ABC, abstractmethod
from datetime import datetime
from flask import current_app, session

from ..models import db, Memory

class SlideshowModes(enum.Enum):
    CHRONOLOGICAL = "chronological"
    RANDOM = "random"
    REVERSE_CHRONOLOGICAL = "reverse-chronological"

class MemoryManagement(ABC):

    @staticmethod
    def upload_memory(description, date, vault_id, latitude=None, longitude=None, image_file=None):
        memory_date = datetime.strptime(date, '%Y-%m-%d').date()

        image_uri = None
        if image_file:
            image_uri = MemoryManagement.save_image(image_file)

        new_memory = Memory(description=description,
                            date=memory_date,
                            latitude=latitude,
                            longitude=longitude,
                            image_uri=image_uri,
                            vault_id=vault_id)
        db.session.add(new_memory)
        db.session.commit()

    @staticmethod
    def save_image(image_file):
        if current_app.config["USE_S3"]:
            pass
        else:
            filename = f'{session["user_id"]}_{datetime.strftime(datetime.now(), "%Y_%m_%d-%H_%M_%S")}.jpg'
            save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            image_file.save(save_path)
            return filename

    @staticmethod
    def get_memory_data(id):
        memory = Memory.query.filter_by(id=id).first()

        return memory.to_json()

    @staticmethod
    def get_slideshow_order(vault_id, order:SlideshowModes, period_start, period_end):

        query = Memory.query.filter_by(vault_id=vault_id)
        query = query.filter(Memory.date.between(period_start, period_end))

        memories = query.order_by(Memory.date.asc()).all()
        memories_ids = [memory.id for memory in memories]

        if order == SlideshowModes.CHRONOLOGICAL:
            return memories_ids
        elif order == SlideshowModes.RANDOM:
            random.shuffle(memories_ids)
            return memories_ids
        elif order == SlideshowModes.REVERSE_CHRONOLOGICAL:
            return memories_ids[::-1]