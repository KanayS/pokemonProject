let appendTypesPerCard = (types, card) => {
    types.forEach((item) => {
        let span = document.createElement("SPAN");
        span.textContent = item.charAt(0).toUpperCase() + item.slice(1);
        console.log("."+ card +"Types")
        document.querySelector("."+ card +"Types").appendChild(span);
        });
};

let styleCardID = (color, cardID, card) => {
    cardID.style.background = `radial-gradient(circle at 50% 0%, ${color} 36%, #ffffff 36%)`;
    cardID.querySelectorAll("." + card + "Types span").forEach((typeColor) => {
        typeColor.style.backgroundColor = color;
        });
};

const typeColor = {
      bug: "#26de81",
      dragon: "#ffeaa7",
      electric: "#fed330",
      fairy: "#FF0069",
      fighting: "#30336b",
      fire: "#f0932b",
      flying: "#81ecec",
      grass: "#00b894",
      ground: "#EFB549",
      ghost: "#a55eea",
      ice: "#74b9ff",
      normal: "#95afc0",
      poison: "#6c5ce7",
      psychic: "#a29bfe",
      rock: "#2d3436",
      water: "#0190FF",
};

function updateCard(pokeDict, playerID, card){
    console.log(pokeDict);
    var element = document.getElementById(playerID);
    element.classList.remove("invisible");
    element.classList.add("visible");
    const mainAttribute = pokeDict['types'][0];
    const themeColor = typeColor[mainAttribute];
    console.log(mainAttribute)
    console.log(themeColor);
    const imgSrc = pokeDict.url;
    const attack = pokeDict.attack;
    const defense = pokeDict.defense;
    const hp = pokeDict.hp;
    const types = pokeDict.types;
    const pokeName = pokeDict.name;
    cardID = document.getElementById(card)

    cardID.innerHTML = `
    <p class="hp">
      <span>HP</span>
        ${hp}
    </p>
    <img src=${imgSrc} />
    <h2 class="poke-name">${pokeName}</h2>
    <div class=${card + "Types"} >

    </div>
    <div class="stats">
      <div>
        <h3>${attack}</h3>
        <p>Attack</p>
      </div>
      <div>
        <h3>${defense}</h3>
        <p>Defense</p>
      </div>
    </div>
`;

appendTypesPerCard(types, card);
styleCardID(themeColor, cardID, card);
}

function showTopCard(cardDeck, cardID){
        fetch('/cycleCard/' + cardDeck)
        .then(topCard => topCard.json())
        .then(topCard => {
            if (topCard !== null){
                updateCard(topCard, cardDeck, cardID);
                updateCardCount();
            }
            else {
                noCardCheck(cardDeck);
            }
        });
}
function noCardCheck(cardDeck){
    if (cardDeck == "firstPlayerDeck") {
        element = document.getElementById("firstPlayerCycle");
        element.classList.add("invisible");
        element = document.getElementById("playerOneCardBack");
        element.classList.remove("cardBack")
        element.classList.add("pikaMeme");
        element = document.getElementById("firstPlayerCard");
        element.classList.remove("cardShadow");
        alert("The first player deck has ran out of cards :(");
    }
    else {
        element = document.getElementById("secondPlayerCycle");
        element.classList.add("invisible");
        element = document.getElementById("playerTwoCardBack");
        element.classList.remove("cardBack");
        element.classList.add("pikaMeme");
        element = document.getElementById("secondPlayerCard");
        element.classList.remove("cardShadow");
        alert("The second player deck has ran out of cards :(");
    }

    element = document.getElementById(cardID);
    element.innerHTML = `
    <h2 class="text-center noCardMsg"> No Cards Left :( </h2>
    `;

}

function updateCardCount() {
    fetch('/updateCardCounter/')
        .then(cardCounts => cardCounts.json())
        .then(topCard => {
        console.log(topCard)
        const playerOneCardCount = topCard[0];
        const playerTwoCardCount = topCard[1];

        var element = document.getElementById("firstPlayerCounter");
        element.innerHTML = playerOneCardCount;
        element = document.getElementById("secondPlayerCounter");
        element.innerHTML = playerTwoCardCount;
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

            swapAttackButton(firstPlayerAttacking);
            return attackList
        });
}

function showInitialCard(cardDeck, cardID, attackList){
    console.log(cardDeck);
    console.log(cardID);
    fetch('/showInitialCard/' + cardDeck)
        .then(topCard => topCard.json())
        .then(topCard => {
            if (topCard !== null){
                updateCard(topCard, cardDeck, cardID);
                updateCardCount();
                if (attackList){
                updateHP(attackList);
                }
            }
            else {
                noCardCheck(cardDeck);
            }
        });
}

function swapAttackButton(firstPlayerAttacking){
    fetch('/renderCardButtons')
        .then(template => template.text())
        .then(template => {
            console.log(template);
            if (firstPlayerAttacking == false) {
                element = document.getElementById("firstPlayerAttackBtn");
                element.innerHTML = template
                element.classList.remove("invisible")
                element = document.getElementById("secondPlayerAttackBtn");
                element.classList.add("invisible");
            }
            else {
                element = document.getElementById("secondPlayerAttackBtn");
                element.innerHTML = template
                element.classList.remove("invisible")
                element = document.getElementById("firstPlayerAttackBtn");
                element.classList.add("invisible");
            }
        });
}

function updateHP(attackList) {
    console.log(attackList);
    const hp = attackList[1];
    const firstPlayerAttacking = attackList[2];
    if (firstPlayerAttacking == true){
        element = document.getElementById('secondPlayerCard');
        console.log(document.querySelector("#secondPlayerCard"));
        console.log(document.querySelector("#secondPlayerCard .hp"));
        document.querySelector("#secondPlayerCard .hp").innerHTML = `
        <span>HP</span>
        ${hp}
        `;
    }
    else {
        element = document.getElementById('firstPlayerCard');
        console.log(document.querySelector("#firstPlayerCard"));
        console.log(document.querySelector("#firstPlayerCard .hp"));
        document.querySelector("#firstPlayerCard .hp").innerHTML = `
        <span>HP</span>
        ${hp}
        `;
    }

}