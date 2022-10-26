function colour(){
    document.getElementByTagName("th").style.background = typeColor[i];
    for(i = 1; i < table.rows.length; i++)
        {table.rows[i].style.background-color = typeColor[i]
        }
    }

function highlight(){

    var table = document.getElementById("table");
    for( var i = 1; i < table.rows.length; i++)
        {
            for(var j = 0; j < table.rows[i].cells.length; j++)
                {table.rows[i].cells[0].style.background-color = "red"
                table.rows[0].cells[j].style.background-color = "red"
                }
        }

}