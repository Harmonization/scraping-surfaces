import requests
from difflib import SequenceMatcher
from pyquery import PyQuery as pq

DOMAIN = 'https://ru.wikipedia.org'
URL = DOMAIN + '/wiki/Поверхность_второго_порядка'

def create_data_for_db():
    surfaces = parse_surfaces()
    return (dict(name=surfaces['Поверхность'][i], 
                latex_expr=surfaces['Уравнение'][i],
                latex_img=surfaces['Формулы'][i],
                img=surfaces['Изображения'][i],
                text=surfaces['Текст'][i],
                link=surfaces['Ссылки'][i]) 
                for i in range(len(surfaces['Поверхность'])))

def parse_surfaces():
    # Парсим таблицу с поверхностями 2 порядка: нужны названия и формулы
    if (response := requests.get(URL)):
        html = pq(response.text)
        table = html('table.wikitable tbody')
        table_rows = table.items('tr')

        # Имена колонок
        col_names = next(table_rows)
        surfaces_dict = {name.text(): [] for i, name in enumerate(col_names.items('th')) if i < 2}
        name_1, name_2 = surfaces_dict.keys()

        # Значения колонок
        latex_img = []
        links = []
        for row in table_rows:
            data_row = row.items('td')
            data = next(data_row)
            surfaces_dict[name_1].append(data.text())
            img = next(data_row)('span img')
            surfaces_dict[name_2].append(img.attr('alt'))

            latex_img.append(img.attr('src'))
            links.append(DOMAIN + data('a').attr('href'))

        surfaces = surfaces_dict | {'Формулы': latex_img, 'Ссылки': links}  

        # Проход по всем ссылкам, сбор img, text
        images = []
        text = []
        for link in links:
            if (response := requests.get(link)):
                html_link = pq(response.text)
                images.append('https:' + html_link('img.mw-file-element').attr('src'))
                text.append(next(html_link.items('p')).text())

        # Дополняем изображениями с текущей страницы
        # (На странице есть таблицы содержащие img некоторых из поверхностей)
        tables = html.items('table.standard')
        for t in tables:
            th_gen = t.items('tr th')
            img_gen = t.items('tr td span a img')
            for (th, img) in zip(th_gen, img_gen):
                name = th.text()[:-1]
                img_src = 'https:' + img.attr('src')

                for i, name_ in enumerate(surfaces[name_1]):
                    if SequenceMatcher(None, name, name_).ratio() > .9: # Сравнение схожести строк
                        images[i] = img_src
                        break

        surfaces |= {'Изображения': images, 'Текст': text}
        return surfaces


