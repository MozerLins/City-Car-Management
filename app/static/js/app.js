let token = '';

function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch('http://localhost:5000/v1/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Login or Password is Wrong');
        }
        return response.json();
    })
    .then(data => {
        if (data.access_token) {
            token = data.access_token;
            document.getElementById('login-message').innerText = "Login successful!";
            document.getElementById('login').style.display = 'none';
            document.getElementById('add-owner').style.display = 'block';
            document.getElementById('add-car').style.display = 'block';
            document.getElementById('owners-list').style.display = 'block';
            loadOwners(); 
            document.getElementById('login-message').innerText = "Login failed!";
        }
    })
    .catch(error => {
        document.getElementById('login-message').innerText = 'Error: ' + error.message;
    });
}

function addOwner() {
    const ownerName = document.getElementById("owner-name").value;
    if (!ownerName) {
        document.getElementById('owner-message').innerText = 'Owner name is required!';
        return;
    }

    fetch('http://localhost:5000/v1/owners', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ name: ownerName })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to add owner: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('owner-message').innerText = data.message;
        document.getElementById("owner-name").value = ''; 
        loadOwners();
        setTimeout(() => {
            document.getElementById('owner-message').innerText = ''; 
        }, 5000);
    })
    .catch(error => {
        document.getElementById('owner-message').innerText = 'Error: ' + error.message;
    });
}

async function loadOwners() {
    try {
        const response = await fetch('http://localhost:5000/v1/owners', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const owners = await response.json();

        const ownerSelect = document.getElementById('owner-select');
        ownerSelect.innerHTML = ''; 

        owners.forEach(owner => {
            const option = document.createElement('option');
            option.value = owner.id; 
            option.textContent = owner.name; 
            ownerSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading owners:', error);
    }
}

function loadCarOptions() {
    const colors = ['yellow', 'blue', 'gray'];
    const models = ['hatch', 'sedan', 'convertible'];

    const colorSelect = document.getElementById("car-color");
    const modelSelect = document.getElementById("car-model");

    colors.forEach(color => {
        let option = document.createElement("option");
        option.value = color;
        option.textContent = color.charAt(0).toUpperCase() + color.slice(1); 
        colorSelect.appendChild(option);
    });

    models.forEach(model => {
        let option = document.createElement("option");
        option.value = model;
        option.textContent = model.charAt(0).toUpperCase() + model.slice(1); 
        modelSelect.appendChild(option);
    });
}

function addCar() {
    const ownerId = document.getElementById("owner-select").value; 
    const carColor = document.getElementById("car-color").value;
    const carModel = document.getElementById("car-model").value;

    if (!ownerId || !carColor || !carModel) {
        document.getElementById('car-message').innerText = 'All fields are required!';
        return;
    }

    fetch(`http://localhost:5000/v1/owners/${ownerId}/cars`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ color: carColor, model: carModel })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to add car: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('car-message').innerText = data.message;
        document.getElementById("car-color").value = '';
        document.getElementById("car-model").value = '';
        setTimeout(() => {
            document.getElementById('car-message').innerText = ''; 
        }, 5000);
    })
    .catch(error => {
        document.getElementById('car-message').innerText = 'Error: ' + error.message;
    });
}

function getOwners() {
    fetch('http://localhost:5000/v1/owners', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch owners: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        const ownersList = document.getElementById('owners');
        ownersList.innerHTML = '';
        if (data.length === 0) {
            ownersList.innerHTML = '<li>No owners found.</li>';
        } else {
            data.forEach(owner => {
                let li = document.createElement('li');
                li.innerHTML = `<strong>Owner:</strong> ${owner.name} (ID: ${owner.id}) <br> <strong>Cars:</strong> ${owner.cars.map(car => car.color + ' ' + car.model).join(', ')}`;
                ownersList.appendChild(li);
            });
        }
    })
    .catch(error => {
        console.error('Error fetching owners:', error);
    });
}

document.addEventListener('DOMContentLoaded', (event) => {
    loadCarOptions();
    loadOwners(); 
});
