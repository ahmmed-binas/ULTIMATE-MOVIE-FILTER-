import tkinter as tk
from tkinter import ttk

def gui():
    WIDTH = 1000
    HEIGHT = 500
    
    window = tk.Tk()
    window.title("MOVIE FILTER APPLICATION")
    window.geometry(f"{WIDTH}x{HEIGHT}")
    
    heading = tk.Label(window, text="ULTIMATE MOVIE FILTER", font=('Helvetica', 12))
    heading.pack(ipadx=25, ipady=10)
    
    search_bar(window)
    option_section(window)
    
    movie_data = {
        "title": "Inception",
        "year": 2010,
        "img_url": "example for modelling analisys.PNG",
        "youtube_link": "https://www.youtube.com/watch?v=YoHD9XEInc0",
        "movie_link": "https://www.imdb.com/title/tt1375666/"
    }

    movie_component = MovieComponent(window, **movie_data)
    movie_component.pack(padx=10, pady=10)
    
    window.mainloop()

def search_bar(window):
    style = ttk.Style()
    style.configure("Custom.TButton", padding=(2), font=('Helvetica', 14))

    search_var = tk.StringVar()
    frame = ttk.Frame(window)
    frame.pack(padx=20, pady=20, fill="x")
    
    heading_search = tk.Label(frame, text="Link", font=('Helvetica', 12))
    heading_search.grid(row=1, column=1, padx=(0, 5))

    search_entry = ttk.Entry(frame, textvariable=search_var, width=25)
    search_entry.grid(row=1, column=0, padx=(0, 5))
    search_entry.config(font=('Helvetica', 17))

def option_section(window):
    frame_heading = ttk.Frame(window)
    frame_heading.pack(padx=5, pady=(5, 0), fill="x")
    
    heading_opt = tk.Label(frame_heading, text="FILTER", font=('Helvetica', 20))
    heading_opt.grid(row=0, column=0, padx=20, pady=10)

    frame = ttk.Frame(window)
    frame.pack(padx=20, pady=5, fill="x")

    ratings_label = tk.Label(frame, text="Ratings:", font=('Helvetica', 12))
    ratings_label.grid(row=0, column=0, padx=5, pady=0, sticky='e')

    ratings_var = tk.StringVar()
    ratings_opt = ["Any", "1 - 2", "3 - 4", "5 - 6", "7 - 8", "9 - 10"]
    ratings_dropdown = ttk.Combobox(frame, textvariable=ratings_var, values=ratings_opt, font=('Helvetica', 12))
    ratings_dropdown.grid(row=0, column=1, padx=5, pady=0, sticky='w')

    year_label = tk.Label(frame, text="Year:", font=('Helvetica', 12))
    year_label.grid(row=0, column=2, padx=5, pady=0, sticky='e')

    year_var = tk.StringVar()
    year_opt = [str(year) for year in range(1900, 2025)]
    year_dropdown = ttk.Combobox(frame, textvariable=year_var, values=year_opt, font=('Helvetica', 12))
    year_dropdown.grid(row=0, column=3, padx=5, pady=0, sticky='w')

    genre_label = tk.Label(frame, text="Genre:", font=('Helvetica', 12))
    genre_label.grid(row=1, column=0, padx=5, pady=(25, 0), sticky='e')
    
    genre_var = tk.StringVar()
    genre_opt = ["Any", "Action", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Thriller"]
    genre_dropdown = ttk.Combobox(frame, textvariable=genre_var, values=genre_opt, font=('Helvetica', 12))
    genre_dropdown.grid(row=1, column=1, padx=5, pady=(25, 0), sticky='w')

    search_btn = ttk.Button(frame, text="Search", command=handle_search, style="Custom.TButton")
    search_btn.grid(row=1, column=4, padx=20, pady=(25, 0), sticky='w')

class MovieComponent(ttk.Frame):
    def __init__(self, parent, title, year, img_url, youtube_link, movie_link):
        super().__init__(parent)
        
        self.image_label = ttk.Label(self)
        self.image_label.grid(row=0, column=0)
        
        self.title_label = ttk.Label(self, text=title, font=('Helvetica', 12, 'bold'))
        self.title_label.grid(row=0, column=1, padx=10)
        
        self.year_label = ttk.Label(self, text=year, font=('Helvetica', 10))
        self.year_label.grid(row=0, column=2, padx=10)

        self.youtube_link = youtube_link
        self.youtube_button = ttk.Button(self, text="YouTube", command=self.open_youtube)
        self.youtube_button.grid(row=1, column=1, pady=5)
        
        self.movie_link = movie_link
        self.movie_button = ttk.Button(self, text="Movie", command=self.open_movie)
        self.movie_button.grid(row=1, column=2, pady=5)

    def load_image(self, img_url):
        pass

    def open_youtube(self):
        pass

    def open_movie(self):
        pass

def list_section():
    pass

def handle_search():
    pass

gui()
