const requesters = [
  {
    id: "R001",
    name: "John Doe",
    priority: "High Priority - Flood affected",
    additionalItems: "Baby food, Medicine",
    requestDate: "2023-08-01",
    location: "Dhaka",
    emergencyContact: "+880123456789",
    stockItems: [
      { stockId: "S001", item: "Water", quantity: 100 },
      { stockId: "S002", item: "Food", quantity: 200 }
    ]
  },
  {
    id: "R002",
    name: "Jane Smith",
    priority: "Medium Priority - Medical Emergency",
    additionalItems: "First Aid kits",
    requestDate: "2023-08-05",
    location: "Chittagong",
    emergencyContact: "+880987654321",
    stockItems: [
      { stockId: "S003", item: "Medicine", quantity: 50 }
    ]
  }
];

const volunteers = [
  { id: "V001", name: "Alice" },
  { id: "V002", name: "Bob" },
  { id: "V003", name: "Charlie" }
];

const eventTypes = [
  "Flood",
  "Earthquake",
  "Cyclone",
  "Medical Emergency"
];

const requesterSelect = document.getElementById('requesterSelect');
const priorityField = document.getElementById('priority');
const additionalItemsField = document.getElementById('additionalItems');
const requestDateField = document.getElementById('requestDate');
const locationField = document.getElementById('location');
const emergencyContactField = document.getElementById('emergencyContact');
const volunteersSelect = document.getElementById('volunteersSelect');
const leaderSelect = document.getElementById('leaderSelect');
const stockContainer = document.getElementById('stockContainer');
const eventTypeSelect = document.getElementById('eventType');
const addStockBtn = document.getElementById('addStockBtn');

function populateRequesterOptions() {
  requesters.forEach(r => {
    const opt = document.createElement('option');
    opt.value = r.id;
    opt.textContent = `${r.name} (${r.id})`;
    requesterSelect.appendChild(opt);
  });
}

function populateVolunteers() {
  volunteers.forEach(v => {
    const opt = document.createElement('option');
    opt.value = v.id;
    opt.textContent = v.name;
    volunteersSelect.appendChild(opt);
  });
}

function populateEventTypes() {
  eventTypes.forEach(et => {
    const opt = document.createElement('option');
    opt.value = et;
    opt.textContent = et;
    eventTypeSelect.appendChild(opt);
  });
}

function clearStockItems() {
  stockContainer.innerHTML = '';
}

function addStockRow(stockItem = { stockId: '', item: '', quantity: '' }) {
  const div = document.createElement('div');
  div.classList.add('stock-row');
  div.innerHTML = `
    <input type="text" class="stock-id" placeholder="Stock ID" value="${stockItem.stockId}" />
    <input type="text" class="stock-item" placeholder="Item Name" value="${stockItem.item}" />
    <input type="number" class="stock-qty" placeholder="Quantity" value="${stockItem.quantity}" min="1" />
    <button type="button" class="remove-stock-btn">Remove</button>
  `;
  stockContainer.appendChild(div);

  div.querySelector('.remove-stock-btn').addEventListener('click', () => {
    div.remove();
  });
}

function fillRequesterDetails(id) {
  if (!id) {
    // Clear and make fields editable
    priorityField.value = '';
    priorityField.readOnly = false;

    additionalItemsField.value = '';
    additionalItemsField.readOnly = false;

    requestDateField.value = '';
    requestDateField.readOnly = false;

    locationField.value = '';
    locationField.readOnly = false;

    emergencyContactField.value = '';
    emergencyContactField.readOnly = false;

    clearStockItems();
    return;
  }

  const requester = requesters.find(r => r.id === id);
  if (!requester) return;

  priorityField.value = requester.priority;
  priorityField.readOnly = true;

  additionalItemsField.value = requester.additionalItems;
  additionalItemsField.readOnly = true;

  requestDateField.value = requester.requestDate;
  requestDateField.readOnly = true;

  locationField.value = requester.location;
  locationField.readOnly = true;

  emergencyContactField.value = requester.emergencyContact;
  emergencyContactField.readOnly = true;

  clearStockItems();
  requester.stockItems.forEach(item => addStockRow(item));
}

function updateLeaderOptions() {
  leaderSelect.innerHTML = '<option value="">-- Select leader from volunteers --</option>';

  const selectedVols = Array.from(volunteersSelect.selectedOptions);

  selectedVols.forEach(opt => {
    const v = volunteers.find(v => v.id === opt.value);
    if (v) {
      const option = document.createElement('option');
      option.value = v.id;
      option.textContent = v.name;
      leaderSelect.appendChild(option);
    }
  });
}

requesterSelect.addEventListener('change', () => {
  fillRequesterDetails(requesterSelect.value);
});

volunteersSelect.addEventListener('change', () => {
  updateLeaderOptions();
});

addStockBtn.addEventListener('click', () => {
  addStockRow();
});

populateRequesterOptions();
populateVolunteers();
populateEventTypes();
