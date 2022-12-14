let appendTypes = (types) => {
    types.forEach((item) => {
        let span = document.createElement("SPAN");
        span.textContent = item.charAt(0).toUpperCase() + item.slice(1);
        document.querySelector(".types").appendChild(span);
        });
};

let styleCard = (color) => {
    card.style.background = `radial-gradient(circle at 50% 0%, ${color} 36%, #ffffff 36%)`;
    card.querySelectorAll(".types span").forEach((typeColor) => {
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

function getPokeCard(){
    var pokeDict;
    pokeName = document.getElementById("pokeSearch");
    pokeName = pokeName.value;
    fetch('/getPokeCard/' + pokeName)
        .then(pokeParse => pokeParse.json())
        .then(pokeParse => updateCardUI(pokeParse));
}

function updateCardUI(pokeDict){
    var element = document.getElementById("cardClass");
    element.classList.remove("invisible");
    element.classList.add("visible");
    const mainAttribute = pokeDict.types[0];
    const themeColor = typeColor[mainAttribute];
    console.log(mainAttribute)
    console.log(themeColor);
    console.log(pokeDict);
    const imgSrc = pokeDict.url;
    const attack = pokeDict.attack;
    const defense = pokeDict.defense;
    const hp = pokeDict.hp;
    const types = pokeDict.types;
    const name = pokeDict.name;

    card.innerHTML = `
        <p class="hp">
          <span>HP</span>
            ${hp}
        </p>
        <img src=${imgSrc} />
        <h2 class="poke-name">${pokeName}</h2>
        <div class="types">

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

    appendTypes(pokeDict.types);
    styleCard(themeColor);
}


function downloadData(){
    var element = document.getElementById("cardClass");
    element.classList.remove("visible");
    element.classList.add("invisible");

    element = document.getElementById("contents");
    element.classList.remove("visible");
    element.classList.add("invisible");

    element = document.getElementById("pokedexBackground");
    element.classList.remove("bg");
    element.classList.add("loadingGIF");
//    loading icon visible
    return fetch('/downloadData')
        .then(noData => noData.text())
        .then(noData => {
        if (noData == 'False'){
        getPokeList();
        } else {
        alert("Pokemon API not working");
        }
        });

}

function getPokeList(){
    fetch('/pokeList')
    .then(data => data.text())
    .then(data => {
            element = document.getElementById("pokeSearch");
            element.innerHTML = data
        });

    element = document.getElementById("pokedexBackground");
    element.classList.remove("loadingGIF");
    element.classList.add("bg");
    console.log("list updated");

    element = document.getElementById("contents");
    element.classList.remove("invisible");
    element.classList.add("visible");
}
