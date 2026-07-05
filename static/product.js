document.addEventListener('DOMContentLoaded', function () {
    const info = document.getElementById('product-info');
    if (!info) return;

    const price = parseFloat(info.dataset.price);
    const discount = parseFloat(info.dataset.discount) || 0;
    const stock = parseInt(info.dataset.stock, 10) || 0;

    // Calculate and display the discounted price
    const finalPrice = Math.round(price - (price * discount / 100));
    const finalPriceEl = document.getElementById('final-price');
    if (finalPriceEl) {
        finalPriceEl.textContent = 'Rs. ' + finalPrice;
    }

    // Show In Stock / Out of Stock based on quantity
    const stockBadge = document.getElementById('stock-status');
    if (stockBadge) {
        if (stock > 0) {
            stockBadge.textContent = 'In Stock';
            stockBadge.className = 'badge bg-success';
        } else {
            stockBadge.textContent = 'Out of Stock';
            stockBadge.className = 'badge bg-danger';
        }
    }

    // Disable the Add to Cart button when there's no stock
    const addToCartBtn = document.getElementById('add-to-cart-btn');
    if (addToCartBtn) {
        addToCartBtn.disabled = stock <= 0;
    }
});