document.addEventListener('DOMContentLoaded', function () {
    const search = document.getElementById('product-search');
    if (!search) return;

    const cards = document.querySelectorAll('#product-grid .product-col');
    const noResults = document.getElementById('no-results');

    search.addEventListener('input', function () {
        const term = search.value.toLowerCase().trim();
        let visibleCount = 0;

        cards.forEach(function (col) {
            const name = col.querySelector('.card-title').textContent.toLowerCase();
            if (name.indexOf(term) !== -1) {
                col.style.display = '';
                visibleCount++;
            } else {
                col.style.display = 'none';
            }
        });

        if (noResults) {
            noResults.classList.toggle('d-none', visibleCount > 0);
        }
    });
});