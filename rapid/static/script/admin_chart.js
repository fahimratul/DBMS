document.addEventListener("DOMContentLoaded", function () {
  const xValues = [100,200,300,400,500,600,700,800,900,1000];

  const canvas = document.getElementById("myChart");
  if (!canvas) {
    console.error("Canvas element with id 'myChart' not found.");
    return;
  }
  const ctx = canvas.getContext("2d");

  // Create gradient for first dataset (red)
  const gradientRed = ctx.createLinearGradient(0, 0, 0, 400);
  gradientRed.addColorStop(0, "rgba(17, 245, 253, 0.93)");
  gradientRed.addColorStop(1, "rgba(255, 255, 255, 0)");

  // Create gradient for second dataset (green)
  const gradientGreen = ctx.createLinearGradient(0, 0, 0, 400);
  gradientGreen.addColorStop(0, "rgba(200, 0, 173, 0.69)");
  gradientGreen.addColorStop(1, "rgba(255, 255, 255, 0)");

  new Chart(ctx, {
    type: "line",
    data: {
      labels: xValues,
      datasets: [
        { 
          data: [860,1140,1060,1060,1070,1110,1330,2210,7830,2478],
          borderColor: "blue",
          tension: 0.4,
          backgroundColor: gradientRed,
          fill: true
        },
        { 
          data: [1600,1700,1700,1900,2000,2700,4000,5000,6000,7000],
          borderColor: "purple",
          tension: 0.4,
          backgroundColor: gradientGreen,
          fill: true
        }
      ]
    },
    options: {
      plugins: {
        legend: { display: true }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { display: false } // Hide x axis ticks
        },
        y: {
          grid: { display: false },
          ticks: { display: false } // Hide y axis ticks
        }
      }
    }
  });
});