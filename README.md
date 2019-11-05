# Публикация комиксов xckd в группе ВК

Приложение скачивает случайный комикс от [xckd](https://xkcd.com/) и публикует в указанной группе ВК. 

### Установка

Для работы приложения требуется **Python 3**.

Установить зависимости приложения:
```
pip install -r requirements.txt
```

### Настройка

Подготовить файл для хранения конфигурации приложения:
```
cp .env.example .env
```

---
Создать группу в [ВК](https://vk.com/groups?tab=admin).

Добавить в `.env` id группы ([как узнать id группы?](http://regvk.com/id/)):
```
VK_GROUP_ID=
```

---

Создать приложение в [ВК](https://vk.com/editapp?act=create)

Получить **id** приложения (можно взять из адресной строки, если перейти в редактирование приложения). 

---

Получить **access_token** для работы с приложением.

Открыть в браузере адрес (необходимо подставить свой **id приложения**):

```
https://oauth.vk.com/authorize?client_id={id}&response_type=token&scope=photos,groups,wall
```

Значение **access_token** необходимо взять из адресной строки после выполнения вышеуказанного запроса и поместить в `.env` своего приложения:
```
VK_ACCESS_TOKEN=
```

---

Добавить в `.env` версию VK API ([узнать версию API](https://vk.com/dev/versions)):
```
VK_API_VERSION=
```




### Запуск

```
python main.py
```

После успешной публикации комикса приложение выведет сообщение:
```
Comics published. Id - 15.
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).