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
});