document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.classList.add('fade-out');
        }, 1500);
    });
});


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



document.addEventListener("DOMContentLoaded", function() {
    const flashMessageContainer = document.getElementById("flash-message-container");

    if (flashMessageContainer && flashMessageContainer.querySelector(".flash-message")) {
        flashMessageContainer.style.display = "block"; // Show flash message container
        
        setTimeout(function() {
            flashMessageContainer.style.display = "none"; // Hide after 5 seconds
        }, 2000); // 5 seconds
    }
});
