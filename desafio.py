import tkinter as tk
from tkinter import ttk, simpledialog
from tkinter import messagebox
from ttkthemes import ThemedStyle

class CaixaEletronico:
    def __init__(self, root):
        self.saldo = 0
        self.limite = 500
        self.extrato = ""
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3

        self.menu = """
        [d] Depositar
        [s] Sacar
        [e] Extrato
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

    def executar_operacao(self):
        opcao = self.opcao_entry.get()

        if opcao == "d":
            self.depositar()

        elif opcao == "s":
            self.sacar()

        elif opcao == "e":
            self.exibir_extrato()

        elif opcao == "q":
            self.root.destroy()

        else:
            messagebox.showinfo("Erro", "Operação inválida, por favor selecione novamente a operação desejada")

    def depositar(self):
        valor_str = simpledialog.askstring("Depósito", "Informe o valor do depósito:")
        try:
            valor = float(valor_str)
            if valor > 0:
                self.saldo += valor
                self.extrato += f"Depósito: R$ {valor:.2f}\n"
                self.atualizar_saldo_label()
            else:
                messagebox.showinfo("Erro", "Operação falhou! O valor informado é inválido.")
        except ValueError:
            messagebox.showinfo("Erro", "Operação falhou! O valor informado é inválido.")

    def sacar(self):
        valor_str = simpledialog.askstring("Saque", "Informe o valor do saque:")
        try:
            valor = float(valor_str)

            excedeu_saldo = valor > self.saldo
            excedeu_limite = valor > self.limite
            excedeu_saque = self.numero_saques >= self.LIMITE_SAQUES

            if excedeu_saldo:
                messagebox.showinfo("Erro", "Saldo Insuficiente.")

            elif excedeu_limite:
                messagebox.showinfo("Erro", "Valor do saque excede o limite disponível.")

            elif excedeu_saque:
                messagebox.showinfo("Erro", "Número máximo de saques excedido.")

            elif valor > 0:
                self.saldo -= valor
                self.extrato += f"Saque: R$ {valor:.2f}\n"
                self.numero_saques += 1
                self.atualizar_saldo_label()
            else:
                messagebox.showinfo("Erro", "Operação falhou! O valor informado é inválido.")
        except ValueError:
            messagebox.showinfo("Erro", "Operação falhou! O valor informado é inválido.")

    def exibir_extrato(self):
        messagebox.showinfo("Extrato", "Não foram realizadas movimentações." if not self.extrato else self.extrato)

    def atualizar_saldo_label(self):
        self.saldo_label.config(text=f"Saldo: R$ {self.saldo:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    caixa_eletronico = CaixaEletronico(root)
    root.mainloop()
