function resetForm() {
    const form = document.querySelector('form');
    form.querySelector('input[name="q"]').value = '';
    form.querySelector('select[name="level"]').value = 'all';
    form.submit();
}

function toggleColumn(className) {
    const cells = document.querySelectorAll('.' + className);
    cells.forEach(cell => {
        cell.style.display = (cell.style.display === 'none') ? '' : 'none';
    });
}

function toggleContent(className) {
    const cells = document.querySelectorAll('.' + className);
    cells.forEach(cell => {
    if (cell.classList.contains('hidden-text')) {
        cell.classList.remove('hidden-text');
    } else {
        cell.classList.add('hidden-text');
    }
    });
}