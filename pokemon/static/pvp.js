function swapAttackButton(firstPlayerAttacking){
    fetch('/renderCardButtons')
        .then(template => template.text())
        .then(template => {
            console.log(template);
            if (firstPlayerAttacking == false) {
                element = document.getElementById("firstPlayerAttackBtn");
                element.innerHTML = template;
                element.classList.remove("invisible");
                element = document.getElementById("secondPlayerAttackBtn");
                element.classList.add("invisible");
            }
            else {
                element = document.getElementById("secondPlayerAttackBtn");
                element.innerHTML = template;
                element.classList.remove("invisible");
                element = document.getElementById("firstPlayerAttackBtn");
                element.classList.add("invisible");
            }
        });
}

function attack(attackType) {
    console.log(attackType);
    fetch('/attack/' + attackType)
        .then(attackList => attackList.json())
        .then(attackList => {
            console.log(attackList);
            const damage = attackList[0]; //make animation attack with this damage
            var hp = attackList[1];
            const firstPlayerAttacking = attackList[2];
            const gameStage = attackList[3];
            swapAttackButton(firstPlayerAttacking);
            playAnimations(firstPlayerAttacking, attackList);
            //attack animation function with firstPlayerAttacking as argument
            if (gameStage == 0) {
                if (firstPlayerAttacking == true){
                    showInitialCard('secondPlayerDeck', 'secondPlayerCard',attackList);
                }
                else {
                    showInitialCard('firstPlayerDeck', 'firstPlayerCard', attackList);
                }
            }
            else{
            updateHP(attackList);
            }
        });
}

function winCheck(){
    fetch('/winCheck')
        .then(roundInfoDict => roundInfoDict.json())
        .then(roundInfoDict => {
            console.log(roundInfoDict);
            const gameOver = roundInfoDict.gameOver;
            const beginningPlayerTopCard = roundInfoDict.beginningPlayerTopCard;
            const attackTypes = roundInfoDict.attackTypes;
            var firstPlayerAttacking = roundInfoDict.firstPlayerAttacking;
            const firstPlayerCounter = roundInfoDict.firstPlayerCounter;
            const secondPlayerCounter = roundInfoDict.secondPlayerCounter;
            const timeout = 3000;
            setTimeout(() => {
                updateCardCount();
                if (firstPlayerAttacking) {
                    element = document.getElementById("secondPlayerCard");
                    element.innerHTML = "";
                    element.removeAttribute('style');
                }
                else{
                    element = document.getElementById("firstPlayerCard");
                    element.innerHTML = "";
                    element.removeAttribute('style');
                }
                 if (!gameOver){
                    buttonSwap = firstPlayerAttacking !== true;
                    swapAttackButton(buttonSwap);
                }
            }, timeout);


                element = document.getElementById("firstPlayerAttackBtn");
                element.classList.remove("visible");
                element.classList.add("invisible");
                element = document.getElementById("secondPlayerAttackBtn");
                element.classList.remove("visible");
                element.classList.add("invisible");
                if (gameOver) {
                    document.getElementById("secondPlayerCard").removeAttribute('style');
                    document.getElementById("firstPlayerCard").removeAttribute('style');
                    if (firstPlayerAttacking){
                        noCardCheck('firstPlayerDeck', 'firstPlayerCard');
                    }
                    else {
                        noCardCheck('secondPlayerDeck', 'secondPlayerCard');
                    }
                }

        });

}