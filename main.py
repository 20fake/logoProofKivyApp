from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
#from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.filechooser import FileChooserListView
from kivy import platform
import os
import cv2
from PIL import Image as PILImage
import numpy as np

if platform == "android":
   from android.permissions import request_permissions, Permission
   request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

# Window.size = (360, 640)
Config.set('graphics', 'resizable', 0)

class LogoproofApp(App):
    def __init__(self, **kwargs):
        super(LogoproofApp, self).__init__(**kwargs)
        self.icon = "iconsplash.png"
        self.password = "Admin123"
        self.layout = FloatLayout()
        self.home_background = 'foto/hallog-01.png'
        self.selected_image_path_admin = None

        with self.layout.canvas:
            self.background_image = Image(source=self.home_background, size=('360dp','640dp'))

        self.admin_button = Button(text='ADMIN', on_press=self.on_admin_click,
                              background_color=[0, 0, 1, 1],
                              size_hint=(.8, .09),
                              #size=(250, 50),
                              font_size=40,
                              pos_hint={'center_x': 0.5, 'center_y': 0.45})
        
        self.user_button = Button(text='USER', on_press=self.on_user_click,
                             background_color=[0, 0, 1, 1],
                             size_hint=(.8, .09),
                            #  size=(250, 50),
                             font_size=40,
                             pos_hint={'center_x': 0.5, 'center_y': 0.3})
        
        self.CP_Label = Label(text='Copyright by Deswita Ramadani',
                            size_hint=(None, None),
                            size=(340, 50),
                            font_size=25,
                            pos_hint={'center_x': 0.5, 'center_y': 0.05},
                            color=(0.5, 0.5, 0.5, 1))
        
        self.layout.add_widget(self.admin_button)
        self.layout.add_widget(self.user_button)
        self.layout.add_widget(self.CP_Label)

    def build(self):
        return self.layout

    def on_admin_click(self, instance):
        pass_layout = FloatLayout()
        
        with pass_layout.canvas:
            self.background_image = Image(source='foto/halpass-01.png', size=('360dp','640dp'))
        
        home_icon = "foto/b.home.png"
        home_button = Button(background_normal=home_icon, on_press=self.home_click,
                        size_hint=(None, None),
                        size=(90,90),
                        font_size=20,
                        pos_hint={'center_x': 0.1, 'center_y': 0.95})
        
        pass_Label = Label(text='Masukkan Password Anda:',
                            size_hint=(None, None),
                            size=(550, 100),
                            font_size=30,
                            halign="left",
                            pos_hint={'center_x': 0.27, 'center_y': 0.67}) 
        
        self.input_pass = TextInput(multiline=False,
                               size_hint=(None, None),
                               size=(550, 100),
                               font_size=30,
                               pos_hint={'center_x': 0.44, 'center_y': 0.6},
                               password=True)
        
        show_password_button = Button(background_normal='foto/b.eye.png', on_press=self.show_password,
                                   size_hint=(None, None),
                                    size=(90, 90),
                                    pos_hint={'center_x': 0.92, 'center_y': 0.6})
        
        submit_button = Button(text='SUBMIT', on_press=self.check_password,
                             background_color=[0, 0, 1, 1],
                             size_hint=(None, None),
                             size=(550, 100),
                             font_size=30,
                             pos_hint={'center_x': 0.5, 'center_y': 0.45})
        
        self.message_label = Label(text='',
                                   size_hint=(0., None),
                                #    size=(340, 50),
                                   font_size=40,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.3})
        
        CP_Label = Label(text='Copyright by Deswita Ramadani',
                            size_hint=(None, None),
                            size=(340, 50),
                            font_size=25,
                            pos_hint={'center_x': 0.5, 'center_y': 0.05})
        
        pass_layout.add_widget(home_button)
        pass_layout.add_widget(pass_Label)
        pass_layout.add_widget(self.input_pass)
        pass_layout.add_widget(self.message_label)
        pass_layout.add_widget(show_password_button)
        pass_layout.add_widget(submit_button)
        pass_layout.add_widget(CP_Label)
        self.layout.clear_widgets()
        self.layout.add_widget(pass_layout)

    def choose_image_admin(self, instance):
        file_chooser = FileChooserListView()
        file_chooser.bind(on_submit=self.on_image_selected_admin)
        popup = Popup(content=file_chooser, size_hint=(None, None), size=(300, 500))
        popup.open()
        
    def on_user_click(self, instance):
        self.decode_steganography()

    def home_click(self, instance):
        self.background_image.source = self.home_background
        self.layout.clear_widgets()
        self.layout.add_widget(self.admin_button)
        self.layout.add_widget(self.user_button)
        self.layout.add_widget(self.CP_Label)

    def check_password(self, instance):
        if self.input_pass.text == self.password:
            self.layout.clear_widgets()
            self.add_encrypt_widgets()
        else:
            self.message_label.text='Error! The password is incorrect.'

    def on_image_selected_admin(self, instance, selected, *args):
        if len(selected) > 0:
            selected_path = selected[0]
            if selected_path.endswith(('.jpg', '.png')):
                self.selected_image_path_admin = selected_path
                self.show_popup("Berhasil!", "Gambar telah dipilih untuk enkripsi")
            else:
                self.show_popup("Error!", "Pilih file dengan format JPG atau PNG")

    def add_encrypt_widgets(self):
        with self.layout.canvas:
            self.background_image = Image(source='foto/halpass-01.png', size=('360dp','640dp'))
        
        #button home
        home_icon = "foto/b.home.png"
        home_button = Button(background_normal=home_icon, on_press=self.home_click,
                        size_hint=(None, None),
                        size=(90,90),
                        font_size=20,
                        pos_hint={'center_x': 0.1, 'center_y': 0.95})
        
        #button pilih gambar di halaman admin
        if self.selected_image_path_admin:
            self.image_input = Label(text="Gambar Terpilih:\n{}".format(self.selected_image_path_admin),
                                     size_hint=(None, None),
                                     size=(340, 100),
                                     font_size=14,
                                     pos_hint={'center_x': 0.5, 'center_y': 0.6})
        else:
            self.image_input = Button(text="Pilih Gambar", on_press=self.choose_image_admin,
                                      size_hint=(.8, .09),
                                      background_color=[0, 0, 1, 1],
                                      font_size=30,
                                          #size=(250, 50),
                                      pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.message_input = TextInput(hint_text="Masukkan Informasi Keaslian Gambar",
                                       size_hint=(None, None),
                                       size=(550, 100),
                                       font_size=25,
                                       pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.encode_button = Button(text="Enkripsi", on_press=self.encode,
                                    size_hint=(None, None),
                                    size=(340, 50),
                                    font_size=25,
                                    pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.result_label = Label(text="",
                                  size_hint=(None, None),
                                  size=(340, 50),
                                  font_size=20,
                                  pos_hint={'center_x': 0.5, 'center_y': 0.3})
        CP_Label = Label(text='Copyright by Deswita Ramadani',
                         size_hint=(None, None),
                         size=(340, 50),
                         font_size=25,
                         pos_hint={'center_x': 0.5, 'center_y': 0.05})
        
        self.layout.add_widget(home_button)
        self.layout.add_widget(self.image_input)
        self.layout.add_widget(self.message_input)
        self.layout.add_widget(self.encode_button)
        self.layout.add_widget(self.result_label)
        self.layout.add_widget(CP_Label)

    def data2binary(self, data):
        if type(data) == str:
            p = ''.join([format(ord(i), '08b')for i in data])
        elif type(data) == bytes or type(data) == np.ndarray:
            p = [format(i, '08b')for i in data]
        return p

    def hide_data(self, img, data):
        data += "$$"
        d_index = 0
        b_data = self.data2binary(data)
        len_data = len(b_data)

        for value in img:
            for pix in value:
                r, g, b = self.data2binary(pix)
                if d_index < len_data:
                    pix[0] = int(r[:-1] + b_data[d_index])
                    d_index += 1
                if d_index < len_data:
                    pix[1] = int(g[:-1] + b_data[d_index])
                    d_index += 1
                if d_index < len_data:
                    pix[2] = int(b[:-1] + b_data[d_index])
                    d_index += 1
                if d_index >= len_data:
                    break
        return img

    import os

    def encode(self, instance):
        if self.selected_image_path_admin:
            img_name = self.selected_image_path_admin
            image = cv2.imread(img_name)
            img = PILImage.open(img_name, 'r')
            w, h = img.size
            data = self.message_input.text
            if len(data) == 0:
                self.show_popup("Error", "Empty data")
                return
            enc_img_name = "Asli_" + os.path.basename(img_name)  # Mengambil nama file saja tanpa path lengkapnya
            enc_img_path = os.path.join(os.path.dirname(img_name), enc_img_name)  # Menyimpan di direktori yang sama dengan gambar sumber
            enc_data = self.hide_data(image, data)
            cv2.imwrite(enc_img_path, enc_data)
            img1 = PILImage.open(enc_img_path, 'r')
            img1 = img1.resize((w, h), PILImage.ANTIALIAS)
            if w != h:
                img1.save(enc_img_path, optimize=True, quality=65)
            else:
                img1.save(enc_img_path)
            self.show_popup("Success", "Image encoded successfully: {}".format(enc_img_path))
        else:
            self.show_popup("Error", "Silakan pilih gambar terlebih dahulu.")

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content),
                      size_hint=(.9, .2),
                      size=(350, 100))
        popup.open()
        
    def show_password(self, instance):
        self.input_pass.password = not self.input_pass.password
    
    def decode_steganography(self):
        layout = FloatLayout()
        
        with layout.canvas:
            self.background_image = Image(source='foto/haluser-01.png', size=('360dp','640dp'))
            
        home_icon = "foto/b.home.png"
        home_button = Button(background_normal=home_icon, on_press=self.home_click,
                             size_hint=(None, None),
                             size=(90,90),
                             font_size=20,
                             pos_hint={'center_x': 0.1, 'center_y': 0.95})
        
        self.image_input = Button(text="Pilih Gambar", on_press=self.choose_image,
                      size_hint=(.8, .09),
                      background_color=[0, 0, 1, 1],
                    #   size=(250, 50),
                      font_size=30,
                      pos_hint={'center_x': 0.5, 'center_y': 0.6})
        
        self.decode_button = Button(text="Verifikasi",
                        on_press=self.decode,#Tombol verifikasi atau proses dekripsi/decode
                        background_color=[0, 0, 1, 1],
                        size_hint=(.8, .09),
                        # size=(250, 50),
                        font_size=30,
                        pos_hint={'center_x': 0.5, 'center_y': 0.45})
        
        self.result_label = Label(text="",
                        size=(340, 50),
                        font_size=24,
                        pos_hint={'center_x': 0.5, 'center_y': 0.3})
        
        CP_Label = Label(text='Copyright by Deswita Ramadani',
                         size_hint=(None, None),
                         size=(340, 50),
                         font_size=25,
                         pos_hint={'center_x': 0.5, 'center_y': 0.05})
        
        layout.add_widget(home_button)
        layout.add_widget(self.image_input)
        layout.add_widget(self.decode_button)
        layout.add_widget(self.result_label)
        layout.add_widget(CP_Label)
        
        self.layout.clear_widgets()
        self.layout.add_widget(layout)

    def data2binary(self, data):
        if type(data) == str:
            p = ''.join([format(ord(i), '08b')for i in data])
        elif type(data) == bytes or type(data) == np.ndarray:
            p = [format(i, '08b')for i in data]
        return p

    def find_data(self, img):
        bin_data = ""
        for value in img:
            for pix in value:
                r, g, b = self.data2binary(pix)
                bin_data += r[-1]
                bin_data += g[-1]
                bin_data += b[-1]

        all_bytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]

        readable_data = ""
        for x in all_bytes:
            readable_data += chr(int(x, 2))
            if len(readable_data) >= 2 and readable_data[-2:] == "$$":
                return readable_data[:-2]
        
        return None


    def choose_image(self, instance):
        file_chooser = FileChooserListView()
        file_chooser.bind(on_submit=self.on_image_selected_user)
        popup = Popup(content=file_chooser, size_hint=(0.65, .6)) #size=(300, 500))
        popup.open()

    def on_image_selected_user(self, instance, selected, *args):
        if len(selected) > 0:
            selected_image_path = selected[0]
            if selected_image_path.lower().endswith(('.png', '.jpg')):
                self.selected_image_path = selected_image_path
                self.show_popup("Berhasil!", "Lanjutkan dengan menekan Tombol Verifikasi")
            else:
                self.show_popup("Error!", "Pilih file dengan format PNG atau JPG")

    def decode(self, instance):
        if hasattr(self, 'selected_image_path') and self.selected_image_path:
            img_name = self.selected_image_path
            image = cv2.imread(img_name)
            img = PILImage.open(img_name, 'r')
            msg = self.find_data(image)
            self.result_label.text = "[size=18]Hasil Verifikasi Gambar:[/size]\n[b]{}[/b]".format(msg)
            self.result_label.font_size = '35sp'
            self.result_label.markup = True
            self.result_label.halign = 'center'
        else:
            self.show_popup("Error!", "Silakan pilih gambar terlebih dahulu.")

if __name__ == '__main__':
    LogoproofApp().run()
