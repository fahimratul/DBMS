const modal = document.getElementById("eventModal");
const closeBtn = modal.querySelector(".close");

function clearTableBody(tbody) {
  while (tbody.firstChild) tbody.removeChild(tbody.firstChild);
}

function showModal(eventId) {
  
  const data = eventsData.find(ev => ev.event_id == eventId);
  if (!data) return alert("No data found for event: " + eventId);

  document.getElementById("modalEventId").innerText = data.event_id;
  document.getElementById("modalEventType").innerText = data.event_type || "N/A";
  const statusEl = document.getElementById("modalStatus");
  statusEl.innerText = data.status || "Unknown";
  statusEl.className = "status " + (data.status ? data.status.toLowerCase() : "");
  document.getElementById("modalPriority").innerText = data.priority_message || "—";
  document.getElementById("modalRequestDate").innerText = data.request_date || "—";
  document.getElementById("modalCompletionDate").innerText = data.end_date || "—";
  document.getElementById("modalLocation").innerText = data.location || "—";
  document.getElementById("modalRequester").innerText = data.requester_name || "—";
  document.getElementById("modalRequesterContact").innerText = data.requester_contact || "—";
  document.getElementById("modalAdditional").innerText = data.additional_item || "—";

  const teamTbody = document.getElementById("modalTeamMembers");
  clearTableBody(teamTbody);

  if (data.volunteers && data.volunteers.length > 0) {
    document.getElementById("modalLeader").innerText = data.volunteers[0].name || "—";

    data.volunteers.forEach(vol => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${vol.name || "Unknown"}</td>
        <td>${vol.volunteer_id || "—"}</td>
        <td>${vol.phone || "—"}</td>
      `;
      teamTbody.appendChild(tr);
    });
  } else {
    document.getElementById("modalLeader").innerText = "—";
  }

  const itemsTbody = document.getElementById("modalAllocatedItems");
  clearTableBody(itemsTbody);

  if (data.item_id_list) {
    const itemTokens = data.item_id_list.split("$").filter(Boolean);
    itemTokens.forEach(token => {
      const [itemId, itemName, qty] = token.split("#");
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${itemName || "N/A"}</td>
        <td>${qty || "0"}</td>
        <td>${itemId || "—"}</td>
      `;
      itemsTbody.appendChild(tr);
    });
  }

  modal.style.display = "block";
}



document.querySelectorAll(".details-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const eventId = btn.dataset.eventId;  // safe and explicit
    showModal(eventId);
  });
});


closeBtn.onclick = () => modal.style.display = "none";

window.onclick = (event) => {
  if (event.target === modal) {
    modal.style.display = "none";
  }
};
