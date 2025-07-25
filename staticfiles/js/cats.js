function openEditForm(catId) {
    fetch(`/cats/edit/${catId}/`)
    .then(response => response.text())
    .then(html => {
        document.getElementById('editModal').innerHTML = html;
        document.getElementById('editModal').classList.add('active');
    });
}

function closeModal() {
    document.getElementById('editModal').classList.remove('active');
}

function submitEditForm(event, catId) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    fetch(`/cats/edit/${catId}/`, {
    method: 'POST',
    body: formData,
    headers: {'X-Requested-With': 'XMLHttpRequest'},
    credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
    if(data.success){
        alert('Gato actualizado');
        closeModal();
        location.reload(); // Para simplificar, recargamos la lista
    } else {
        alert('Errores: ' + JSON.stringify(data.errors));
    }
    });
}
