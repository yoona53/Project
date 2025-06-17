 function btnClick(){
    const hint = document.getElementById('kanji-div');
    const button = document.getElementById('kanji-button');

    const isHidden = window.getComputedStyle(hint).display === 'none';

    if(isHidden){
        // ヒントを表示する
        hint.style.display = 'block';
        // ボタンのテキストを変更
        button.textContent = '漢字ヒントを非表示';
    }else{
        // ヒントを非表示する
        hint.style.display = 'none';
        // ボタンのテキストを変更
        button.textContent = '漢字ヒントを表示';
    }
}