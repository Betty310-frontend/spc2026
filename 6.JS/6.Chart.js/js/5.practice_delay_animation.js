const canvas = document.getElementById("my-canvas");
const btnContainer = document.getElementById("btn-container");

let delayed;
let selectedDatasetIndex = null;

const DATA_COUNT = 7;
const NUMBER_CFG = { count: DATA_COUNT, min: -100, max: 100 };

const baseColors = [
  Utils.CHART_COLORS.red,
  Utils.CHART_COLORS.blue,
  Utils.CHART_COLORS.green,
];

function datasetColor(datasetIndex) {
  const baseColor = baseColors[datasetIndex];

  if (selectedDatasetIndex === null || selectedDatasetIndex === datasetIndex) {
    return baseColor;
  }

  return Utils.transparentize(baseColor, 0.7);
}

const labels = Utils.months({ count: 7 });
const data = {
  labels: labels,
  datasets: [
    {
      label: "Dataset 1",
      data: Utils.numbers(NUMBER_CFG),
      backgroundColor: () => datasetColor(0),
    },
    {
      label: "Dataset 2",
      data: Utils.numbers(NUMBER_CFG),
      backgroundColor: () => datasetColor(1),
    },
    {
      label: "Dataset 3",
      data: Utils.numbers(NUMBER_CFG),
      backgroundColor: () => datasetColor(2),
    },
  ],
};

const config = {
  type: "bar",
  data: data,
  options: {
    responsive: false,
    animation: {
      onComplete: () => {
        delayed = true;
      },
      delay: (context) => {
        let delay = 0;
        if (context.type === "data" && context.mode === "default" && !delayed) {
          delay = context.dataIndex * 300 + context.datasetIndex * 100;
        }
        return delay;
      },
    },
    scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true,
      },
    },
    onClick: (event, elements, chart) => {
      if (elements.length === 0) {
        selectedDatasetIndex = null;
        chart.update();
        return;
      }

      const clickedDatasetIndex = elements[0].datasetIndex;

      selectedDatasetIndex =
        selectedDatasetIndex === clickedDatasetIndex
          ? null
          : clickedDatasetIndex;

      chart.update();
    },
  },
};

const myChart = new Chart(canvas, config);

const actions = [
  {
    name: "Randomize",
    handler(chart) {
      chart.data.datasets.forEach((dataset) => {
        dataset.data = Utils.numbers({
          count: chart.data.labels.length,
          min: -100,
          max: 100,
        });
      });
      chart.update();
    },
  },
];

actions.forEach((action) => {
  const button = document.createElement("button");
  button.className =
    "px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600";
  button.textContent = action.name;
  button.addEventListener("click", () => {
    action.handler(myChart);
  });
  btnContainer.appendChild(button);
});
