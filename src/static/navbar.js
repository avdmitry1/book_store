const btnDropdown = document.getElementById('btn-dropdown');
const dropdownMenu = document.getElementById('dropdown'); // Меню (список)
const dropdownBox = document.getElementById('dropdown-box'); // Контейнер меню

if (btnDropdown && dropdownMenu && dropdownBox) {
    // Константи для тексту кнопки 
    const MENU_CLOSED_HTML = 'MENU &nbsp; <i class="fa-solid fa-caret-down"></i>';
    const MENU_OPENED_HTML = 'MENU &nbsp; <i class="fa-solid fa-xmark"></i>';

    btnDropdown.addEventListener('click', () => {
        const isHidden = dropdownMenu.classList.toggle('hidden');

        // Змінюємо іконку при натисканні
        btnDropdown.innerHTML = isHidden ? MENU_CLOSED_HTML : MENU_OPENED_HTML;
        // Оновлюємо атрибут доступності
        btnDropdown.setAttribute('aria-expanded', !isHidden);
    });

    dropdownBox.addEventListener('mouseleave', () => {
        // Скриваєм меню
        dropdownMenu.classList.add('hidden');
        // Повертаємо іконку
        btnDropdown.innerHTML = MENU_CLOSED_HTML;
        // Оновлюємо атрибут доступності
        btnDropdown.setAttribute('aria-expanded', 'false');
    });
} else {
    console.error('Один из элементов не найден');
}