from aiogram.filters.callback_data import CallbackData
from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class QuestionHomeSquareData(CallbackData, prefix="qhs"):
    city: int


class QuestionBudgetData(CallbackData, prefix="qb"):
    city: int
    square: int


class QuestionFinally(CallbackData, prefix="qf"):
    city: int
    square: int
    budget: int


def get_manager_link() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Менеджер", url="https://t.me/BuvayutOgorchenia")
    return kb.as_markup()


def get_founder_link() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Наш основатель", url="https://t.me/igorignatkov11")
    return kb.as_markup()


def question_yes_no() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Да", callback_data="question_yesno_yes")
    kb.button(text="Нет", callback_data="question_cancel")
    kb.adjust(2)
    return kb.as_markup()


def question_home_location() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Москва", callback_data=QuestionHomeSquareData(city=0).pack()),
           types.InlineKeyboardButton(text="Санкт-Петербург",
                                      callback_data=QuestionHomeSquareData(city=1).pack()))
    kb.row(types.InlineKeyboardButton(text="Екатеринбург",
                                      callback_data=QuestionHomeSquareData(city=2).pack()))
    kb.row(types.InlineKeyboardButton(text="Отмена",
                                      callback_data="question_cancel"))
    return kb.as_markup()


def question_home_square(city) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="До 100 м²",
                                      callback_data=QuestionBudgetData(city=city, square=0).pack()),
           types.InlineKeyboardButton(text="От 100 до 300 м²",
                                      callback_data=QuestionBudgetData(city=city, square=1).pack()))
    kb.row(types.InlineKeyboardButton(text="Больше 300 м²",
                                      callback_data=QuestionBudgetData(city=city, square=2).pack()))
    kb.row(types.InlineKeyboardButton(text="Отмена", callback_data="question_cancel"))
    return kb.as_markup()


def question_home_budget(city, square) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="До 10 млн руб",
                                      callback_data=QuestionFinally(city=city, square=square,
                                                                    budget=0).pack()),
           types.InlineKeyboardButton(text="От 10 до 20 млн руб",
                                      callback_data=QuestionFinally(city=city, square=square,
                                                                    budget=1).pack()))
    kb.row(types.InlineKeyboardButton(text="От 20 млн руб",
                                      callback_data=QuestionFinally(city=city, square=square,
                                                                    budget=2).pack()))
    kb.row(types.InlineKeyboardButton(text="Отмена", callback_data="question_cancel"))
    return kb.as_markup()
