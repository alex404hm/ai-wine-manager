document.getElementById("table").style.display = "block";
fetch("/api/v1/wines")
.then(function(response){
  return response.json();
})

.then(function(products){
  let placeholder = document.querySelector("#data-output");
  let out = "";
  
  for(let product of products){
      out += `
         <tr>
            <td>${product.wine_name}</td>
            <td>${product.type}</td>
            <td>${product.vintage}</td>
            <td>${product.producer}</td>
            <td>${product.grape}</td>
            <td>${product.classification}</td>
            <td>${product.region}</td>
         </tr>
      `;
   }
   placeholder.innerHTML = out;
})