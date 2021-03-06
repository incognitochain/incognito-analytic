import os

postgresuser = os.getenv('postgresuser', 'postgres')
postgrespwd = os.getenv('postgrespwd', 'postgres')
postgreshost = os.getenv('postgreshost', '127.0.0.1')
postgresport = os.getenv('postgresport', '5432')
postgresdb = os.getenv('postgresdb', 'pdex')
SQLALCHEMY_DATABASE_URI = 'postgresql://' + postgresuser + ':' + postgrespwd + '@' + postgreshost + ':' + postgresport + '/' + postgresdb + ''
