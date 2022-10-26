var highlight = function(){

    var table = document.getElementById("table");
    for( var i = 1; i < table.rows.length; i++)
        {
            for(var j = 0; j < table.rows[i].cells.length; j++){
                table.rows[i].cells[0].style.text = "red";
                table.rows[0].cells[j].style.text = "red";
                }
        }
}