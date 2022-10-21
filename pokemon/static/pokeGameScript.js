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
    const types = pokeDict.types;
    const pokeName = pokeDict.name;
    cardID = document.getElementById(card)

    cardID.innerHTML = `
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
    console.log(cardDeck);
    fetch('/cycleCard/' + cardDeck)
        .then(topCard => topCard.json())
        .then(topCard => {
        console.log(topCard)
        updateCard(topCard, cardDeck, cardID);
        updateCardCount();
        });
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