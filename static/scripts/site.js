// Highcharts.getJSON(
//   "https://demo-live-data.highcharts.com/aapl-c.json",
//   function (data) {
//     // Create the chart
//     Highcharts.stockChart("container", {
//       rangeSelector: {
//         selected: 1,
//       },

//       title: {
//         text: "AAPL Stock Price",
//       },

//       series: [
//         {
//           name: "AAPL",
//           data: data,
//           tooltip: {
//             valueDecimals: 2,
//           },
//         },
//       ],
//     });
//   }
// );

// console.log("hello world");

async function callback() {
  const stock = document.getElementById("stock").value;
  const period = document.getElementById("period").value;
  const interval = document.getElementById("interval").value;
  let response = await fetch(
    "/callback/getStock?data=" +
      stock +
      "&period=" +
      period +
      "&interval=" +
      interval
  );
  if (response.ok) {
    let chartJson = await response.json();
    if (response.ok) {
      response = await fetch("/callback/getInfo?data=" + stock);
      let infoJson = await response.json();
      info(infoJson);
      Plotly.newPlot("chart", chartJson, {});
    } else {
      alert("HTTP-Error: " + response.status + "on getInfo");
    }
  } else {
    alert("HTTP-Error: " + response.status + "on getStock");
  }
}
function info(json) {
  let name = document.getElementById("companyName");
  name.innerHTML = json.shortName;
  name = document.getElementById("symbol");
  name.innerHTML = json.symbol;
  name = document.getElementById("dayHigh");
  name.innerHTML = json.dayHigh;
  name = document.getElementById("dayLow");
  name.innerHTML = json.dayLow;
}
