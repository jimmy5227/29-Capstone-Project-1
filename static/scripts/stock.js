const symbol = document.querySelector("#symbol").innerText;

const currentPrice = document.querySelector("#price");
const titlePrice = document.querySelector("#title");
const updatePrice = () => {
  fetch(`/stock/${symbol}/currentPrice`).then((res) => {
    res.text().then((text) => {
      currentPrice.innerText = $ + text;
      titlePrice.innerText = symbol + " - " + text + " | WSB";
    });
  });
};
setInterval(updatePrice, 5000);

const ticker = async () => {
  let period = document.getElementById("period").value; // Change to accept user input
  let interval = document.getElementById("interval").value; // Change to accept user input

  const status = document.querySelector("#status");
  status.innerText = `Period of ${period} in ${interval} interval.`;

  let res = await fetch(
    `/stock/${symbol}/getStock?data=${symbol}&period=${period}&interval=${interval}`
  );
  if (res.ok) {
    let chartJson = await res.json();
    if (res.ok) {
      res = await fetch(`/stock/${symbol}/getInfo?data=${symbol}`);
      let infoJson = await res.json();
      info(infoJson);
      Plotly.newPlot("chart", chartJson, {});
    } else {
      alert("HTTP-Error: " + res.status + "on getInfo");
    }
  } else {
    alert("HTTP-Error: " + response.status + "on getStock");
  }
};

const info = (json) => {
  let name = document.getElementById("dayHigh");
  name.innerHTML = Math.round(json.dayHigh * 100) / 100;
  name = document.getElementById("dayLow");
  name.innerHTML = Math.round(json.dayLow * 100) / 100;
};

const button = document.querySelector("#fetch");
button.addEventListener("click", ticker);

ticker();
