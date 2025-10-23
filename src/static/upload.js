const form = document.getElementById("upload-form");
const input = document.getElementById("image-input");
const errorMessage = document.getElementById("error-message");
const succesMessage = document.getElementById("succes-message");

form.addEventListener("submit", async function(e) {
    e.preventDefault();
    const file = input.files[0];
    if (!file) return; 

    const allowedTypes = ["image/jpeg", "image/png", "image/gif"];

    if (!allowedTypes.includes(file.type)) {
        errorMessage.textContent = "Error: Only JPG, PNG, GIF files are allowed!";
        errorMessage.style.color = "red";
        input.value = "";
        return;
    }

    // upload to /upload
    const fd = new FormData(form);
    try {
      const res = await fetch('/dashboard', { method: 'POST', body: fd });
      if (!res.ok) throw new Error('Upload failed');
      succesMessage.textContent = "Successfully uploaded";
      succesMessage.style.color = "green";

      // optionally call AI after saving:
      // getWine(); 
    } catch (err) {
      errorMessage.textContent = err.message || 'Upload error';
      errorMessage.style.color = "red";
    } finally {
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
}