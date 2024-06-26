import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from tkinter import Scrollbar


movies = {}
review_entry = None
happiness_var = None
review_window = None
main_window = None
DO_NOT_SHOW_FILE = "do_not_show_review.txt"


def send_email(review, happiness_meter):
    email_sender = "binasahmed8@gmail.com"
    email_receiver = "random08296@gmail.com"
    password = "dnbw xfqq rypv obds"

    subject = "Movie App Review, what should we improve on or changes we should make which will improve my application?"
    body = f"heres the users Review: {review}\n and the Happiness Meter: {happiness_meter}"

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(email_sender, password)
        smtp.send_message(msg)
    print("Email sent successfully.")

def gui():
    global main_window

    WIDTH = 1000
    HEIGHT = 500

    main_window = tk.Tk()
    main_window.title("MOVIE FILTER APPLICATION")
    main_window.geometry(f"{WIDTH}x{HEIGHT}")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TFrame", background="#f0f0f0")  

    title_bar = tk.Frame(main_window, height=20)
    title_bar.pack(fill=tk.X)

    heading = tk.Label(title_bar, text="ULTIMATE MOVIE FILTER", font=('Times New Roman', 20), fg="#000099", bg="#f0f0f0")
    heading.pack(ipadx=25, ipady=10)

    search_bar(main_window)
    option_section(main_window)
    
    
    main_window.protocol("WM_DELETE_WINDOW", on_closing)
    main_window.mainloop()


def search_bar(window):
    global search_var, frame

    search_var = tk.StringVar()
    frame = ttk.Frame(window)
    frame.pack(padx=20, pady=20, fill=tk.X)

    heading_search = tk.Label(frame, text="Paste the Link of the page to search", fg="#000099",
                               font=('Helvetica', 12))
    heading_search.grid(row=1, column=1, padx=(0, 5))

    search_entry = ttk.Entry(frame, textvariable=search_var, width=25)
    search_entry.grid(row=1, column=0, padx=(0, 5))
    search_entry.config(font=('Helvetica', 12))


def validate_numeric_input(P):
    if re.match(r'^\d*$', P):
        return True
    return False


def option_section(window):
    global ratings_var, genre_var, count_var, button_frame, movie_frame

    frame_heading = ttk.Frame(window)
    frame_heading.pack(padx=5, pady=(5, 0), fill=tk.X)

    heading_opt = tk.Label(frame_heading, text="FILTER", fg="#000099", font=('Helvetica', 20))
    heading_opt.grid(row=0, column=0, padx=20, pady=10)

    frame = ttk.Frame(window)
    frame.pack(padx=20, pady=5, fill=tk.X)

    ratings_label = tk.Label(frame, text="Ratings:", fg="#000099", font=('Helvetica', 12))
    ratings_label.grid(row=0, column=0, padx=5, pady=0, sticky='e')

    ratings_var = tk.StringVar()
    ratings_opt = ["Any", "1 - 2", "3 - 4", "5 - 6", "7 - 8", "9 - 10"]
    ratings_dropdown = ttk.Combobox(frame, textvariable=ratings_var, values=ratings_opt, font=('Helvetica', 12))
    ratings_dropdown.grid(row=0, column=1, padx=5, pady=0, sticky='w')
    ratings_dropdown.set("Any")

    genre_label = tk.Label(frame, fg="#000099", text="Genre:", font=('Helvetica', 12))
    genre_label.grid(row=1, column=0, padx=5, pady=(25, 0), sticky='e')

    genre_var = tk.StringVar()
    genre_opt = ["Any", "Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi",
                 "Thriller"]
    genre_dropdown = ttk.Combobox(frame, textvariable=genre_var, values=genre_opt, font=('Helvetica', 12))
    genre_dropdown.grid(row=1, column=1, padx=5, pady=(25, 0), sticky='w')
    genre_dropdown.set("Any")

    count_label = tk.Label(frame, text="Count of Movies:", font=('Helvetica', 12), fg="#000099")
    count_label.grid(row=1, column=2, padx=5, pady=(25, 0), sticky='e')

    count_var = tk.StringVar()
    count_var.set("1")

    validate_cmd = (window.register(validate_numeric_input), '%P')
    count_entry = ttk.Entry(frame, textvariable=count_var, validate='key', validatecommand=validate_cmd,
                            font=('Helvetica', 12))
    count_entry.grid(row=1, column=3, padx=5, pady=(25, 0), sticky='w')

    button_frame = ttk.Frame(window)
    button_frame.pack(padx=20, pady=10, fill=tk.X)

    search_button = tk.Button(button_frame, text="Search", command=handle_search)
    search_button.grid(row=0, column=0, padx=10, pady=5)

    clear_button = tk.Button(button_frame, text="Clear", command=clear_movies)
    clear_button.grid(row=0, column=1, padx=10, pady=5)

    movie_frame = ttk.Frame(window)
    movie_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH, expand=True)

class MovieComponent(ttk.Frame):
    def __init__(self, parent, title, year, rating, img_url, youtube_link, movie_link, genre):
        super().__init__(parent)

        self.title = title
        self.year = year
        self.rating = rating
        self.img_url = img_url
        self.youtube_link = youtube_link
        self.movie_link = movie_link
        self.genre = genre

        border_frame = ttk.Frame(self, borderwidth=2, relief="solid", width=1000, height=150, style="Dark.TFrame")
        border_frame.pack_propagate(False)
        border_frame.pack(padx=10, pady=12, fill=tk.X)

        self.image_label = ttk.Label(border_frame)
        self.image_label.grid(row=0, column=0, rowspan=4, padx=10, pady=10)
        self.load_image(img_url)

        opt_frame = ttk.Frame(border_frame, style="Dark.TFrame")
        opt_frame.grid(row=0, column=1, sticky='n')

        title_label = ttk.Label(opt_frame, text=f"Title: {title}", font=('Comic Sans MS', 12),background="#DDDDDD" , style="Light.TLabel")
        title_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        year_label = ttk.Label(opt_frame, text=f"Year: {year}", background="#F0F0F0", font=('Comic Sans MS', 12), style="Light.TLabel")
        year_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        rating_label = ttk.Label(opt_frame, text=f"Rating: {rating}", background="#F0F0F0",font=('Comic Sans MS', 12), style="Light.TLabel")
        rating_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        genre_label = ttk.Label(opt_frame, text=f"Genre: {genre}", background="#F0F0F0" , font=('Comic Sans MS', 12), style="Light.TLabel")
        genre_label.grid(row=2, column=1, padx=200, pady=5, sticky='w')

        youtube_button = ttk.Button(opt_frame, text="Trailer", command=self.open_youtube, style="Dark.TButton")
        youtube_button.grid(row=4, column=0, padx=10, pady=25, sticky='w')

        movie_button = ttk.Button(opt_frame, text="Movie", command=self.open_movie, style="Dark.TButton")
        movie_button.grid(row=4, column=1, padx=10, pady=25, sticky='w')



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
            url = "https://swatchseries.is/genre/family"

        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        links_set = set()
        global movies
        movies = {}

        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]

        for link in links:
            if '/watch-' in link and link not in links_set:
                links_set.add(link)
                try:
                    movie_response = requests.get(link)
                    movie_response.raise_for_status()
                    movie_soup = BeautifulSoup(movie_response.content, 'html.parser')
                    m_id_content = movie_soup.find('div', class_='m_i-d-content')
                    m_id_poster = movie_soup.find('div', class_='m_i-d-poster')

                    img_url = None

                    if m_id_poster:
                        poster_element = m_id_poster.find('div', class_='film-poster')
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
                            rating_text = rating_element.next_sibling.strip() if rating_element else None
                            try:
                                rating = float(rating_text)
                            except (ValueError, TypeError):
                                rating = None
                                print(f"Rating conversion error: {rating_text}")

                        rating_filter = ratings_var.get()
                        selected_genre = genre_var.get()

                        if rating_filter == "Any" or \
                                (rating_filter == "1 - 2" and rating and rating <= 2) or \
                                (rating_filter == "3 - 4" and rating and 3 <= rating <= 4) or \
                                (rating_filter == "5 - 6" and rating and 5 <= rating <= 6) or \
                                (rating_filter == "7 - 8" and rating and 7 <= rating <= 8) or \
                                (rating_filter == "9 - 10" and rating and rating >= 9):
                            row_lines = m_id_content.find_all('div', class_='row-line')
                            release_date = None
                            genres = []

                            for line in row_lines:
                                span = line.find('span', class_='type')
                                if span:
                                    if span.text.strip() == 'Released:':
                                        release_date = line.get_text(strip=True).replace("Released:", "").strip()
                                    elif span.text.strip() == 'Genre:':
                                        genre_links = line.find_all('a')
                                        genres = [link.get_text(strip=True) for link in genre_links]

                            if selected_genre == "Any" or selected_genre in genres:
                                movies[movie_name] = {
                                    'link': link,
                                    'rating': rating,
                                    'release_date': release_date,
                                    'genres': genres,
                                    'img_url': img_url
                                }

                                print("Movie added:", movies[movie_name])
                except Exception as e:
                    print(f"Error processing movie at {link}: {e}")
                    continue

        if not movies:
            show_error("No movies found matching the criteria!")

        create_movie_components()
        print("All movies:", movies)

    except requests.RequestException as e:
        show_error(f"Error fetching URL: {e}")




        
            

def display_movies(movies, count):
    clear_movies()

    canvas = tk.Canvas(movie_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(movie_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    inner_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    for i, (movie_name, movie_data) in enumerate(movies.items()):
        if i >= count:
            break
        movie_component = MovieComponent(inner_frame, title=movie_name, year=movie_data['release_date'],
                                         rating=movie_data['rating'],
                                         img_url=movie_data['img_url'],
                                         youtube_link=f"https://www.youtube.com/results?search_query={'+'.join(movie_name.split())}",
                                         movie_link=movie_data['link'], genre=", ".join(movie_data['genres']))
        movie_component.pack(fill=tk.X, padx=10, pady=5)

    inner_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    
    
def create_movie_components():
    count = int(count_var.get()) 
    display_movies(movies, count)



def clear_movies():
    for widget in movie_frame.winfo_children():
        widget.destroy()


def show_error(message):
    messagebox.showerror("Error", message)


def on_closing():
    global review_window
    if not os.path.exists(DO_NOT_SHOW_FILE):
        open_review_prompt()
    else:
        main_window.destroy()


def open_review_prompt():
    global review_entry, happiness_var, review_window

    review_window = tk.Toplevel()
    review_window.title("Review")
    review_window.geometry("300x250")

    review_label = tk.Label(review_window, text="Please leave a review:", font=('Helvetica', 12))
    review_label.pack(pady=10)

    review_entry = tk.Entry(review_window, font=('Helvetica', 12), width=30)
    review_entry.pack(pady=5)

    happiness_label = tk.Label(review_window, text="How satisfied are you with the app?", font=('Helvetica', 12))
    happiness_label.pack(pady=5)

    happiness_var = tk.IntVar()
    happiness_scale = tk.Scale(review_window, from_=1, to=10, orient=tk.HORIZONTAL, variable=happiness_var)
    happiness_scale.pack(pady=5)

    button_frame = tk.Frame(review_window)
    button_frame.pack(pady=10)

    submit_button = tk.Button(button_frame, text="Submit", command=submit_review)
    submit_button.grid(row=0, column=0, padx=5)

    cancel_button = tk.Button(button_frame, text="Cancel", command=review_window.destroy)
    cancel_button.grid(row=0, column=1, padx=5)

    if not os.path.exists(DO_NOT_SHOW_FILE):
        do_not_show_checkbox = tk.Button(review_window, text="Don't show this box again", command=disable_review_prompt)
        do_not_show_checkbox.pack()

    review_window.protocol("WM_DELETE_WINDOW", close_all_window)

def submit_review():
    global review_window
    review = review_entry.get()
    happiness_meter = happiness_var.get()
    send_email(review, happiness_meter)
    review_window.destroy()
    main_window.destroy()


def disable_review_prompt():
    global review_window
    with open(DO_NOT_SHOW_FILE, 'w') as file:
        file.write("delete this file to disable the review box?")
    review_window.destroy()
    main_window.destroy()


def close_all_window():
    if review_window:
        review_window.destroy()
    if main_window:
        main_window.destroy()


if __name__ == "__main__":
    gui()
