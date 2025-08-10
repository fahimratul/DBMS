const donorTableData = {
  D001: {
    name: "Mohammad Ali",
    phone: "01710000001",
    email: "mohammad.ali@example.com",
    address: "Kurigram, Rangpur, Bangladesh"
  },
  D002: {
    name: "Nasima Akter",
    phone: "01710000002",
    email: "nasima.akter@example.com",
    address: "Gaibandha, Rangpur, Bangladesh"
  },
  D003: {
    name: "Shahidul Islam",
    phone: "01710000003",
    email: "shahidul.islam@example.com",
    address: "Dhaka, Bangladesh"
  }
};

// Populate donor table body
const donorBody = document.getElementById("donorTableBody");
for (const donorId in donorTableData) {
  const donor = donorTableData[donorId];
  const tr = document.createElement("tr");
  tr.innerHTML = `
    <td>${donorId}</td>
    <td>${donor.name}</td>
    <td>${donor.phone}</td>
    <td>${donor.email}</td>
    <td>${donor.address}</td>
  `;
  donorBody.appendChild(tr);
}

// Search function (same as in your request table)
function searchTable(inputId, tableId) {
  const input = document.getElementById(inputId);
  if (!input) return;

  const filter = input.value.toLowerCase();
  const table = document.getElementById(tableId);
  if (!table) return;

  const rows = table.getElementsByTagName("tr");

  for (let i = 1; i < rows.length; i++) {
    const rowText = rows[i].innerText.toLowerCase();
    rows[i].style.display = rowText.includes(filter) ? "" : "none";
  }
}
