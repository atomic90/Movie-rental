import streamlit as st

# -----------------------------
# Helpers for "console" output
# -----------------------------
def init_state():
    if "initialized" in st.session_state:
        return
    st.session_state.initialized = True

    # Data (exactly as provided)
    st.session_state.catalog_movies = [
        "Avengers: Endgame", "Forrest Gump", "Jurassic Park", "Toy Story",
        "The Shawshank Redemption", "Mad Max: Fury Road", "The Dark Knight",
        "Inception", "The Lion King", "Spirited Away"
    ]
    st.session_state.genres = [
        "Action", "Drama", "Science Fiction", "Animation", "Drama",
        "Action", "Action", "Science Fiction", "Animation", "Animation"
    ]

    # State
    st.session_state.rented_movies = []   # stores positions 1..N
    st.session_state.last_rented_genre = ""
    st.session_state.phase = "rent"       # "rent" -> "return" -> "done"
    st.session_state.prompt_shown = False
    st.session_state.log = []             # list of console lines

def print_line(s=""):
    st.session_state.log.append(s)

def print_with_leading_newline(s):
    st.session_state.log.append("")
    st.session_state.log.append(s)

def show_console():
    # Show as monospaced block, preserving lines
    st.code("\n".join(st.session_state.log) if st.session_state.log else "", language=None)

def process_rent_input(user_text):
    # Expect integer input
    try:
        selection = int(user_text.strip())
    except Exception:
        # In the original console app, a non-integer would raise.
        # To keep a smooth UX, treat non-integers as invalid number.
        print_with_leading_newline("Invalid movie number. Please try again.")
        st.session_state.prompt_shown = False
        return

    catalog = st.session_state.catalog_movies
    genres = st.session_state.genres
    rented = st.session_state.rented_movies

    if selection == 0:
        st.session_state.phase = "return"
        print_with_leading_newline("Thank you for using our rental service. See you soon!")
        st.session_state.prompt_shown = False
        return

    if 1 <= selection <= len(catalog) and selection not in rented:
        # Rent the movie
        rented.append(selection)
        st.session_state.last_rented_genre = genres[selection - 1]
        print_with_leading_newline("You have rented " + catalog[selection - 1])

        # Recommendations
        print_with_leading_newline("Based on your last rental, we recommend:")
        for i in range(len(catalog)):
            current = i + 1
            g = genres[i]
            if g == st.session_state.last_rented_genre and current not in rented:
                print_line(str(current) + ") " + catalog[i])

    elif selection in rented:
        print_with_leading_newline("You have already rented this movie. Please try again.")
    else:
        print_with_leading_newline("Invalid movie number. Please try again.")

    st.session_state.prompt_shown = False

def rent_phase():
    catalog = st.session_state.catalog_movies
    genres = st.session_state.genres

    if not st.session_state.prompt_shown:
        # Prints match original console outputs
        print_with_leading_newline("Movie Catalog:")
        for i in range(len(catalog)):
            movie = catalog[i]
            genre = genres[i]
            print_line(str(i + 1) + ") " + movie + " (" + genre + ")")
        print_with_leading_newline("What movie would you like to rent (enter the number or '0' to exit)? ")
        st.session_state.prompt_shown = True

    with st.form("rent_form", clear_on_submit=True):
        user_text = st.text_input("", key="rent_input", label_visibility="collapsed")
        submitted = st.form_submit_button("Enter")
    if submitted:
        process_rent_input(user_text)

def process_return_input(user_text):
    try:
        selection = int(user_text.strip())
    except Exception:
        print_with_leading_newline("Invalid movie number. Please try again.")
        st.session_state.prompt_shown = False
        return

    catalog = st.session_state.catalog_movies
    rented = st.session_state.rented_movies

    if selection == 0:
        st.session_state.phase = "done"
        print_with_leading_newline("Thank you for using our returning service. See you soon!")
        st.session_state.prompt_shown = False
        return

    if 1 <= selection <= len(rented):
        title = catalog[rented[selection - 1] - 1]
        print_with_leading_newline("You have returned " + title)
        rented.pop(selection - 1)
    else:
        print_with_leading_newline("Invalid movie number. Please try again.")

    st.session_state.prompt_shown = False

def return_phase():
    rented = st.session_state.rented_movies
    catalog = st.session_state.catalog_movies
    genres = st.session_state.genres

    if len(rented) == 0:
        # Exact message and immediate end (matches original)
        print_line("You have not rented movies.")
        st.session_state.phase = "done"
        st.session_state.prompt_shown = False
        return

    if not st.session_state.prompt_shown:
        print_with_leading_newline("Rented Movies:")
        for i in range(len(rented)):
            movie = catalog[rented[i] - 1]
            genre = genres[rented[i] - 1]
            print_line(str(i + 1) + ") " + movie + " (" + genre + ")")
        print_with_leading_newline("Which movie would you like to return (enter the number or '0' to exit)? ")
        st.session_state.prompt_shown = True

    with st.form("return_form", clear_on_submit=True):
        user_text = st.text_input("", key="return_input", label_visibility="collapsed")
        submitted = st.form_submit_button("Enter")
    if submitted:
        process_return_input(user_text)

# -----------------------------
# App entry
# -----------------------------
st.set_page_config(page_title="Movie Rental (Console-like)", page_icon="🎬", layout="centered")
st.title("Movie Rental – Console-like")

init_state()

# Drive the phases
if st.session_state.phase == "rent":
    rent_phase()
elif st.session_state.phase == "return":
    return_phase()
else:
    # done
    pass

# Always display the console log
show_console()