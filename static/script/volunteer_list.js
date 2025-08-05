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