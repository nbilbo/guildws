#-*- coding: utf-8 -*-

class Controle:
	"""
	responsavel por criar, estabelecer conexao 
	com o banco de dados e executar querys.
	"""
	def __init__(self):
		self.conexao = self.conectar()


	def conectar(self):
		#vai procurar por um arquivo chamando guildws.db3, 
		#se existir, ele estabelece a conexao,
		#se nao existir, ele cria um.
		from sqlite3 import connect
		from os import listdir
		from re import search, findall
		from re import compile as reCompile

		#guardar a conexao com o banco
		conexao = None

		#diretorios
		pathModel = r"../model"

		#verificar se existe o arquivo guildws.db3
		#se exister, apenas conectamos.
		#se nao exister, criamos o arquivo juntamente com as tabelas.

		if "guildws.db3" in listdir(pathModel):
			conexao = connect(pathModel + r"/guildws.db3")
		else:
			conexao = connect(pathModel + r"/guildws.db3")
			cursor = conexao.cursor()
			scriptBanco = open(pathModel + r"/script banco.sql").read()
			pattern = reCompile("(.*?;)")
			result = findall(pattern, scriptBanco)
			for query in result:
				cursor.execute(query)
			conexao.commit()

		return conexao

	#Create
	def createData(self, valores):
		#Adicionar um novo dado a tabela data.
		if self.conexao:
			cursor = self.conexao.cursor()
			cursor.execute("insert into data (data) values (?)", (valores,) )
			self.conexao.commit()
			return cursor.lastrowid

		return False

	def createJogador(self, valores):
		#Adicionar um novo dado a tabela jogador.
		if self.conexao:
			cursor = self.conexao.cursor()
			cursor.execute("insert into jogador (nome, id_cargo) values (?, ?)", valores)
			self.conexao.commit()
			
			return True

		return False

	def createGp(self, valores):
		#Adicionar um novo dado a tabela gp.
		if self.conexao:
			cursor = self.conexao.cursor()
			cursor.execute("insert into gp (id_data, nome, cargo, gp) values (?, ?, ?, ?)", valores)
			self.conexao.commit()
			return True

		return False

	#Read
	def readData(self, iddata):
		if self.conexao:
			cursor = self.conexao.cursor()
			cursor.execute("select data from data where iddata = ?;", (iddata,))
			rows = cursor.fetchall()
			return rows

	def readJogadorId(self, idjogador):
		if self.conexao:
			cursor = self.conexao.cursor()
			cursor.execute("select * from v_jogador where idjogador = ?;",(idjogador,) )
			rows = cursor.fetchall()
			return rows

	def readJogadorNome(self, nome):
		if self.conexao:
			cursor = self.conexao.cursor()
			query = "select * from v_jogador where nome = ?;"
			cursor.execute(query, (nome,))
			rows = cursor.fetchall()
			return rows

	def readGp(self, values):
		if self.conexao:
			cursor = self.conexao.cursor()
			query = "select * from v_gp where iddata = ? and nome = ?"
			cursor.execute(query, values)
			rows = cursor.fetchall()
			return rows


	def readAllData(self):
		if self.conexao:
			cursor = self.conexao.cursor()
			query = "select * from data;"
			cursor.execute(query)
			rows = cursor.fetchall()
			return rows

	def readAllJogador(self) :
		if self.conexao:
			cursor = self.conexao.cursor()
			query = "select * from v_jogador;"
			cursor.execute(query)
			rows = cursor.fetchall()
			return rows


	def readAllGp(self, iddata):
		if self.conexao:
			cursor = self.conexao.cursor()
			query = "select * from v_gp where iddata = ?;"
			cursor.execute(query, (iddata,))
			rows = cursor.fetchall()
			return rows

	def readAllData(self):
		if self.conexao:
			cursor = self.conexao.cursor()
			query = "select * from data;"
			cursor.execute(query)
			rows = cursor.fetchall()
			return rows

	#Update
	def updateData(self, values):
		if self.conexao:
			cursor = self.conexao.cursor()
			query = "update data set data = ? where iddata = ?"
			cursor.execute(query, values)
			self.conexao.commit()
			return True

		return False

	def updateJogador(self, values):
		if self.conexao:
			cursor = self.conexao.cursor()
			query = "update jogador set nome = ?, id_cargo = ? where idjogador = ?"
			cursor.execute(query, values)
			self.conexao.commit()
			return True

		return False

	def updateGp(self, values):
		if self.conexao:
			cursor = self.conexao.cursor()
			query = "update gp set gp  = ? where id_data = ? and nome = ?;"
			cursor.execute(query, values)
			self.conexao.commit()
			return True

		return False

	def triggerUpdateJogador(self, idjogador, nomeAntigo):
		if self.conexao:
			#obter os dados atuais do jogador
			cursor = self.conexao.cursor()
			query = "select nome, cargo from v_jogador where idjogador = ?;"
			cursor.execute(query, (idjogador,) )
			row = cursor.fetchall()[0]

			#atulizar a tabela gp
			valores = (row[0], row[1], nomeAntigo)
			query = "update gp set nome = ?, cargo = ? where nome = ?;"
			cursor.execute(query, valores)
			self.conexao.commit()
			return True

		return False


	#Delete
	def deleteJogador(self, idjogador):
		if self.conexao:
			cursor = self.conexao.cursor()
			query = "delete from jogador where idjogador = ?;"
			cursor.execute(query, (idjogador,))
			self.conexao.commit()
			return True

		return False

	def deleteData(self, iddata):
		if self.conexao:
			cursor = self.conexao.cursor()

			query = "delete from gp where id_data = ?"
			cursor.execute(query, (iddata,) )

			query = "delete from data where iddata = ?;"
			cursor.execute(query, (iddata,) )

			self.conexao.commit()
			return True

if __name__ == "__main__":
	c = Controle()
