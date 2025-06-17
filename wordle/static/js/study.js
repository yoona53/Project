// 検索条件をクリアする関数
function resetForm() {
    const form = document.querySelector('form');
    form.querySelector('input[name="q"]').value = '';
    form.querySelector('select[name="level"]').value = 'all';
    form.submit();
}

// 列のブラインド処理をする関数
function toggleColumn(className) {
    const cells = document.querySelectorAll('.' + className);
    cells.forEach(cell => {
        cell.style.display = (cell.style.display === 'none') ? '' : 'none';
    });
}

// 列を表示・非表示する関数
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