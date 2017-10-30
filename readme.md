# Библиотека для работы с API MyTarget

## Быстрый старт

**Перед началом работы**

1. Внесите параметры приложения, от имени которого вы будете делать запросы в API, в файл config.yaml. Пример:

**config.yaml**
```
mytarget:
    key1:
        Client ID: T3j...4k
        Client secret: M4...j5l
```

2. При первом запуске сгенерируйте refresh_token и access_token. В дальнейшем обновление access_token происходит автоматически при каждом запросе (обновляется при истечении срока действия). Для клиента, от имени которого вы будете делать запросы, вызовите файл pyMyTarget.py:

```python
mt = MyTarget( client = 'my_client_name' )
mt.generateRefreshToken()
```

При успешном прохождении авторизации в файле params.yaml будет записан access_token для запросов и информация для его обновления при необходимости.

Адреса файлов можно задавать вручную. Варианты значений configPath в текущей версии:

* 'current directory': берем текущую директорию, в которой лежит файл pyMyTarget.py
* 'tableau': папка файла config.yaml на ВМ Tableau, т. е. 'C:\Users\prod\config'
* в других случаях возвращает self.configPath (например, если путь прописан явно)

3. Для получения статистики по рекламной кампании выполните:

```python
print mt.campaign( my_campaign_id )
```

Вы должны получить статистику по кампании вида:

```
{ u'items': 
	[
		{ u'total': 
			{ u'base': 
				{ u'cpm': u'394.79', u'ctr': 1.1448874851954205 u'cpa': u'0', u'cpc': u'34.48', u'spent': u'1000', u'goals': 0, u'cr': 0, u'clcks': 29, u'shows': 2533 }
			}, 

			u'rows': 
				[
					{u'date': u'2017-10-01', u'base': {u'cpm' u'394.79', u'ctr': 1.1448874851954205, u'cpa': u'0', u'cpc': u'34.48', u'spent: u'1000', u'goals': 0, u'cr': 0, u'clicks': 29, u'shows': 2533 }
				}
			], 

			u'id': 830876
		}
	], 

	u'total': 
		{ u'base': 
			{ u'cpm': u'394.79', u'ctr': 1.1448874851954205, u'cpa: u'0', u'cpc': u'34.48', u'spent': u'1000', u'goals': 0, u'cr': 0, u'clicks':9, u'shows': 2533 }
		}
}
```

## Описание ошибок

Все ошибки должны быть описаны в файле error.py.

* ConfigFileNotFoundError - файл config.yaml не найден
* ClientIDOrClientSecretNotFoundError - в config.yaml нет client_id или client_secret
* ParamsFileNotFoundError - файл params.yaml не найден в папке библиотеки
* ParamsFileReadError - ошибка при чтении файла params.yaml. Скорее всего ошибка в названии ключа
* UnknownRequestTypeError - неизвестный тип запроса в http.HTTP.makeRequest
* AccessDeniedError - неверный токен access_token
* WrongCampaignIDError - некорректное значение ID кампании