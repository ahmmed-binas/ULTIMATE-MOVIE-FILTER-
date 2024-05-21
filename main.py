import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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
    
    '''
    movie_data_1 = {
        "title": "Inception",
        "year": 2010,
        "img_url": "example for modelling analisys.PNG",
        "youtube_link": "https://www.youtube.com/watch?v=YoHD9XEInc0",
        "movie_link": "https://www.imdb.com/title/tt1375666/"
    }

    movie_data_2 = {
        "title": "Interstellar",
        "year": 2014,
        "img_url": "example for modelling analisys.PNG",
        "youtube_link": "https://www.youtube.com/watch?v=zSWdZVtXT7E",
        "movie_link": "https://www.imdb.com/title/tt0816692/"
    }

    movie_component_1 = MovieComponent(window, **movie_data_1)
    movie_component_1.pack(padx=10, pady=10, fill=tk.X)

    movie_component_2 = MovieComponent(window, **movie_data_2)
    movie_component_2.pack(padx=10, pady=10, fill=tk.X)
    '''
    window.mainloop()

def search_bar(window):
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
        
        self.title = title
        self.year = year
        self.img_url = img_url
        self.youtube_link = youtube_link
        self.movie_link = movie_link

        border_frame = ttk.Frame(self, borderwidth=2, relief="solid", width=600, height=200)
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


        youtube_button = ttk.Button(opt_frame, text="Trailer", command=self.open_youtube)
        youtube_button.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        movie_button = ttk.Button(opt_frame, text="Movie", command=self.open_movie)
        movie_button.grid(row=3, column=0, padx=10, pady=5, sticky='w')

    def load_image(self, img_url):
        try:
            img = Image.open(img_url)
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

def handle_search():
    print("Search button clicked")

if __name__ == "__main__":
    gui()
