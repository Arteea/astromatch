from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


class RegistrationKeyboards:
    '''
    Класс содержит кнопки и клавиатуры для использования в процессе регистрации пользователя
    '''

    contact_step_button = [[KeyboardButton(text="Телефон",request_contact=True)]]
    contact_step_keyboard = ReplyKeyboardMarkup(keyboard=contact_step_button, resize_keyboard=True,
                                  one_time_keyboard=True, 
                                  input_field_placeholder="Отправьте свой контакт для регистрации:")



    gender_step_button = [[InlineKeyboardButton(text="Мужской",callback_data="gender:male"),
            InlineKeyboardButton(text="Женский", callback_data="gender:female")]]
    gender_step_keyboard = InlineKeyboardMarkup(inline_keyboard=gender_step_button,
                                        resize_keyboard=True,
                                        one_time_keyboard=True, 
                                        input_field_placeholder="Ваш пол:")
    

    location_step_button = [[KeyboardButton(text="Местоположение", request_location=True)]]  
    location_step_keyboard = ReplyKeyboardMarkup(keyboard=location_step_button, resize_keyboard=True,
                                  one_time_keyboard=True, 
                                  input_field_placeholder="Отправьте свое местоположение, чтобы мы могли подобрать пару рядом с вами")
    
    finish_download_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅ Завершить загрузку", callback_data="finish_media_upload")]])
    
