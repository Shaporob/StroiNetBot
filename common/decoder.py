def d_city(city):
    str_city = ""
    match city:
        case 0:
            str_city = "Москва"
        case 1:
            str_city = "Санкт-Петербург"
        case 2:
            str_city = "Екатеринбург"
    return str_city


def d_square(square):
    str_square = ""
    match square:
        case 0:
            str_square = "До 100 м²"
        case 1:
            str_square = "От 100 до 300 м²"
        case 2:
            str_square = "Больше 300 м²"
    return str_square


def d_budget(budget):
    str_budget = ""
    match budget:
        case 0:
            str_budget = "До 10 млн руб"
        case 1:
            str_budget = "От 10 до 20 млн руб"
        case 2:
            str_budget = "От 20 млн руб"
    return str_budget
