# -*- coding: utf-8 -*-
# Тесты для библиотеки работы с MyTarget
# Библиотека написана в рамках задачи https://support.rt.ru/browse/ANALYTICS-76

import unittest

import pyMyTarget
import http

from error import ConfigFileNotFoundError
from error import ClientIDOrClientSecretNotFoundError
from error import ParamsFileNotFoundError
from error import ParamsFileReadError
from error import ParamsFileReadError
from error import UnknownRequestTypeError
from error import AccessDeniedError
from error import WrongCampaignIDError

class TestPyMytarget( unittest.TestCase ):
	"""
	Группы тестов:

	1. Ошибки в файле config.yaml при инициализации инстанса:
		- наличие файла config.yaml
		- наличие необходимых для работы с API ключей для всех клиентов ('Client ID', 'Client secret') 
		- попытка инициализации инстанса с несуществующим файлом параметров

	2. Отправка и обработка запросов (http.py):
		- передача некорректного типа запроса
		- неверный или устаревший токен при запросе к API
		- некорректное значение ID кампании

	3. Проверки возвращаемых значений для методов:
		- проверка значений, которые возвращает метод campaign
	"""

	# ---------------------------------------------------------------
	# Инициализация pyMyTarget
	# ---------------------------------------------------------------

	def test_init_and_check_if_config_file_exists( self ):
		"""	Наличие файла config.yaml при инициализации инстанса """

		# инициализация с несуществующим файлом
		with self.assertRaises( ConfigFileNotFoundError ):
			pyMyTarget.MyTarget( configFile = 'test/config_non-existent.yaml' )

		# путь указан неправильным выражением
		with self.assertRaises( ConfigFileNotFoundError ):
			pyMyTarget.MyTarget( configPath = '123_current directory' )

	def test_init_credentials_in_config_file( self ):
		"""	config.yaml должен содержать client_id и client_secret """

		with self.assertRaises( ClientIDOrClientSecretNotFoundError ):
			pyMyTarget.MyTarget( configPath = 'test', configFile = 'config_broken_client_id.yaml' )

		with self.assertRaises( ClientIDOrClientSecretNotFoundError ):
			pyMyTarget.MyTarget( configPath = 'test', configFile = 'config_broken_client_secret.yaml' )

	def test_init_and_check_if_params_file_exists( self ):
		"""	Наличие файла params.yaml при инициализации инстанса """

		# инициализация с несуществующим файлом
		with self.assertRaises( ParamsFileNotFoundError ):
			pyMyTarget.MyTarget( paramsFile = '123_params.yaml' )

		# файл найден, но составлен некорректно
		with self.assertRaises( ParamsFileReadError ):
			pyMyTarget.MyTarget( paramsFile = 'test\params_broken.yaml' )


	# ---------------------------------------------------------------
	# Отправка и обработка запросов http.py
	# ---------------------------------------------------------------

	def test_makeRequest_wrong_request_type( self ):
		"""	Передача некорректного типа запроса """

		with self.assertRaises( UnknownRequestTypeError ):
			http.HTTP( 'some_request_type', '/statistics/campaigns/summary.json' ).makeRequest()

	def test_makeRequest_access_denied_error( self ):
		"""	Неверный или устаревший токен при запросе к API """

		with self.assertRaises( AccessDeniedError ):
			http.HTTP( 'get', '/statistics/campaigns/summary.json' ).makeRequest( access_token = '123' )

	def test_makeRequest_wrong_campaign_id_error( self ):
		"""Некорректное значение ID кампании"""

		access_token = pyMyTarget.MyTarget().updateAccessToken()

		with self.assertRaises( WrongCampaignIDError ):
			http.HTTP( 'get', '/statistics/campaigns/summary.json', id = 12345, date_from = '2017-10-01', date_to = '2017-10-01', metrics = 'base' ).makeRequest( access_token = access_token )


	# ---------------------------------------------------------------
	# Возвращаемые значения для методов
	# ---------------------------------------------------------------

	def test_method_campaign_for_date( self ):
		"""Проверка значений, которые возвращает метод campaign"""

		campaignStatsData = pyMyTarget.MyTarget( client = 'center-b2b-vats' ).campaign( 8308976, date_from = '2017-10-01', date_to = '2017-10-01' )
		
		self.assertEqual( campaignStatsData['items'][0]['rows'][0]['date'], '2017-10-01' )
		self.assertEqual( campaignStatsData['items'][0]['rows'][0]['base']['shows'], 2533 )
		self.assertEqual( campaignStatsData['items'][0]['rows'][0]['base']['clicks'], 29 )
		self.assertEqual( campaignStatsData['items'][0]['rows'][0]['base']['spent'], '1000' )


if __name__ == '__main__':
	unittest.main()