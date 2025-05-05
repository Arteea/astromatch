from aiogram.types import User, Chat, Contact
from bot.routers.registration import RegistrationForm

TEST_USER = User(id=111, is_bot=False, first_name="Feo", last_name="Corneo", username="username", language_code="ru-RU")
ANOTHER_TEST_USER = User(id=222, is_bot=False, first_name="Leo", last_name="Barleo", username="username", language_code="ru-RU")
TEST_USER_CHAT = Chat(id=11, type="private", username=TEST_USER.username, 
                      first_name=TEST_USER.first_name, last_name=TEST_USER.last_name)

TEST_USER_CONTACT = Contact(phone_number="+79999999999",first_name=TEST_USER.first_name, last_name=TEST_USER.last_name, user_id=TEST_USER.id)
NOT_USER_CONTACT = Contact(phone_number="+78888888888",first_name=ANOTHER_TEST_USER.first_name, last_name=ANOTHER_TEST_USER.last_name, user_id=ANOTHER_TEST_USER.id)


class HandlersData:

    start_handler_data = [
        (TEST_USER),
        (ANOTHER_TEST_USER)
    ]

    contact_handler_data = [
                (TEST_USER, TEST_USER_CONTACT, TEST_USER_CHAT, RegistrationForm.name.state,
                "Введите ваше имя(именно так вас будут видеть другие пользователи):",b"+79999999999"),
                (TEST_USER, NOT_USER_CONTACT, TEST_USER_CHAT, None,
                "Пожалуйста, отправьте именно свой номер через кнопку, не пересылайте чужой контакт 🙏",None)
                            ]