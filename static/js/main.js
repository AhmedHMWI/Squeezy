function setDeleteFormAction(actionUrl) {
    document.getElementById("deleteForm").action = actionUrl;
}

document.addEventListener('DOMContentLoaded', function() {
    // Handle image preview change
    const imageInput = document.getElementById('imageInput');
    if (imageInput) {
        imageInput.addEventListener("change", function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById("preview").src = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Handle flash message fade-out after 2 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.classList.add('fade-out');
        }, 2000);
    });

    // Toggle password visibility
    const togglePassword = document.querySelector('.toggle-password');
    if (togglePassword) {
        togglePassword.addEventListener('click', function () {
            const passwordField = document.getElementById('password');
            const icon = this.querySelector('i');
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                icon.classList.replace('fa-eye', 'fa-eye-slash');
            } else {
                passwordField.type = 'password';
                icon.classList.replace('fa-eye-slash', 'fa-eye');
            }
        });
    }

    // Modal for delete juice
    const deleteJuiceButtons = document.querySelectorAll('[data-bs-toggle="modal"][data-bs-target="#deleteJuiceModal"]');
    const deleteJuiceForm = document.getElementById('deleteForm');

    deleteJuiceButtons.forEach(button => {
        button.addEventListener('click', function() {
            const juiceId = this.getAttribute('data-id');
            deleteJuiceForm.action = '/user/juice/delete/' + juiceId;
        });
    });

    // Modal for delete fruit
    const deleteFruitButtons = document.querySelectorAll('[data-bs-toggle="modal"][data-bs-target="#deleteFruitModal"]');
    deleteFruitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const fruitId = this.getAttribute('data-id');
            deleteJuiceForm.action = '/admin/fruit/delete/' + fruitId;
        });
    });
});

// Dark mode toggle functionality
const currentTheme = localStorage.getItem('theme');
document.documentElement.setAttribute('data-theme', currentTheme || 'light');

function toggleTheme() {
    let theme = document.documentElement.getAttribute('data-theme');
    const newTheme = theme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}
