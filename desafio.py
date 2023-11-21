import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from ttkthemes import ThemedStyle


class CaixaEletronico:
    def __init__(self, root):
        self.saldo = 0
        self.limite = 500
        self.extrato = ""
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3
        self.usuarios = {}

        self.menu = """
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [c] Cadastrar Usuário
        [a] Cadastrar Conta Bancária
        [q] Sair

        => """

        self.root = root
        self.root.title("Caixa Eletrônico")

        style = ThemedStyle(root)
        style.set_theme("plastik")

        self.saldo_label = ttk.Label(root, text="Saldo: R$ 0.00", style="TLabel")
        self.saldo_label.pack(pady=10)

        self.opcao_entry = ttk.Entry(root, width=30)
        self.opcao_entry.pack(pady=10)

        self.executar_button = ttk.Button(root, text="Executar", command=self.executar_operacao)
        self.executar_button.pack(pady=10)

        # Configurando a geometria da janela principal
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.4)
        window_height = int(screen_height * 0.4)
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def executar_operacao(self):
        opcao = self.opcao_entry.get()

        if opcao == "d":
            self.depositar()
        elif opcao == "s":
            self.sacar()
        elif opcao == "e":
            self.exibir_extrato()
        elif opcao == "c":
            self.cadastrar_usuario()
        elif opcao == "a":
            self.cadastrar_conta()
        elif opcao == "q":
            self.root.destroy()
        else:
            messagebox.showinfo("Erro", "Operação inválida, por favor selecione novamente a operação desejada")

    def depositar(self):
        nome = simpledialog.askstring("Depósito", "Informe o nome do usuário:")
        if nome in self.usuarios:
            valor_str = simpledialog.askstring("Depósito", "Informe o valor do depósito:")
            try:
                valor = float(valor_str)
                if valor > 0:
                    self.usuarios[nome]["saldo"] += valor
                    self.usuarios[nome]["extrato"] += f"Depósito: R$ {valor:.2f}\n"
                    self.atualizar_saldo_label()
                else:
                    messagebox.showinfo("Erro", "Operação falhou! O valor informado é inválido.")
            except ValueError:
                messagebox.showinfo("Erro", "Operação falhou! O valor informado é inválido.")
        else:
            messagebox.showinfo("Erro", "Usuário não cadastrado. Por favor, cadastre o usuário antes de realizar operações.")

    def sacar(self):
        nome = simpledialog.askstring("Saque", "Informe o nome do usuário:")
        if nome in self.usuarios:
            valor_str = simpledialog.askstring("Saque", "Informe o valor do saque:")
            try:
                valor = float(valor_str)

                excedeu_saldo = valor > self.usuarios[nome]["saldo"]
                excedeu_limite = valor > self.limite
                excedeu_saque = self.usuarios[nome]["saques"] >= self.LIMITE_SAQUES

                if excedeu_saldo:
                    messagebox.showinfo("Erro", "Saldo Insuficiente.")

                elif excedeu_limite:
                    messagebox.showinfo("Erro", "Valor do saque excede o limite disponível.")

                elif excedeu_saque:
                    messagebox.showinfo("Erro", "Número máximo de saques excedido.")

                elif valor > 0:
                    self.usuarios[nome]["saldo"] -= valor
                    self.usuarios[nome]["extrato"] += f"Saque: R$ {valor:.2f}\n"
                    self.usuarios[nome]["saques"] += 1
                    self.atualizar_saldo_label()
                else:
                    messagebox.showinfo("Erro", "Operação falhou! O valor informado é inválido.")
            except ValueError:
                messagebox.showinfo("Erro", "Operação falhou! O valor informado é inválido.")
        else:
            messagebox.showinfo("Erro", "Usuário não cadastrado. Por favor, cadastre o usuário antes de realizar operações.")

    def exibir_extrato(self):
        nome = simpledialog.askstring("Extrato", "Informe o nome do usuário:")
        if nome in self.usuarios:
            messagebox.showinfo("Extrato", "Não foram realizadas movimentações." if not self.usuarios[nome]["extrato"] else self.usuarios[nome]["extrato"])
        else:
            messagebox.showinfo("Erro", "Usuário não cadastrado. Por favor, cadastre o usuário antes de realizar operações.")

    def cadastrar_usuario(self):
        nome = simpledialog.askstring("Cadastro de Usuário", "Informe o nome do usuário:")
        cpf = simpledialog.askstring("Cadastro de Usuário", "Informe o CPF do usuário:")
        telefone = simpledialog.askstring("Cadastro de Usuário", "Informe o telefone do usuário:")
        if nome and cpf and telefone:
            self.usuarios[nome] = {"saldo": 0, "limite": 500, "extrato": "", "saques": 0, "cpf": cpf, "telefone": telefone}
            messagebox.showinfo("Cadastro de Usuário", f"Usuário {nome} cadastrado com sucesso!")

    def cadastrar_conta(self):
        nome = simpledialog.askstring("Cadastro de Conta Bancária", "Informe o nome do usuário para cadastrar a conta:")
        if nome in self.usuarios:
            conta = simpledialog.askstring("Cadastro de Conta Bancária", "Informe o número da conta:")
            if conta:
                self.usuarios[nome]["conta"] = conta
                messagebox.showinfo("Cadastro de Conta Bancária", f"Conta {conta} cadastrada para o usuário {nome}")
            else:
                messagebox.showinfo("Erro", "Operação falhou! Número da conta inválido.")
        else:
            messagebox.showinfo("Erro", "Operação falhou! Usuário não encontrado.")

    def atualizar_saldo_label(self):
        self.saldo_label.config(text=f"Saldo: R$ {self.usuarios['nome']['saldo']:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    caixa_eletronico = CaixaEletronico(root)
    root.mainloop()
