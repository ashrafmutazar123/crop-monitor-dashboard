document.addEventListener('DOMContentLoaded', function() {
    // Fetch chart data
    fetch('/api/chart-data/')
        .then(response => response.json())
        .then(data => {
            if (data.timestamps && data.timestamps.length > 0) {
                createSoilChart(data);
                createEnvChart(data);
            }
        })
        .catch(error => {
            console.log('No data available yet:', error);
        });

    // Auto-refresh every 5 minutes
    setInterval(() => {
        location.reload();
    }, 300000);
});

function createSoilChart(data) {
    const ctx = document.getElementById('soilChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.timestamps,
            datasets: [
                {
                    label: 'Soil Moisture (%)',
                    data: data.soil_moisture,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: false,
                    pointRadius: 4,
                    pointHoverRadius: 8,
                    borderWidth: 2
                },
                {
                    label: 'Soil pH',
                    data: data.soil_ph,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: false,
                    pointRadius: 4,
                    pointHoverRadius: 8,
                    borderWidth: 2,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Time (Hours)'
                    },
                    grid: {
                        display: true,
                        color: 'rgba(0,0,0,0.1)'
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Soil Moisture (%)'
                    },
                    grid: {
                        display: true,
                        color: 'rgba(59, 130, 246, 0.1)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'pH Level'
                    },
                    grid: {
                        drawOnChartArea: false,
                    }
                }
            }
        }
    });
}

function createEnvChart(data) {
    const ctx = document.getElementById('envChart').getContext('2d');
    
    // Convert light intensity to thousands for better display
    const lightData = data.light_intensity.map(val => val / 1000);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.timestamps,
            datasets: [
                {
                    label: 'VPD (kPa)',
                    data: data.vpd,
                    borderColor: '#8b5cf6',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    tension: 0.4,
                    fill: false,
                    pointRadius: 4,
                    pointHoverRadius: 8,
                    borderWidth: 2
                },
                {
                    label: 'Light Intensity (k lux)',
                    data: lightData,
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    tension: 0.4,
                    fill: false,
                    pointRadius: 4,
                    pointHoverRadius: 8,
                    borderWidth: 2,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Time (Hours)'
                    },
                    grid: {
                        display: true,
                        color: 'rgba(0,0,0,0.1)'
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'VPD (kPa)'
                    },
                    grid: {
                        display: true,
                        color: 'rgba(139, 92, 246, 0.1)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Light Intensity (k lux)'
                    },
                    grid: {
                        drawOnChartArea: false,
                    }
                }
            }
        }
    });
}