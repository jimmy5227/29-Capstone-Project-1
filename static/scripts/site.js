const redirect = document.getElementById("redirect");
const search = document.getElementById("search");

search.addEventListener("click", () => {
  window.location.href = `/stock/${redirect.value}`;
});
