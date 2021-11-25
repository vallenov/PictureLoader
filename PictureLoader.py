from flask import Flask
from flask_restful import request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)

def get_all_categories(lst: list) -> list:
    '''
    Получение списка всех доступных категорий
    '''
    allcatlist = []
    for cur in lst:
        for cat in cur['categs']:
            if cat not in allcatlist:
                allcatlist.append(cat)
    return allcatlist

def get_list_of_dict_from_csv() -> list:
    '''
    Получение словаря из csv файла
    Output:
    [{Name, amount, [categories]},
     {Name, amount, [categories]},
     ...,
     {Name, amount, [categories]}
    ]
    '''
    with open('db.csv', 'r') as file:
        inf = file.read()
        inf = inf.split('\n')
        allpic = []
        for i in range(1, len(inf)):
            tmp = inf[i].split(';')
            if len(tmp) < 2: break
            picdb = {}
            picdb['name'], picdb['amount'], picdb['categs'] = tmp[0], tmp[1], tmp[2:]
            allpic.append(picdb)
    return allpic

def get_pic(pictures: list,needed_categories: list) -> str:
    needed_pictures = []
    for pic in pictures:
        for category in needed_categories:
            if category in pic['categs']:
                needed_pictures.append(pic['name'])
    return ', '.join(needed_pictures)

@app.route('/')
def index():
    categories = request.args.keys()
    if not categories:
        return 'Введите требуемые категории'
    catlist = []
    for cat in categories:
        catlist.append(request.args.get(cat))
    if len(catlist) > 10:
        return 'Слишком много категорий!'
    res = get_pic(get_list_of_dict_from_csv(), catlist)
    return res

if __name__ == '__main__':
    app.run(debug=True)
