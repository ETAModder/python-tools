import tkinter as tk
from tkinter import scrolledtext, Canvas, PhotoImage
from urllib import request, parse
from urllib.parse import urljoin
from html.parser import HTMLParser
import threading
import base64

class SimpleHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.images = []
        self.colors = {}
        self.fonts = {}

    def handle_starttag(self, tag, attrs):
        style = {key: value for key, value in attrs}
        if tag == 'img':
            if 'src' in style:
                self.images.append(style['src'])
        elif tag in ['p', 'span', 'div']:
            if 'style' in style:
                styles = style['style'].split(';')
                for s in styles:
                    if 'color' in s:
                        color = s.split(':')[1].strip()
                        self.colors[len(self.text)] = color
                    if 'font-family' in s:
                        font = s.split(':')[1].strip()
                        self.fonts[len(self.text)] = font

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        return ''.join(self.text)

    def get_images(self):
        return self.images

    def get_styles(self):
        return self.colors, self.fonts

class SimpleWebBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("eWEB | boring, but reliable | v2")
        self.root.config(bg='#50AB65')

        self.url_entry = tk.Entry(root, width=50, fg="#1E6934", bg='#50B867', font="LanaPixel")
        self.url_entry.pack(pady=10)

        self.go_button = tk.Button(root, text="GO", command=self.load_url, fg="#1E6934", bg='#50B867', activebackground='#50B867', cursor="hand2", font="LanaPixel")
        self.go_button.pack(pady=5)

        self.output_area = scrolledtext.ScrolledText(root, width=80, height=20, fg="black", bg='lightgray', font="Arial")
        self.output_area.pack(pady=10)

        self.canvas = Canvas(root, bg='#50B867')
        self.canvas.pack(pady=10)
        self.image_cache = []  # To keep references to image objects

    def load_url(self):
        # Run the loading in a separate thread to keep the GUI responsive
        threading.Thread(target=self.fetch_and_display).start()

    def fetch_and_display(self):
        url = self.url_entry.get()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url

        self.output_area.delete(1.0, tk.END)
        self.canvas.delete("all")
        self.image_cache.clear()
        self.output_area.insert(tk.END, f"LOADING {url}...\n")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.114 Safari/537.36'
        }
        req = request.Request(url, headers=headers)

        try:
            response = request.urlopen(req)
            content = response.read().decode()

            parser = SimpleHTMLParser()
            parser.feed(content)
            text = parser.get_text()
            images = parser.get_images()
            colors, fonts = parser.get_styles()

            self.output_area.insert(tk.END, text)
            self.apply_styles(colors, fonts)
            self.fetch_and_display_images(images, url)
        except Exception as e:
            self.output_area.insert(tk.END, f"ERR: {str(e)}\n")

    def apply_styles(self, colors, fonts):
        for index, color in colors.items():
            self.output_area.tag_add(f"color{index}", f"1.{index}", f"1.{index + 1}")
            self.output_area.tag_configure(f"color{index}", foreground=color)

        for index, font in fonts.items():
            self.output_area.tag_add(f"font{index}", f"1.{index}", f"1.{index + 1}")
            self.output_area.tag_configure(f"font{index}", font=(font, 10))

    def fetch_and_display_images(self, images, base_url):
        for img_src in images:
            img_url = urljoin(base_url, img_src)
            try:
                with request.urlopen(img_url) as img_response:
                    image_data = img_response.read()
                    image_b64 = base64.b64encode(image_data)
                    img_tk = PhotoImage(data=image_b64)

                    self.image_cache.append(img_tk)  # Keep a reference to avoid garbage collection
                    self.canvas.create_image(10, len(self.image_cache) * 210, anchor=tk.NW, image=img_tk)
            except Exception as e:
                self.output_area.insert(tk.END, f"ERR LOADING IMG: {img_url}: {str(e)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleWebBrowser(root)
    root.mainloop()
