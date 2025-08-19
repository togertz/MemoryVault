"""
Module containing utility classes for memory management.
"""
import os
import io
import enum
import random
from abc import ABC
from datetime import datetime
from PIL import Image
from azure.storage.blob import BlobServiceClient
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
        # Generate filename
        filename = f'{session["user_id"]}_{datetime.strftime(
            datetime.now(), "%Y_%m_%d-%H_%M_%S")}.jpg'

        # Resize image for saving storage space
        image = Image.open(image_file)
        max_size = current_app.config["IMAGE_MAX_SIZE"]
        image.thumbnail(max_size)
        image_buffer = io.BytesIO()
        image.save(image_buffer, format="JPEG")
        image_buffer.seek(0)

        if current_app.config["USE_BLOB_STORAGE"]:
            blob_service = BlobServiceClient.from_connection_string(
                current_app.config["AZURE_STORAGE_CONNECTION_STRING"]
            )

            blob_client = blob_service.get_blob_client(
                container=current_app.config["UPLOAD_FOLDER"],
                blob=filename
            )

            blob_client.upload_blob(image_buffer, overwrite=True)
        else:
            save_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"], filename)

            with open(save_path, "wb") as fp:
                fp.write(image_buffer.getvalue())

        return filename

    @staticmethod
    def get_image_bytes(filename: str) -> str:
        """
        Loads image from file storage.

        Parameters:
            filename: str
                Filename of the image.

        Returns:
            str: byte representation of image
        """
        if current_app.config["USE_BLOB_STORAGE"]:
            blob_service = BlobServiceClient.from_connection_string(
                current_app.config["AZURE_STORAGE_CONNECTION_STRING"]
            )

            blob_client = blob_service.get_blob_client(
                container=current_app.config["UPLOAD_FOLDER"],
                blob=filename
            )

            downloader = blob_client.download_blob()
            img_bytes = downloader.readall()
            return img_bytes
        else:
            image_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )

            with open(image_path, "rb") as img_file:
                img_bytes = img_file.read()

            return img_bytes

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
            list: containing the information of the memory
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
