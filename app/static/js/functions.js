function message_error(obj) {
    //pasamos el objeto, y lo iteremos con each,
    //como es un diccionario usaremos una funcion y le pasaremos la clave y valor
    var html = '';
    if (typeof (obj) === 'object') {
        html += '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += "<li>" + key + ': ' + value + '</li>';
        });
    }else{
        //De esta forma verificaría si el error es un objeto, ejemplo json, o si es otro tipo de error
        //lo enviaría a este else
        html+='<p>'+obj+'</p>';
    }
    html += '</ul>';
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}