// Show table on page load
document.getElementById("table").style.display = "table";

// Fetch and display wine data
async function fetchData() {
   fetch("/api/v1/wines")
      .then(function(response) {
         return response.json();
      })
      .then(function(products) {
         let placeholder = document.querySelector("#data-output");
         let out = "";
         
         for(let product of products) {
            out += `
               <tr class="hover:bg-white/5 transition">
                  <td class="px-6 py-4"><img src="${product.image_src}" class="w-16 h-auto rounded-lg border border-gray-700"></td>
                  <td class="px-6 py-4">${product.wine_name}</td>
                  <td class="px-6 py-4">${product.type}</td>
                  <td class="px-6 py-4">${product.vintage}</td>
                  <td class="px-6 py-4">${product.producer}</td>
                  <td class="px-6 py-4">${product.grape}</td>
                  <td class="px-6 py-4">${product.classification}</td>
                  <td class="px-6 py-4">${product.region}</td>
               </tr>
            `;
         }
         placeholder.innerHTML = out;
      });
}

// Fetch data immediately on page load
fetchData();

// Auto-refresh every 10 seconds
setInterval(fetchData, 10000);