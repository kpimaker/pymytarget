# -*- coding: utf-8 -*-
# Классы для обработки ошибок при работе с API MyTarget
# В рамках задачи https://support.rt.ru/browse/ANALYTICS-76

class ConfigFileNotFoundError():
	"""Файл config.yaml не найден"""
	pass

class ClientIDOrClientSecretNotFoundError():
	"""В config.yaml нет client_id или client_secret"""
	pass

class ParamsFileNotFoundError():
	"""Файл params.yaml не найден в папке библиотеки"""
	pass

class ParamsFileReadError():
	"""Ошибка при чтении файла params.yaml. Скорее всего ошибка в названии ключа"""
	pass

class UnknownRequestTypeError():
	"""Неизвестный тип запроса в http.HTTP.makeRequest"""
	pass

class AccessDeniedError():
	"""Неверный токен access_token"""
	pass

class WrongCampaignIDError():
	"""Некорректное значение ID кампании"""
	pass