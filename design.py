from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, BorderImage
from kivy.config import Config
from kivy.uix.label import Label
from kivy.core.image import Image as CoreImage
from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
import code
# Config.set('graphics', 'resizable', '0')
# Config.set('graphics', 'height', '800')
# Config.set('graphics', 'width', '1000')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'height', '1000')
Config.set('graphics', 'width', '1777')

class DotaAppApp(App):
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def winrate_action(self, instance):
        ranks_translator = {'Рекрут':3, 'Страж':4, 'Рыцарь':5, 'Герой':6, 'Легенда':7, 'Властелин':8, 'Божество':9,
                            'Титан':10, 'Профессиональный':11}
        roles_translator = {0:'Nuker', 1:'Jungler', 2:'Initiator', 3:'Disabler', 4:'Pusher', 5:'Escape', 6:'Support',
                            7:'Durable', 8:'Carry'}
        rank = ranks_translator[instance.text]
        roles = set()
        list_cb = (self.win_nuker_cb, self.win_jungler_cb, self.win_initiator_cb, self.win_disabler_cb,
                   self.win_pusher_cb, self.win_escape_cb, self.win_support_cb, self.win_durable_cb, self.win_carry_cb)
        for i in range(9):
            if list_cb[i].active == True:
                roles.add(roles_translator[i])
        table_strings = code.fill_table(rank, roles)
        self.win_table.text = table_strings

    def select_all_pressed(self, instance):
        with open('winrates.json', 'r') as f:
            s = f.readlines()
            count_heroes = len(s) - 1
            for i in range(count_heroes):
                name = self.hero_btns[i].background_normal[9:]
                name = name[:name.find('_img')]
                self.hero_btns[i].background_normal = 'dota_img/' + name + '_img.jpg'

    def delete_all_pressed(self, instance):
        with open('winrates.json', 'r') as f:
            s = f.readlines()
            count_heroes = len(s) - 1
            for i in range(count_heroes):
                name = self.hero_btns[i].background_normal[9:]
                name = name[:name.find('_img')]
                self.hero_btns[i].background_normal = 'dota_img/' + name + '_img_black.jpg'

    def end_select_pressed(self, instance):
        end_select_popup_content = StackLayout()
        bl_btns = BoxLayout(orientation='horizontal')
        bl_top = BoxLayout(orientation='vertical')
        bl = BoxLayout(orientation='horizontal', size_hint=[1, .25])
        bl_top.add_widget(Label(text='Герои противника',

                                font_size=20))
        enemy_btns = []
        for i in range(5):
            enemy_btns.append(Button(size_hint=[None, None], size=(128, 72)))
            bl_btns.add_widget(enemy_btns[i])
        bl_top.add_widget(bl_btns)
        bl.add_widget(bl_top)
        bl.add_widget(Label(text='asdfasdfadf'))
        end_select_popup_content.add_widget(bl)
        for i in range(119):
            name = self.hero_btns[i].background_normal[9:]
            name = name[:name.find('_img')]
            if self.hero_btns[i].background_normal == 'dota_img/' + name + '_img.jpg':
                end_select_popup_content.add_widget(Button(background_normal='dota_img/' + name + '_img.jpg',
                                                           size_hint=[None, None],
                                                           size=(128, 72)))
        end_select_popup = Popup(title='Контр-пикер',
                                 content=end_select_popup_content,
                                 size_hint=[None, None],
                                 size=(1777, 1000))
        end_select_popup.open()

    def background_change(self, instance):
        name = instance.background_normal[9:]
        name = name[:name.find('_img')]
        if instance.background_normal == 'dota_img/' + name + '_img.jpg':
            instance.background_normal = 'dota_img/' + name + '_img_black.jpg'
        else:
            instance.background_normal = 'dota_img/' + name + '_img.jpg'

    def build(self):
        menu_al = AnchorLayout()
        menu_bl = BoxLayout(orientation='vertical',
                            size_hint=[.25, .1],
                            spacing=10)

        # winrate table design

        win_p_content = StackLayout()
        self.win_table = Label(text='Сначала выберите роли, затем ранг', size_hint=(.75, .75))
        win_herald = ToggleButton(text='Рекрут', group='Ранг', on_press=self.winrate_action)
        win_guardian = ToggleButton(text='Страж', group='Ранг', on_press=self.winrate_action)
        win_crusader = ToggleButton(text='Рыцарь', group='Ранг', on_press=self.winrate_action)
        win_archon = ToggleButton(text='Герой', group='Ранг', on_press=self.winrate_action)
        win_legend = ToggleButton(text='Легенда', group='Ранг', on_press=self.winrate_action)
        win_ancient = ToggleButton(text='Властелин', group='Ранг', on_press=self.winrate_action)
        win_divine = ToggleButton(text='Божество', group='Ранг', on_press=self.winrate_action)
        win_immortal = ToggleButton(text='Титан', group='Ранг', on_press=self.winrate_action)
        win_pro = ToggleButton(text='Профессиональный', group='Ранг', on_press=self.winrate_action)
        rank_bl = BoxLayout(orientation='vertical',
                            size_hint=[.25, .75],
                            padding=[0, 50, 0, 0])
        rank_bl.add_widget(win_herald)
        rank_bl.add_widget(win_guardian)
        rank_bl.add_widget(win_crusader)
        rank_bl.add_widget(win_archon)
        rank_bl.add_widget(win_legend)
        rank_bl.add_widget(win_ancient)
        rank_bl.add_widget(win_divine)
        rank_bl.add_widget(win_immortal)
        rank_bl.add_widget(win_pro)
        win_roles = GridLayout(cols=9,
                               size_hint=[1, .25],
                               padding=[0, 0, 0, 100])
        win_nuker_lab = Label(text='Nuker')
        win_jungler_lab = Label(text='Jungler')
        win_initiator_lab = Label(text='Initiator')
        win_disabler_lab = Label(text='Disabler')
        win_pusher_lab = Label(text='Pusher')
        win_escape_lab = Label(text='Escape')
        win_support_lab = Label(text='Support')
        win_durable_lab = Label(text='Durable')
        win_carry_lab = Label(text='Carry')
        self.win_nuker_cb = CheckBox()
        self.win_jungler_cb = CheckBox()
        self.win_initiator_cb = CheckBox()
        self.win_disabler_cb = CheckBox()
        self.win_pusher_cb = CheckBox()
        self.win_escape_cb = CheckBox()
        self.win_support_cb = CheckBox()
        self.win_durable_cb = CheckBox()
        self.win_carry_cb = CheckBox()
        win_roles.add_widget(win_nuker_lab)
        win_roles.add_widget(win_jungler_lab)
        win_roles.add_widget(win_initiator_lab)
        win_roles.add_widget(win_disabler_lab)
        win_roles.add_widget(win_pusher_lab)
        win_roles.add_widget(win_escape_lab)
        win_roles.add_widget(win_support_lab)
        win_roles.add_widget(win_durable_lab)
        win_roles.add_widget(win_carry_lab)
        win_roles.add_widget(self.win_nuker_cb)
        win_roles.add_widget(self.win_jungler_cb)
        win_roles.add_widget(self.win_initiator_cb)
        win_roles.add_widget(self.win_disabler_cb)
        win_roles.add_widget(self.win_pusher_cb)
        win_roles.add_widget(self.win_escape_cb)
        win_roles.add_widget(self.win_support_cb)
        win_roles.add_widget(self.win_durable_cb)
        win_roles.add_widget(self.win_carry_cb)
        win_p_content.add_widget(self.win_table)
        win_p_content.add_widget(rank_bl)
        win_p_content.add_widget(win_roles)
        win_popup = Popup(title='Топ винрейты',
                          content=win_p_content,
                          size_hint=(None, None),
                          size=(800, 1000))
        btn_wintable = Button(text='Таблица винрейтов', on_press=win_popup.open)

        # counter-picker design
        counter_p_content = StackLayout()
        counter_label = Label(text='Выберите пул героев,\nна которых вы сможете сыграть')
        select_all_btn = Button(text='Выбрать всех', on_press=self.select_all_pressed)
        delete_all_btn = Button(text='Удалить всех', on_press=self.delete_all_pressed)
        end_btn = Button(text='Закончить выбор героев', on_press=self.end_select_pressed)
        counter_btn_bl = BoxLayout(orientation='vertical')
        counter_btn_bl.add_widget(select_all_btn)
        counter_btn_bl.add_widget(delete_all_btn)
        counter_top_bl = BoxLayout(orientation='horizontal',
                                   spacing=80,
                                   size_hint=[1, .2])
        counter_top_bl.add_widget(counter_label)
        counter_top_bl.add_widget(counter_btn_bl)
        counter_top_bl.add_widget(end_btn)
        counter_p_content.add_widget(counter_top_bl)
        with open('winrates.json', 'r') as f:
            s = f.readlines()
            self.hero_btns = []
            for i in range(1, 120):
                s[i] = s[i].split(';')
                name = s[i][1]
                self.hero_btns.append(Button(background_normal='dota_img/' + name + '_img.jpg',
                                             size_hint=[None, None],
                                             size=(128, 72),
                                             on_press=self.background_change))
                counter_p_content.add_widget(self.hero_btns[i-1])
        counter_popup = Popup(title='Контр-пикер',
                              content=counter_p_content,
                              size_hint=(None, None),
                              size=(1777, 1000))
        btn_cpick = Button(text='Контр-пикер', on_press=counter_popup.open)
        menu_bl.add_widget(btn_wintable)
        menu_bl.add_widget(btn_cpick)
        menu_al.add_widget(menu_bl)
        menu_al.bind(size=self._update_rect, pos=self._update_rect)
        with menu_al.canvas.before:
            texture = CoreImage("dota-2-header.jpg").texture
            self.rect = Rectangle(size=menu_al.size, pos=menu_al.pos, texture=texture)
        return menu_al


if __name__ == "__main__":
    DotaAppApp().run()
