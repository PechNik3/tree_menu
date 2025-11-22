## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/PechNik3/tree_menu.git
cd tree_menu
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
pip install django
```

2. Добавьте tree_menu в INSTALLED_APPS вашего проекта:
```
INSTALLED_APPS = [
    ...
    'tree_menu',
]
```
3. Примените миграции:
```
python manage.py migrate
```

## Создание меню
1. Перейдите в админку (/admin/).

2. В разделе Menu Items добавляйте пункты меню:

    Menu name — имя меню (main_menu)

    Title — название пункта

    Parent — родительский пункт (оставьте пустым для корня)

    Explicit URL — прямой URL (/about/)

    Named URL — имя URL (app:detail)

    Order — порядок сортировки