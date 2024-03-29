from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import path
import random

import string
from urllib.parse import urlparse
'''---------------
решение в классе
# from django.utils.baseconv import base56
# from random import randint
# print("hello"+ " " + str(base56.encode(randint(1234, 12312541212312341)))) #ну типо дешевле по ресурсам
---------------'''
# Задание 3. URL shortener
#
# Реализуйте сервис для сокращения ссылок. Примеры таких сервисов:
# http://bit.ly, http://t.co, http://goo.gl
# Пример ссылки: http://bit.ly/1qJYR0y
#
# Вам понадобится шаблон с формой для отправки ссылки (файл index.html),
# и две функции, одна для обработки запросов GET и POST для сабмита URL
# и отображения результата, и вторая для редиректа с короткого URL на исходный.
# Для хранения соответствий наших коротких ключей и полных URL мы будем
# использовать кеш Django, django.core.cache
# Экземпляр cache уже импортирован, и используется следующим образом.
# Сохранить значение:
#
#  cache.add(key, value)
#
# Извлечь значение:
#
#  cache.get(key, default_value)
#
# Второй аргумент метода get - значение по умолчанию,
# если ключ не найден в кеше.
#
# Вы можете запустить сервер для разработки, и посмотреть
# ответы ваших функций в браузере:
#
# python homework03.py runserver


# Конфигурация, не нужно редактировать
if not settings.configured:
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['']
        }]
    )
"""
    Случайный короткий ключ, состоящий из цифр и букв.
    Минимальная длина ключа - 5 символов. Для генерации случайных
    последовательностей вы можете воспользоваться библиотекой random.
"""
def random_key(): #минимизация рандомов
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=5))
"""
    При запросе методом GET, отдаем HTML страницу (шаблон index.html) с формой
    с одним полем url типа text (отредактируйте шаблон, дополните форму).

        При отправке формы методом POST извлекаем url из request.POST и
        делаем следующее:

        1. Проверяем URL. Допускаются следующие схемы: http, https, ftp

        Если URL не прошел проверку - отобразите на нашей странице с формой
        сообщение о том, какие схемы поддерживаются.

        Если URL прошел проверку:

        2. Создаем случайный короткий ключ, состоящий из цифр и букв
        (функция random_key).

        3. Сохраняем URL в кеш со сгенерированным ключом:

         cache.add(key, url)

        4. Отдаем ту же страницу с формой и дополнительно отображаем на ней
        кликабельную короткую ссылку (HTML тег 'a') вида
         http://localhost:8000/<key>
"""
def index(request):
    if request.method == 'POST':
        context = {}
        url = request.POST.get('url')  # достаём URL который ввели
        result = urlparse(url)
        if result.scheme in ('http', 'https', 'ftp'):
            key = random_key()
            cache.add(key, url)  # сохранение в кеш url по ключу
            context['url'] = key
            return render(request, 'index.html', context)
        else:
            context['message'] = 'Только в формате https, http, ftp '
            return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


"""
    Функция обрабатывает сокращенный URL вида http://localhost:8000/<key>
    Ищем ключ в кеше (cache.get). Если ключ не найден,
    редиректим на главную страницу (/). Если найден,
    редиректим на полный URL, сохраненный под данным ключом.
"""

def redirect_view(request, key):
    return redirect(cache.get(key, '/'))

"""
    Статистика кликов на сокращенные ссылки.
    В теле ответа функция возращает количество
    переходов по данному коду.
"""
# Проверить на уникальность!! типо дополнительное задание, не понятно как посмотреть на кеш
def stats(request, key): #записываем в кеш переменную

    key += ':stats'
    return render(request, 'index.html', {'stats': cache.get(key, 0)})


urlpatterns = [
    path('', index),
    path(r'stats/<key>', stats),
    path(r'<key>', redirect_view),
]


if __name__ == '__main__':
    import sys
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
