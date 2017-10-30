# -*- coding: utf-8 -*-
# Классы для отправки запросов к API MyTarget
# В рамках задачи https://support.rt.ru/browse/ANALYTICS-76

import requests
import time
import random

import error

API_URL = 'https://target.my.com/api/v2'

# служебное сообщение, которое отдает метод self.__apiResponseErrorHandler при необходимости повторить запрос
API_NET_ERROR_HANDLER_MESSAGE = 'Again'
API_OK_RESPONSE_HANDLER_MESSAGE = 'Ok'

class HTTP():
	"""
	Класс для отправки запросов к API MyTarget
	"""

	def __init__( self, requestType, path, **kwargs ):
		"""
		Инициализация инстанса для запросов requests с параметрами:
			- API_URL + requestPath это запрос
			- requestType - тип запроса (POST для авторизации и GET для получения статистики)
			- **kwargs - параметры запроса
		"""

		self.requestType = requestType
		self.path = path

		self.params = kwargs

	def makeRequest( self, access_token = '' ):
		"""
		Отправка запроса API MyTarget. В случае сетевых ошибок делаем запрос с экспоненциальной задержкой.
		"""

		for n in range( 0, 5 ):
			try:

				if self.requestType == 'post':
					requestData = self.__postRequest()

				elif self.requestType == 'get':
					self.access_token = access_token
					requestData = self.__getRequest()

				else:
					raise error.UnknownRequestTypeError

				requestDataJSON = requestData.json()

				repeatOrContinue = self.__apiResponseErrorHandler( netError = False, response = requestData )

				if repeatOrContinue == API_OK_RESPONSE_HANDLER_MESSAGE:
					return requestDataJSON

				else:
					print 'Sleeping for {} seconds'.format( 2**n )
					time.sleep((2 ** n) + random.random())

			# отлов сетевых ошибок
			except Exception as e:

				print 'Sleeping for {} seconds'.format( 2**n )
				time.sleep((2 ** n) + random.random())

		raise Exception( 'There was net error for 5 times' )

	def __postRequest( self ):
		"""
		Отправка POST-запроса для авторизации. Параметры передаются в теле запроса
		"""

		# print self.path
		# print self.params

		return requests.post( API_URL + self.path, data = self.params )

	def __getRequest( self ):
		"""
		Отправка GET-запроса для получения статистики. Параметры передаются в параметрах запроса + необходимо передавать access_token в заголовке
		"""

		headers = { 'Authorization': 'Bearer {}'.format( self.access_token ) }

		return requests.get( API_URL + self.path, params = self.params, headers = headers )

	def __apiResponseErrorHandler( self, netError = True, response = '' ):
		"""
		Обработка ошибки при запросе к API MyTarget. Параметр netError = True означает ошибку на уровне сети (получаем Exception).
		netError = False означает получение ошибки от API MyTarget (например, неверный токен). 
		
		Коды ошибок API MyTarget https://target.my.com/adv/api-marketing/doc/api-arrangement/
		Для 400-х ошибок API MyTarget выдаем Exception. Для 500-х и netError = True - ждем и делаем еще один запрос.

		Пример текста ошибки:
		{
			"error": {
				"message": "entities are not found",
				"code": "WRONG_CAMPAIGNS"
			}
		}
		"""

		if netError:
			return API_NET_ERROR_HANDLER_MESSAGE

		else:
			if response.status_code != 200:
				# print response.text

				if 'error' in response.json():
					if response.json()['error']['code'] == 'ACCESS_DENIED':
						raise error.AccessDeniedError

					if response.json()['error']['code'] == 'WRONG_CAMPAIGNS':
						raise error.WrongCampaignIDError

				return API_NET_ERROR_HANDLER_MESSAGE

			# похоже на правильный ответ
			else:
				return API_OK_RESPONSE_HANDLER_MESSAGE
