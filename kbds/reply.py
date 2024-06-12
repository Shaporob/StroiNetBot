from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="О нас")
    kb.button(text="Примеры наших работ")
    kb.button(text="Связь с менеджером")
    kb.button(text="Основатель фирмы")
    kb.button(text="Купить дом")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def delete_menu():
    kb = types.ReplyKeyboardRemove()
    return kb
