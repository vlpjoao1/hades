var vents = {
    //Datos de la cabecera (Sale)
    items: {
        cli: '',
        date_joined: 0.00,
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        //los productos
        products: []
    },
    add: function (item) {
        //Agregamos el item a la variable products
        this.items.products.push(item);
        //listamos el item en la tabla
        this.list();
    },
    list: function () {
        $('#tblProducts').dataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            /*Debido a que no estamos usando ajax, podemos pasarle la data como una lista de valores
            * Usando THIS podemos hacer referncia a la variable donde estamos trabajando
            * Le mandamos una coleccion de diccionarios*/
            data: this.items.products,
            // Aqui definimos los valores que van en cada posicion de la columna, definimos las columnas de cada posicion
            columns: [
                {'data': 'id'},
                {'data': 'name'},
                {'data': 'cat.name'},
                {'data': 'pvp'},
                {'data': 'cant'},
                {'data': 'subtotal'},
            ],
            //definimos las columnas una por una, especificando su posicion
            columnDefs: [
                {
                    targets: [0],
                    class: 'tex-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    //que PVP y subtotal se les anada un $ a su valor
                    targets: [-3, -1],
                    class: 'tex-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'tex-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm" autocomplete="off" value="' + data + '">';
                    }
                },
            ],
            //se ejecuta cuando ya se cargue la tabla
            initComplete: function (settings, jsong) {
            }
        });
    }
}
$(function () {
    $('.select2').select2({
        //podemos escoger temas para el select2
        theme: 'bootstrap4',
        language: 'es'
    });

    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format('YYYY-MM-DD'),
        locale: 'es',
        maxDate: moment().format('YYYY-MM-DD')
    });
    //TouchSpin
    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    });

    //Search Products
    $('input[name="search"]').autocomplete({
        //source: availableTags,
        //Opciones que se van a mostrar.
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    //De esta manera obtenemos lo que el buscador esta escribiendo
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                // Especificamos que la respuesta es el array de datos obtenido del ajax
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {
            });
        },
        //The delay is needed for reduce the charge of server
        delay: 500,
        minLength: 1,
        // Cuando seleccionamos la palabra se ejecutara esta funcion
        select: function (event, ui) {
            //Detenemos el evento y continuamos con lo demas ya que no nos permitiria continuar con el limpiado del form
            event.preventDefault();
            //Ya que cantidad es una variable que no viene de la busqueda, debemos asignarla manualmente
            ui.item.cant = 1;
            ui.item.subtotal = 0.00;
            vents.add(ui.item);
            //Limpiamos el formulario de busqueda para escoger otro producto.
            $(this).val('');
        }
    });
});