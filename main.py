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

base64_icon = "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"

class BlueToneApp(MDApp):
    dialog: MDDialog

    def build(self) -> MDScreen:
        self.title = "BlueTone"
        icon_data = b64decode(base64_icon)
        
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