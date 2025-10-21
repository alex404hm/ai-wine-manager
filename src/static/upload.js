const form = document.getElementById("upload-form");
const input = document.getElementById("image-input");
const errorMessage = document.getElementById("error-message");
const succesMessage = document.getElementById("succes-message");

form.addEventListener("submit", function(e) {
    const file = input.files[0];
    if (!file) return; 

    const allowedTypes = ["image/jpeg", "image/png"];

    if (!allowedTypes.includes(file.type)) {
        e.preventDefault();
        errorMessage.textContent = "Error: Only JPG, PNG files are allowed!";
        errorMessage.style.color = "red";
        input.value = "";
    } else {
        errorMessage.textContent = "";
    }

    if (allowedTypes.includes(file.type)) {
        e.preventDefault();
        errorMessage.textContent = "Succesfully. Image uploaded";
        errorMessage.style.color = "green";
        input.value = "";
    }
});

// /api/v1/ai
function getWine() {
const url = 'http://127.0.0.1:5000/api/v1/ai';
const formData = new FormData();
formData.append('image', document.getElementById('image-input').files[0]);

fetch(url, {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error(error));
}