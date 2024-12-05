#!/usr/bin/env python3

from typing import Dict, Callable
from kivymd.app import MDApp
from base64 import b64decode
from kivy.core.image import Image as CoreImage
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemHeadlineText,
    MDListItemSupportingText,
)
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)
from kivymd.uix.button import MDButton, MDButtonText
from subprocess import run, CalledProcessError
from os import chdir, chdir, path, devnull
import sys
import tempfile
from kivy.config import Config
import icon

Config.set("graphics", "resizable", False)

sys.stdout = open(devnull, 'w')
sys.stderr = open(devnull, 'w')


temperaturas: Dict[int, str] = {
    1700: "Match flame, low pressure sodium lamps (LPS/SOX)",
    1850: "Candle flame, sunset/sunrise",
    2400: "Standard incandescent lamps",
    2550: "Soft white incandescent lamps",
    2700: "Soft white compact fluorescent and LED lamps",
    3000: "Warm white compact fluorescent and LED lamps",
    3200: "Studio lamps, photofloods",
    3350: "Studio 'CP' light",
    4100: "Horizon daylight",
    5000: "Tubular fluorescent or daylight compact fluorescent lamps (CFL)",
    6500: "LCD or CRT screen",
    15000: "Clear blue poleward sky",
}

class BlueToneApp(MDApp):
    dialog: MDDialog

    def build(self) -> MDScreen:
        self.title = "BlueTone"
        icon_data = b64decode(icon.base64_icon)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(icon_data)
            temp_icon_path = temp_file.name
        
        self.icon = temp_icon_path
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        screen: MDScreen = MDScreen()
        if not self.verificar_xsct_instalado():
            self.mostrar_dialogo_instalacao()
        else:
            self.criar_alias_e_mover_app()
            self.adicionar_lista_temperaturas(screen)

        return screen

    def verificar_xsct_instalado(self) -> bool:
        try:
            run(["xsct"], capture_output=True, text=True, check=True)
            return True
        except FileNotFoundError:
            return False

    def instalar_xsct(self, instance=None) -> None:   
        self.senha_input = MDTextField(
            hint_text="Senha sudo",
            password=True,
            multiline=False,
            size_hint=(1, None),
            height=40,
        )
        
        self.dialog = MDDialog(
            MDDialogHeadlineText(
                text="Diretório 'sct' já existe",
            ),
            MDDialogSupportingText(
                text=(
                    "O diretório 'sct' já existe. Deseja sobrescrevê-lo ou continuar com a versão existente?"
                ),
            ),
            MDDialogContentContainer(
                MDLabel(
                    text="Por favor, insira sua senha sudo para continuar a instalação.",
                    halign="center"
                ),
                self.senha_input,
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(
                        text="Instalar",
                    ),
                    on_release=self.realizar_instalacao,
                ),
                MDButton(
                    MDButtonText(
                        text="Usar versão existente",
                    ),
                    on_release=self.continuar_com_existente,
                ),
                spacing="8dp",
            ),
        )
        self.dialog.open()
            
    def continuar_com_existente(self, instance=None) -> None:
        try:
            if path.exists("sct"):
                chdir("sct")
                run(["make"], check=True)
                run(["sudo", "make", "install"], check=True)
                print("xsct já está instalado.")
                self.dialog.dismiss()
                self.root.clear_widgets()
                self.root.add_widget(self.build())
            else:
                return
        except CalledProcessError as e:
            print(f"Erro ao usar a versão existente do xsct: {e}")
            sys.exit(1)
            
    def mostrar_dialogo_instalacao(self) -> None:
        MDDialog(
            MDDialogHeadlineText(
                text="Instalação Necessária",
            ),
            MDDialogSupportingText(
                text=(
                    "O xsct não foi encontrado no sistema.\n"
                    "Ele é necessário para ajustar a temperatura de cor. Deseja instalá-lo agora?"
                ),
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(
                        text="Cancelar",
                    ),
                    on_release=lambda _: sys.exit(0),
                ),
                MDButton(
                    MDButtonText(
                        text="Instalar",
                    ),
                    on_release=self.instalar_xsct,
                ),
                spacing="8dp",
            ),
        ).open()
        
    def realizar_instalacao(self, instance=None) -> None:      
        try:
            if not self.senha_input.text.strip():
                print("Erro: Senha não fornecida.")
                return 
        
            run(["rm", "-rf", "sct"], check=True)
            run(["git", "clone", "https://github.com/faf0/sct.git"], check=True)
            senha = self.senha_input.text
            try:
                run(["sudo", "-S", "echo", "Senha correta"], input=senha, text=True, check=True)
                self.senha_input.text = ""
                print("Senha correta. Continuando a instalação...")
                self.instalar_dependencias_com_sudo()
                self.mover_para_diretorio_global()
                if self.dialog:
                    self.dialog.dismiss()
            except CalledProcessError as e:
                print(f"Erro ao validar a senha do sudo: {e}")
                self.senha_input.text = ""
                self.mostrar_dialogo_senha_incorreta()
        except CalledProcessError as e:
            print(f"Erro durante a instalação do xsct: {e}")
            self.root.clear_widgets()
            self.mostrar_dialogo_instalacao()
            
    def instalar_dependencias_com_sudo(self) -> None:
        try:
            if not path.exists("sct"):
                print("Erro: Diretório 'sct' não encontrado.")
                return

            chdir("sct")
            run(["make"], check=True)
            print("Compilação concluída com sucesso.")
            senha = self.senha_input.text
            run(["sudo", "-S", "make", "install"], input=senha, text=True, check=True)
            print("Instalação concluída com sucesso.")
            
            if self.dialog:
                self.dialog.dismiss()
            
            self.root.clear_widgets()
            self.root.add_widget(self.build())
        except CalledProcessError as e:
            print(f"Erro durante a instalação: {e}")
            sys.exit(1)
        finally:
            chdir("..")
            
    def mover_para_diretorio_global(self) -> None:
        try:
            senha = self.senha_input.text        
            if path.exists("/usr/local/bin/sct"):
                print("Removendo versão anterior do xsct...")
                run(["sudo", "-S", "rm", "-rf", "/usr/local/bin/sct"], input=senha, text=True, check=True)

            print("Movendo xsct para o diretório global...")
            run(["sudo", "-S", "mv", "sct", "/usr/local/bin/sct"], input=senha, text=True, check=True)
            run(["xsct", "--help"], check=True)
            print("xsct foi instalado e movido para o diretório global com sucesso.")

        except CalledProcessError as e:
            print(f"Erro ao mover xsct para o diretório global: {e}")
            sys.exit(1)


    def mostrar_dialogo_senha_incorreta(self) -> None:
        dialog = MDDialog(
            title="Senha Incorreta",
            text="A senha informada está incorreta. Tente novamente.",
            buttons=[
                MDButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def adicionar_lista_temperaturas(self, screen: MDScreen) -> None:
        scroll_view: ScrollView = ScrollView()
        md_list: MDList = MDList()
        for temp, descricao in temperaturas.items():
            md_list.add_widget(
                MDListItem(
                    MDListItemHeadlineText(
                        text=f"{temp}K",
                    ),
                    MDListItemSupportingText(
                        text=f"{descricao}",
                    ),
                    on_release=self.ajustar_temperatura(temp),
                )
            )

        scroll_view.add_widget(md_list)
        screen.add_widget(scroll_view)

    def ajustar_temperatura(self, temperatura: int) -> Callable:
        def callback(item) -> None:
            try:
                run(["xsct", str(temperatura)], check=True)
                print(f"Temperatura ajustada para {temperatura}K")
            except CalledProcessError as e:
                print(f"Erro ao ajustar temperatura: {e}")

        return callback
    
    def criar_alias_e_mover_app(self) -> None:
        try:
            senha = self.senha_input.text.strip()
            if not senha:
                print("Erro: Senha não fornecida.")
                return

            app_dir = path.abspath("BlueTone")
            destino_global = "/usr/local/bin/BlueTone"

            if path.exists(destino_global):
                print("Diretório já existe, removendo...")
                run(["sudo", "-S", "rm", "-rf", destino_global], input=senha, text=True, check=True)

            print(f"Movendo o diretório {app_dir} para {destino_global}...")
            run(["sudo", "-S", "mv", app_dir, destino_global], input=senha, text=True, check=True)

            shell_config_file = path.expanduser("~/.bashrc") if path.exists(path.expanduser("~/.bashrc")) else path.expanduser("~/.zshrc")
            alias_command = f"alias BlueTone='python3 {destino_global}/BlueTone.py'"

            with open(shell_config_file, "a") as file:
                file.write(f"\n# Alias para BlueTone\n{alias_command}\n")
            
            print(f"Alias criado com sucesso! Para carregar o alias, execute: source {shell_config_file}")

        except CalledProcessError as e:
            print(f"Erro ao mover o aplicativo ou criar o alias: {e}")
            sys.exit(1)


if __name__ == "__main__":
    BlueToneApp().run()
