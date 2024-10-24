from telegram import ReplyKeyboardMarkup
from PIL import Image
import io

# Возможные размеры для ресайза
RESIZE_OPTIONS = {
    "300x250": (300, 250),
    "600x400": (600, 400),
    "1024x768": (1024, 768)
}

# Функция команды /start с кнопками для выбора размера
async def start(update, context):
    print("Получена команда /start")  # Логируем получение команды
    keyboard = [['300x250', '600x400', '1024x768']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)  # Кнопки будут отображены только один раз
    
    await update.message.reply_text(
        "Привет! Выбери размер изображения для ресайза:",
        reply_markup=reply_markup
    )

# Функция для обработки выбора размера
async def choose_size(update, context):
    size = update.message.text  # Получаем выбранный размер
    print(f"Выбран размер: {size}")  # Логируем выбор размера
    if size in RESIZE_OPTIONS:
        context.user_data['chosen_size'] = RESIZE_OPTIONS[size]  # Сохраняем выбор пользователя
        await update.message.reply_text(f"Размер {size} выбран! Теперь отправь изображение.")
    else:
        await update.message.reply_text("Пожалуйста, выбери один из предложенных размеров.")

# Функция для обработки изображения с учётом выбранного размера и обрезкой по центру
async def handle_image(update, context):
    print("Получено изображение")  # Логируем получение изображения
    chosen_size = context.user_data.get('chosen_size')  # Получаем выбранный размер
    if not chosen_size:
        await update.message.reply_text("Пожалуйста, сначала выберите размер изображения.")
        return

    file = await update.message.photo[-1].get_file()  # Получаем фото в наивысшем разрешении
    image_bytes = await file.download_as_bytearray()
    
    img = Image.open(io.BytesIO(image_bytes))

    # Ресайз изображения с сохранением пропорций, чтобы полностью покрыть нужный размер
    img_ratio = img.width / img.height
    target_width, target_height = chosen_size
    target_ratio = target_width / target_height

    if img_ratio > target_ratio:
        # Если изображение шире, чем целевое соотношение, уменьшаем по высоте
        new_height = target_height
        new_width = int(new_height * img_ratio)
    else:
        # Если изображение выше, чем целевое соотношение, уменьшаем по ширине
        new_width = target_width
        new_height = int(new_width / img_ratio)

    img = img.resize((new_width, new_height), Image.ANTIALIAS)

    # Обрезаем по центру до точного размера
    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    right = (new_width + target_width) / 2
    bottom = (new_height + target_height) / 2

    img = img.crop((left, top, right, bottom))
    
    # Конвертация изображения обратно в байты
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    await update.message.reply_photo(photo=img_byte_array)





