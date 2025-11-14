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
        # --- NUEVO AVISO ---
        if len(rented) > 0:
            print_newline_then("You still have movies to return.")
        # --------------------

        st.session_state.phase = "done"
        print_line("Thank you for using our returning service. See you soon!")
        st.session_state.prompt_mode = None
        st.rerun()
        return

    if 1 <= selection <= len(rented):
        title = catalog[rented[selection - 1] - 1]
        print_newline_then("You have returned " + title)
        rented.pop(selection - 1)

        if len(rented) == 0:
            print_line("You have not rented movies.")
            st.session_state.phase = "done"
            st.session_state.prompt_mode = None
            st.rerun()
            return
        else:
            print_rented_list_and_prompt()
            return
    else:
        print_newline_then("Invalid movie number. Please try again.")
        print_rented_list_and_prompt()
        return