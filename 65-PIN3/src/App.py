import tkinter as tk
import subprocess
import threading
import os
from solver import *

net = 'ow'
clean_all_configurations()

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.minsize(400, 300)
        self.title("Application")

        # Cria o frame da esquerda, que irá conter os radiobuttons para escolha do método
        self.left_frame = tk.Frame(self, width=250, padx=10)
        self.left_frame.pack(side="left", fill="both")

        # Cria o frame da direita, que irá conter os radiobuttons para escolha da opção
        self.right_frame = tk.Frame(self, width=250, padx=10)
        self.right_frame.pack(side="right", fill="both")

        # Cria o label que fica no frame da esquerda
        self.label_left = tk.Label(
            self.left_frame, text="Selecione uma instância:")
        self.label_left.pack(pady=(30, 10))

        # Cria o radiobutton "Rede OW" no frame da esquerda
        self.var_instance = tk.StringVar(value="Rede OW")
        self.radio_inst_ow = tk.Radiobutton(
            self.left_frame, text="Rede OW", variable=self.var_instance, value="Rede OW")
        self.radio_inst_ow.pack(anchor="w")

        # Cria o radiobutton "Rede ND" no frame da esquerda
        self.radio_inst_nd = tk.Radiobutton(
            self.left_frame, text="Rede ND", variable=self.var_instance, value="Rede ND")
        self.radio_inst_nd.pack(anchor="w")

        # Cria o label que fica no frame da direita
        self.label_right = tk.Label(
            self.right_frame, text="Selecione um método:")
        self.label_right.pack(pady=(30, 10))

        # Cria o radiobutton "Simple Local Search" no frame da direita
        self.var_method = tk.StringVar(value="Simple Local Search")
        self.radio_met_sls = tk.Radiobutton(
            self.right_frame, text="Simple Local Search", variable=self.var_method, value="Simple Local Search")
        self.radio_met_sls.pack(anchor="w")

        # Cria o radiobutton "Irace" no frame da direita
        self.radio_met_red = tk.Radiobutton(
            self.right_frame, text="Irace", variable=self.var_method, value="Irace")
        self.radio_met_red.pack(anchor="w")

        # Cria o radiobutton "Configurador" no frame da direita
        self.radio_met_red = tk.Radiobutton(
            self.right_frame, text="Configurador", variable=self.var_method, value="Configurador")
        self.radio_met_red.pack(anchor="w")

        # Cria o campo de texto 1 para o frame da esquerda
        self.textfield_left_label = tk.Label(
            self.left_frame, text="MaxExperiments:", anchor='w')
        self.textfield_left_label.pack(pady=(35, 10))
        self.textfield_left = tk.Entry(self.left_frame)
        self.textfield_left.pack()

        # Cria o campo de texto 2 para o frame da esquerda
        self.textfield_right_label = tk.Label(
            self.right_frame, text="Budget:", anchor='w')
        self.textfield_right_label.pack(pady=(10, 10))
        self.textfield_right = tk.Entry(self.right_frame)
        self.textfield_right.pack()

        # Cria o botão de confirmação para a janela
        self.confirm_button = tk.Button(
            self, text="Confirmar", command=self.confirm)
        self.confirm_button.pack(pady=(250, 10))

    def confirm(self):
        # Obtém as escolhas feitas pelo usuário
        maxExperiments = self.textfield_left.get()
        instance_choice = self.var_instance.get()
        method_choice = self.var_method.get()
        budget = self.textfield_right.get()

        # Cria uma nova janela de confirmação
        confirm_window = tk.Toplevel(self.master)
        confirm_window.title("Confirmação")
        confirm_window.minsize(275, 200)

        # Adiciona uma mensagem na nova janela de confirmação
        message = f"Deseja confirmar as opções selecionadas?\n\n"
        message += f"Método: {instance_choice}\nOpção: {method_choice}\n\n"
        if maxExperiments:
            message += f"MaxExperiments: {maxExperiments}\n"
        if budget:
            message += f"Budget: {budget}\n"
        message_label = tk.Label(confirm_window, text=message)
        message_label.pack(pady=20)

        # Adiciona um botão de confirmação na nova janela de confirmação
        confirm_button = tk.Button(
            confirm_window, text="Confirmar", command=lambda: self.on_confirm(confirm_window))
        confirm_button.pack(side="left", padx=(10, 0), pady=(0, 10))

        # Adiciona um botão de cancelamento na nova janela de confirmação
        cancel_button = tk.Button(
            confirm_window, text="Cancelar", command=confirm_window.destroy)
        cancel_button.pack(side="right", padx=(0, 10), pady=(0, 10))

    def on_confirm(self, confirm_window):
        # Close the confirmation window
        confirm_window.destroy()

        # Open the selected options window
        result_window = tk.Toplevel(self.master)
        result_window.title("Resultados: ")

        # Get the selected options
        method = self.var_instance.get()
        option = self.var_method.get()

        if method == 'Rede OW':
            net = 'ow'
        else:
            net = 'nd'

        if option == 'Irace':
            result = self.run_irace(result_window, net)
            self.display_result(result_window, result)
        elif option == 'sla':
            result = self.run_sla()
            self.display_result(result_window, result)

    def run_irace(self, result_window, net):
        # Navigate to the desired folder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        target_dir = os.path.join(
            current_dir, "..", "src", "irace_files", net)
        os.chdir(target_dir)

        # Capture the output of irace for later display
        process = subprocess.Popen(
            ['irace'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        output, _ = process.communicate()
        result = output.decode("utf-8")

        # Create the console window
        console_window = tk.Toplevel(self.master)
        console_window.title("Console do irace")

        # Create a Text widget to display the output of irace
        console_text = tk.Text(console_window)
        console_text.pack(fill=tk.BOTH, expand=True)

        # Redirect the output of irace to the Text widget
        def redirect_output():
            console_text.insert(tk.END, result)
            console_text.see(tk.END)
            console_text.update_idletasks()

        # Start the redirect thread
        redirect_thread = threading.Thread(target=redirect_output)
        redirect_thread.start()

        return result

    def display_result(self, result_window, result):
        result_text = str(get_all_elites_params(net))
        result_label = tk.Label(result_window, text=result_text)
        result_label.pack()



if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()
