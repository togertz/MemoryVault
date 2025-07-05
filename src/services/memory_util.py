from datetime import datetime

from ..models import db, Memory

def upload_memory(description, date):
    memory_date = datetime.strptime(date, '%Y-%m-%d').date()

    new_memory = Memory(description=description,
                        date=memory_date)
    db.session.add(new_memory)
    db.session.commit()