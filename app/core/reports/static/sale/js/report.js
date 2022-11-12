var date_range = null;
var date_now = new moment().format('YYYY-MM-DD');
function generate_report(start_date, end_date) {
    var parameters = {
        'action': 'search_report',
        'start_date': '',
        'end_date': ''
    }
    // Si la variable no es nula va a setear startdate y enddate  https://www.daterangepicker.com/#options
    if (date_range !== null) {
        parameters['start_date'] = date_range.startDate.format('YYYY-MM-DD');
        parameters['end_date'] = date_range.endDate.format('YYYY-MM-DD');
    }
    ;
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        /*Cuando mandamos una lista desde python como se hace esta, noo hace falta definir las columnas desde aca
        * */
        // columns: [
        //     {"data": "id"},
        //     {"data": "name"},
        //     {"data": "cat.name"},
        //     {"data": "image"},
        //     {"data": "pvp"},
        //     {"data": "id"},
        // ],
        columnDefs: [
            {
                //Para el iva, total y subtotal
                targets: [-1, -2, -3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
};
$(function () {
    $('input[name="date_ranger"]').daterangepicker(
        {
            locale: {
                format: 'YYYY-MM-DD',
                applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar',
                cancelLabel: '<i class="fas fa-times"></i> Cancelar',
            }
        }
    ).on('apply.daterangepicker', function (ev, picker) {
        //Picker contiene las fechas
        // var start_date = picker.startDate.format('YYYY-MM-DD');
        // var end_date = picker.endDate.format('YYYY-MM-DD');
        // generate_report(start_date,end_date);

        date_range = picker;
        generate_report();
    }).on('cancel.daterangepicker', function (ev, picker) {
        //Setea la fecha cuando damos en CANCELAR
        $(this).data('daterangepicker').setStartDate(date_now);
        $(this).data('daterangepicker').setEndDate(date_now);
        date_range = picker;
        generate_report();
    });
});