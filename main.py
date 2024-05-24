import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import validators



movies={}


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
    count_entry.insert(0, "3")  # Default count is 20

    search_button = tk.Button(window, text="Search", command=lambda:handle_search())
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



def handle_search():
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
        movies = {}
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]

        for link in links:
            if '/tv/watch-' in link and link not in links_set:  
                links_set.add(link)
                link_listbox.insert(tk.END, link)

                try:
                    movie_response = requests.get(link)
                    movie_response.raise_for_status()
                    movie_soup = BeautifulSoup(movie_response.content, 'html.parser')
                    m_id_content = movie_soup.find('div', class_='m_i-d-content')
                    m_id_poster = movie_soup.find('div', class_='m_i-d-poster')
                    
                    img_url = None
                    if m_id_poster:
                        poster_element = m_id_poster.find('div' , class_='film-poster')
                        img_tag = poster_element.find('img') if poster_element else None
                        img_url = img_tag['src'] if img_tag else None
                    
                    if m_id_content:
                        heading_element = m_id_content.find('h2', class_='heading-name')
                        heading_link = heading_element.find('a') if heading_element else None
                        movie_name = heading_link.text.strip() if heading_link else "Unknown"

                        stats = m_id_content.find('div', class_='stats')
                        rating = None
                        if stats:
                            rating_element = stats.find('i', class_='fas fa-star mr-2')
                            rating = float(rating_element.next_sibling.strip()) if rating_element else None
                       
                            row_lines = m_id_content.find_all('div', class_='row-line')
                            if len(row_lines) >= 3:
                                release_year_div = row_lines[2] 
                                release_date_text = release_year_div.get_text(strip=True)
                                release_date = release_date_text.replace("Released:", "").strip()
                                print("Release Date:", release_date)
                            else:
                                print("Release year information not found")
                                
                            row_lines = m_id_content.find_all('div', class_='row-line')
                            
                        if len(row_lines) >= 2:
                            genre_div = row_lines[1]  # Second occurrence
                            genre_links = genre_div.find_all('a')
                            genres = [link.get_text(strip=True) for link in genre_links]
                            print("Genres:", genres)
                        else:
                            print("Genre information not found")
                                
                                
                except Exception as e:
                    link_listbox.insert(tk.END, f"Error processing movie page: {link}, Error: {e}")

        print(movies)

    except requests.RequestException as e:
        show_error(f"Error fetching URL: {e}")
        
        
        
def show_error(message):
    error_window = tk.Toplevel()
    error_window.title("Error")
    
    error_label = tk.Label(error_window, text=message,width=50,height=50)
    error_label.pack(padx=10, pady=10)
    
    ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
    ok_button.pack(pady=10)
   
        

if __name__=="__main__":
    gui()