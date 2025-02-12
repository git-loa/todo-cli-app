import psycopg2 
import os


def get_env_variable(env_var):
	"""
	Get environment variable required to connect to a postgres database.
	"""
	value = os.getenv(env_var)
	if value is None:
		raise EnvironmentError(f"Environment variable {env_var} is not set.")
	return value

def connect_db():
	"""
	Function to connect app to PostgreSQL.
	"""

	# Variables needed to establish a database connection
	params = {
		'dbname': get_env_variable('DB_NAME'),
		'user' : get_env_variable('DB_USER'),
		'password' : get_env_variable('DB_PASSWORD'),
		'host' : get_env_variable('DB_HOST'),
		'port' : get_env_variable('DB_PORT')
	}
	
	# Establishing the connection
	try:
		conn =  psycopg2.connect(**params)
		return conn
	except psycopg2.OperationalError:
		print("Error connecting to the databse :/")
