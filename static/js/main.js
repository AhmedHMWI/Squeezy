document.querySelectorAll('.delete-juice-btn').forEach(function (button) {
    button.addEventListener('click', function (e) {
        e.preventDefault();

        const juiceId = this.getAttribute('data-juice-id');
        const url = `/user/juice/delete/${juiceId}`;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token() }}'  // CSRF protection if needed
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Remove the juice element from the page without reloading
                document.getElementById('juice-' + juiceId).remove(); // Remove the deleted juice row
                alert(data.message);  // Show success message
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting juice');
        });
    });
});