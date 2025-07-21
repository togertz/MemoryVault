import os
from abc import ABC, abstractmethod
from datetime import datetime
from flask import current_app, session

from ..models import db, Memory

class MemoryManagement(ABC):

    @staticmethod
    def upload_memory(description, date, vault_id, image_file=None):
        memory_date = datetime.strptime(date, '%Y-%m-%d').date()

        image_uri = None
        if image_file:
            image_uri = MemoryManagement.save_image(image_file)

        new_memory = Memory(description=description,
                            date=memory_date,
                            location="None",
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