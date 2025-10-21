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
