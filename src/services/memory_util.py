"""
Module containing utility classes for memory management.
"""
import os
import enum
import random
from abc import ABC
from datetime import datetime
from flask import current_app, session

from ..models import db, Memory


class SlideshowModes(enum.Enum):
    """
    Enumeration for storing all possible modes a slideshow can be accessed.
    """
    CHRONOLOGICAL = "chronological"
    RANDOM = "random"
    REVERSE_CHRONOLOGICAL = "reverse-chronological"


class MemoryManagement(ABC):
    """
    Utility class for creating and retrieving memories from database.
    """
    @staticmethod
    def upload_memory(description: str,
                      date: str,
                      vault_id: int,
                      latitude: str = None,
                      longitude: str = None,
                      image_file: str = None) -> None:
        """
        Creates memory in a specified vault and contaings description,
        date, and optional coordinates and image.

        Parameters:
            description: str
                Description of the uploaded memory.
            date: str
                Date of the memory in %Y-%m-%d format.
            vault_id: int
                Id of the vault the memory will be uploaded to
            latitude: str (optional)
                Latitude of the coordinate
            longitude: str (optional)
                Longitude of the coordinate
            image_file: str (optional)
                Bytes of the image.

        Returns:
            None
        """
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
    def save_image(image_file: str) -> str:
        """
        Saves uploaded image to local folder or S3 storage.

        Parameters:
            image_file: str (optional)
                Bytes of the image.

        Returns:
            str: uri of the saved image
        """
        if current_app.config["USE_S3"]:
            pass
        else:
            filename = f'{session["user_id"]}_{datetime.strftime(
                datetime.now(), "%Y_%m_%d-%H_%M_%S")}.jpg'
            save_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"], filename)
            image_file.save(save_path)
            return filename

    @staticmethod
    def get_memory_data(memory_id: int) -> dict:
        """
        Requests memory information from database and returns dict.

        Parameters:
            memory_id: int

        Returns:
            dict: containing the information of the memory
        """
        memory = Memory.query.filter_by(id=memory_id).first()

        return memory.to_json()

    @staticmethod
    def get_slideshow_order(vault_id: int,
                            order: SlideshowModes,
                            period_start: datetime.date,
                            period_end: datetime.date) -> list:
        """
        Lists all memories of a vault in a specified timespan

        Parameters:
            memory_id: int

        Returns:
            dict: containing the information of the memory
        """
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
        else:
            return memories_ids
