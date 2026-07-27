/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication()
  const form = document.getElementById('login-form')
  console.log(form)
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    formData = new FormData(form)
    data = Object.fromEntries(formData)
    console.log(data);
    loginUser(data.email, data.password)
  })
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
      const token = getCookie('token');
      const loginLink = document.getElementById('login-link');
      console.log(token);
      
      if (!token) {
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
      // Make a GET request to fetch places data
      // Include the token in the Authorization header
      // Handle the response and pass the data to displayPlaces function
  }