import sqlite3
class SQLigther:
	def __init__(self, database_file):
		'''подключение к БД и сохранение курсора соединения'''
		self.connection = sqlite3.connect(database)
		self.cursor = self.connection.cursor()

	def get_subscription(self, status = True):
		'''получаем всех активных подписчиков'''
		with self.connection:
			return self.cursor.execute('SELECT * FROM "users" WHERE "status" = ?', (status,)).fetchall()

	def subscriber_exist(self, user_id):
		'''проверяем есть ли юзер в базе'''
		with self.connection:
			result = self.cursor.execute("SELECT FROM 'users' WHERE 'user_id' = ?", (user_id,)).fetchall()
			return bool(len(result))

	def add_subscriber(self, user_id, status = True):
		with self.connection:
			return self.cursor.execute("INSERT INTO 'users' ('user_id', 'status') VALUES (?,?)", (user_id, status))

	def update_subscription(self, user_id, status):
		with self.connection:
			return self.cursor.execute("UPDATE 'users' SET 'status' = ? WHERE 'user_id' = >?", (status,user_id))

	def close(self):
		with self.connection:
			return self.connection.close()
			