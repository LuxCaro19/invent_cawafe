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

document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("toggle-actions");
    const actionsContainer = document.getElementById("action-buttons");
    let visible = false;

    toggleBtn.addEventListener("click", function () {
      if (!visible) {
        const filtrarBtn = document.createElement("button");
        filtrarBtn.className = "btn btn-primary btn-sm";
        filtrarBtn.id = "filter-button";
        filtrarBtn.textContent = "Filtrar";

        const agruparBtn = document.createElement("button");
        agruparBtn.className = "btn btn-secondary btn-sm";
        agruparBtn.id = "group-button";
        agruparBtn.textContent = "Agrupar";

        actionsContainer.appendChild(filtrarBtn);
        actionsContainer.appendChild(agruparBtn);
        visible = true;
      } else {
        actionsContainer.innerHTML = "";
        visible = false;
      }
    });
  });