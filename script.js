// Function to handle Discord login
function loginWithDiscord() {
    window.location.href = '/login';
}

// Function to get user's servers
function getServers() {
    const userId = document.getElementById('user-id').value;

    fetch(`/api/servers?user_id=${userId}`)
        .then(res => res.json())
        .then(data => {
            const serversSelect = document.getElementById('servers');
            serversSelect.innerHTML = ''; // Clear current options

            const placeholder = document.createElement('option');
            placeholder.value = '';
            placeholder.text = 'Select a Server';
            serversSelect.appendChild(placeholder);

            data.servers.forEach(server => {
                const option = document.createElement('option');
                option.value = server.id;
                option.text = server.name;
                serversSelect.appendChild(option);
            });
        });
}

// Function to handle adding a custom command
function addCommand() {
    const name = document.getElementById('command-name').value;
    const response = document.getElementById('command-response').value;

    fetch('/api/commands', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
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
}

// Function to handle deleting a custom command
function deleteCommand(commandId) {
    fetch(`/api/commands/${commandId}`, {
        method: 'DELETE'
    })
    .then(res => {
        if (res.ok) {
            location.reload();
        }
    });
}

// On document ready
document.addEventListener("DOMContentLoaded", function() {
    // Fetch and populate user's servers on page load
    fetch('/api/servers')
        .then(res => res.json())
        .then(data => {
            const serversSelect = document.getElementById('servers');
            serversSelect.innerHTML = ''; // Clear current options

            const placeholder = document.createElement('option');
            placeholder.value = '';
            placeholder.text = 'Select a Server';
            serversSelect.appendChild(placeholder);

            data.servers.forEach(server => {
                const option = document.createElement('option');
                option.value = server.id;
                option.text = server.name;
                serversSelect.appendChild(option);
            });

            // Show server selection section
            document.getElementById('server-select').style.display = 'block';
        });

    // ... (any additional initialization code) ...
});
