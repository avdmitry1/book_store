const copyButton = document.getElementById('copy-btn-box');
const bookIdElement = document.getElementById('book-id-box');

copyButton.addEventListener('click', () => {
    const bookId = bookIdElement.textContent;
    navigator.clipboard.writeText(bookId).then(() => {
        copyButton.innerText = 'Copied!';
    });
});
