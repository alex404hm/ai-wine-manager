// DOM Element References
const form = document.getElementById("upload-form");
const input = document.getElementById("image-input");
const errorMessage = document.getElementById("error-message");
const succesMessage = document.getElementById("succes-message");

// Allowed file types
const allowedTypes = ["image/jpeg", "image/png", "image/gif"];

// Form submit handler
form.addEventListener("submit", async function(e) {
    e.preventDefault();
    
    const file = input.files[0];
    if (!file) return; 

    // Validate file type
    if (!allowedTypes.includes(file.type)) {
        errorMessage.textContent = "Error: Only JPG, PNG, GIF files are allowed!";
        errorMessage.style.color = "red";
        input.value = "";
        return;
    }

    try {
        // Step 1: Upload the file
        const formData = new FormData(form);
        const uploadRes = await fetch('/dashboard', { method: 'POST', body: formData });
        if (!uploadRes.ok) throw new Error('Upload failed');
        
        const uploadData = await uploadRes.json();
        const filename = uploadData.filename;
        
        succesMessage.textContent = "Uploaded successfully, analyzing...";
        succesMessage.style.color = "green";
        
        // Step 2: Analyze the image with AI
        const analyzeFormData = new FormData();
        analyzeFormData.append('image', file);
        analyzeFormData.append('filename', filename);
        
        const analyzeRes = await fetch('/api/v1/ai', { method: 'POST', body: analyzeFormData });
        if (!analyzeRes.ok) throw new Error('Analysis failed');
        
        const analyzeData = await analyzeRes.json();
        succesMessage.textContent = "Wine analyzed successfully!";
        succesMessage.style.color = "green";
        
        input.value = "";

    } catch (err) {
        errorMessage.textContent = "Error: " + (err.message || 'Something went wrong');
        errorMessage.style.color = "red";
        input.value = "";
    }
});