const eventsData = {
  E00023: {
    eventType: "Flood",
    status: "Completed",
    statusClass: "completed",
    priority: "High",
    requestDate: "17 Dec, 2022",
    completionDate: "20 Dec, 2022",
    location: "Dhaka",
    teamLeader: "Alice",
    teamMembers: [
      { name: "Alice", volunteerId: "V001", contact: "+880100000001" },
      { name: "Bob", volunteerId: "V002", contact: "+880100000002" },
      { name: "Charlie", volunteerId: "V003", contact: "+880100000003" }
    ],
    allocatedItems: [
      { item: "Water", quantity: 100, stockId: "S001" },
      { item: "Food", quantity: 200, stockId: "S002" },
      { item: "Blankets", quantity: 50, stockId: "S003" }
    ],
    requester: "John Doe",
    requesterContact: "+880123456789",
    additional: "Baby food, Medicine",
    feedback: [
      { giver: "Volunteer", text: "Very well organized." },
      { giver: "Requester", text: "Help arrived quickly, much appreciated." },
      { giver: "Donor", text: "Glad to contribute to this event." }
    ]
  },

  E00032: {
    eventType: "Flood",
    status: "Completed",
    statusClass: "completed",
    priority: "High",
    requestDate: "17 Dec, 2022",
    completionDate: "20 Dec, 2022",
    location: "Char Islampur, Ward-13, Kurigram, Rangpur, Bangladesh",
    teamLeader: "Ayesha Siddiqua",
    teamMembers: [
      { name: "Rafiul Islam", volunteerId: "V123", contact: "017xxxxxxxx" },
      { name: "Sadia Khatun", volunteerId: "V124", contact: "018xxxxxxxx" },
      { name: "Tanvir Hasan", volunteerId: "V125", contact: "019xxxxxxxx" }
    ],
    allocatedItems: [
      { item: "Rice Bags", quantity: 50, stockId: "S101" },
      { item: "Water Bottles", quantity: 100, stockId: "S102" },
      { item: "Blankets", quantity: 30, stockId: "S103" }
    ],
    requester: "Md. Nazmul Haque",
    requesterContact: "016xxxxxxxx",
    additional: "Elderly care kits",
    feedback: [
      { giver: "Volunteer", text: "Challenging but rewarding experience." },
      { giver: "Requester", text: "Support helped my family a lot." }
    ]
  }
};

const modal = document.getElementById("eventModal");
const closeBtn = modal.querySelector(".close");

function clearTableBody(tbody) {
  while (tbody.firstChild) tbody.removeChild(tbody.firstChild);
}

function showModal(eventId) {
  const data = eventsData[eventId];
  if (!data) {
    alert("No data found for event: " + eventId);
    return;
  }

  document.getElementById("modalEventId").innerText = eventId;
  document.getElementById("modalEventType").innerText = data.eventType;

  const statusEl = document.getElementById("modalStatus");
  statusEl.innerText = data.status;
  statusEl.className = "status " + data.statusClass;

  document.getElementById("modalPriority").innerText = data.priority;
  document.getElementById("modalRequestDate").innerText = data.requestDate;
  document.getElementById("modalCompletionDate").innerText = data.completionDate;
  document.getElementById("modalLocation").innerText = data.location;
  document.getElementById("modalLeader").innerText = data.teamLeader;
  document.getElementById("modalRequester").innerText = data.requester;
  document.getElementById("modalRequesterContact").innerText = data.requesterContact;
  document.getElementById("modalAdditional").innerText = data.additional;

  const teamTbody = document.getElementById("modalTeamMembers");
  clearTableBody(teamTbody);
  data.teamMembers.forEach(member => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${member.name}</td>
      <td>${member.volunteerId}</td>
      <td>${member.contact}</td>
    `;
    teamTbody.appendChild(tr);
  });


  const itemsTbody = document.getElementById("modalAllocatedItems");
  clearTableBody(itemsTbody);
  data.allocatedItems.forEach(item => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.item}</td>
      <td>${item.quantity}</td>
      <td>${item.stockId}</td>
    `;
    itemsTbody.appendChild(tr);
  });

  const feedbackList = document.getElementById("modalFeedbackList");
  feedbackList.innerHTML = ""; // clear previous feedback
  if (data.feedback && data.feedback.length > 0) {
    data.feedback.forEach(fb => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>${fb.giver}:</strong> ${fb.text}`;
      feedbackList.appendChild(li);
    });
  } else {
    const li = document.createElement("li");
    li.innerText = "No feedback available.";
    feedbackList.appendChild(li);
  }

  modal.style.display = "block";
}

document.querySelectorAll(".details-btn").forEach(btn => {
  btn.addEventListener("click", (e) => {
    const row = e.target.closest("tr");
    const eventId = row.querySelector("td").innerText.trim();
    showModal(eventId);
  });
});

closeBtn.onclick = () => modal.style.display = "none";

window.onclick = (event) => {
  if (event.target === modal) {
    modal.style.display = "none";
  }
};
