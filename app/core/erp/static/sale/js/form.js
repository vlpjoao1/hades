var tblProducts;
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
    //Calcular factura
    calculate_invoice: function () {
        // Con esta variable iremos obteniendo la suma de todos los productos
        var subtotal = 0.00;
        //obtenemos el % del iva
        var iva = $('input[name="iva"]').val();

        //Si iteramos una lista, obtendremos el index y value, que en este caso sera la POS y el DICT
        $.each(this.items.products, function (pos, dict) {
            //Multiplicamos la cantidadd de productos por el precio, lo que nos da el total
            dict.subtotal = dict.cant * parseFloat(dict.pvp);
            subtotal += dict.subtotal;
        });//Calculamos el subtotal de cada producto

        this.items.subtotal = subtotal;
        //Calculamos el IVA
        this.items.iva = (this.items.subtotal * iva) / 100;
        this.items.total = this.items.subtotal + this.items.iva;

        //Seteamos en el formulario subtotal
        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function (item) {
        //Agregamos el item a la variable products
        this.items.products.push(item);
        //listamos el item en la tabla
        this.list();
    },
    /*
    * Debido a que los productos del items se van creciendo, cada vez que ejecutas el LIST este destruye la tabla
    * y le agrega los valores del los items en la data
    * */
    list: function () {
        //Calculamos la factura al listar
        this.calculate_invoice();
        //Asignamos el datatable a la variable
        tblProducts = $('#tblProducts').DataTable({
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
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + data + '">';
                    }
                },
            ],
            //https://datatables.net/reference/option/rowCallback
            //A medida que se vayan creando registro de la tabla, puedo ir modificando registros de la tabla.
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                /* Explicacion:
                *  rowCallback se ejecuta antes de renderizar el dato en pantalla, esto nos permite modificarlo antes de
                * mostrarlo. esto te devueelve la fila, los datos y algo mas
                * */
                // En el row buscamos el input llamado cantidad y le agregamos el touchspin
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 0,
                    max: 100000000,
                    step: 1,
                }).on('change', function () {
                    //Recalcular factura al cambiar el IVA
                    vents.calculate_invoice();
                });

            },
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

    //TouchSpin https://www.virtuosoft.eu/code/bootstrap-touchspin/
    // IVA porcentaje
    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function () {
        //Recalcular factura al cambiar el IVA
        vents.calculate_invoice();
    }).val(12);

    //Search Products
    $('input[name="search"]').autocomplete({
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

    // Evento cantidad formulario
    // Usamos keyup porque cuando usamos solo CHANGE tenemos que quitar el focus del form para que se ejecute el script
    $('#tblProducts tbody').on('change', 'input[name="cantidad"]', function () {
        //obtenemos la cantidad
        var cant = parseInt($(this).val());

        // Obtenemos la posición de la celda donde esta ubicada la instancia actual.
        var tr = tblProducts.cell($(this).closest('td, li')).index();

        //Actualizamos el producto con la nueva cantidad obtenida del formulario
        vents.items.products[tr.row].cant = cant;

        //recalculamos la factura
        vents.calculate_invoice();
        //td:eq(n) hace referencia a la posicion del td dentro del row.
        //https://datatables.net/reference/api/row().node()
        //Obtenemos la columna que vamos a modificar y luego le modificamos el html con html()
        $('td:eq(5)', tblProducts.row(tr.row).node()).html('$'+vents.items.products[tr.row].subtotal.toFixed(2));
        console.log(vents.items.products);

    });
});