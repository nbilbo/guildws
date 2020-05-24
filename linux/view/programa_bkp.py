#-*- coding: utf-8 -*-

from tkinter import Tk, Frame, Label, Menu, Scrollbar, Toplevel, Entry, Button, StringVar, OptionMenu
from tkinter.messagebox import showinfo
from tkinter.ttk import Treeview, Style, Button as Buttonttk, Label as Labelttk, Entry as Entryttk, OptionMenu as OptionMenuttk
#pasta onde está a classe responsavel por acessar o banco de dados.
from sys import path
path.append(r"../control")
from controle import Controle


class Programa(Tk):
	"""
	Responsavel pro criar a parte grafica.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.controle = Controle()
		self.createMenubar()
		self.createContainer()
		
	def createMenubar(self):
		menubar = Menu()
		self.config(menu = menubar)

		menubarMenu = Menu(menubar, tearoff = 0)
		menubarMenu.add_command(label = "Jogador", command = lambda: self.setFrame("ListaJogador"))
		menubarMenu.add_command(label = "Pontos de guild", command = lambda: self.setFrame("ListaPontosDeGuild"))

		menubar.add_cascade(label = "Menu", menu = menubarMenu)
		menubar.add_command(label = "Sobre", command = lambda: showinfo(title = "Sobre", message = "Um programa para auxiliar os jogadores.\nSem fins lucraticos."))

	def createContainer(self):
		container = Frame(self, bg = "blue")
		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		self.frames = {}
		for f in (ListaJogador, ListaPontosDeGuild):
			name = f.__name__
			frame = f(container, self.controle)
			frame.grid(row = 0, column = 0, sticky = "nsew")
			self.frames[name] = frame

		#definindo a tela inicial
		self.setFrame('ListaJogador')
		container.pack(side="top", fill = "both", expand = True, padx = 5, pady = 5)

	def setFrame(self, frame_name):
		self.frames[frame_name].tkraise()
	
	def executar(self):
		self.geometry("650x400")
		self.resizable(0, 0)
		self.title("1.0")
		self.mainloop()


class ListaJogador(Frame):
	def __init__(self, parent, controle, **kwargs ):
		super().__init__(parent, **kwargs)
		self.controle = controle
		self.createTree()
		self.createButton()
		self.updateTree()
	
	def createTree(self):
		#crinando os widgets

		#frame onde ficara a tree
		frame = Frame(self, bg = "green", height = 300, width = 300)
		style = Style()
		style.configure("mystyle.Treeview", font = (None, 12))
		style.configure("mystyle.Treeview.Heading", font = (None, 12))
		self.tree = Treeview(frame, style = "mystyle.Treeview")
		scroll = Scrollbar(frame)

		#'vinculando' tree com o scroll
		self.tree.configure(yscrollcommand = scroll.set)
		scroll.configure(command = self.tree.yview)

		#configurando a tree
		self.tree["columns"] = ("nome", "cargo")

		self.tree.heading("nome", text = "Nome")
		self.tree.heading("cargo", text = "Cargo")

		self.tree.column("#0", stretch = False, minwidth = 0, width = 0)
		
		#posicionando
		frame.pack(fill = "both", expand = True, padx = 5, pady = 5)
		frame.pack_propagate(False)
		self.tree.pack(side = "left", fill = "both", expand = True)
		scroll.pack(side = "left", fill = "y")

		#bind
		#chamar o método updateJogador, sempre que for clicado 2x em cima de um item da tree.
		self.tree.bind("<Double-Button-1>", self.updateJogador)

	def createButton(self):
		#criando os widgets button
		style = Style()
		style.configure("mystyle.TButton", font = (None, 11))
		buttonAdicionar = Buttonttk(self, text = "Adicionar", width = 10, style = "mystyle.TButton", command = self.buttonAdicionarClick)
		buttonRemover = Buttonttk(self, text = "Remover", width = 10, style = "mystyle.TButton", command = self.buttonRemoverClick)

		#posicionando
		buttonAdicionar.pack(side = "left", padx = 5, pady = 5)
		buttonRemover.pack(side = "right", padx = 5, pady = 5)

	def buttonAdicionarClick(self):
		#abrir uma nova janela p/ definir o nome e o cargo do novo jogador.

		def clearLabelAviso(event):
			#limpar o text de labelAviso sempre que algo começar a ser digitado em entryNome
			nonlocal labelAviso

			if labelAviso["text"].strip():
				labelAviso["text"] = ""

		def buttonConfirmarClick():
			#inserir os dados ao banco de dados e atualizar a tree
			#usando o nonlocal para evitar ter que passar muitos parametros nessa função
			nonlocal entryNome, stringOpcao, dicionarioOpcoes, tree, controle, labelAviso

			nome = entryNome.get().lower()
			cargo = dicionarioOpcoes[stringOpcao.get()]
			
			#verificar se foi digitado algo
			if nome.strip():

				#verificar se possui repetição de nomes
				#se nao existir, inserir no banco.
				try:
					jaExiste = controle.readJogadorNome(nome)
					if jaExiste:
						labelAviso["text"]="usuario ja existe."

					else:
						dados = (nome, cargo)
						#inserindo os dados ao banco
						controle.createJogador(dados)
						#atualizando a tree
						self.updateTree()
						#limpando o campo de entrada do nome
						entryNome.delete(0, "end")
						#atualizando o label aviso
						labelAviso["text"] = "Inserido com sucesso."
						entryNome.focus()

				except Exception as e:
					print(e)

			#se o botão for clicado e campo do nome estiver em branco
			else:
				labelAviso["text"] = "Campo vazio."
			
		#criando os widgets
		style = Style()
		style.configure("TLabel", font = (None, 14))
		style.configure("TMenubutton", font = (None, 13))

		novaJanela = Toplevel()
		novaJanela.geometry(f"500x100+{self.winfo_rootx()}+{self.winfo_rooty()}")
		novaJanela.title("Adicionar jogador")


		frameTop = Frame(novaJanela, height = 20, bg = 'red')
		labelNome = Labelttk(frameTop, text = "Nome")
		entryNome = Entryttk(frameTop, font = (None, 12))
		entryNome.focus()

		#apenas para 'encontrar' essas variaveis dentro da função buttonConfirmClick
		tree = self.tree 
		controle = self.controle

		#criando o menu de opcoes
		dicionarioOpcoes = {
		"novato":1, "explorador": 2, "herdeiro": 3, "lider": 4
		}
		listaOpcoes = [opcao for opcao in dicionarioOpcoes.keys()]
		stringOpcao = StringVar()
		
		menuOpcao = OptionMenuttk(frameTop, stringOpcao, listaOpcoes[0], *listaOpcoes)
		menuOpcao["width"] = 10
		
		labelAviso = Labelttk(novaJanela)
		buttonConfirmar = Buttonttk(novaJanela, text = "Confirmar", width = 10, style = "mystyle.TButton", command = buttonConfirmarClick)
		
		#posicionando
		frameTop.pack(fill = "x", expand = True, anchor = "nw", padx = 5, pady = 5)
		labelNome.pack(side = "left", fill = "y")
		entryNome.pack(side = "left", fill = "both", expand = True)
		menuOpcao.pack()

		labelAviso.pack(padx = 5, pady = 5)
		buttonConfirmar.pack(padx = 5, pady = 5)

		#bind
		entryNome.bind("<Key>", clearLabelAviso)

	def buttonRemoverClick(self):
		#remover os jogadores selecionados na tree.

		jogadores = self.tree.selection()
		if jogadores:
			for jogador in jogadores:
				idjogador = self.tree.item(jogador)["text"]
				self.controle.deleteJogador(idjogador)
			self.updateTree()

	def updateJogador(self, event):
		#abrir uma nova janela p/ atualizar os dados do jogador

		def clearLabelAviso(event):
			#limpar o text de labelAviso

			#usando o nonlocal p/ evitar ter que passar por paramentro
			nonlocal labelAviso

			if labelAviso["text"]:
				labelAviso["text"] = ""

		def buttonAtualizarClick(*args):
			#usando o nonlocal p/ evitar ter que passar muitos paramentros 
			nonlocal labelAviso, entryNome, dicionarioOpcoes, stringOpcao, idjogador

			#caso o campo do nome esteja valido
			if entryNome.get().strip():
				nomeAntigo = self.controle.readJogadorId(idjogador)[0][1]
				nome = entryNome.get().lower()
				cargo = dicionarioOpcoes[stringOpcao.get()]

				#atualizando o banco com os novos valores
				valores = (nome, cargo, idjogador)
				try:
					if self.controle.updateJogador(valores):
						self.updateTree()
						self.controle.triggerUpdateJogador(idjogador, nomeAntigo)

						labelAviso["text"] = "Atualizado."
						entryNome.focus()

				except Exception as e:
					print(e)
				

			#caso o campo do nome esteja invalido
			else:
				labelAviso["text"] = "Campo vazio."


		#1-> obter os dados do jogador a ser atualizado
		atual = self.tree.focus()

		if atual:
			valores = self.tree.item(atual)["values"]
			idjogador = self.tree.item(atual)["text"]
			nome = valores[0]
			cargo = valores[1]
			
			#criando os widgets
			novaJanela = Toplevel()
			novaJanela.geometry(f"500x100+{self.winfo_rootx()}+{self.winfo_rooty()}")
			novaJanela.title("Atualizar jogador")

			style = Style()
			style.configure("TLabel", font = (None, 14))
			style.configure("TMenubutton", font = (None, 13))

			frameTop = Frame(novaJanela, height = 20)	
			labelNome = Labelttk(frameTop, text = "Nome")	
			entryNome = Entryttk(frameTop, font = (None, 12))
			entryNome.insert("end", nome)
			entryNome.focus()

			#criando o menu de opcoes
			dicionarioOpcoes = {
			"novato": 1, "explorador": 2, "herdeiro": 3, "lider":4
			}
			listaOpcoes = [opcao for opcao in dicionarioOpcoes.keys()]
			stringOpcao = StringVar()
			stringOpcao.set(cargo)
			menuOpcao = OptionMenuttk(frameTop, stringOpcao, cargo, *listaOpcoes)
			menuOpcao["width"] = 10

			labelAviso = Labelttk(novaJanela)
			buttonAtualizar = Buttonttk(novaJanela, text = "atualizar", width = 10, style = "mystyle.TButton")
			buttonAtualizar["command"] = buttonAtualizarClick

			#posicionando
			frameTop.pack(fill = "x", expand = True, anchor = "nw", padx = 5, pady = 5)
			labelNome.pack(side = "left", fill = "y")
			entryNome.pack(side = "left", fill = "both", expand = True)
			menuOpcao.pack(side = "left")

			labelAviso.pack(padx = 5, pady = 5)
			buttonAtualizar.pack(padx = 5, pady = 5)

			#bind
			entryNome.bind("<Key>", clearLabelAviso)

	def updateTree(self):
		#remover todos os dados da tree.
		self.tree.delete(*self.tree.get_children())
		#adicionar todos os dados do banco.
		todosJogadores = self.controle.readAllJogador()
		for jogador in todosJogadores:
			id = jogador[0]
			nome = jogador[1]
			cargo = jogador[2]
			self.tree.insert("", "end", text = id, values = (nome, cargo))


class ListaPontosDeGuild(Frame):
	#criar uma janela com um local p/ mostrar a data e outro local p/ mostrar o gp dos jogadores.
	def __init__(self, parent, controle, **kwargs):
		super().__init__(parent, **kwargs)
		self.controle = controle
		self.createListaData()
		self.createListaGp()
		self.updateTreeData()
		
	def createListaData(self):
		#criar o frame onde vai ficar a lista de datas e os botoes de adicionar e remover

		style = Style()
		style.configure("TButton", font = (None, 11, "bold"))
		style.configure("Treeview", font = (None, 11))
		style.configure("Treeview.Heading", font = (None, 12))

		#criando os frame
		mainFrame = Frame(self, width = 200)
		subFrame = Frame(mainFrame)

		#criando e configurando a tree e o scroll
		self.treeData = Treeview(subFrame)
		scroll = Scrollbar(subFrame, command = self.treeData.yview)
		self.treeData.configure(yscrollcommand = scroll.set)

		#configurando a tree e suas colunas
		self.treeData["columns"] = ("id", "data")

		self.treeData.heading("data", text = "Data")

		self.treeData.column("#0", width = 0, stretch = False)
		self.treeData.column("id", width = 0, stretch = False)
		self.treeData.column("data", minwidth = 185, width = 185, stretch = False)

		#criando os botoes
		buttonAdicionar = Buttonttk(mainFrame, text = "+", command = self.buttonAdicionarClick)
		buttonRemover = Buttonttk(mainFrame, text = "-", command = self.buttonRemoverClick)

		#posicioando
		mainFrame.pack(side = "left", fill = "y", padx = 5, pady = 5)
		mainFrame.pack_propagate(False)

		subFrame.pack(fill = "both", expand = True)
		subFrame.pack_propagate(False)

		self.treeData.pack(side = "left", fill = "both", expand = True )
		scroll.pack(side = "left", fill = "y")

		buttonAdicionar.pack(side = "left", fill = "both", expand = True, padx = 5, pady = 5 )
		buttonRemover.pack(side = "left", fill = "both", expand = True, padx = 5, pady = 5)

		#bind
		#chamar o metodo updateTreeGp sempre que for clicado 2x em cima de uma data.
		self.treeData.bind("<Double-Button-1>", self.updateTreeGp)

	def createListaGp(self):
		#criar os widgets de onde vai mostrar o gp dos jogadores.

		def definirGp(event):
			#abrir uma nova janela p/ definir a quantidade de gp do jogador

			def clearLabelAviso(event):
				#limpar o text de labelAviso sempre que for digitado algo em entryGp
				nonlocal labelAviso

				if labelAviso["text"]:
					labelAviso["text"] = ""

			def buttonConfirmarClick(*args):
				#usando o nonlocal p/ evitar ter que passar muitos argumentos
				nonlocal entryGp, labelAviso, id_data, nome, novaJanela

				#varificar se é um gp valido.
				if entryGp.get().strip().isnumeric() and int(entryGp.get()) >= 0:
					#atualizar o banco de dados e a treeGp.
					valores = (
						int(entryGp.get()), id_data, nome
					)
					#atualizando o banco.
					self.controle.updateGp(valores)
					#atualizando a treeGp.
					self.clearTreeGp()
					self.updateTreeGp()
					novaJanela.destroy()

				#se nao for um gp válido.
				else:
					labelAviso["text"] = "Campo invalido."

			if self.treeGp.focus() and self.treeData.focus():
				#dados atuais
				id_data = self.treeData.item(self.treeData.focus())["values"][0]
				nome = self.treeGp.item(self.treeGp.focus())["values"][0]
				gpAtual = self.treeGp.item(self.treeGp.focus())["values"][2]
				
				#criando a nova janela
				novaJanela = Toplevel()
				novaJanela.geometry(f"300x100+{self.winfo_rootx()}+{self.winfo_rooty()}")
				novaJanela.title("Atualizar gp")

				#criando os widgets da janela
				style = Style()
				style.configure("TLabel", font = (None, 12))

				frameTop = Frame(novaJanela)
				label = Labelttk(frameTop, text = "Gp")
				entryGp = Entryttk(frameTop, font = (None, 12))
				entryGp.insert("end", str(gpAtual))
				entryGp.focus()

				labelAviso = Labelttk(novaJanela, text = "")
				buttonConfirmar = Buttonttk(novaJanela, text = "Confirmar", command = buttonConfirmarClick)

				#posicianando
				frameTop.pack(fill = "x", padx = 5, pady = 5)
				label.pack(side = "left", fill = "y", padx = 5 )
				entryGp.pack(side = "left", fill = "both", expand = True)

				labelAviso.pack(padx = 5, pady = 5)
				buttonConfirmar.pack(padx = 5, pady = 5)

				#bind
				label.bind("<Double-Button-1>", lambda event: entryGp.focus() )
				entryGp.bind("<Key>", clearLabelAviso)

		#crinando os frame
		mainFrame = Frame(self, bg = "red")

		#crinando a treeGp e o scroll
		style = Style()
		style.configure("Treeview", font = (None, 11, "bold"))
		self.treeGp = Treeview(mainFrame)
		scroll = Scrollbar(mainFrame, command = self.treeGp.yview)
		self.treeGp.configure(yscrollcommand = scroll.set)

		#configurando as colunas da treeGp
		self.treeGp["columns"] = ("nome", "cargo", "gp")

		self.treeGp.heading("nome", text = "Nome")
		self.treeGp.heading("cargo", text =  "Cargo")
		self.treeGp.heading("gp", text = "Gp")

		self.treeGp.column("#0", width = 0, stretch = False)
		self.treeGp.column("nome", minwidth = 150, width = 150, stretch = False)
		self.treeGp.column("cargo", minwidth = 150, width = 150, stretch = False)
		self.treeGp.column("gp", minwidth = 105, width = 105, stretch = False)

		#posicionando
		mainFrame.pack(side = "left", fill = "both", expand = True, padx = 5, pady = 5)
		mainFrame.pack_propagate(False)

		self.treeGp.pack(side = "left", fill = "both", expand = True)
		scroll.pack(side = "left", fill = "y")

		#bind
		self.treeGp.bind("<Double-Button-1>", definirGp)

	def buttonAdicionarClick(self):
		#criar uma nova janela onde deve ser inserido a data.
		from datetime import date

		def clearLabelAviso(event):
			#limpar o texto de labelAviso sempre que for digitado algo
			nonlocal labelAviso

			if labelAviso["text"]:
				labelAviso["text"] = ""

		def buttonConfirmarClick():
			from re import search, compile as reCompile

			nonlocal frameDia, frameMes, frameAno, novaJanela

			dia = frameDia.entry.get()
			mes = frameMes.entry.get()
			ano = frameAno.entry.get()

			#verificar se os campos são validos
			patterns = [
				reCompile("^[0-9]{2}$"), reCompile("^[0-9]{2}$"), reCompile("^[0-9]{4}$")
			]
			valido = True
			for indice, valor in enumerate((dia, mes, ano)):
				if not search(patterns[indice], valor):
					valido = False
					labelAviso["text"] = "Campo invalido."
					break
			#se os campos estiverem validos
			#formatar para poder adicioanr ao banco
			#adicionar ao banco
			#atualizar a tabela 'gp' do banco de dados.
			#atualizar o treeData
			#destruir a janela
			if valido:
				valores = (f"{ano}/{mes}/{dia}")
				id_data = self.controle.createData(valores)

				#aqui que irei atualizar a tabela gp
				#preencher a tebela 'gp' com todos os jogades que estão na tabela 'jogador' e definir o valor da coluna 'gp' em zero.
				#confuso né? sorry
				for tuplaJogador in self.controle.readAllJogador():
					#tuplaJogador[1] se refere a coluna 'nome' da tabela 'v_jogador'
					#tuplaJogador[2] se refere a coluna 'cargo' da tabela 'v_jogador'
					valores = (id_data, tuplaJogador[1], tuplaJogador[2], 0)
					self.controle.createGp(valores)

				self.updateTreeData()
				novaJanela.destroy()
				
		novaJanela = Toplevel()
		novaJanela.geometry(f"300x150+{self.winfo_rootx()}+{self.winfo_rooty()}")
		novaJanela.title("Adicionar data")

		

		#criando os campos de entrada de dados
		frameDia = NormalEntry(novaJanela, text = "Dia")
		frameMes = NormalEntry(novaJanela, text = "Mês")
		frameAno = NormalEntry(novaJanela, text = "Ano")

		#atualizando os valores com a data atual do sistema
		dataAtual = date.today()
		frameDia.entry.insert("end", dataAtual.strftime("%d"))
		frameMes.entry.insert("end", dataAtual.strftime("%m"))
		frameAno.entry.insert("end", dataAtual.strftime("%Y"))

		#label de aviso
		labelAviso = Labelttk(novaJanela, text = "")

		#buttonConfirmar
		buttonConfirmar = Buttonttk(novaJanela, text = "Confirmar", width = 10, command = buttonConfirmarClick)

		#posicionando
		frameDia.posicionar()
		frameMes.posicionar()
		frameAno.posicionar()

		labelAviso.pack(padx = 5, pady = 5)
		buttonConfirmar.pack(padx = 5, pady = 5)

		#bind
		#limpar o texto de labelAviso sempre que for digitado algo
		for f in (frameDia, frameMes, frameAno):
			f.entry.bind("<Key>", clearLabelAviso)

	def buttonRemoverClick(self):
		#remover as datas selecionadas na treeData
		#atualizar a treeData
		datas = self.treeData.selection()
		if datas:
			for data in datas:
				values = self.treeData.item(data)["values"]
				iddata = values[0]
				self.controle.deleteData(iddata)
			self.updateTreeData()
			self.clearTreeGp()

	def updateTreeData(self):
		#apagar todos os dados da tree
		#adicionar a tree os dados que estão no banco de dados
		self.treeData.delete(*self.treeData.get_children())
		datas = self.controle.readAllData()
		for resultado in datas:
			iddata = resultado[0]
			dataFormatada ="/".join([valor for valor in resultado[1].split("/")][::-1])
			self.treeData.insert("", "end", values = (iddata, dataFormatada))			

	def updateTreeGp(self, *args):
		#atualizar self.treeGp
		atual = self.treeData.focus()
		if atual:
			iddata = self.treeData.item(atual)["values"][0]
			valores = self.controle.readAllGp(iddata)
			self.clearTreeGp()
			if valores:
				
				for valor in valores:
					nome = valor[2]
					cargo = valor[3]
					gp = valor[4]
					self.treeGp.insert("", "end", values = (nome, cargo, gp))

	def clearTreeGp(self):
		self.treeGp.delete(*self.treeGp.get_children())
			

#Um frame com um label e um entry
class NormalEntry(Frame):
	def __init__(self, parent, text = "Label", **kwargs):
		from datetime import date

		super().__init__(parent, **kwargs)
		self["background"] = "blue"
		self["width"] = 250
		self["height"] = 20
		self.pack_propagate(False)

		style = Style()
		style.configure("TLabel", font = (None, 11, "bold"))

		label = Labelttk(self, text = text)
		label["width"] = 6
		self.entry = Entryttk(self, font = (None, 11))


		label.pack(side = "left", fill = "y")
		self.entry.pack(side = "left", fill = "both", expand = True)

		#bind
		#focar o entry sempre que for clicado com o mouse em cima do label
		label.bind("<ButtonRelease-1>", lambda event: entry.focus())

	def posicionar(self):
		self.pack(side = "top", fill = "x", expand = False, anchor = "n", padx = 5, pady = 5)



def main():
	programa = Programa()
	programa.executar()

if __name__ == '__main__':
	main()
