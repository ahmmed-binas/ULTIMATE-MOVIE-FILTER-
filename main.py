import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time


def gui():
    global search_var, ratings_var, year_var, genre_var, frame, count_var

    WIDTH = 1000
    HEIGHT = 500

    window = tk.Tk()
    window.title("MOVIE FILTER APPLICATION")
    window.geometry(f"{WIDTH}x{HEIGHT}")

    heading = tk.Label(window, text="ULTIMATE MOVIE FILTER", font=('Helvetica', 12))
    heading.pack(ipadx=25, ipady=10)

    search_bar(window)
    option_section(window)

    canvas = tk.Canvas(window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    window.mainloop()


def search_bar(window):
    global search_var

    style = ttk.Style()
    style.configure("Custom.TButton", padding=(2), font=('Helvetica', 14))

    search_var = tk.StringVar()
    frame = ttk.Frame(window)
    frame.pack(padx=20, pady=20, fill=tk.X)

    heading_search = tk.Label(frame, text="Link", font=('Helvetica', 12))
    heading_search.grid(row=1, column=1, padx=(0, 5))

    search_entry = ttk.Entry(frame, textvariable=search_var, width=25)
    search_entry.grid(row=1, column=0, padx=(0, 5))
    search_entry.config(font=('Helvetica', 17))


def option_section(window):
    global ratings_var, year_var, genre_var, count_var

    frame_heading = ttk.Frame(window)
    frame_heading.pack(padx=5, pady=(5, 0), fill=tk.X)

    heading_opt = tk.Label(frame_heading, text="FILTER", font=('Helvetica', 20))
    heading_opt.grid(row=0, column=0, padx=20, pady=10)

    frame = ttk.Frame(window)
    frame.pack(padx=20, pady=5, fill=tk.X)

    ratings_label = tk.Label(frame, text="Ratings:", font=('Helvetica', 12))
    ratings_label.grid(row=0, column=0, padx=5, pady=0, sticky='e')

    ratings_var = tk.StringVar()
    ratings_opt = ["Any", "1 - 2", "3 - 4", "5 - 6", "7 - 8", "9 - 10"]
    ratings_dropdown = ttk.Combobox(frame, textvariable=ratings_var, values=ratings_opt, font=('Helvetica', 12))
    ratings_dropdown.grid(row=0, column=1, padx=5, pady=0, sticky='w')
    ratings_dropdown.set("Any")

    year_label = tk.Label(frame, text="Year:", font=('Helvetica', 12))
    year_label.grid(row=0, column=2, padx=5, pady=0, sticky='e')

    year_var = tk.StringVar()
    year_opt = ["Any"]
    year_dropdown = ttk.Combobox(frame, textvariable=year_var, values=year_opt, font=('Helvetica', 12))
    year_dropdown.grid(row=0, column=3, padx=5, pady=0, sticky='w')
    year_dropdown.set("Any")

    genre_label = tk.Label(frame, text="Genre:", font=('Helvetica', 12))
    genre_label.grid(row=1, column=0, padx=5, pady=(25, 0), sticky='e')

    genre_var = tk.StringVar()
    genre_opt = ["Any"]
    genre_dropdown = ttk.Combobox(frame, textvariable=genre_var, values=genre_opt, font=('Helvetica', 12))
    genre_dropdown.grid(row=1, column=1, padx=5, pady=(25, 0), sticky='w')
    genre_dropdown.set("Any")

    count_label = tk.Label(frame, text="Count of Movies:", font=('Helvetica', 12))
    count_label.grid(row=2, column=0, padx=5, pady=(25, 0), sticky='e')

    count_var = tk.StringVar()
    count_entry = ttk.Entry(frame, textvariable=count_var, width=8, font=('Helvetica', 12))
    count_entry.grid(row=2, column=1, padx=5, pady=(25, 0), sticky='w')
    count_entry.insert(0, "20")  # Default count is 20

    search_button = tk.Button(window, text="Search", command=lambda: handle_search(frame))
    search_button.pack()


class MovieComponent(ttk.Frame):
    def __init__(self, parent, title, year, rating, img_url, youtube_link, movie_link):
        super().__init__(parent)

        self.title = title
        self.year = year
        self.rating = rating
        self.img_url = img_url
        self.youtube_link = youtube_link
        self.movie_link = movie_link

        border_frame = ttk.Frame(self, borderwidth=2, relief="solid", width=1000, height=200)
        border_frame.pack_propagate(False)
        border_frame.pack(padx=10, pady=10, fill=tk.X)

        self.image_label = ttk.Label(border_frame)
        self.image_label.grid(row=0, column=0, rowspan=4, padx=10, pady=10)
        self.load_image(img_url)

        opt_frame = ttk.Frame(border_frame)
        opt_frame.grid(row=0, column=1, sticky='n')

        title_label = ttk.Label(opt_frame, text=f"Title: {title}", font=('Helvetica', 12))
        title_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        year_label = ttk.Label(opt_frame, text=f"Year: {year}", font=('Helvetica', 12))
        year_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        rating_label = ttk.Label(opt_frame, text=f"Rating: {rating}", font=('Helvetica', 12))
        rating_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        youtube_button = ttk.Button(opt_frame, text="Trailer", command=self.open_youtube)
        youtube_button.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        movie_button = ttk.Button(opt_frame, text="Movie", command=self.open_movie)
        movie_button.grid(row=4, column=0, padx=10, pady=5, sticky='w')

    def load_image(self, img_url):
        try:
            response = requests.get(img_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((100, 150), Image.LANCZOS)
            self.img = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.img)
        except Exception as e:
            print(f"Error loading image: {e}")

    def open_youtube(self):
        import webbrowser
        webbrowser.open(self.youtube_link)

    def open_movie(self):
        import webbrowser
        webbrowser.open(self.movie_link)
        
        
def handle_search(frame):
    try:
        url = search_var.get() 

        if not url.strip(): 
            url = "https://swatchseries.is/top-imdb"

        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        link_window = tk.Toplevel()
        link_window.title("Movie Links")
        
        link_listbox = tk.Listbox(link_window, width=100, height=20)
        link_listbox.pack(padx=10, pady=10)

        links_set = set()  

        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]

        for link in links:
            if '/tv/watch-' in link and link not in links_set:  
                links_set.add(link)
                link_listbox.insert(tk.END, link)

                try:
                    movie_response = requests.get(link)
                    movie_response.raise_for_status()
                    movie_soup = BeautifulSoup(movie_response.content, 'html.parser')

                    main_wrapper = movie_soup.find('div', id='main-wrapper')

                    if main_wrapper:
                        movie_info = main_wrapper.find('div', class_='movie_information')
                        if movie_info:
                            container = movie_info.find('div', class_='container')
                            if container:
                                m_id_content = container.find('div', class_='m_i-d-content')
                                if m_id_content:
                                    stats = m_id_content.find('div', class_='stats')
                                    if stats:
                                        rating_element = stats.find('i', class_='fas fa-star mr-2')
                                        rating = float(rating_element.next_sibling.strip()) if rating_element else None
                                        if rating is not None:
                                            link_listbox.insert(tk.END, f"Rating found for {link}: {rating}")
                                        else:
                                            link_listbox.insert(tk.END, f"No rating found for {link}")

                except Exception as e:
                    link_listbox.insert(tk.END, f"Error processing movie page: {link}, Error: {e}")

    except requests.RequestException as e:
        error_window = tk.Toplevel()
        error_window.title("Error")
        
        error_label = tk.Label(error_window, text=f"Error fetching URL: {e}")
        error_label.pack(padx=10, pady=10)
        
        ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
        ok_button.pack(pady=10)


if __name__=="__main__":
    gui()