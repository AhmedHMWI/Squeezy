function setDeleteFormAction(actionUrl) {
    document.getElementById("deleteForm").action = actionUrl;
}


document.addEventListener('DOMContentLoaded', function() {
    // Ensure the element exists before adding an event listener
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

    // Handle the flash message fade-out
    const flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.classList.add('fade-out');
        }, 1500);
    });
});


document.addEventListener('DOMContentLoaded', function () {
    // Flash message fade-out behavior
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.classList.add('fade-out');
        }, 1500);
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
});





document.addEventListener("DOMContentLoaded", function() {
    // Find all flash messages
    const flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(function(message) {
        // Set a timeout to hide the message after 1 second
        setTimeout(function() {
            message.classList.add('hidden'); // Apply the 'hidden' class to hide it
        }, 1000); // 1000 ms = 1 second
    });
});












// Modal for delete juice
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('[data-bs-toggle="modal"][data-bs-target="#deleteConfirmModal"]');
    const deleteForm = document.getElementById('deleteForm');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const juiceId = this.getAttribute('data-id');
            // Set the form action dynamically based on the juice ID
            deleteForm.action = '/user/juice/delete/' + juiceId;
        });
    });
});



// Modal for delete fruit
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('[data-bs-toggle="modal"][data-bs-target="#deleteConfirmModal"]');
    const deleteForm = document.getElementById('deleteForm');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const fruitId = this.getAttribute('data-id');
            // Set the form action dynamically based on the fruit ID
            deleteForm.action = '/admin/fruit/delete/' + fruitId;
        });
    });
});







// Check if dark mode is already stored in localStorage
const currentTheme = localStorage.getItem('theme');

if (currentTheme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
} else {
    document.documentElement.setAttribute('data-theme', 'light');
}

// Toggle Dark Mode
function toggleTheme() {
    let theme = document.documentElement.getAttribute('data-theme');

    if (theme === 'light') {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
    }
}
