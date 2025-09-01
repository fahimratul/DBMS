document.addEventListener('DOMContentLoaded', function() {
  // Open modal and fetch details
  document.querySelectorAll('.details-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      const taskId = this.getAttribute('data-task-id');
      fetch(`/admin/admin_events/${taskId}`)
        .then(response => response.json())
        .then(data => {
          // Fill modal fields
          document.getElementById('modalEventId').textContent = data.task_id ? `E${String(data.task_id).padStart(5, '0')}` : '';
          document.getElementById('modalEventType').textContent = data.event_type || '';
          document.getElementById('modalStatus').textContent = data.status || '';
          document.getElementById('modalPriority').textContent = data.priority_message || '';
          document.getElementById('modalRequestDate').textContent = formatDate(data.request_date);
          document.getElementById('modalCompletionDate').textContent = formatDate(data.completed_date);
          document.getElementById('modalLocation').textContent = data.location || '';
          document.getElementById('modalLeader').textContent = data.leader_name || '';
          document.getElementById('modalRequester').textContent = data.requester_name || '';
          document.getElementById('modalRequesterContact').textContent = data.requester_phone || '';
          document.getElementById('modalAdditional').textContent = data.additional_item || '';

          // Team Members
          const teamMembers = data.team_members || [];
          const teamTable = document.getElementById('modalTeamMembers');
          teamTable.innerHTML = '';
          teamMembers.forEach(member => {
            teamTable.innerHTML += `<tr>
              <td>${member.name}</td>
              <td>${member.volunteer_id}</td>
              <td>${member.phone}</td>
            </tr>`;
          });

          // Allocated Items
          const items = data.allocated_items || [];
          const itemsTable = document.getElementById('modalAllocatedItems');
          itemsTable.innerHTML = '';
          items.forEach(item => {
            itemsTable.innerHTML += `<tr>
              <td>${item.item_name}</td>
              <td>${item.quantity}</td>
              <td>${item.stock_id}</td>
            </tr>`;
          });

          // Feedback
          const feedbackList = document.getElementById('modalFeedbackList');
          feedbackList.innerHTML = '';
          (data.feedback || []).forEach(fb => {
            feedbackList.innerHTML += `<li>${fb.message}</li>`;
          });

          document.getElementById('eventModal').style.display = 'flex';
        });
    });
  });

  // Close modal
  document.querySelector('.modal .close').onclick = function() {
    document.getElementById('eventModal').style.display = 'none';
  };
  window.onclick = function(event) {
    const modal = document.getElementById('eventModal');
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  };

  function formatDate(dateStr) {
    if (!dateStr) return '';
    return dateStr.split('T')[0];
  }
});