$(document).ready(function () {
    // Click sobre fila
    $(".clickable-row").click(function () {
        window.location = $(this).data("href");
    });

    // Búsqueda en tiempo real
    $('#search-input').on('input', function () {
        var searchTerm = $(this).val().toLowerCase();
        $('table tbody tr').each(function () {
            var rowText = $(this).text().toLowerCase();
            $(this).toggle(rowText.indexOf(searchTerm) !== -1);
        });
    });

    // Placeholder para filtros y agrupaciones
    $('#filter-button').click(function () {
        // Implementar lógica de filtrado aquí
    });

    $('#group-button').click(function () {
        // Implementar lógica de agrupación aquí
    });
});

