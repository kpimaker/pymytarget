# -*- coding: utf-8 -*-
# Классы для работы с API MyTarget
# В рамках задачи https://support.rt.ru/browse/ANALYTICS-76

import yaml
import os

import error
import auth
import http

from datetime import datetime, timedelta


class MyTarget():
	"""
	Класс для отправки и обработки запросов к API MyTarget.
	Дополнение задачи отчетности по контексту данными по MyTarget
	https://support.rt.ru/browse/ANALYTICS-76
	https://target.my.com/doc/api/detailed/#resource_statistics
	https://target.my.com/adv/api-marketing/doc/stat-v2
	
	"""

	def __init__( self, client = 'center-b2b-vats', key = 'key1', configPath = 'current directory', configFile = 'config.yaml', paramsFile = 'params.yaml' ):
		"""
		Инициализация инстанса и основных параметров:
		Варианты значений configPath описаны в методе __setConfigPath
		"""

		# ---------------------------------------------------------------
		# задание self.configPathRealAddress
		# ---------------------------------------------------------------
		self.client = client
		self.key = key

		self.configFile = configFile
		self.configPath = configPath

		self.paramsFile = paramsFile

		# реальный адрес директории, в которой лежит config.yaml
		self.configPathRealAddress = self.__setConfigPath()

		try:
			self.config = yaml.load( file( os.path.join( self.configPathRealAddress, self.configFile ) ) )

		except:
			raise error.ConfigFileNotFoundError


		# ---------------------------------------------------------------
		# задание self.client_id и client_secret
		# ---------------------------------------------------------------

		try:
			self.client_id = self.config['mytarget'][ self.key ]['Client ID']
			self.client_secret = self.config['mytarget'][ self.key ]['Client secret']

		except:
			raise error.ClientIDOrClientSecretNotFoundError


		# ---------------------------------------------------------------
		# чтение параметров params.yaml и задание токенов
		# ---------------------------------------------------------------

		try:
			self.params = yaml.load( file( os.path.join( os.path.dirname( os.path.abspath(__file__) ), self.paramsFile ) ) )

		except:
			raise error.ParamsFileNotFoundError

		
		try:
			self.login = self.params['clients'][ self.client ]['login']
			self.refresh_token = self.params['clients'][ self.client ]['refresh_token']

			self.access_token = self.params['clients'][ self.client ]['access_token']
			self.expires_in = self.params['clients'][ self.client ]['expires_in']

		except:
			raise error.ParamsFileReadError


	def __setConfigPath( self ):
		"""
		Перевод значения configPath из словесной формы в адрес.
		Варианты значений в текущей версии:
			- 'current directory': берем текущую директорию, в которой лежит файл pyMyTarget.py
			- 'tableau': папка файла config.yaml на ВМ Tableau, т. е. 'C:\Users\prod\config'
			- в других случаях возвращает self.configPath (например, если путь прописан явно)
		"""

		if self.configPath == 'current directory':
			# текущая директория файла
			return os.path.dirname( os.path.abspath(__file__) )

		elif self.configPath == 'tableau':
			return 'C:\\Users\\prod\\config'

		else:
			return self.configPath

	def generateRefreshToken( self ):
		"""
		Прохождение процедуры авторизации при первом запуске. Получаем refresh token.
		Результат пишется в файл auth_info.txt
		"""

		return auth.Auth( self.client_id, self.client_secret, self.client ).generateRefreshToken()

	def timeToUpdateToken( self ):
		"""
		Проверяем не пора ли обновить токен. Сравниваем текущее время с self.expires_in плюс сутки
		"""

		return datetime.now() > self.expires_in

	def updateAccessToken( self ):
		"""
		Проверка и обновление access_token в случае истечения его срока действия.
		"""

		# время обновить токен
		if self.timeToUpdateToken():
			print 'Updating token'

			tokenData = auth.Auth( self.client_id, self.client_secret, self.client, refresh_token = self.refresh_token ).updateAccessToken()
			""" tokenData представляем собой JSON вида:
			{
				u'access_token': u'W...h', 
				u'token_type': u'Bearer', 
				u'expires_in': 86400, 
				u'refresh_token': u'D...v'
			}
			"""
			
			# обновляем значение access_token и expires_in для текущего клиента
			self.params['clients'][ self.client ]['access_token'] = tokenData['access_token']
			self.params['clients'][ self.client ]['expires_in'] = datetime.now() + timedelta( seconds = tokenData['expires_in'] )

			with open( os.path.join( os.path.dirname( os.path.abspath(__file__) ), self.paramsFile ), 'w' ) as f:
				yaml.dump( self.params, f )

		return self.access_token

	def campaign( self, campaignID, date_from = '2017-10-01', date_to = '2017-10-01', metrics = 'base' ):
		"""
		Получение статистики по дням кампании campaignID

		Пример

		"""

		self.access_token = self.updateAccessToken()
		campaignData = http.HTTP( 'get', '/statistics/campaigns/day.json', id = campaignID, date_from = date_from, date_to = date_to, metrics = metrics ).makeRequest( access_token = self.access_token )
		
		return campaignData


if __name__ == '__main__':

	# генерация refresh_token для разных client_id при первом запуске
	mt = MyTarget( client = 'center-b2b-vats' )
	# mt.generateRefreshToken()

	print mt.campaign( 8308976 )