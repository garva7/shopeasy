document.addEventListener('DOMContentLoaded', function () {
    const modalEl = document.getElementById('out-of-stock-modal');
    if (!modalEl) return;

    const modal = new bootstrap.Modal(modalEl);
    const messageEl = document.getElementById('out-of-stock-message');

    document.querySelectorAll('.cart-update-form').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const input = form.querySelector('input[name="quantity"]');
            const stock = parseInt(input.dataset.stock, 10);
            const qty = parseInt(input.value, 10);

            // Let native validation / server handle empty or non-positive values
            if (isNaN(qty) || qty < 1) return;

            if (qty > stock) {
                e.preventDefault();
                if (stock <= 0) {
                    messageEl.textContent = 'This item is currently out of stock.';
                } else {
                    messageEl.textContent = 'Only ' + stock + ' item(s) available in stock.';
                }
                modal.show();
            }
        });
    });
});
