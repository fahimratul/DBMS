const requesters = jsRequesters;
const volunteers = jsVolunteers;
const eventTypes = jsEventTypes;
const allItems = jsAllItems; 


const requesterSelect = document.getElementById('requesterSelect');
const priorityField = document.getElementById('priority');
const additionalItemsField = document.getElementById('additionalItems');
const requestDateField = document.getElementById('requestDate');
const locationField = document.getElementById('location');
const contactField = document.getElementById('contact');
const emergencyContactField = document.getElementById('emergencyContact');
const volunteersSelect = document.getElementById('volunteersSelect');
const leaderSelect = document.getElementById('leaderSelect');
const itemContainer = document.getElementById('itemContainer');
const eventTypeSelect = document.getElementById('eventType');
const addItemBtn = document.getElementById('addItemBtn');

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

function clearItems() {
  itemContainer.innerHTML = '';
}

function addItemRow(item = { itemId: '', item: '', quantity: '', isFilled: false }) {
  const div = document.createElement('div');
  div.classList.add('item-row');

  let options = `<option value="">-- Select an item --</option>`;
  allItems.forEach(it => {
    const selected = item.itemId == it.item_id ? 'selected' : '';
    options += `<option value="${it.item_id}#${it.name}" ${selected}>${it.name}</option>`;
  });

  div.innerHTML = `
    <select class="item-select" ${item.isFilled ? 'disabled' : ''}>${options}</select>
    <input type="number" class="item-qty" placeholder="Quantity" value="${item.quantity}" min="1" ${item.isFilled ? 'readonly' : ''} />
    <input type="hidden" class="item-id" value="${item.itemId}" />
    <button type="button" class="remove-item-btn">Remove</button>
  `;

  itemContainer.appendChild(div);

  const select = div.querySelector('.item-select');
  const idInput = div.querySelector('.item-id');

  if (!item.isFilled) {
    select.addEventListener('change', () => {
      const val = select.value;
      if (val) {
        const [id, name] = val.split('#');
        idInput.value = id;
      } else {
        idInput.value = '';
      }
    });
  }

  div.querySelector('.remove-item-btn').addEventListener('click', () => div.remove());
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

    clearItems();
    return;
  }

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

  clearItems();
  requester.items.forEach(item => addItemRow({...item, isFilled: true}));

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

addItemBtn.addEventListener('click', () => {
  addItemRow();
});


populateRequesterOptions();
populateVolunteers();
populateEventTypes();

const form = document.getElementById('createEventForm');

form.addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(form);
    const data = new URLSearchParams();
    for (const pair of formData) {
      data.append(pair[0], pair[1]);
    }
    fetch('/admin/admin_create_event', { method: 'POST', body: data })
    .then(response => response.text()) 
    .then(result => {
        console.log('Success:', result);
        alert('Event created successfully!');
        window.location.reload(); 
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error creating event.');
    });
});