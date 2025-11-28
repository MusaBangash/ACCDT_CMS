/**
 * Dashboard JavaScript
 * Fetches dashboard data from API and renders charts and statistics
 */

let coursesChart, feesTrendChart;

document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();
});

function loadDashboardData() {
    fetch('/api/dashboard')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch dashboard data');
            }
            return response.json();
        })
        .then(data => {
            updateStatistics(data);
            renderCoursesChart(data.courses_data);
            renderFeesTrendChart(data.fee_trend);
        })
        .catch(error => {
            console.error('Error loading dashboard data:', error);
            showError('Failed to load dashboard data. Please refresh the page.');
        });
}

function updateStatistics(data) {
    // Student statistics
    document.getElementById('total_students').textContent = data.total_students;
    document.getElementById('total_students_2').textContent = data.total_students;
    document.getElementById('total_male').textContent = data.total_male;
    document.getElementById('total_female').textContent = data.total_female;

    // Admission type breakdown
    document.getElementById('total_day_scholars').textContent = data.total_day_scholars;
    document.getElementById('total_day_scholars_male').textContent = data.total_day_scholars_male;
    document.getElementById('total_day_scholars_female').textContent = data.total_day_scholars_female;

    document.getElementById('total_hostel').textContent = data.total_hostel;
    document.getElementById('total_hostel_male').textContent = data.total_hostel_male;
    document.getElementById('total_hostel_female').textContent = data.total_hostel_female;

    // Course and enrollment
    document.getElementById('total_courses').textContent = data.total_courses;

    // Monthly statistics
    document.getElementById('new_admissions_this_month').textContent = data.new_admissions_this_month;
    
    const feesCollected = formatCurrency(data.fees_collected_month);
    document.getElementById('fees_collected_month').textContent = feesCollected;
    document.getElementById('fees_collected_month_2').textContent = feesCollected;

    const feesPending = formatCurrency(data.fees_pending_month);
    document.getElementById('fees_pending_month').textContent = feesPending;

    // Attendance
    document.getElementById('attendance_percent').textContent = data.attendance_percent.toFixed(1) + '%';
}

function renderCoursesChart(coursesData) {
    const ctx = document.getElementById('coursesChart').getContext('2d');
    
    // Prepare data for chart
    const labels = coursesData.map(c => c.name);
    const counts = coursesData.map(c => c.students);

    if (coursesChart) {
        coursesChart.destroy();
    }

    coursesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Students Enrolled',
                    data: counts,
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(240, 147, 251, 0.8)',
                        'rgba(5, 163, 74, 0.8)',
                        'rgba(255, 159, 67, 0.8)',
                        'rgba(238, 90, 111, 0.8)',
                    ],
                    borderRadius: 4,
                    borderSkipped: false,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

function renderFeesTrendChart(feesTrendData) {
    const ctx = document.getElementById('feesTrendChart').getContext('2d');
    
    const labels = feesTrendData.map(f => f.month);
    const amounts = feesTrendData.map(f => f.amount);

    if (feesTrendChart) {
        feesTrendChart.destroy();
    }

    feesTrendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Fees Collected (Rs.)',
                    data: amounts,
                    borderColor: 'rgba(102, 126, 234, 1)',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 2,
                    pointRadius: 4,
                    pointBackgroundColor: 'rgba(102, 126, 234, 1)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'Rs. ' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

function formatCurrency(amount) {
    return 'Rs. ' + parseFloat(amount).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function showError(message) {
    const alertHtml = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    const container = document.querySelector('main');
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = alertHtml;
    container.insertBefore(tempDiv.firstElementChild, container.firstElementChild);
}
