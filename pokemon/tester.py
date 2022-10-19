@app.route("/download")
def downloadData:
    ...



function getdata(){
    fetch('/downloadData)
        .then(unused => createList());
}

function createList() {
    fetch('/')
    .then(data= > data.text())
    .then(data= > {
    element = document.getElementById("pokeList");
    element.innerHTML = data
});