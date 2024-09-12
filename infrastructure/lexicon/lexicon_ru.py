COMANDS: dict = {
    'start': 'Приветствую, {name}! Я твой помощник в области теоретической механики. \nЕсли ты хочешь зарегистрироваться как обучающийся с правами доступа, то выполни команду /register. \nДля открытия справки выполни команду /help.',
    'help': """
Привет! Я твой робот-помощник в освоении предмета "Теоретическая механика".
В меню встроенной клавиатуры ты можешь найти пособия для самостоятельной работы, учебник.
Также возможно найти свой вариант, студенческий рейтинг, расписание преподавателя.
Список доступных команд:
/help - вывести справку по чат-боту
/menu - вызов встроенной клавиатуры
/mic - расшифровка голосовых сообщений
Разработчик © Юрий Солдатов
        """,
    'register': 'Давай познакомимся, напиши свою фамилию имя отчество. Если ты хочешь выйти из процесса регистрации, отправь /cancel.',
    'cancel': 'Вы вышли из меню регистрации.',
    'cancel_not': 'Отменять нечего. Вы вне машины состояний\n\nЧтобы перейти к заполнению анкеты - отправьте команду /fillform',
    'menu': 'Клавиатура выведена ⌨️'
}

USER: dict = {
    'available': 'Подтвердите личность: {name}, направление {profile}, группа {group}',
    'uncorrect': 'Неправильно, попробуй ещё раз! Для выхода отправь /cancel',
    'yes': 'Приятно познакомиться! Я зарегистрировал пользователя: {name}, профиль {profile}, группа {group}. Теперь ты можешь пользоваться продвинутым режимом чат-бота. Вариант для выполнения расчётных работ {var}, для Д1 - {var_d1}',
    'no': 'Хорошо, попробуйте снова ввести свою фамилию имя отчество. Для выхода отправь /cancel',
    'register_admin': 'Зарегистрирован пользователь {name}, профиль {profile}, группа {group}.',
    'metodic': 'Ссылки на методические указания:',
    'textbook': 'Ссылка на учебник: "Краткий курс теоретической механики"',
    'contact': 'Контакты преподавателя можете найти по ссылке ниже:',
    'profile': 'Пользователь: {name}, профиль {profile}, группа {group}. \nВариант для выполнения расчётных работ {var}, для Д1 - {var_d1}',
    'graph_task': 'Выберите задачу, которую хотите сдать.',
    'graph_task_prepod': 'Запрос на оценку задачи {task} обучающемуся {name}.',
    'graph_task_call': 'Заявка на приём задачи {task} отправлена преподавателю.',
    'graph_task_score_prepod': 'Обучающемуся {name} выставлен балл "{score}" за задачу {task}.',
    'graph_task_score_user': 'Поздравляю! За задачу {task} тебе выставлен балл "{score}".',
    'permission_denied': 'Ошибка! Доступ запрещён!'

}

ADMIN: dict = {
    'mailer': 'Выберите профиль обучающихся для рассылки.',
    'message_mailer': 'Введите сообщение для рассылки.',
    'available': 'Подтвердите отправку для {profile} {group}.'
}
