import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
MANAGER_ID = int(os.getenv("MANAGER_ID"))
BOT_ID = int(BOT_TOKEN.split(':')[0])

class FormStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    alarm_brand = State()
    alarm_model = State()
    alarm_year = State()
    alarm_engine_volume = State()
    alarm_engine_type = State()
    alarm_start_type = State()
    alarm_functionality = State()
    repair_brand = State()
    repair_model = State()
    repair_year = State()
    repair_engine_volume = State()
    repair_engine_type = State()
    repair_start_type = State()
    repair_problem = State()
    extra_brand = State()
    extra_model = State()
    extra_year = State()
    extra_equipment = State()
    other_brand = State()
    other_model = State()
    other_year = State()
    other_engine_volume = State()
    other_engine_type = State()
    other_start_type = State()
    other_problem = State()

def get_reason_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Установка сигнализации", callback_data="reason_alarm")],
        [InlineKeyboardButton(text="Диагностика и ремонт", callback_data="reason_repair")],
        [InlineKeyboardButton(text="Установка дополнительного оборудования", callback_data="reason_extra")],
        [InlineKeyboardButton(text="Другая причина", callback_data="reason_other")]
    ])

router = Router()
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

@router.message(F.text, State(None))
async def start_conversation(message: Message, state: FSMContext):
    if message.from_user.id == BOT_ID:
        return
    user_name = message.from_user.first_name or "Клиент"
    await message.answer(
        f"Здравствуйте, {user_name}, выберите из списка причину обращения.",
        reply_markup=get_reason_keyboard()
    )
    await state.update_data(client_name=user_name, client_id=message.from_user.id)

@router.callback_query(F.data.startswith("reason_"))
async def reason_selected(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    reason = callback.data
    user_name = (await state.get_data()).get("client_name", "Клиент")
    if reason == "reason_alarm":
        await callback.message.answer("Укажите марку авто")
        await state.set_state(FormStates.alarm_brand)
    elif reason == "reason_repair":
        await callback.message.answer("Укажите марку авто")
        await state.set_state(FormStates.repair_brand)
    elif reason == "reason_extra":
        await callback.message.answer("Укажите марку авто")
        await state.set_state(FormStates.extra_brand)
    elif reason == "reason_other":
        await callback.message.answer("Укажите марку авто")
        await state.set_state(FormStates.other_brand)

# === УСТАНОВКА СИГНАЛИЗАЦИИ ===
@router.message(FormStates.alarm_brand)
async def alarm_brand_handler(message: Message, state: FSMContext):
    await state.update_data(alarm_brand=message.text)
    await message.answer("Укажите модель авто")
    await state.set_state(FormStates.alarm_model)

@router.message(FormStates.alarm_model)
async def alarm_model_handler(message: Message, state: FSMContext):
    await state.update_data(alarm_model=message.text)
    await message.answer("Укажите год своего автомобиля")
    await state.set_state(FormStates.alarm_year)

@router.message(FormStates.alarm_year)
async def alarm_year_handler(message: Message, state: FSMContext):
    await state.update_data(alarm_year=message.text)
    await message.answer("Укажите объём двигателя")
    await state.set_state(FormStates.alarm_engine_volume)

@router.message(FormStates.alarm_engine_volume)
async def alarm_engine_volume_handler(message: Message, state: FSMContext):
    await state.update_data(alarm_engine_volume=message.text)
    await message.answer("Укажите тип двигателя (бензин, дизель)")
    await state.set_state(FormStates.alarm_engine_type)

@router.message(FormStates.alarm_engine_type)
async def alarm_engine_type_handler(message: Message, state: FSMContext):
    await state.update_data(alarm_engine_type=message.text)
    await message.answer("Укажите, как запускается авто (с ключа или с кнопки Start/Stop)")
    await state.set_state(FormStates.alarm_start_type)

@router.message(FormStates.alarm_start_type)
async def alarm_start_type_handler(message: Message, state: FSMContext):
    await state.update_data(alarm_start_type=message.text)
    await message.answer("Укажите, что бы вы хотели получить от сигнализации (функционал)")
    await state.set_state(FormStates.alarm_functionality)

@router.message(FormStates.alarm_functionality)
async def alarm_functionality_handler(message: Message, state: FSMContext):
    await state.update_data(alarm_functionality=message.text)
    data = await state.get_data()
    client_name = data.get("client_name", "Клиент")
    await message.answer(f"{client_name}, ваша заявка передана менеджеру, пожалуйста укажите, как к вам можно обращаться.")
    await state.set_state(FormStates.waiting_for_name)

# === ДИАГНОСТИКА И РЕМОНТ ===
@router.message(FormStates.repair_brand)
async def repair_brand_handler(message: Message, state: FSMContext):
    await state.update_data(repair_brand=message.text)
    await message.answer("Укажите модель авто")
    await state.set_state(FormStates.repair_model)

@router.message(FormStates.repair_model)
async def repair_model_handler(message: Message, state: FSMContext):
    await state.update_data(repair_model=message.text)
    await message.answer("Укажите год своего автомобиля")
    await state.set_state(FormStates.repair_year)

@router.message(FormStates.repair_year)
async def repair_year_handler(message: Message, state: FSMContext):
    await state.update_data(repair_year=message.text)
    await message.answer("Укажите объём двигателя")
    await state.set_state(FormStates.repair_engine_volume)

@router.message(FormStates.repair_engine_volume)
async def repair_engine_volume_handler(message: Message, state: FSMContext):
    await state.update_data(repair_engine_volume=message.text)
    await message.answer("Укажите тип двигателя (бензин, дизель)")
    await state.set_state(FormStates.repair_engine_type)

@router.message(FormStates.repair_engine_type)
async def repair_engine_type_handler(message: Message, state: FSMContext):
    await state.update_data(repair_engine_type=message.text)
    await message.answer("Укажите, как запускается авто (с ключа или с кнопки Start/Stop)")
    await state.set_state(FormStates.repair_start_type)

@router.message(FormStates.repair_start_type)
async def repair_start_type_handler(message: Message, state: FSMContext):
    await state.update_data(repair_start_type=message.text)
    await message.answer("Подробно опишите вашу проблему с автомобилем")
    await state.set_state(FormStates.repair_problem)

@router.message(FormStates.repair_problem)
async def repair_problem_handler(message: Message, state: FSMContext):
    await state.update_data(repair_problem=message.text)
    data = await state.get_data()
    client_name = data.get("client_name", "Клиент")
    await message.answer(f"{client_name}, ваша заявка передана менеджеру, пожалуйста укажите, как к вам можно обращаться.")
    await state.set_state(FormStates.waiting_for_name)

# === УСТАНОВКА ДОП. ОБОРУДОВАНИЯ ===
@router.message(FormStates.extra_brand)
async def extra_brand_handler(message: Message, state: FSMContext):
    await state.update_data(extra_brand=message.text)
    await message.answer("Укажите модель авто")
    await state.set_state(FormStates.extra_model)

@router.message(FormStates.extra_model)
async def extra_model_handler(message: Message, state: FSMContext):
    await state.update_data(extra_model=message.text)
    await message.answer("Укажите год своего автомобиля")
    await state.set_state(FormStates.extra_year)

@router.message(FormStates.extra_year)
async def extra_year_handler(message: Message, state: FSMContext):
    await state.update_data(extra_year=message.text)
    await message.answer("Подробно укажите, что бы вы хотели установить на ваш автомобиль")
    await state.set_state(FormStates.extra_equipment)

@router.message(FormStates.extra_equipment)
async def extra_equipment_handler(message: Message, state: FSMContext):
    await state.update_data(extra_equipment=message.text)
    data = await state.get_data()
    client_name = data.get("client_name", "Клиент")
    await message.answer(f"{client_name}, ваша заявка передана менеджеру, пожалуйста укажите, как к вам можно обращаться.")
    await state.set_state(FormStates.waiting_for_name)

# === ДРУГАЯ ПРИЧИНА ===
@router.message(FormStates.other_brand)
async def other_brand_handler(message: Message, state: FSMContext):
    await state.update_data(other_brand=message.text)
    await message.answer("Укажите модель авто")
    await state.set_state(FormStates.other_model)

@router.message(FormStates.other_model)
async def other_model_handler(message: Message, state: FSMContext):
    await state.update_data(other_model=message.text)
    await message.answer("Укажите год своего автомобиля")
    await state.set_state(FormStates.other_year)

@router.message(FormStates.other_year)
async def other_year_handler(message: Message, state: FSMContext):
    await state.update_data(other_year=message.text)
    await message.answer("Укажите объём двигателя")
    await state.set_state(FormStates.other_engine_volume)

@router.message(FormStates.other_engine_volume)
async def other_engine_volume_handler(message: Message, state: FSMContext):
    await state.update_data(other_engine_volume=message.text)
    await message.answer("Укажите тип двигателя (бензин, дизель)")
    await state.set_state(FormStates.other_engine_type)

@router.message(FormStates.other_engine_type)
async def other_engine_type_handler(message: Message, state: FSMContext):
    await state.update_data(other_engine_type=message.text)
    await message.answer("Укажите, как запускается авто (с ключа или с кнопки Start/Stop)")
    await state.set_state(FormStates.other_start_type)

@router.message(FormStates.other_start_type)
async def other_start_type_handler(message: Message, state: FSMContext):
    await state.update_data(other_start_type=message.text)
    await message.answer("Пожалуйста, опишите проблему, с которой вы столкнулись, и симптомы её возникновения как можно подробнее")
    await state.set_state(FormStates.other_problem)

@router.message(FormStates.other_problem)
async def other_problem_handler(message: Message, state: FSMContext):
    await state.update_data(other_problem=message.text)
    data = await state.get_data()
    client_name = data.get("client_name", "Клиент")
    await message.answer(f"{client_name}, ваша заявка передана менеджеру, пожалуйста укажите, как к вам можно обращаться.")
    await state.set_state(FormStates.waiting_for_name)

# === ФИНАЛ: ИМЯ → ТЕЛЕФОН → ОТПРАВКА МЕНЕДЖЕРУ ===
@router.message(FormStates.waiting_for_name)
async def get_contact_name(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(contact_name=message.text)
        await message.answer("Укажите контактный номер телефона для связи")
        await state.set_state(FormStates.waiting_for_phone)
    else:
        await message.answer("Пожалуйста, введите имя текстом.")

@router.message(FormStates.waiting_for_phone)
async def get_phone(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, введите номер телефона текстом.")
        return

    await state.update_data(contact_phone=message.text)
    data = await state.get_data()

    client_id = data.get("client_id")
    client_display = data.get("client_name", "Клиент")
    contact_name = data.get("contact_name", "Не указано")
    contact_phone = data.get("contact_phone", "Не указано")

    if client_id:
        client_link = f"[{client_display}](tg://user?id={client_id})"
    else:
        client_link = client_display

    lines = ["📩 **НОВАЯ ЗАЯВКА**\n"]
    lines.append(f"Клиент: {client_link}")
    lines.append(f"Обращаться как: {contact_name}")
    lines.append(f"Телефон: {contact_phone}")
    lines.append("")

    if "alarm_brand" in data:
        lines.append("Тип обращения: Установка сигнализации")
        lines.append(f"Марка авто: {data['alarm_brand']}")
        lines.append(f"Модель: {data['alarm_model']}")
        lines.append(f"Год: {data['alarm_year']}")
        lines.append(f"Объём двигателя: {data['alarm_engine_volume']}")
        lines.append(f"Тип двигателя: {data['alarm_engine_type']}")
        lines.append(f"Запуск авто: {data['alarm_start_type']}")
        lines.append(f"Функционал сигнализации: {data['alarm_functionality']}")
    elif "repair_brand" in data:
        lines.append("Тип обращения: Диагностика и ремонт")
        lines.append(f"Марка авто: {data['repair_brand']}")
        lines.append(f"Модель: {data['repair_model']}")
        lines.append(f"Год: {data['repair_year']}")
        lines.append(f"Объём двигателя: {data['repair_engine_volume']}")
        lines.append(f"Тип двигателя: {data['repair_engine_type']}")
        lines.append(f"Запуск авто: {data['repair_start_type']}")
        lines.append(f"Описание проблемы: {data['repair_problem']}")
    elif "extra_brand" in data:
        lines.append("Тип обращения: Установка дополнительного оборудования")
        lines.append(f"Марка авто: {data['extra_brand']}")
        lines.append(f"Модель: {data['extra_model']}")
        lines.append(f"Год: {data['extra_year']}")
        lines.append(f"Оборудование: {data['extra_equipment']}")
    elif "other_brand" in data:
        lines.append("Тип обращения: Другая причина")
        lines.append(f"Марка авто: {data['other_brand']}")
        lines.append(f"Модель: {data['other_model']}")
        lines.append(f"Год: {data['other_year']}")
        lines.append(f"Объём двигателя: {data['other_engine_volume']}")
        lines.append(f"Тип двигателя: {data['other_engine_type']}")
        lines.append(f"Запуск авто: {data['other_start_type']}")
        lines.append(f"Описание проблемы: {data['other_problem']}")

    report = "\n".join(lines)
    bot = message.bot
    try:
        await bot.send_message(MANAGER_ID, report, parse_mode="Markdown")
    except Exception as e:
        fallback = report.replace("[", "").replace("]", "").replace("(tg://user?id=", " (ID: ").replace(")", "")
        await bot.send_message(MANAGER_ID, fallback)

    await message.answer(
        f"{client_display}, спасибо большое, что выбрали нас. "
        f"В ближайшее время наш менеджер свяжется с вами для уточнения времени записи и суммы работы."
    )
    await state.clear()

async def main():
    bot = Bot(token=BOT_TOKEN)
    logging.info("✅ Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())