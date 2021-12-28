from flask import Flask
from flask_restful import request
import random

app = Flask(__name__)


class Pictures:
    def __init__(self):
        self.pictures = get_list_of_dict_from_csv()
        self.all_categories = get_all_categories(self.pictures)
        self.last = ''


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


def get_pic(pictures: list, needed_categories: list) -> str or None:
    '''
    Получение требуемых картинок по тегам
    '''
    needed_pictures = []
    for pic in pictures:
        for category in needed_categories:
            if category in pic['categs'] and pic['name'] not in needed_pictures:
                needed_pictures.append(pic['name'])
    if needed_pictures:
        rand = random.randint(0, len(needed_pictures) - 1)
        if len(needed_pictures) > 1 and needed_pictures[rand] == pic_class.last: #механизм неповторения картинки
            for i in range(len(needed_pictures)):
                if i != rand:
                    rand = i
                    break
        for i in range(len(pic_class.pictures)):
            if pic_class.pictures[i]['name'] != needed_pictures[rand]:
                continue
            else:
                pic_class.pictures[i]['amount'] = str(int(pic_class.pictures[i]['amount']) - 1)
                pic_class.last = pic_class.pictures[i]['name']
            if int(pic_class.pictures[i]['amount']) == 0:
                pic_class.pictures.pop(i)
                break
        return needed_pictures[rand]
    else:
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    catlist = []
    if request.method == 'POST':
        catlist = request.form.get('categ').split(',')
    else:
        categories = request.args.keys()
        if not categories:
            catlist = pic_class.all_categories
        else:
            for cat in categories:
                catlist.append(request.args.get(cat))
            if len(catlist) > 10:
                return 'Слишком много категорий!'
    res = get_pic(pic_class.pictures, catlist)
    return f'''<img src="/static/images/{res}.jpg">''' if res else 'Картинки закончились'

if __name__ == '__main__':
    pic_class = Pictures()
    app.run(debug=True)
