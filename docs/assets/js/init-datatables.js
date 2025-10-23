document.addEventListener("DOMContentLoaded", function() {
  const tables = document.querySelectorAll("table.datatable");
  tables.forEach(function(tbl) {
    if (window.jQuery && typeof window.jQuery.fn.dataTable === "function") {
      window.jQuery(tbl).DataTable({
        pageLength: 25,
        order: [],
        deferRender: true
      });
    }
  });
});