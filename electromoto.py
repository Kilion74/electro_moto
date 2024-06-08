import requests  # pip install requests
from bs4 import BeautifulSoup  # pip install bs4
import csv

# pip install lxml
print('Выберите нужную вам категорию: электровелосипеды, электросамокаты, электроскутеры', 'электротрициклы')
glav = input()
get_name = ''
if glav == 'электровелосипеды':
    get_name = 'ehlektrovelosipedy'
elif glav == 'электросамокаты':
    get_name = 'ehlektrosamokaty'
elif glav == 'электроскутеры':
    get_name = 'ehlektroskutery'
elif glav == 'электротрициклы':
    get_name = 'ehlektrotricikly'
else:
    print('Ошибка, повторите ввод снова...')

url = f'https://energomoto.ru/{get_name}/?limit=100'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
data = requests.get(url, headers=headers).text
block = BeautifulSoup(data, 'lxml')
heads = block.find_all('div', class_='product-thumb uni-item')
print(len(heads))
for i in heads:
    w = i.find_next('div', class_='product-thumb__image').find('a').get('href')
    # print(w)
    both = requests.get(w, headers=headers).text
    loom = BeautifulSoup(both, 'lxml')
    name = loom.find('h1')
    print(name.text.strip())
    head = (name.text.strip())
    price = loom.find('div', class_='product-page__price price')
    print(price.text.strip().replace('RUB', ''))
    cena = (price.text.strip().replace('RUB', ''))
    new_price = float(cena)  # преобразуем строку в число
    total = new_price * 1.15  # увеличиваем цену на 15%
    print(total)
    new_total = round(total)  # округляем до десятых долей
    print(new_total)
    photo = loom.find('div', class_='product-page__image-main-carousel').find('img').get('src')
    print(photo)
    params = loom.find('div', id='tab-specification').find_all('div', class_='product-data__item')
    scumpa = []
    for eel in params:
        kias = eel.find_all_next('div', class_='product-data__item-div')
        # print(kias[0].text.strip())
        value_1 = (kias[0].text.strip())
        # print(kias[1].text.strip())
        value_2 = (kias[1].text.strip())
        all_params = value_1 + ':' + ' ' + value_2
        print(all_params)
        scumpa.append(all_params)
    print('\n')

    storage = {'name': head, 'price': new_total, 'photo': photo, 'params': ';'.join(scumpa)}

    with open(f'{get_name}.csv', 'a+', encoding='utf-16') as file:
        pisar = csv.writer(file, delimiter=';', lineterminator='\r')
        pisar.writerow([storage['name'], storage['price'], storage['photo'], storage['params']])
