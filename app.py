import streamlit as st

# -----------------------------
# Initialization
# -----------------------------
def init_state():
    if "initialized" in st.session_state:
        return
    st.session_state.initialized = True

    st.session_state.catalog_movies = [
        "Avengers: Endgame", "Forrest Gump", "Jurassic Park", "Toy Story",
        "The Shawshank Redemption", "Mad Max: Fury Road", "The Dark Knight",
        "Inception", "The Lion King", "Spirited Away"
    ]
    st.session_state.genres = [
        "Action", "Drama", "Science Fiction", "Animation", "Drama",
        "Action", "Action", "Science Fiction", "Animation", "Animation"
    ]

    st.session_state.rented_movies = []      # stores catalog positions 1..N
    st.session_state.last_rented_genre = ""
    st.session_state.phase = "rent"          # rent -> return -> done
    st.session_state.log = []
    st.session_state.prompt_mode = None      # "rent" or "return" (control de impresión)

def print_line(s=""):
    st.session_state.log.append(s)

def print_newline_then(s):
    st.session_state.log.append("")
    st.session_state.log.append(s)

def render_console(placeholder):
    placeholder.code("\n".join(st.session_state.log), language=None)

# -----------------------------
# Printing helpers (exact texts)
# -----------------------------
def print_catalog_and_prompt():
    print_newline_then("Movie Catalog:")
    for i, title in enumerate(st.session_state.catalog_movies):
        g = st.session_state.genres[i]
        print_line(f"{i + 1}) {title} ({g})")
    print_newline_then("What movie would you like to rent (enter the number or '0' to exit)?")
    st.session_state.prompt_mode = "rent"

def print_rented_list_and_prompt():
    rented = st.session_state.rented_movies
    catalog = st.session_state.catalog_movies
    genres = st.session_state.genres

    print_newline_then("Rented Movies:")
    for i in range(len(rented)):
        movie = catalog[rented[i] - 1]
        genre = genres[rented[i] - 1]
        print_line(f"{i + 1}) {movie} ({genre})")
    print_newline_then("Which movie would you like to return (enter the number or '0' to exit)?")
    st.session_state.prompt_mode = "return"

# -----------------------------
# Rent Phase
# -----------------------------
def process_rent_input(user_text):
    # Igual que en consola: si no es entero, lo tratamos como inválido
    try:
        selection = int(user_text.strip())
    except Exception:
        print_newline_then("Invalid movie number. Please try again.")
        print_catalog_and_prompt()
        return

    catalog = st.session_state.catalog_movies
    genres = st.session_state.genres
    rented = st.session_state.rented_movies

    if selection == 0:
        # salir de alquiler y pasar a devolución
        print_newline_then("Thank you for using our rental service. See you soon!")
        st.session_state.phase = "return"
        # inmediatamente mostrar lista de alquiladas (aunque esté vacía, el original pasa a devolución)
        if len(rented) == 0:
            print_line("You have not rented movies.")
            st.session_state.phase = "done"
            st.session_state.prompt_mode = None
            st.rerun()
        else:
            print_rented_list_and_prompt()
            st.rerun()
        return

    if 1 <= selection <= len(catalog) and selection not in rented:
        # alquiler válido
        rented.append(selection)
        st.session_state.last_rented_genre = genres[selection - 1]
        print_newline_then("You have rented " + catalog[selection - 1])

        # recomendaciones
        print_newline_then("Based on your last rental, we recommend:")
        for i in range(len(catalog)):
            current = i + 1
            if genres[i] == st.session_state.last_rented_genre and current not in rented:
                print_line(f"{current}) {catalog[i]}")

        # inmediatamente volver a imprimir el catálogo y repreguntar
        print_catalog_and_prompt()
        return

    elif selection in rented:
        print_newline_then("You have already rented this movie. Please try again.")
        print_catalog_and_prompt()
        return

    else:
        print_newline_then("Invalid movie number. Please try again.")
        print_catalog_and_prompt()
        return

def rent_phase():
    console_placeholder = st.empty()

    # Si todavía no hemos mostrado el catálogo inicial, hazlo ahora
    if st.session_state.prompt_mode != "rent":
        print_catalog_and_prompt()

    # Render arriba
    render_console(console_placeholder)

    # Input debajo
    with st.form("rent_form", clear_on_submit=True):
        user_text = st.text_input("", key="rent_input", label_visibility="collapsed")
        submitted = st.form_submit_button("Enter")
    if submitted:
        process_rent_input(user_text)
        render_console(console_placeholder)

# -----------------------------
# Return Phase
# -----------------------------
def process_return_input(user_text):
    try:
        selection = int(user_text.strip())
    except Exception:
        print_newline_then("Invalid movie number. Please try again.")
        print_rented_list_and_prompt()
        return

    rented = st.session_state.rented_movies
    catalog = st.session_state.catalog_movies

    if selection == 0:
        st.session_state.phase = "done"
        print_newline_then("Thank you for using our returning service. See you soon!")
        st.session_state.prompt_mode = None
        st.rerun()
        return

    if 1 <= selection <= len(rented):
        title = catalog[rented[selection - 1] - 1]
        print_newline_then("You have returned " + title)
        rented.pop(selection - 1)

        if len(rented) == 0:
            # comportamiento del ejemplo: inmediatamente informa que ya no hay alquiladas
            print_line("You have not rented movies.")
            st.session_state.phase = "done"
            st.session_state.prompt_mode = None
            st.rerun()
            return
        else:
            # volver a imprimir la lista actualizada y repreguntar
            print_rented_list_and_prompt()
            return
    else:
        print_newline_then("Invalid movie number. Please try again.")
        print_rented_list_and_prompt()
        return

def return_phase():
    console_placeholder = st.empty()

    # Si no hay alquiladas, terminar igual que el script original
    if len(st.session_state.rented_movies) == 0:
        print_line("You have not rented movies.")
        st.session_state.phase = "done"
        st.session_state.prompt_mode = None
        render_console(console_placeholder)
        return

    # Si no hemos mostrado la lista inicial de devoluciones, hazlo
    if st.session_state.prompt_mode != "return":
        print_rented_list_and_prompt()

    # Render arriba
    render_console(console_placeholder)

    # Input debajo
    with st.form("return_form", clear_on_submit=True):
        user_text = st.text_input("", key="return_input", label_visibility="collapsed")
        submitted = st.form_submit_button("Enter")
    if submitted:
        process_return_input(user_text)
        render_console(console_placeholder)

# -----------------------------
# App Entry
# -----------------------------
st.set_page_config(page_title="Movie Rental (Console-like)", page_icon="🎬", layout="centered")
st.title("Movie Rental – Console-like")

init_state()

if st.session_state.phase == "rent":
    rent_phase()
elif st.session_state.phase == "return":
    return_phase()
else:
    st.code("\n".join(st.session_state.log), language=None)