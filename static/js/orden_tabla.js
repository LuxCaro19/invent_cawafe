document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("table.ordenable").forEach(table => {
    const headers = table.querySelectorAll("th.sortable");
    headers.forEach((header, index) => {
      header.addEventListener("click", () => {
        const tbody = table.querySelector("tbody");
        const rows = Array.from(tbody.querySelectorAll("tr"));
        const isAsc = header.classList.toggle("asc");
        header.classList.remove("desc");
        headers.forEach(h => {
          if (h !== header) {
            h.classList.remove("asc", "desc");
            const icon = h.querySelector(".sort-icon");
            if (icon) icon.textContent = "";
          }
        });

        header.classList.toggle("desc", !isAsc);
        const icon = header.querySelector(".sort-icon");
        if (icon) icon.textContent = isAsc ? "↑" : "↓";

        rows.sort((a, b) => {
          const aText = a.children[index].textContent.trim();
          const bText = b.children[index].textContent.trim();
          return isAsc
            ? aText.localeCompare(bText, undefined, { numeric: true })
            : bText.localeCompare(aText, undefined, { numeric: true });
        });

        rows.forEach(row => tbody.appendChild(row));
      });
    });
  });
});
