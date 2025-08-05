const receiverTable = {
  R101: {
    name: "Mohammad Ali",
    phone: "01710000001",
    emergency: "01810000001",
    address: "Kurigram, Rangpur, Bangladesh"
  },
  R102: {
    name: "Nasima Akter",
    phone: "01710000002",
    emergency: "01810000002",
    address: "Gaibandha, Rangpur, Bangladesh"
  }
};

const donationRequests = {
  DR001: {
    receiverId: "R101",
    requestDate: "01 Jan, 2025",
    priorityMessage: "Urgent need due to flood damage",
    requestedItems: [
      { item: "Rice", quantity: 30 },
      { item: "Water", quantity: 50 }
    ],
    additionalItems: "Baby food, Blankets"
  },
  DR002: {
    receiverId: "R102",
    requestDate: "05 Feb, 2025",
    priorityMessage: "Affected by river erosion",
    requestedItems: [
      { item: "Tents", quantity: 5 },
      { item: "Medical Kit", quantity: 10 }
    ],
    additionalItems: "Mosquito nets"
  }
};

const requestBody = document.getElementById("requestTableBody");
for (const requestId in donationRequests) {
  const req = donationRequests[requestId];
  const rec = receiverTable[req.receiverId];
  const tr = document.createElement("tr");
  tr.innerHTML = `
    <td>${requestId}</td>
    <td>${req.receiverId}</td>
    <td>${req.requestDate}</td>
    <td>${rec?.name || "Unknown"}</td>
    <td>${rec?.phone || "Unknown"}</td>
    <td><button class="details-btn" data-id="${requestId}">Details</button></td>
  `;
  requestBody.appendChild(tr);
}

const modal = document.getElementById("requestModal");
const closeBtn = modal.querySelector(".close");

function clearTableBody(tbody) {
  while (tbody.firstChild) tbody.removeChild(tbody.firstChild);
}

function showRequestModal(requestId) {
  const data = donationRequests[requestId];
  const rec = receiverTable[data.receiverId];

  document.getElementById("modalRequestId").innerText = requestId;
  document.getElementById("modalRequestDate").innerText = data.requestDate;
  document.getElementById("modalPriorityMessage").innerText = data.priorityMessage;

  const itemBody = document.getElementById("modalRequestedItems");
  clearTableBody(itemBody);
  data.requestedItems.forEach(it => {
    const row = document.createElement("tr");
    row.innerHTML = `<td>${it.item}</td><td>${it.quantity}</td>`;
    itemBody.appendChild(row);
  });

  document.getElementById("modalAdditionalItems").innerText = data.additionalItems;
  document.getElementById("modalReceiverId").innerText = data.receiverId;
  document.getElementById("modalReceiverName").innerText = rec?.name || "—";
  document.getElementById("modalReceiverPhone").innerText = rec?.phone || "—";
  document.getElementById("modalReceiverEmergency").innerText = rec?.emergency || "—";
  document.getElementById("modalReceiverAddress").innerText = rec?.address || "—";

  modal.style.display = "block";
}


document.addEventListener("click", (e) => {
  if (e.target.matches(".details-btn")) {
    const requestId = e.target.getAttribute("data-id");
    showRequestModal(requestId);
  }
});

closeBtn.onclick = () => modal.style.display = "none";
window.onclick = (e) => {
  if (e.target === modal) modal.style.display = "none";
};

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
