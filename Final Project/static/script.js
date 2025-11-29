// script.js - Roosevelt Transit Lens Frontend Logic

let currentData = null;
let lastUpdateTime = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    updateClock();
    setInterval(updateClock, 1000);
    
    fetchData();
    setInterval(fetchData, 30000); // Update every 30 seconds
    
    setInterval(updateTimeAgo, 1000); // Update "time ago" every second
});

// Update clock in status bar
function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: false 
    });
    
    document.getElementById('current-time').textContent = timeString;
    
    const detailTime = document.getElementById('detail-time');
    if (detailTime) {
        detailTime.textContent = timeString;
    }
}

// Fetch transit data from API
async function fetchData() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        currentData = data;
        lastUpdateTime = new Date();
        
        updateUI(data);
    } catch (error) {
        console.error('Error fetching data:', error);
        showError();
    }
}

// Force refresh data
async function forceRefresh() {
    const refreshBtn = document.querySelector('.refresh-btn');
    refreshBtn.textContent = 'Refreshing...';
    refreshBtn.style.pointerEvents = 'none';
    
    try {
        const response = await fetch('/api/refresh');
        const result = await response.json();
        
        if (result.success) {
            currentData = result.data;
            lastUpdateTime = new Date();
            updateUI(result.data);
        }
    } catch (error) {
        console.error('Error refreshing:', error);
    } finally {
        setTimeout(() => {
            refreshBtn.textContent = 'Tap to refresh';
            refreshBtn.style.pointerEvents = 'auto';
        }, 1000);
    }
}

// Update UI with fetched data
function updateUI(data) {
    if (!data) return;
    
    // Update overall status
    updateOverallStatus(data.overall_status);
    
    // Update F Train
    if (data.f_train) {
        updateTransitCard('f-train', data.f_train);
    }
    
    // Update Tram
    if (data.tram) {
        updateTram(data.tram);
    }
    
    // Update Ferry
    if (data.ferry) {
        updateFerry(data.ferry);
    }
    
    // Update Weather
    if (data.weather) {
        updateWeather(data.weather);
    }
}

// Update overall status indicator
function updateOverallStatus(status) {
    const statusCircle = document.getElementById('status-circle');
    const statusIcon = document.getElementById('status-icon');
    const statusText = document.getElementById('status-text');
    
    // Remove all status classes
    statusCircle.classList.remove('normal', 'delays', 'problems');
    statusText.classList.remove('normal', 'delays', 'problems');
    
    switch(status) {
        case 'normal':
            statusCircle.classList.add('normal');
            statusText.classList.add('normal');
            statusIcon.textContent = 'OK';
            statusText.textContent = 'All Systems Normal';
            break;
        case 'delays':
            statusCircle.classList.add('delays');
            statusText.classList.add('delays');
            statusIcon.textContent = '⚠';
            statusText.textContent = 'Some Delays';
            break;
        case 'problems':
            statusCircle.classList.add('problems');
            statusText.classList.add('problems');
            statusIcon.textContent = '✕';
            statusText.textContent = 'Service Issues';
            break;
        default:
            statusIcon.textContent = '?';
            statusText.textContent = 'Status Unknown';
    }
}

// Update transit card (F Train)
function updateTransitCard(cardId, data) {
    const statusLabel = document.getElementById(`${cardId}-status`);
    const timeValue = document.getElementById(`${cardId}-time`);
    
    // Update status
    statusLabel.classList.remove('normal', 'delays', 'problems');
    statusLabel.classList.add(data.status);
    
    switch(data.status) {
        case 'normal':
            statusLabel.textContent = 'On Time';
            break;
        case 'delays':
            statusLabel.textContent = 'Delays';
            break;
        case 'problems':
            statusLabel.textContent = 'Service Issues';
            break;
        default:
            statusLabel.textContent = 'Unknown';
    }
    
    // Update next train time
    if (data.next_trains && data.next_trains.length > 0) {
        const nextTrain = data.next_trains[0];
        timeValue.textContent = `${nextTrain.minutes} min`;
    } else {
        timeValue.textContent = '--';
    }
}

// Update tram card
function updateTram(data) {
    const statusLabel = document.getElementById('tram-status');
    const timeValue = document.getElementById('tram-time');
    
    statusLabel.classList.remove('normal', 'delays', 'problems');
    
    if (data.status === 'normal') {
        statusLabel.classList.add('normal');
        statusLabel.textContent = 'Operating';
        timeValue.textContent = data.next_departure ? `${data.next_departure} min` : '--';
    } else {
        statusLabel.textContent = 'Not Operating';
        timeValue.textContent = '--';
    }
}

// Update ferry card
function updateFerry(data) {
    const statusLabel = document.getElementById('ferry-status');
    const timeValue = document.getElementById('ferry-time');
    
    statusLabel.classList.remove('normal', 'delays', 'problems');
    statusLabel.classList.add(data.status);
    
    if (data.status === 'normal') {
        statusLabel.textContent = 'Normal Service';
        timeValue.textContent = data.next_arrival ? `${data.next_arrival} min` : '--';
    } else {
        statusLabel.textContent = 'Service Issue';
        timeValue.textContent = '--';
    }
}

// Update weather card
function updateWeather(data) {
    const weatherIcon = document.getElementById('weather-icon');
    const weatherCondition = document.getElementById('weather-condition');
    const weatherDetails = document.getElementById('weather-details');
    const travelConditions = document.getElementById('travel-conditions');
    
    // Set weather icon based on condition
    const iconMap = {
        'Clear': '☀️',
        'Clouds': '⛅',
        'Rain': '🌧️',
        'Snow': '❄️',
        'Thunderstorm': '⛈️',
        'Drizzle': '🌦️',
        'Mist': '🌫️',
        'Fog': '🌫️'
    };
    
    weatherIcon.textContent = iconMap[data.condition] || '⛅';
    weatherCondition.textContent = data.description;
    weatherDetails.textContent = `${data.temp}°F • Wind: ${data.wind_speed} mph`;
    
    // Determine travel conditions
    if (data.condition === 'Rain' || data.condition === 'Thunderstorm') {
        travelConditions.textContent = 'Consider covered transit';
    } else if (data.wind_speed > 15) {
        travelConditions.textContent = 'Windy conditions';
    } else {
        travelConditions.textContent = 'Good travel conditions';
    }
}

// Update "time ago" text
function updateTimeAgo() {
    if (!lastUpdateTime) return;
    
    const now = new Date();
    const diff = Math.floor((now - lastUpdateTime) / 1000); // seconds
    
    let timeAgo;
    if (diff < 60) {
        timeAgo = `${diff} seconds`;
    } else if (diff < 3600) {
        const mins = Math.floor(diff / 60);
        timeAgo = `${mins} minute${mins > 1 ? 's' : ''}`;
    } else {
        timeAgo = 'over an hour';
    }
    
    document.getElementById('last-update').textContent = timeAgo;
}

// Show detail view
function showDetail(type) {
    const mainView = document.getElementById('main-view');
    const detailView = document.getElementById('detail-view');
    const detailHeader = document.getElementById('detail-header');
    const detailContent = document.getElementById('detail-content');
    
    mainView.style.display = 'none';
    detailView.style.display = 'block';
    
    if (type === 'f-train' && currentData && currentData.f_train) {
        showFTrainDetail(detailHeader, detailContent, currentData.f_train);
    } else if (type === 'tram' && currentData && currentData.tram) {
        showTramDetail(detailHeader, detailContent, currentData.tram);
    } else if (type === 'ferry' && currentData && currentData.ferry) {
        showFerryDetail(detailHeader, detailContent, currentData.ferry);
    }
}

// Show F Train detail
function showFTrainDetail(header, content, data) {
    header.innerHTML = `
        <div class="transit-icon f-train-icon" style="width: 60px; height: 60px; font-size: 30px; margin: 0 auto 15px;">
            <span>F</span>
        </div>
        <h2>F Train Details</h2>
        <p class="status-label ${data.status}">${getStatusText(data.status)}</p>
    `;
    
    let trainsHTML = '<div class="upcoming-trains"><h3>Upcoming Trains</h3>';
    
    if (data.next_trains && data.next_trains.length > 0) {
        data.next_trains.forEach((train, index) => {
            trainsHTML += `
                <div class="train-item ${index === 0 ? 'next' : ''}">
                    <div class="train-time">${train.minutes} min</div>
                    <div class="train-info">To ${train.direction}</div>
                </div>
            `;
        });
    } else {
        trainsHTML += '<p style="color: #888;">No upcoming trains</p>';
    }
    
    trainsHTML += '</div>';
    
    let alertsHTML = '<div class="alerts-section"><h3>Service Alerts</h3>';
    
    if (data.alerts && data.alerts.length > 0) {
        data.alerts.forEach(alert => {
            alertsHTML += `
                <div class="alert-item problem">
                    <strong>${alert.header}</strong>
                    <p style="margin-top: 8px; font-size: 13px; color: #aaa;">${alert.description}</p>
                </div>
            `;
        });
    } else {
        alertsHTML += `
            <div class="alert-item">
                <strong>No delays or service changes</strong>
                <p style="margin-top: 8px; font-size: 13px; color: #aaa;">All trains running on schedule</p>
            </div>
        `;
    }
    
    alertsHTML += '</div>';
    
    content.innerHTML = trainsHTML + alertsHTML;
}

// Show Tram detail
function showTramDetail(header, content, data) {
    header.innerHTML = `
        <div class="transit-icon tram-icon" style="width: 60px; height: 60px; font-size: 35px; margin: 0 auto 15px;">
            <span>🚡</span>
        </div>
        <h2>Roosevelt Tram</h2>
        <p class="status-label ${data.status}">${getStatusText(data.status)}</p>
    `;
    
    content.innerHTML = `
        <div class="upcoming-trains">
            <h3>Schedule Information</h3>
            <div class="train-item">
                <div class="train-time">${data.next_departure ? `${data.next_departure} min` : 'Not operating'}</div>
                <div class="train-info">${data.frequency}</div>
            </div>
            <p style="margin-top: 20px; color: #888; font-size: 13px;">
                The Roosevelt Island Tramway operates daily from 6:00 AM to 2:00 AM.
                Frequency increases during rush hours.
            </p>
        </div>
    `;
}

// Show Ferry detail
function showFerryDetail(header, content, data) {
    header.innerHTML = `
        <div class="transit-icon ferry-icon" style="width: 60px; height: 60px; font-size: 35px; margin: 0 auto 15px;">
            <span>⛴</span>
        </div>
        <h2>NYC Ferry</h2>
        <p class="status-label ${data.status}">${getStatusText(data.status)}</p>
    `;
    
    content.innerHTML = `
        <div class="upcoming-trains">
            <h3>Next Arrival</h3>
            <div class="train-item">
                <div class="train-time">${data.next_arrival ? `${data.next_arrival} min` : '--'}</div>
                <div class="train-info">${data.route}</div>
            </div>
            <p style="margin-top: 20px; color: #888; font-size: 13px;">
                NYC Ferry provides service between Roosevelt Island and various NYC locations.
                Check weather conditions for outdoor travel comfort.
            </p>
        </div>
    `;
}

// Hide detail view
function hideDetail() {
    document.getElementById('main-view').style.display = 'block';
    document.getElementById('detail-view').style.display = 'none';
}

// Get status text
function getStatusText(status) {
    switch(status) {
        case 'normal': return 'Service Status: Normal';
        case 'delays': return 'Service Status: Delays';
        case 'problems': return 'Service Status: Issues';
        default: return 'Status Unknown';
    }
}

// Show error state
function showError() {
    const statusText = document.getElementById('status-text');
    statusText.textContent = 'Connection Error';
    statusText.style.color = '#e74c3c';
}