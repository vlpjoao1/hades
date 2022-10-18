function message_error(obj) {
    //pasamos el objeto, y lo iteremos con each,
    //como es un diccionario usaremos una funcion y le pasaremos la clave y valor
    var html = '';
    if (typeof (obj) === 'object') {
        html += '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += "<li>" + key + ': ' + value + '</li>';
        });
    } else {
        //De esta forma verificaría si el error es un objeto, ejemplo json, o si es otro tipo de error
        //lo enviaría a este else
        html += '<p>' + obj + '</p>';
    }
    html += '</ul>';
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}

//https://craftpip.github.io/jquery-confirm/
function submit_with_ajax(url,title,content, parameters, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url, //window.location.pathname
                        type: 'POST',
                        data: parameters,
                        dataType: 'json'
                    }).done(function (data) {
                        console.log(data);
                        if (!data.hasOwnProperty('error')) {
                            callback();
                            return false;
                        }
                        message_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}