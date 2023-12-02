// Get list of custom commands
fetch('/api/commands')
  .then(res => res.json())
  .then(commands => {

    // Populate custom command table 
    commands.forEach(command => {
      let row = `
        <tr>
          <td>${command.name}</td>
          <td>${command.response}</td>
          <td><button onclick="deleteCommand('${command.id}')">Delete</td>
        </tr>
      `;
      document.getElementById('command-list').insertAdjacentHTML('beforeend', row); 
    });

  });

// Handle add command form  
const form = document.getElementById('add-command-form');
form.onsubmit = () => {

  const name = form.name.value;
  const response = form.response.value;
  
  fetch('/api/commands', {
    method: 'POST',
    body: JSON.stringify({
      name, 
      response
    })
  })
    .then(res => {
      if (res.ok) {
        location.reload(); 
      }
    });

  return false;
};

// Embed Builder
const embedForm = document.getElementById('embed-form');
embedForm.onsubmit = () => {

  const title = embedForm.title.value; 
  const description = embedForm.description.value;

  // Make API call to Bot to send embed
  fetch('/api/send-embed', {
    method: 'POST',
    body: JSON.stringify({
      title,
      description 
    })
  });

  return false;
}; 

// Get moderation logs
document.getElementById('get-logs').onclick = () => {

  fetch('/api/mod-logs')
    .then(res => res.json())
    .then(logs => {
      
      logs.forEach(log => {

        const row = `
          <tr>
            <td>${log.action}</td>
            <td>${log.moderator}</td>
            <td>${log.user}</td>
            <td>${log.date}</td>
          </tr>
        `;

        document.getElementById('mod-logs-table').insertAdjacentHTML('beforeend', row);

      });

    });

};

// Ban user
const banForm = document.getElementById('ban-user-form');

banForm.onsubmit = () => {
  
  const user_id = banForm.user_id.value; 
  
  fetch('/api/ban', {
    method: 'POST',
    body: JSON.stringify({
      user_id
    })
  })
    .then(res => {
      if(res.ok) {
        location.reload();
      }
    });

  return false;

};
