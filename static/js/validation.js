document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const emailError = document.getElementById("email-error");
    const passwordError = document.getElementById("password-error");

    // Email validation function
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Validate the form when the submit button is clicked
    form.addEventListener("submit", function (e) {
        let isValid = true;
        emailError.textContent = "";
        passwordError.textContent = "";

        // Validate email
        if (!emailInput.value.trim()) {
            emailError.textContent = "يجب إدخال البريد الإلكتروني.";
            isValid = false;
        } else if (!validateEmail(emailInput.value.trim())) {
            emailError.textContent = "يرجى إدخال بريد إلكتروني صحيح.";
            isValid = false;
        }

        // Validate password
        if (!passwordInput.value.trim()) {
            passwordError.textContent = "يجب إدخال كلمة المرور.";
            isValid = false;
        } else if (passwordInput.value.length < 6) {
            passwordError.textContent = "يجب أن تتكون كلمة المرور من 6 أحرف على الأقل.";
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault(); // Prevent form submission if there are errors
        }

        // Hide error messages after 2 seconds
        if (emailError.textContent) {
            setTimeout(function () {
                emailError.textContent = "";
            }, 2000); // 2 seconds
        }

        if (passwordError.textContent) {
            setTimeout(function () {
                passwordError.textContent = "";
            }, 2000); // 2 seconds
        }
    });

    // Show/hide password
    document.querySelector('.toggle-password').addEventListener('click', function () {
        const icon = this.querySelector('i');
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            icon.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            passwordInput.type = "password";
            icon.classList.replace('fa-eye-slash', 'fa-eye');
        }
    });
});
