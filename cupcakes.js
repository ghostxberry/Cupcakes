const BASE_URL = "http://localhost:5000/api";
const cupcakesList = document.getElementById("cupcakes-list");

function generateCupcakeHTML(cupcake) {
  return `
    <div data-cupcake-id=${cupcake.id}>
      <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="delete-button">X</button>
      </li>
      <img class="Cupcake-img"
            src="${cupcake.image}"
            alt="(no image provided)">
    </div>
  `;
}

async function showInitialCupcakes() {
  const response = await fetch(`${BASE_URL}/cupcakes`);
  const data = await response.json();

  for (let cupcakeData of data.cupcakes) {
    let newCupcake = document.createElement("div");
    newCupcake.innerHTML = generateCupcakeHTML(cupcakeData);
    cupcakesList.appendChild(newCupcake);
  }
}

document.getElementById("new-cupcake-form").addEventListener("submit", async function (evt) {
  evt.preventDefault();

  let flavor = document.getElementById("form-flavor").value;
  let rating = document.getElementById("form-rating").value;
  let size = document.getElementById("form-size").value;
  let image = document.getElementById("form-image").value;

  const response = await fetch(`${BASE_URL}/cupcakes`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      flavor,
      rating,
      size,
      image
    }),
  });

  const data = await response.json();
  let newCupcake = document.createElement("div");
  newCupcake.innerHTML = generateCupcakeHTML(data.cupcake);
  cupcakesList.appendChild(newCupcake);
  document.getElementById("new-cupcake-form").reset();
});

cupcakesList.addEventListener("click", function (evt) {
  if (evt.target.classList.contains("delete-button")) {
    evt.preventDefault();
    let cupcake = evt.target.closest("div");
    let cupcakeId = cupcake.getAttribute("data-cupcake-id");

    fetch(`${BASE_URL}/cupcakes/${cupcakeId}`, {
      method: 'DELETE',
    });

    cupcake.remove();
  }
});

document.addEventListener("DOMContentLoaded", showInitialCupcakes);
