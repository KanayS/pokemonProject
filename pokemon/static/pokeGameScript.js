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
    cardID = document.getElementById(card);

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
                noCardCheck(cardDeck,cardID);
            }
        });
}

function noCardCheck(cardDeck, cardID){
    if (cardDeck == "firstPlayerDeck") {
        document.getElementById("playerOneCardBack").classList.remove("cardBack");
        document.getElementById("playerOneCardBack").classList.add("pikaMeme");
        document.getElementById("firstPlayerCard").classList.remove("cardShadow");
        alert("The first player deck has ran out of cards :(");
    }
    else {
        document.getElementById("playerTwoCardBack").classList.remove("cardBack");
        document.getElementById("playerTwoCardBack").classList.add("pikaMeme");
        document.getElementById("secondPlayerCard").classList.remove("cardShadow");
        alert("The second player deck has ran out of cards :(");
    }

    element = document.getElementById(cardID);
    element.innerHTML = `
    <h2 class="text-center noCardMsg">No Cards Left</h2>
    `;
    setTimeout(function(){ window.location.href= '/victory/';}, 4000);
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

function updateHP(attackList) {
    console.log(attackList);
    const damage = attackList[0];
    const hp = attackList[1];
    const attackType = attackList[4];
    const firstPlayerAttacking = attackList[2];
    const color = typeColor[attackType];
    var pokemon = ";"
    if (firstPlayerAttacking == true){
        pokemon = document.querySelector("#firstPlayerCard .poke-name").innerHTML;
        document.querySelector("#secondPlayerCard .hp").innerHTML = `
        <span>HP</span>
        ${hp}
        `;
    }
    else {
        pokemon = document.querySelector("#secondPlayerCard .poke-name").innerHTML;
        document.querySelector("#firstPlayerCard .hp").innerHTML = `
        <span>HP</span>
        ${hp}
        `;
    }
    document.getElementById("damageText").style.color = color;
    document.getElementById("damageText").innerHTML = (pokemon + " did " + damage + " damage with " + attackType + "!");

    if (hp == "Fainted"){
        winCheck();
    }
}

function playAnimations(firstPlayerAttacking, attackList){
    if (firstPlayerAttacking) {
        console.log("ANIMATION STUFF");
	    element = document.querySelector("#firstPlayerCard img ");
        element.classList.add("a-slide");
        element.setAttribute('data-animation', 'once');
        element.style.animationPlayState = "running";

        element = document.getElementById("playerOneAnimation");
        element.classList.add("a-slide");
        element.classList.remove("invisible");
        element.setAttribute('data-animation', 'once');
        element.style.animationPlayerState ="running";
    }
    else {
	element = document.querySelector("#secondPlayerCard img ");
        element.classList.add("a-slide");
        element.setAttribute('data-animation', 'once');
        element.style.animationPlayState = "running";

        element = document.getElementById("playerTwoAnimation");
        element.classList.add("a-slide2");
        element.classList.remove("invisible");
        element.setAttribute('data-animation', 'twice');
        element.style.animationPlayerState ="running";
    }
    var fireballSound = new Audio('/static/fireballSound.wav');
    fireballSound.loop = false;
    fireballSound.play();
    checkCollision(firstPlayerAttacking);
}

function checkCollision(firstPlayerAttacking) {
    if (firstPlayerAttacking) { // MIGHT NEED TO SWAP CONDITION
        var defender = document.getElementById('playerTwoCardBack');
        var elem = document.getElementById("playerOneAnimation");
        if (detectOverlap(elem, defender)) {
            element = document.getElementById("playerOneAnimation")
            element.classList.remove("a-slide");
            element.classList.add("invisible");
            document.getElementById("playerTwoExplosion").src = '/static/explosion.gif';
            setTimeout(() => {document.getElementById("playerTwoExplosion").src = "" }, 400);
            var fireballBoom = new Audio('/static/fireballBoom.mp3');
            fireballBoom.loop = false;
            fireballBoom.play();
        }
        else {
        setTimeout(checkCollision, 10, firstPlayerAttacking);
        }
    }
    else {
        var defender = document.getElementById('playerOneCardBack');
        var elem = document.getElementById("playerTwoAnimation");
        if (detectOverlap(elem, defender)) {
            element = document.getElementById("playerTwoAnimation")
            element.classList.remove("a-slide2");
            element.classList.add("invisible");
            document.getElementById("playerOneExplosion").src = '/static/explosion.gif';
            setTimeout(() => {document.getElementById("playerOneExplosion").src = "" }, 400);
            var fireballBoom = new Audio('/static/fireballBoom.mp3');
            fireballBoom.loop = false;
            fireballBoom.play();
        }
        else {
            setTimeout(checkCollision, 10, firstPlayerAttacking);
        }
    }

}

var detectOverlap = (function () {
    function getPositions(elem) {
        var pos = elem.getBoundingClientRect();
        return [[pos.left, pos.right], [pos.top, pos.bottom]];
    }

    function comparePositions(p1, p2) {
        var r1, r2;
        r1 = p1[0] < p2[0] ? p1 : p2;
        r2 = p1[0] < p2[0] ? p2 : p1;
        return r1[1] > r2[0] || r1[0] === r2[0];
    }

    return function (a, b) {
        var pos1 = getPositions(a),
            pos2 = getPositions(b);
        return comparePositions(pos1[0], pos2[0]) && comparePositions(pos1[1], pos2[1]);
    };
})();

window.onload = function() {
    document.getElementById("my_audio").play();
}