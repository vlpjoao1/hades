$(function () {
    $('input[name="date_ranger"]').daterangepicker(
        {
            locale: {
                format:'YYYY-MM-DD',
                applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar',
                cancelLabel: '<i class="fas fa-times"></i> Cancelar',
            }
        }
    );
});