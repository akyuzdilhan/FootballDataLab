document.addEventListener('click', function(event) {
    var targetElement = event.target;

    while (targetElement != null) {
        if (targetElement.classList && targetElement.classList.contains('view-full-list-button')) {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            break;
        }
        targetElement = targetElement.parentElement;
    }
});
