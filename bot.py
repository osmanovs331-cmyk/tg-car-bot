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

# ... (все обработчики из предыдущего финального кода) ...

# === ФИНАЛ ===
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

    if "alarm_brand" in 
        lines.append("Тип обращения: Установка сигнализации")
        lines.append(f"Марка авто: {data['alarm_brand']}")
        lines.append(f"Модель: {data['alarm_model']}")
        lines.append(f"Год: {data['alarm_year']}")
        lines.append(f"Объём двигателя: {data['alarm_engine_volume']}")
        lines.append(f"Тип двигателя: {data['alarm_engine_type']}")
        lines.append(f"Запуск авто: {data['alarm_start_type']}")
        lines.append(f"Функционал сигнализации: {data['alarm_functionality']}")
    elif "repair_brand" in 
        lines.append("Тип обращения: Диагностика и ремонт")
        lines.append(f"Марка авто: {data['repair_brand']}")
        lines.append(f"Модель: {data['repair_model']}")
        lines.append(f"Год: {data['repair_year']}")
        lines.append(f"Объём двигателя: {data['repair_engine_volume']}")
        lines.append(f"Тип двигателя: {data['repair_engine_type']}")
        lines.append(f"Запуск авто: {data['repair_start_type']}")
        lines.append(f"Описание проблемы: {data['repair_problem']}")
    elif "extra_brand" in 
        lines.append("Тип обращения: Установка дополнительного оборудования")
        lines.append(f"Марка авто: {data['extra_brand']}")
        lines.append(f"Модель: {data['extra_model']}")
        lines.append(f"Год: {data['extra_year']}")
        lines.append(f"Оборудование: {data['extra_equipment']}")
    elif "other_brand" in 
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