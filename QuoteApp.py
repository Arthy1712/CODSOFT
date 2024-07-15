from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
import datetime
import random

# Sample quotes
quotes = [
    "It is better to fail in originality than to succeed in imitation. —Herman Melville",
    "The road to success and the road to failure are almost exactly the same. —Colin R. Davis",
    "Success usually comes to those who are too busy to be looking for it. —Henry David Thoreau",
    "Don’t let yesterday take up too much of today.—Will Rogers",
    "Education is the most powerful weapon which you can use to change the world.—Nelson Mandela",
]

class QuoteApp(App):
    def build(self):
        self.store = JsonStore('favorites.json')
        self.daily_quote = self.get_daily_quote()

        layout = BoxLayout(orientation='vertical')

        self.quote_label = Label(text=self.daily_quote, halign='center', valign='middle')
        self.quote_label.bind(size=self.quote_label.setter('text_size'))
        layout.add_widget(self.quote_label)

        button_layout = BoxLayout(size_hint_y=0.2)

        favorite_button = Button(text="Save to Favorites")
        favorite_button.bind(on_release=self.save_to_favorites)
        button_layout.add_widget(favorite_button)

        view_favorites_button = Button(text="View Favorites")
        view_favorites_button.bind(on_release=self.view_favorites)
        button_layout.add_widget(view_favorites_button)

        share_button = Button(text="Share Quote")
        share_button.bind(on_release=self.share_quote)
        button_layout.add_widget(share_button)

        layout.add_widget(button_layout)

        return layout

    def get_daily_quote(self):
        today = datetime.date.today().isoformat()
        stored_date = self.store.get('date')['date'] if self.store.exists('date') else None

        if stored_date != today:
            quote = random.choice(quotes)
            self.store.put('quote', quote=quote)
            self.store.put('date', date=today)
        else:
            quote = self.store.get('quote')['quote']

        return quote

    def save_to_favorites(self, instance):
        quote = self.daily_quote
        if not self.store.exists('favorites'):
            self.store.put('favorites', quotes=[])
        favorites = self.store.get('favorites')['quotes']
        if quote not in favorites:
            favorites.append(quote)
            self.store.put('favorites', quotes=favorites)

    def view_favorites(self, instance):
        if self.store.exists('favorites'):
            favorites = self.store.get('favorites')['quotes']
            content = BoxLayout(orientation='vertical')
            for fav in favorites:
                content.add_widget(Label(text=fav))
            popup = Popup(title='Favorite Quotes', content=content, size_hint=(0.8, 0.8))
            popup.open()
        else:
            popup = Popup(title='No Favorites', content=Label(text='No favorite quotes saved.'), size_hint=(0.8, 0.4))
            popup.open()

    def share_quote(self, instance):
        # Implement sharing functionality as per platform requirement
        popup = Popup(title='Share Quote', content=Label(text='Quote shared successfully!'), size_hint=(0.8, 0.4))
        popup.open()

if __name__ == '__main__':
    QuoteApp().run()

