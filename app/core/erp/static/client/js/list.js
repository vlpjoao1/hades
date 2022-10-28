// Creamos una funcion para refrescar el datatable solo llamandolo
var tbClient;
function getData(){
    //Asignamos el datatable a una variable para poder acceder a sus metodos
    tbClient = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        //si cargamos la tabla con ajax, esto servirá como un async
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },//parameters
            //dataSrc se usa para especificar una key dentro de un dict. https://datatables.net/manual/ajax#JSON-data-source
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "names"},
            {"data": "surnames"},
            {"data": "dni"},
            {"data": "date_birthday"},
            {"data": "gender"},
            {"data": "id"},
        ],
        //definimos las columnas una por una, especificando su posicion
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        //se ejecuta cuando ya se cargue la tabla
        initComplete: function (settings, json) {

        }
    });
};
$(function () {
    getData();
    // Cosas que pasaran cuando presiones el boton Add
    $('.btnAdd').on('click', function(){
        // Agregamos el valor add ya que desde JS cambiaremos a editar
        $('input[name="action"]').val('add');
        //Se hace de esta forma por si hay varios formularios
        //$('form')[0].reset();
        $('#myModalClient').modal('show');
    });

    //Cuando se oculte el modal ejecute esta funcion
    $('#myModalClient').on('shown.bs.modal', function(){
        $('form')[0].reset();
    });

    $('form').on('submit', function (e) {
        e.preventDefault();
        //aquí hacemos referencia al formulario
        //Esto obtiene a forma de diccionario todos los datos del formulario
        //Serializa los datos obtenidos del formulario
        //var parameters = $(this).serializeArray();
        //El formdata incluye los archivos FILES, Le pasamos el formulario como argumento
        var parameters = new FormData(this);
        // new FormData($('form')[0]) -> Si tenemos varios formularios y queremos escoger 1
        //parameters.forEach((key,value)=>console.log(key+':'+value)); -> si queremos iterar cada valor
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estás seguro de que deseas realizar la siguiente acción?', parameters, function () {
            //ocultamos el modal
            $('#myModalClient').modal('hide');
            //refrescamos el datatable
            //getData(); -- Puede ser de esta forma o
            //Con esto podemos reload el ajax https://datatables.net/reference/api/ajax.reload()
            tbClient.ajax.reload();
        });
    });
});
