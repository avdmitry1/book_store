document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("search_form");
    const input = document.getElementById("id_search");

    const BOOK_ID_LENGTH = 36;
    const ISBN_LENGTH = 64;

    if (input) {
        input.focus();

        input.addEventListener("keyup", () => {
            if (input.value.length === BOOK_ID_LENGTH || input.value.length === ISBN_LENGTH) {
                form.submit();
            }
        });
    }
});
