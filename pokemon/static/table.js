function getPokeType(){
    var pokeDict;
    pokeType = document.getElementById("typeSearch");
    pokeType = pokeType.value;
    if (pokeType != 'all') {
        fetch('/getPokeType/' + pokeType)
            .then(pokeParse => pokeParse.text())
            .then(pokeParse => {
                document.getElementById("tbody").innerHTML = pokeParse;
            });
    }
    else {
        fetch('/fullTable')
            .then(pokeParse => pokeParse.text())
            .then(pokeParse => {
                document.getElementById("damage-table").innerHTML = pokeParse;
            });
    }
}
