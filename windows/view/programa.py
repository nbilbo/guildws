#-*- coding: utf-8 -*-

#tentando importar python 2x ou 3x
try:
	#python 2x
	from Tkinter import Tk, Frame, Label, Menu, Scrollbar, Toplevel, Entry, Button, StringVar
	from tkMessageBox import showinfo
	from ttk import Treeview, Style, Button as Buttonttk, Label as Labelttk, Entry as Entryttk, OptionMenu as OptionMenuttk
	from functools import partial
	#print("python 2x")

except ImportError:
	#python 3x
	from tkinter import Tk, Frame, Label, Menu, Scrollbar, Toplevel, Entry, Button, StringVar
	from tkinter.messagebox import showinfo
	from tkinter.ttk import Treeview, Style, Button as Buttonttk, Label as Labelttk, Entry as Entryttk, OptionMenu as OptionMenuttk
	from functools import partial
	#print("python 3x")

except Exception as e:
	print(e)

#pasta onde está a classe Controle
from sys import path
path.append("../control")
from controle import Controle

class Programa(Tk):
	def __init__(self, **kwargs):
		Tk.__init__(self, **kwargs)
		self.title("1.0")
		self.controle = Controle()

		style = Style()
		style.configure("TLabel", font = (None, 18))
		style.configure("TButton", font = (None, 18))
		style.configure("TMenubutton", font = (None, 18))
		style.configure("Treeview", font = (None, 16), rowheight = 30)
		style.configure("Treeview.Heading", font = (None, 18))

		self.createMenubar()
		self.createContainer()

	def createMenubar(self):
		"""
		criar a barra de menu.
		"""

		menubar = Menu(font = (None, 12))
		self.config(menu = menubar)

		menubarMenu = Menu(menubar, tearoff = 0, font = (None, 12))
		menubarMenu.add_command(label = "Jogadores", command = lambda: self.setTela("TelaJogadores"))
		menubarMenu.add_command(label = "Pontos de guild", command = lambda: self.setTela("TelaPontosGuild"))

		menubar.add_cascade(label = "Menu", menu = menubarMenu)
		menubar.add_command(label = "Sobre", command = lambda: showinfo(title = "Sobre", message = "Não sei porque fiz isso.") )

	def createContainer(self):
		"""
		posicionar todas as telas em um mesmo lugar.
		"""
		container = Frame(self)
		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		self.telas = {}
		for tela in (TelaJogadores, TelaPontosGuild):
			name = tela.__name__ 
			instanciaTela = tela(container, controle = self.controle)
			instanciaTela.grid(row = 0, column = 0, sticky = "nswe")
			self.telas[name] = instanciaTela

		self.setTela("TelaJogadores")
		container.pack(fill = "both", expand = True, padx = 5, pady = 5)

	def setTela(self, tela):
		"""
		definiar qual a tela que será mostrada.
		"""
		self.telas[tela].tkraise()

	def executar(self):
		"""
		definindo as dimensões da janela principal.
		"""
		self.geometry("650x400")
		self.mainloop()

#################Tela jogadores########################
class TelaJogadores(Frame):
	"""
	um frame que contem um treeview e scroll
	"""
	def __init__(self, parent, controle, **kwargs):
		Frame.__init__(self, parent, **kwargs)
		self.controle = controle
		self.createTree()
		self.createButton()
		self.updateTree()
		
	def createTree(self):
		"""
		criar self.tree 
		"""

		#criando os widgets
		frame = Frame(self)
		self.tree = Treeview(frame)
		scroll = Scrollbar(frame, width = 22, command = self.tree.yview)
		self.tree.configure(yscrollcommand = scroll.set)

		#configurando as colunas de self.tree
		self.tree["columns"] = ("idjogador", "nome", "cargo")
		self.tree.heading("nome", text = "Nome")
		self.tree.heading("cargo", text = "Cargo")
		self.tree.column("#0", width = 0, stretch = False)
		self.tree.column("idjogador", width = 0, stretch = False)
		self.tree.column("nome", width = 307, minwidth = 307, stretch = True)
		self.tree.column("cargo", width = 307, minwidth = 307, stretch = True)


		#posicioanando
		frame.pack(fill = "both", expand = True)
		self.tree.pack(side = "left", fill = "both", expand = True)
		scroll.pack(side = "left", fill = "y")

		#command

	def createButton(self):
		"""
		criar os botoes p/ adicionar ou remover jogadores
		"""

		#criando os botoes
		buttonAdicionar = Buttonttk(self, width = 10, text = "+")
		buttonRemover = Buttonttk(self, width = 10, text = "-")

		#posicionando
		buttonAdicionar.pack(side = "left", padx = 5, pady = 5)
		buttonRemover.pack(side = "right", padx = 5, pady = 5)

		#command
		#chamado quando o botao é clicado
		buttonAdicionar["command"] = partial(ToplevelJogadorCreate, self)
		buttonRemover["command"] = self.buttonRemoverClick

		#chamando quando é clicado 2x com o mouse em cima da tree
		self.tree.bind("<Double-Button-1>", lambda event: self.updateJogador())

	def updateJogador(self, *args):
		"""
		atualizar os dados de um jogador que já existe.
		"""

		#obtendo os valores do item que foi selecionado
		itens = self.tree.item(self.tree.selection()[0])
		idjogador = itens["values"][0]
		nomeAntigo = itens["values"][1]
		cargoAntigo = itens["values"][2]

		#instanciando o toplevel
		ToplevelJogadorUpdate(self, cargoDefault = cargoAntigo, nome = nomeAntigo, idjogador = idjogador)


	def buttonRemoverClick(self):
		#verificando se é válido a remoção
		itens = self.tree.selection()
		if itens:
			for item in itens:
				idjogador = self.tree.item(item)["values"][0]
				self.controle.deleteJogador(idjogador)
			self.updateTree()
				

	def updateTree(self):
		"""
		atualizar self.tree com todos os valores da tabela 'jogadores'.
		"""
		self.tree.delete(*self.tree.get_children())
		valores = self.controle.readAllJogador()
		for valor in valores:
			idjogador = valor[0]
			nome = valor[1]
			cargo = valor[2]
			self.tree.insert("", "end", values = (idjogador, nome, cargo))

	def getTree(self):
		"""
		retornar self.tree
		"""
		return self.tree

	def getControle(self):
		return self.controle
		

#classe abistrata
#nao deve ser instancializada, apenas expandida
class ToplevelJogador(Toplevel):
	def __init__(self, parent, cargoDefault, nome, **kwargs):
		Toplevel.__init__(self, **kwargs)
		#parent
		self.parent = parent
		

		#dimensão da janela
		x = parent.winfo_rootx()
		y = parent.winfo_rooty()
		self.geometry("650x150+{}+{}".format(x, y))
		self.title("Jogador(a)")

		#frame top
		frameTop = Frame(self)

		#criando o label & entry
		label = Labelttk(frameTop, text = "Nome")
		self.entry = Entryttk(frameTop, font = (None, 18))
		self.entry.insert("end", nome)
		self.entry.focus()

		#criando o menu de cargos
		self.dicionarioCargos = {
		"novato": 1, "explorador": 2, "herdeiro": 3, "lider": 4
		}
		self.stringMenu = StringVar()
		self.menu = OptionMenuttk(frameTop, self.stringMenu, cargoDefault, *[cargo for cargo in self.dicionarioCargos.keys()])
		self.menu["width"] = 11

		#crinando o label de aviso
		self.labelAviso = Labelttk(self)

		#criando o botao
		self.button = Buttonttk(self, text = "B", width = 20)


		#posicionando
		frameTop.pack(fill = "x", padx = 5, pady = 5)
		label.pack(side = "left")
		self.entry.pack(side = "left", fill = "x", padx = 2)
		self.menu.pack(side = "left")
		self.labelAviso.pack(padx = 5, pady = 5)
		self.button.pack(padx = 5, pady = 5)

		#bind
		label.bind("<Double-Button-1>", lambda event: self.entry.focus())
		self.entry.bind("<Key>", lambda event: self.clearLabelAviso())

	def clearLabelAviso(self, *args):
		"""
		caso self.labelTexto estejá mostrando uma mensagem de aviso, ela devesumir sempre que o usuario digitar em self.entry
		"""
		if self.labelAviso["text"]:
			self.labelAviso["text"] = ""

	
	def validar(self):
		nome = self.entry.get().strip().lower()
		cargo = self.dicionarioCargos[self.stringMenu.get()]

		#se os campos de nome e cargo estiverem validos
		if nome and cargo:

			#se for um nome repetido
			if self.parent.controle.readJogadorNome(nome):
				self.labelAviso["text"] = "Jogador(a) já existe."
				return False

			#se nao for um nome repetido
				return True

		#se os campos de nome e cargo nao estiverem validos
		self.labelAviso["text"] = "Campos inválidos."
		return False
	
	
class ToplevelJogadorCreate(ToplevelJogador):
	"""
	criar uma nova janela p/ definir o nome e cargo do novo jogador.
	"""
	def __init__(self, parent, cargoDefault = "novato", nome = "",  **kwargs):
		ToplevelJogador.__init__(self, parent, cargoDefault, nome, **kwargs)
		#definindo o nome do botao
		self.button["text"] = "Adicionar"
		#definindo qual função deve ser chamada quando o botao for clicado
		self.button["command"] = self.buttonClick
		self.entry.bind("<Return>", lambda event: self.buttonClick())

	def buttonClick(self, *args):
		"""
		adicioanar o novo jogador ao banco, atualizar a tree.
		"""

		#referenciando os objetivos necessarios p/ inserir no banco
		tree = self.parent.getTree()
		controle = self.parent.getControle()

		#validando os campos
		nome = self.entry.get().strip().lower()
		cargo = self.dicionarioCargos[self.stringMenu.get()]

		#se for válido os campos
		
		if nome.strip() and cargo:

			#verificar se tem repeticao de nome
			if controle.readJogadorNome(nome):
				self.labelAviso["text"] = "Erro, jogador(a) já existe."

			#se nao possuir repeticao de nome
			else:
				#inserindo o novo jogador na tabela do banco de dados.
				controle.createJogador((nome, cargo))
				#atualizando a tree.
				self.parent.updateTree()
				#limpando o campo de entrada de dados.
				self.entry.delete(0, "end")
				self.labelAviso["text"] = "Adicionado com sucesso."

		#se nao for válido os campos
		else:	
			self.labelAviso["text"] = "Campos inválidos."

class ToplevelJogadorUpdate(ToplevelJogador):
	def __init__(self, parent, cargoDefault = "novato", nome = "", idjogador = -1, **kwargs):
		ToplevelJogador.__init__(self, parent, cargoDefault, nome, **kwargs)
		#atualizando o nome do botao
		self.button["text"] = "Atualizar"
		#preciso do nome antigo p/ saber se vai ter alteração no nome ou só no cargo.
		self.nomeAntigo = nome
		#precido do idjogador para identificar o jogador no banco de dados.
		self.idjogador = idjogador
		#definindo a função que deve ser chamada quando o botão é clicado.
		self.button["command"] = self.buttonClick
		self.entry.bind("<Return>", lambda event: self.buttonClick())

	def buttonClick(self, *args):
		"""
		atualizar as informações do jogador e atualizar a tree
		"""

		#referenciando os objetos 
		controle = self.parent.getControle()
		tree = self.parent.getTree()

		#validando os campos
		nome = self.entry.get().strip().lower()
		cargo = self.dicionarioCargos[self.stringMenu.get()]

		#verificar se o nome não foi alterado
		if nome == self.nomeAntigo:
			controle.updateJogador((nome, cargo, self.idjogador))
			self.labelAviso["text"] = "Atualizado."
			self.parent.updateTree()


		#se o nome for alterado
		else:

			#verificar se o novo nome ja existe
			if controle.readJogadorNome(nome):
				self.labelAviso["text"] = "Erro, usuario ja existe."

			#se o novo nome for valido
			else:
				controle.updateJogador((nome, cargo, self.idjogador))
				self.parent.updateTree()
				self.labelAviso["text"] = "Atualizado."




#################Tela pontos de guild########################	
class TelaPontosGuild(Frame):
	def __init__(self, parent, controle, **kwargs):
		Frame.__init__(self, parent, **kwargs)
		self.controle = controle
		self.createTreeData()
		self.createTreeGp()
		self.updataTreeData()
		

		#alterando o background
		self["background"] = "white"
	
	def createTreeData(self):
		"""
		criar o local das datas
		"""

		#criando um estilo p/ essa tree
		style = Style()
		style.configure("data.Treeview.Heading", font = (None, 12))
		
		#criando os widgets
		mainFrame = Frame(self, width = 200)
		topFrame = Frame(mainFrame)
		bottomFrame = Frame(mainFrame, height = 50)

		#crinando a tree e o scroll
		self.treeData = Treeview(topFrame, style = "data.Treeview")
		scroll = Scrollbar(topFrame, width = 30, command = self.treeData.yview)
		self.treeData.configure(yscrollcommand = scroll.set)

		#configurando as colunas
		self.treeData["columns"] = ("iddata", "data")

		self.treeData.heading("iddata", text = "iddata")
		self.treeData.heading("data", text = "Data")

		self.treeData.column("#0", width = 0, stretch = False)
		self.treeData.column("iddata", width = 0, stretch = False)
		self.treeData.column("data", width = 170, minwidth = 170, stretch = True)

		#criando os botoes
		buttonAdicionar = Buttonttk(bottomFrame, text = "+", width = 5)
		buttonRemover = Buttonttk(bottomFrame, text = "-", width = 5)

		#posicionando
		mainFrame.pack(side = "left", fill = "y", padx = 5, pady = 5)
		mainFrame.pack_propagate(False)
		topFrame.pack(fill = "both", expand = True, pady = 0)
		bottomFrame.pack(fill = "x", pady = 5)

		self.treeData.pack(side = "left", fill = "y")
		scroll.pack(side = "left", fill = "y")

		buttonAdicionar.pack(side = "left")
		buttonRemover.pack(side = "right")

		#command
		#instanciando ToplevelData sempre que buttonAdicionar for clicado
		buttonAdicionar["command"] = lambda parent  = self: ToplevelData(parent)

		#chamando o método removerData sempre que buttonRemover for clicado
		buttonRemover["command"] = self.removerData

		#chamando o método self.updateTeeGp sempre que for clicado 2x em cima de um item de self.treeData
		self.treeData.bind("<Double-Button-1>", self.updateTreeGp)


	def createTreeGp(self):
		"""
		criar o local do gp.
		"""

		#criando os widgets
		frame = Frame(self)

		#criando a tree e o scroll
		self.treeGp = Treeview(frame, style = "data.Treeview")
		scroll = Scrollbar(frame, command = self.treeGp.yview, width = 22)
		self.treeGp.configure(yscrollcommand = scroll.set)

		#configurando as colunas
		self.treeGp["columns"] = ("id_data", "nome", "cargo", "gp")

		self.treeGp.heading("id_data", text = "id_data")
		self.treeGp.heading("nome", text = "nome")
		self.treeGp.heading("cargo", text = "cargo")
		self.treeGp.heading("gp", text = "gp")

		self.treeGp.column("#0", width = 0, stretch = False)
		self.treeGp.column("id_data", width = 0, stretch = False)
		self.treeGp.column("nome", width = 100 )
		self.treeGp.column("cargo", width = 60)
		self.treeGp.column("gp", width = 75)

		#posicionando
		frame.pack(side = "left", fill = "both", expand = True, padx = 5, pady = 5)
		self.treeGp.pack(side = "left", fill = "both", expand = True)
		scroll.pack(side = "left", fill = "y")

		#bind
		#instanciar ToplevelGp sempre que clicar 2x em cima de um jogador
		self.treeGp.bind("<Double-Button-1>", lambda event, parent = self: ToplevelGp(parent))

	def adicionarNovaData(self, dia, mes, ano):
		"""
		inserir a nova data na tabela.
		preencher a tabela gp.
		atualizar a tree que mostra a data.
		atualizar a tree que mostra o gp.
		"""

		#formatando a data para inserir no banco
		data = "/".join([ano, mes, dia])

		#inserindo na tabela data
		id_data = self.controle.createData(data)

		#preenchendo a tabela gp com todos os jogadores que estão na tabela jogadores
		for infoJogador in self.controle.readAllJogador():
			nome = infoJogador[1]
			cargo = infoJogador[2]
			gp = 0
			self.controle.createGp((id_data, nome, cargo, gp))
		self.updataTreeData()


	def removerData(self, *args):
		"""
		remover uma data do banco de dados.
		"""
		selecoes = self.treeData.selection()
		if selecoes:
			#percorer todas as selecoes
			for selecao in selecoes:
				#obtendo o idadata
				iddata = self.treeData.item(selecao)["values"][0]
				#deletando
				self.controle.deleteData(iddata)
			#atualizando self.treeData
			self.updataTreeData()
			self.treeGp.delete(*self.treeGp.get_children())
				

	def updataTreeData(self):
		"""
		atualizar self.treeGp
		"""

		self.treeData.delete(*self.treeData.get_children())

		for infoData in self.controle.readAllData():
			iddata = infoData[0]
			dataFormatada = "/".join([valor for valor in infoData[1].split("/")][::-1])
			self.treeData.insert("", "end", values = (iddata, dataFormatada))


	def updateTreeGp(self, *args):
		"""
		limpar treeGp e depois preencher com os dados atualizados.
		"""

		#obtendo id_data
		if self.treeData.selection():

			id_data = self.treeData.item(self.treeData.selection()[0])["values"][0]

			self.treeGp.delete(*self.treeGp.get_children())

			infoJogadores = self.controle.readAllGp(id_data)
			for infoJogador in infoJogadores:
				nome = infoJogador[2]
				cargo = infoJogador[3]
				gp = infoJogador[4]
				self.treeGp.insert("", "end", values = (id_data, nome, cargo, gp))


	def updateGpDoJogador(self, gp, id_data, nome):
		"""
		alterar o valor da coluna gp de um jogador.
		"""
		self.controle.updateGp((gp, id_data, nome))
		self.updateTreeGp()

class ToplevelData(Toplevel):

	"""
	abrir uma nova janela p/ definir a nova data.
	"""
	def __init__(self, parent, **kwargs):
		Toplevel.__init__(self, **kwargs)

		#importes
		from datetime import date

		#definindo o parent
		self.parent = parent

		#configurando a janela 
		x = self.parent.winfo_rootx()
		y = self.parent.winfo_rooty()
		self.geometry("650x220+{}+{}".format(x, y))
		self.title("Adicionar data")


		#criando os widgets
		frameDia = FrameComEntry(self, "Dia")
		frameMes = FrameComEntry(self, "Mês")
		frameAno = FrameComEntry(self, "Ano")

		self.labelAviso = Labelttk(self)

		button = Buttonttk(self, text = "Adicionar")

		#obtendo a data atual do sistema
		dataAtual = date.today()
		frameDia.setText(dataAtual.strftime("%d"))
		frameMes.setText(dataAtual.strftime("%m"))
		frameAno.setText(dataAtual.strftime("%Y"))

		#posicionando
		for F in (frameDia, frameMes, frameAno):
			F.pack(fill = "x", padx = 5, pady = 5)

		self.labelAviso.pack(padx = 5, pady = 5)
		button.pack(padx = 5, pady = 5)

		#command
		#chamar a função button click sempre que button for clicado.
		button["command"] = lambda: self.buttonClick(frameDia.getText().strip(), frameMes.getText().strip(), frameAno.getText().strip())


	def buttonClick(self, dia, mes, ano):
		"""
		validar a data p/ adicionar ao banco.
		"""
		from re import search, compile as reCompile

		#usar regEx p/ validar
		patterns = [
			reCompile("(^[0-9]{2}$)"), reCompile("(^[0-9]{2}$)"), reCompile("(^[0-9]{4}$)")
		]

		#percorrer todos os valores p/ verificar se estão válidos.
		valido = True
		for indice, valor in enumerate((dia, mes, ano)):
			if not search(patterns[indice], valor):
				valido = False
				break

		#se os campos estiverem Válidos.
		#eu chamo o método responsavel por adicionar a data ao banco de dados
		#atuzalir a tree
		if valido:
			self.parent.adicionarNovaData(dia, mes, ano)
			self.destroy()


		#se os campos estiverem Inválidos.
		else:
			self.setAviso("Campo inválido.")


	def setAviso(self, aviso):
		#definir o text de self.labelAviso
		self.labelAviso["text"] = aviso


class ToplevelGp:
	def __init__(self, parent):
		#verificar se tem um item selecionado
		if parent.treeGp.focus():

			self.parent = parent

			id_data = parent.treeGp.item(parent.treeGp.focus())["values"][0]
			nome = parent.treeGp.item(parent.treeGp.focus())["values"][1]
			gp = parent.treeGp.item(parent.treeGp.focus())["values"][3]

			#se tiver, é criado um toplevel p/ atualizar o gp do jogador(a)
			toplevel = Toplevel()
			toplevel.title("Atualizar gp")

			#geometria
			x = parent.winfo_rootx()
			y = parent.winfo_rooty()
			toplevel.geometry("650x150+{}+{}".format(x, y))

			#crinando os widgets
			frame = Frame(toplevel)
			label = Labelttk(frame, text = "Gp")
			entry = Entryttk(frame, font = (None, 18))
			entry.insert("end", gp)
			entry.focus()

			self.labelAviso = Labelttk(toplevel)
			button = Buttonttk(toplevel, text = "Atualizar")

			#posicionando
			frame.pack(fill = "x", padx = 5, pady = 5)
			label.pack(side = "left")
			entry.pack(side = "left", fill = "x", expand = True, padx = 2)
			self.labelAviso.pack(padx = 5, pady = 5)
			button.pack(padx = 5, pady = 5)

			#command
			button["command"] = lambda entry = entry, id_data = id_data, nome = nome: self.buttonClick(entry, id_data, nome)
			entry.bind("<Key>", lambda event: self.setAviso(""))


	def buttonClick(self, entry, id_data, nome):
		gp = entry.get()
		#validando o gp

		#tentando validar o gp
		try:

			gp = int(gp.strip())
			#chamando o método responsavel por atualizar o banco
			self.parent.updateGpDoJogador(gp, id_data, nome)
			self.setAviso("Atualizado.")

		#caso não seja valido o gp
		except ValueError as e:
			self.setAviso("Campos inválidos.")

	def setAviso(self, aviso):
		self.labelAviso["text"] = aviso


class FrameComEntry(Frame):
	"""
	um frame com um label e um entry.
	"""
	def __init__(self, parent, text, **kwargs):
		Frame.__init__(self, parent, **kwargs)

		self.parent = parent

		#criando os widgets
		label = Labelttk(self, width = 6, text = text)
		self.entry = Entryttk(self, font = (None, 18))

		#posicionando
		label.pack(side = "left", fill = "y")
		self.entry.pack(side = "left", fill = "x", expand = True)

		#bind
		#focar no entry sempre que for clicado 2x com o mouse em cima do label
		label.bind("<Double-Button-1>", lambda envet: self.entry.focus())

		#apagar a mensagem de aviso que está em self.parent
		self.entry.bind("<Key>", lambda event: self.parent.setAviso("") )


	def getText(self):
		#retornar o texto que esta em self.entry
		return self.entry.get()

	def setText(self, text):
		#definir o texto em self.entry
		self.entry.insert("end", text)

#################def main ###############################
def main():
	programa = Programa()
	programa.executar()

if __name__ == '__main__':
	main()

