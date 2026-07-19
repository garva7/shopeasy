document.addEventListener('DOMContentLoaded', function () {
    const modalEl = document.getElementById('logout-modal');
    const forms = document.querySelectorAll('.logout-form');
    if (!modalEl || !forms.length) return;

    const modal = new bootstrap.Modal(modalEl);
    const confirmBtn = document.getElementById('logout-confirm');
    let pendingForm = null;

    forms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            // Already confirmed - let this one through.
            if (form.dataset.confirmed === 'true') return;
            e.preventDefault();
            pendingForm = form;
            modal.show();
        });
    });

    confirmBtn.addEventListener('click', function () {
        if (!pendingForm) return;
        // Re-submit through the form so the CSRF token still goes with it.
        pendingForm.dataset.confirmed = 'true';
        modal.hide();
        pendingForm.submit();
    });
});
