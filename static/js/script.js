document.addEventListener('DOMContentLoaded', function() {
    let content = document.getElementById('page-content');
    if (content) {
        content.style.opacity = 0;
        setTimeout(function() {
            content.style.opacity = 1;
        }, 500);
    }

    let advancedSearchButton = document.querySelector('.btn-link[data-toggle="collapse"]');
    if (advancedSearchButton) {
        advancedSearchButton.addEventListener('click', function() {
            let target = document.querySelector(advancedSearchButton.dataset.target);
            if (target) {
                target.classList.toggle('show');
            }
        });
    }
});
