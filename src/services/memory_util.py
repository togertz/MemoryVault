from abc import ABC, abstractmethod
from datetime import datetime

from ..models import db, Memory

class MemoryManagement(ABC):

    @staticmethod
    def upload_memory(description, date, vault_id):
        memory_date = datetime.strptime(date, '%Y-%m-%d').date()

        new_memory = Memory(description=description,
                            date=memory_date,
                            vault_id=vault_id)
        db.session.add(new_memory)
        db.session.commit()