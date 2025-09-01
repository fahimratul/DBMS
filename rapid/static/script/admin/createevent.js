const requesters = jsRequesters;
const volunteers = jsVolunteers;
const eventTypes = jsEventTypes;

const requesterSelect = document.getElementById('requesterSelect');
const priorityField = document.getElementById('priority');
const additionalItemsField = document.getElementById('additionalItems');
const requestDateField = document.getElementById('requestDate');
const locationField = document.getElementById('location');
const contactField = document.getElementById('contact');
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
  const container = document.getElementById('volunteersSelect');
  container.innerHTML = '';

  volunteers.forEach(v => {
    const div = document.createElement('div');
    div.classList.add('volunteer-row');
    div.style.marginBottom = '5px';
    div.innerHTML = `
      <span>${v.name}</span>
      <button type="button" class="select-volunteer-btn" style="margin-left:10px;">Select</button>
    `;
    container.appendChild(div);

    const button = div.querySelector('.select-volunteer-btn');

    button.addEventListener('click', () => {
      if (button.dataset.selected === 'true') {
        button.dataset.selected = 'false';
        button.textContent = 'Select';
        div.style.backgroundColor = '';
      } else {
        button.dataset.selected = 'true';
        button.textContent = 'Selected';
        div.style.backgroundColor = '#d4edda';
      }
      updateLeaderOptions(); // update leader dropdown
    });
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

    contactField.value = '';
    contactField.readOnly = false;

    emergencyContactField.value = '';
    emergencyContactField.readOnly = false;

    clearStockItems();
    return;
  }

  // Convert select value to number before finding
  const requester = requesters.find(r => r.id === Number(id));
  if (!requester) return;

  priorityField.value = requester.priority;
  priorityField.readOnly = true;

  additionalItemsField.value = requester.additionalItems;
  additionalItemsField.readOnly = true;

  requestDateField.value = requester.requestDate;
  requestDateField.readOnly = true;

  locationField.value = requester.location;
  locationField.readOnly = true;

  contactField.value = requester.contact;
  contactField.readOnly = true;

  emergencyContactField.value = requester.emergencyContact;
  emergencyContactField.readOnly = true;

  clearStockItems();
  requester.stockItems.forEach(item => addStockRow(item));
}


function updateLeaderOptions() {
  const leaderSelect = document.getElementById('leaderSelect');
  leaderSelect.innerHTML = '<option value="">-- Select leader from volunteers --</option>';

  const volunteerRows = document.querySelectorAll('#volunteersSelect .volunteer-row');
  volunteerRows.forEach(row => {
    const button = row.querySelector('.select-volunteer-btn');
    if (button.dataset.selected === 'true') {
      const name = row.querySelector('span').textContent;
      const v = volunteers.find(v => v.name === name);
      if (v) {
        const option = document.createElement('option');
        option.value = v.id;
        option.textContent = v.name;
        leaderSelect.appendChild(option);
      }
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