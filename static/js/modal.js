// Modal for delete juice
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('[data-bs-toggle="modal"][data-bs-target="#deleteJuiceModal"]');
    const deleteForm = document.getElementById('deleteForm');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const juiceId = this.getAttribute('data-id');
            deleteForm.action = '/user/juice/delete/' + juiceId;
        });
    });
});



// Modal for delete fruit
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('[data-bs-toggle="modal"][data-bs-target="#deleteFruitModal"]');
    const deleteForm = document.getElementById('deleteForm');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const fruitId = this.getAttribute('data-id');
            deleteForm.action = '/admin/fruit/delete/' + fruitId;
        });
    });
});


