
from src.database.crud.conversations import insert_conversation, p2p_convo_exists
from src.database.crud.users import insert_user
from src.database.models import Conversation, User, create_tables
from src.database.session_factory import session_factory

create_tables()
session = session_factory()

insert_user(User(email="test1@mail.com", username="test1"), session)
insert_user(User(email="test2@mail.com", username="test2"), session)

insert_conversation(Conversation(type=0), [1, 2], session)


print(p2p_convo_exists(1, 2, session))
print(p2p_convo_exists(2, 3, session))
