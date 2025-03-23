const formModal = document.getElementById('form-modal');
const openModalButton = document.getElementById('open-modal-btn');
const closeModalButton = document.getElementById('cancel-btn');
const backdrop = document.getElementById('backdrop');

openModalButton.addEventListener('click', () => {
    formModal.classList.remove('hidden');
});

closeModalButton.addEventListener('click', () => {
    formModal.classList.add('hidden');
});

formModal.addEventListener('click', (event) => {
    if (event.target === backdrop) {
        formModal.classList.add('hidden');
    }
});