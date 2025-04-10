const btnDropdown = document.getElementById('btn-dropdown');
const dropDownBox = document.getElementById('dropdown-box');
const dropdown = document.getElementById('dropdown');

btnDropdown.addEventListener('click', () => {
    dropdown.classList.toggle('hidden');
    dropdown.innerHTML = dropdown.classList.contains('hidden') ?
        'MENU &nbsp; <i class="fa-solid fa-caret-down"></i>' :
        'MENU &nbsp; <i class="fa-solid fa-xmark"></i>';
});


dropDownBox.addEventListener('mouseleave', () => {
    dropdown.classList.add('hidden');
    dropdown.innerHTML = 'MENU &nbsp; <i class="fa-solid fa-caret-down"></i>';
});