from sqlalchemy import Column, String, UnicodeText

from lib.helpers.database import BASE, SESSION


class Sudo(BASE):
    __tablename__ = "sudo"
    chat_id = Column(String(14), primary_key=True)
    reason = Column(UnicodeText)

    def __init__(self, chat_id, reason):
        self.chat_id = str(chat_id)  # ensure string
        self.reason = reason

    def __repr__(self):
        return f"<BL {self.chat_id}>"


Sudo.__table__.create(checkfirst=True)


def is_sudo(chat_id: int):
    try:
        return sudo if (sudo := SESSION.query(Sudo).get(str(chat_id))) else None
    finally:
        SESSION.close()


def add_sudo(chat_id: int, reason=None):
    user = Sudo(str(chat_id), reason)
    SESSION.add(user)
    SESSION.commit()


def del_sudo(chat_id: int):
    if user := is_sudo(chat_id):
        SESSION.delete(user)
        SESSION.commit()
