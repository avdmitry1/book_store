document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("search_form");
    const input = document.getElementById("id_search");

    if (input) {
        input.focus();

        input.addEventListener("keyup", () => {
            if (input.value.length === 24) {
                form.submit();
            }
        });
    }
});
