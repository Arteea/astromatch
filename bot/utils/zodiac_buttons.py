from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

zodiac_buttons = [
    [InlineKeyboardButton(text="♈ Овен", callback_data="zodiac:aries"),
     InlineKeyboardButton(text="♉ Телец", callback_data="zodiac:taurus")],
    
    [InlineKeyboardButton(text="♊ Близнецы", callback_data="zodiac:gemini"),
     InlineKeyboardButton(text="♋ Рак", callback_data="zodiac:cancer")],
    
    [InlineKeyboardButton(text="♌ Лев", callback_data="zodiac:leo"),
     InlineKeyboardButton(text="♍ Дева", callback_data="zodiac:virgo")],
    
    [InlineKeyboardButton(text="♎ Весы", callback_data="zodiac:libra"),
     InlineKeyboardButton(text="♏ Скорпион", callback_data="zodiac:scorpio")],
    
    [InlineKeyboardButton(text="♐ Стрелец", callback_data="zodiac:sagittarius"),
     InlineKeyboardButton(text="♑ Козерог", callback_data="zodiac:capricorn")],
    
    [InlineKeyboardButton(text="♒ Водолей", callback_data="zodiac:aquarius"),
     InlineKeyboardButton(text="♓ Рыбы", callback_data="zodiac:pisces")]
]

zodiac_keyboard = InlineKeyboardMarkup(inline_keyboard=zodiac_buttons)

list_of_zodiac = {'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'}