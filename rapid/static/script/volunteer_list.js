document.addEventListener('DOMContentLoaded', function () {
    const freeBtn = document.getElementById('free');
    const freeVolunteers = document.getElementById('free_volunteers');
    const assignedBtn = document.getElementById('assigned');
    const assignedVolunteers = document.getElementById('asigned_volunteers');
    const newbtn = document.getElementById('new');
    const newVolunteers = document.getElementById('new_volunteers');
    const blockbtn = document.getElementById('block');
    const blockVolunteers = document.getElementById('block_volunteers');

    
    
    const contentBodies = document.querySelectorAll('.content-body');


    if (freeBtn && freeVolunteers) {
        freeBtn.addEventListener('click', function () {
            contentBodies.forEach(body => body.classList.remove('active'));
            freeVolunteers.classList.add('active');
        });
    }

    if (assignedBtn && assignedVolunteers) {
        assignedBtn.addEventListener('click', function () {
            contentBodies.forEach(body => body.classList.remove('active'));
            assignedVolunteers.classList.add('active');
        });
    }
    
    if (newbtn && newVolunteers) {
        newbtn.addEventListener('click', function () {
            contentBodies.forEach(body => body.classList.remove('active'));
            newVolunteers.classList.add('active');
        });
    }

    if (blockbtn && blockVolunteers) {
        blockbtn.addEventListener('click', function () {
            contentBodies.forEach(body => body.classList.remove('active'));
            blockVolunteers.classList.add('active');
        });
    }

});

// Pagination variables
let currentPage = 1;
const rowsPerPage = 10;
let currentVolunteers = [];

// Initialize pagination when page loads
document.addEventListener('DOMContentLoaded', function() {
    if (typeof window.blockedVolunteers !== 'undefined') {
        currentVolunteers = window.blockedVolunteers;
        displayVolunteers(currentPage);
        createPaginationButtons();
    }
});

// Display volunteers for the current page
function displayVolunteers(page) {
    const tableBody = document.getElementById('volunteer-table-body');
    const startIndex = (page - 1) * rowsPerPage;
    const endIndex = Math.min(startIndex + rowsPerPage, currentVolunteers.length);
    
    // Clear existing rows
    tableBody.innerHTML = '';
    
    // Check if no volunteers
    if (currentVolunteers.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="4">No volunteers found.</td></tr>';
        return;
    }
    
    // Add volunteers for current page
    for (let i = startIndex; i < endIndex; i++) {
        const volunteer = currentVolunteers[i];
        const row = `
            <tr>
                <td>${volunteer.id}</td>
                <td class="volunteer-name">${volunteer.name}</td>
                <td class="volunteer-info">
                    <div>
                        <p><b>Email:</b> ${volunteer.email}</p>
                        <p><b>Phone:</b> ${volunteer.phone}</p>
                        <p><b>Experience:</b> ${volunteer.experience} years</p>
                    </div>
                    <div>
                        <p><b>DOB:</b> ${volunteer.dob}</p>
                        <p><b>Joined Date:</b> ${volunteer.joined_date}</p>
                        <p><b>Address:</b> ${volunteer.address}</p>
                    </div>
                </td>
                <td>
                    <button class="button-style alert">Unblock</button>
                </td>
            </tr>
        `;
        tableBody.innerHTML += row;
    }
    
    // Update pagination info
    updatePaginationInfo(startIndex + 1, endIndex, currentVolunteers.length);
}

// Create pagination buttons
function createPaginationButtons() {
    const totalPages = Math.ceil(currentVolunteers.length / rowsPerPage);
    const paginationContainer = document.getElementById('pagination-buttons');
    
    paginationContainer.innerHTML = '';
    
    // Previous button
    if (currentPage > 1) {
        const prevButton = createPaginationButton('Previous', currentPage - 1);
        paginationContainer.appendChild(prevButton);
    }
    
    // Page number buttons
    for (let i = 1; i <= totalPages; i++) {
        const button = createPaginationButton(i, i);
        if (i === currentPage) {
            button.classList.add('active');
        }
        paginationContainer.appendChild(button);
    }
    
    // Next button
    if (currentPage < totalPages) {
        const nextButton = createPaginationButton('Next', currentPage + 1);
        paginationContainer.appendChild(nextButton);
    }
}

// Create individual pagination button
function createPaginationButton(text, page) {
    const button = document.createElement('button');
    button.className = 'button-style pagination-btn';
    button.textContent = text;
    button.addEventListener('click', function() {
        goToPage(page);
    });
    return button;
}

// Navigate to specific page
function goToPage(page) {
    const totalPages = Math.ceil(currentVolunteers.length / rowsPerPage);
    
    if (page >= 1 && page <= totalPages) {
        currentPage = page;
        displayVolunteers(currentPage);
        createPaginationButtons();
    }
}

// Update pagination info text
function updatePaginationInfo(start, end, total) {
    const infoElement = document.getElementById('pagination-info-text');
    if (infoElement) {
        infoElement.textContent = `Showing ${start}-${end} of ${total} volunteers`;
    }
}