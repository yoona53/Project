 function btnClick(){
    const hint = document.getElementById('kanji-div');
    const button = document.getElementById('kanji-button');

    const isHidden = window.getComputedStyle(hint).display === 'none';

    if(isHidden){
        hint.style.display = 'block';
        button.textContent = '漢字ヒントを非表示';
    }else{
        hint.style.display = 'none';
        button.textContent = '漢字ヒントを表示';
    }
}