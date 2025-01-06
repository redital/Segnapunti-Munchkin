// Salva la posizione di scroll nella session storage
function salvaPosizioneScroll() {
    sessionStorage.setItem('scrollPosition', window.scrollY);
}

// Ripristina la posizione di scroll dalla session storage
function ripristinaPosizioneScroll() {
    const posizioneScroll = sessionStorage.getItem('scrollPosition');
    if (posizioneScroll !== null) {
        window.scrollTo(0, parseInt(posizioneScroll, 10));
    }
}

// Associa gli eventi ai pulsanti dei form
document.addEventListener('DOMContentLoaded', () => {
    // Ripristina la posizione quando la pagina viene caricata
    ripristinaPosizioneScroll();

    // Aggiungi il salvataggio della posizione a ogni pulsante dei form
    const pulsantiForm = document.querySelectorAll('#form-pulsanti button');
    pulsantiForm.forEach(button => {
        button.addEventListener('click', salvaPosizioneScroll);
    });
});
