console.log('Hello from main.js');

const head = document.getElementById('head');
if (head) {
    const goBackBtn = document.getElementById('go-back-btn');
    if (goBackBtn) {
        goBackBtn.addEventListener('click', () => {
            history.back();
        });
    }
}