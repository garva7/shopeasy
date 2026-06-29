document.addEventListener('DOMContentLoaded', function () {
    // Password show/hide toggle
    const toggle = document.getElementById('toggle-password');
    const password = document.getElementById('password');
    if (toggle && password) {
        toggle.addEventListener('click', function () {
            if (password.type === 'password') {
                password.type = 'text';
                toggle.textContent = 'Hide';
            } else {
                password.type = 'password';
                toggle.textContent = 'Show';
            }
        });
    }

    // Form validation
    const loginForm = document.querySelector('form[action="/login"]');
    const registerForm = document.querySelector('form[action="/register"]');

    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            if (!validateLogin()) {
                e.preventDefault();
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', function (e) {
            if (!validateRegister()) {
                e.preventDefault();
            }
        });
    }

    function validateLogin() {
        clearErrors();
        let valid = true;

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!email) {
            showError('email', 'Email is required.');
            valid = false;
        } else if (!emailRegex.test(email)) {
            showError('email', 'Enter a valid email address.');
            valid = false;
        }

        if (!password) {
            showError('password', 'Password is required.');
            valid = false;
        } else if (password.length < 6) {
            showError('password', 'Password must be at least 6 characters.');
            valid = false;
        }

        return valid;
    }

    function validateRegister() {
        clearErrors();
        let valid = true;

        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const phone = document.getElementById('phone').value.trim();
        const password = document.getElementById('password').value;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const phoneRegex = /^[0-9]{10}$/;

        if (!name) {
            showError('name', 'Name is required.');
            valid = false;
        }

        if (!email) {
            showError('email', 'Email is required.');
            valid = false;
        } else if (!emailRegex.test(email)) {
            showError('email', 'Enter a valid email address.');
            valid = false;
        }

        if (phone && !phoneRegex.test(phone)) {
            showError('phone', 'Enter a valid 10-digit phone number.');
            valid = false;
        }

        if (!password) {
            showError('password', 'Password is required.');
            valid = false;
        } else if (password.length < 6) {
            showError('password', 'Password must be at least 6 characters.');
            valid = false;
        }

        return valid;
    }

    function showError(fieldId, message) {
        const field = document.getElementById(fieldId);
        if (field) {
            field.classList.add('is-invalid');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback d-block';
            errorDiv.textContent = message;
            field.parentNode.appendChild(errorDiv);
        }
    }

    function clearErrors() {
        document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
        document.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
    }
});
