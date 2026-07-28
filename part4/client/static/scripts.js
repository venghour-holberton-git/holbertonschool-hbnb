/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication()
  const form = document.getElementById('login-form')
    try {
        document.getElementById('price-filter').addEventListener('change', async (event) => {
        event.preventDefault()
        let selected_value = event.target.value
        places = await fetchPlaces()
        console.log(places);
        if (selected_value !== "All") {
            places = places.filter((place) => Number(place.price) <= selected_value)
        }
        displayPlaces(places)
        });
    } catch (err) {
        console.log("price filter is unavailable", err);
        
    }
//   console.log(form)
    try {
        form.addEventListener("submit", async (e) => {
          e.preventDefault();
          formData = new FormData(form)
          
          const data = Object.fromEntries(formData)
          console.log(data);
          loginUser(data.email, data.password)
        })
    } catch (err) {
        console.log("error ", err);
    }
    try {
        reviewForm = document.getElementById("review-form")
        reviewForm.addEventListener("submit", async (e) => {
            e.preventDefault()
            formData = new FormData(reviewForm)
            const request = Object.fromEntries(formData)
            console.log(request);
            
        })
    } catch (err) {
        console.log("error", err);
        
    }
});

async function loginUser(email, password) {
    console.log(JSON.stringify({ email, password }));
    
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = '/';
    } else {
        alert('Login failed: ' + response.statusText);
    }

}

function checkAuthentication() {
    let token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    console.log(token);
    
    if (!token && !checkIsTokenExpired(token)) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        // Fetch places data if the user is authenticated
        fetchPlaces(token);
    }
}
function getCookie(name) {
let cookies = document.cookie.split(";")
console.log(cookies);
for (let item of cookies) {
    if (item.startsWith(name+"=")) return item.substring(name.length + 1)
}
return undefined
}
async function fetchPlaces(token) {
const response = await fetch('http://127.0.0.1:5000/api/v1/places/',
    {
        method:'GET',
        headers: {
            'Authorization': `token ${getCookie('token')}`,
            'Content-Type': 'application/json'
        }
    }
)
return await response.json();
    // Make a GET request to fetch places data
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaces function
}
function displayPlaces(places) {
const places_container = document.getElementById('places-list')
let display_html = ""
places.forEach(element => {
    display_html += `
            <div class="place-card">
                <h6> ${element.title }</h6>
                <p>Price per Night ${ element.price }</p>
                <button class="details-button">
                    <a href='http://127.0.0.1:5001/places/${element.id}'>View Details</a>
                </button>
            <div>
        `
});
// Might need to add description later
places_container.innerHTML = display_html
// Clear the current content of the places list
// Iterate over the places data
// For each place, create a div element and set its content
// Append the created element to the places list
}
function getPlaceIdFromURL() {
// Extract the place ID from window.location.search
// Your code here
return window.location.search

}
function checkPlaceAuthentication() {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        addReviewSection.style.display = 'none';
    } else {
        addReviewSection.style.display = 'block';
        // Store the token for later use
        fetchPlaceDetails(token, placeId);
    }
}
async function fetchPlaceDetails(token, placeId) {
    // Make a GET request to fetch place details
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaceDetails function
    const response = fetch(`http://127.0.0.1:5000/api/v1/places/${getPlaceIdFromURL()}`, {
    method: 'GET',
    headers: {
        'authorization': `token ${getCookie('token')}`,
        'Content-Type': 'application/json'
    },
    })
}
function displayPlaceDetails(place) {
    // Clear the current content of the place details section
    // Create elements to display the place details (name, description, price, amenities and reviews)
    // Append the created elements to the place details section
}
const checkIsTokenExpired = (token) => {
if (!token) {
    return true;
}

const payload = JSON.parse(atob(token.split('.')[1]));

const expiry = payload.exp * 1000; // convert seconds to milliseconds
const now = Date.now();

return now >= expiry;
}
function checkReviewAuthentication() {
      const token = getCookie('token');
      if (!token) {
          window.location.href = 'index.html';
      }
      return token;
  }
async function submitReview(token, placeId, reviewText) {
      // Make a POST request to submit review data
      // Include the token in the Authorization header
      // Send placeId and reviewText in the request body
      // Handle the response
  }
function handleResponse(response) {
      if (response.ok) {
          alert('Review submitted successfully!');
          // Clear the form
      } else {
          alert('Failed to submit review');
      }
  }