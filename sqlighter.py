import sqlite3


class SQLighter:
	def __init__(self, database_file):
		'''подключение к БД и сохранение курсора соединения'''
		self.connection = sqlite3.connect(database_file)
		self.cursor = self.connection.cursor()

	def get_subscription(self, status = True):
		'''получаем всех активных подписчиков'''
		with self.connection:
			return self.cursor.execute('SELECT * FROM USERS WHERE STATUS = ?', (status,)).fetchall()

	def subscriber_exist(self, user_id):
		'''проверяем есть ли юзер в базе'''
		with self.connection:
			result = self.cursor.execute("SELECT * FROM USERS WHERE USER_ID = ?", (user_id,)).fetchall()
			return bool(len(result))

	def add_subscriber(self, user_id, status = True):
		with self.connection:
			return self.cursor.execute("INSERT INTO users ('user_id', 'status') VALUES (?,?)", (user_id, status))

	def add_sity(self, user_id, sity):
		with self.connection:
			return self.cursor.execute("INSERT INTO users ('user_id', 'sity') VALUES (?,?)", (user_id, sity))

	def get_sity(self, user_id):
		with self.connection:
			return self.cursor.execute('SELECT sity FROM USERS WHERE STATUS = ?', (user_id,)).fetchall()

	def update_subscription(self, user_id, sity, status):
		with self.connection:
			return self.cursor.execute("UPDATE users SET sity = ?, status = ? WHERE user_id = ?", (status, sity, user_id))

	def close(self):
		with self.connection:
			return self.connection.close()
