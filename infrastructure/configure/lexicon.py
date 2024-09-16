import toml

# Загрузка TOML-файла
data = toml.load('infrastructure/configure/lexicon.toml')

BUTTONS_RU = data['buttons_ru']