let intervalId;


document.addEventListener('DOMContentLoaded', (event) => {
        document.getElementById('country').addEventListener('change', updateCountryData);
        document.getElementById('initialize').addEventListener('click', initializeData);
    });

function updateCountryData() {
    var selectedCountry = document.getElementById("country").value;
    document.getElementById("pays").innerText = selectedCountry;
    updateCountryInfo(selectedCountry);
}

function initializeData() {
    var selectedCountry = document.getElementById("country").value;
    updateCountryInfo(selectedCountry);
}

function updateCountryInfo(countryName) {
    fetch(`/get_country_data?country_name=${countryName}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById('année').innerText = data.année;  
        document.getElementById('pays').innerText = data.pays;
        document.getElementById('population').innerText = data.population;
    })
    .catch(error => console.error('Error:', error));
}

async function fetchJSON(url) {
    const response = await fetch(url);
    return await response.json();
}


async function avancer() {
    const country = document.getElementById('country').value;
    const data = await fetchJSON(`/avancer?country=${country}`);
    document.getElementById('année').textContent = data.année;
    document.getElementById('population').textContent = data.population;
}

async function sauvegarder() {
        const prenom = document.querySelector('input[name="prenom"]').value;
        try {
            const response = await fetch('/sauvegarder', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ prenom }),
            });

            const result = await response.json();

            if (response.ok) {
                document.getElementById('success-alert').style.display = 'block';
                setTimeout(() => {
                    document.getElementById('success-alert').style.display = 'none';
                }, 2000);
            } else {
                console.error('Erreur lors de la sauvegarde', result);
            }
        } catch (error) {
            console.error('Erreur lors de l’envoi de la requête', error);
        }
    }

    

function demarrerEvolution() {
    if (intervalId) {
        clearInterval(intervalId);
    }
    intervalId = setInterval(() => {
        avancer();
    }, 1000);
}

function pauseEvolution() {
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
}

function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}