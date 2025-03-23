// Script para redirigir cuando se hace clic en cualquier parte de la fila
$(document).ready(function() {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});

// Agrega el código JavaScript para mantener el encabezado fijo cuando se hace scroll en la tabla
$(document).ready(function() {
    var table = $('table');
    var thead = table.find('thead');
    var tbody = table.find('tbody');
  
    // Ajusta el ancho de los th en el thead
    function adjustColumnWidths() {
        thead.find('th').each(function(index) {
            $(this).width(table.find('tbody tr:first td').eq(index).width());
        });
    }
  
    adjustColumnWidths();

    // Lógica de búsqueda en tiempo real
    $('#search-input').on('input', function() {
        var searchTerm = $(this).val().toLowerCase();
        $('table tbody tr').each(function() {
            var rowText = $(this).text().toLowerCase();
            $(this).toggle(rowText.indexOf(searchTerm) !== -1);
        });
        adjustColumnWidths();
    });

    $('#filter-button').click(function() {
        // Implementar lógica de filtrado aquí
    });

    $('#group-button').click(function() {
        // Implementar lógica de agrupación aquí
    });
});

function toggleEdicion() {
    let vista = document.getElementById("vista-detalle");
    let form = document.getElementById("form-edicion");

    if (vista.style.display === "none") {
        vista.style.display = "block";
        form.style.display = "none";
    } else {
        vista.style.display = "none";
        form.style.display = "block";
    }
}