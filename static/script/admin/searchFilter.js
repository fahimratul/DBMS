const searchInput = document.getElementById('searchInput');
const table = document.getElementById('eventsTable');
const rows = table.tBodies[0].rows;

searchInput.addEventListener('input', () => {
  const query = searchInput.value.toLowerCase();

  for (const row of rows) {
    const cells = Array.from(row.cells);
    const matches = cells.some(cell => cell.textContent.toLowerCase().includes(query));
    row.style.display = matches ? '' : 'none';
  }
});
