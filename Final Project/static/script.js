let currentData = null;
let lastUpdateTime = null;
let isDetailViewOpen = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    updateClock();
    setInterval(updateClock, 1000);
    
    fetchData();
    setInterval(fetchData, 30000); // Update every 30 seconds
    
    // Check for station updates more frequently (every 2 seconds)
    setInterval(checkCurrentStation, 2000);
    
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

async function checkCurrentStation() {
    // Only check if detail view is not manually open
    if (isDetailViewOpen) {
        return;
    }
    
    try {
        const response = await fetch('/api/current_station');
        
        if (response.ok) {
            const stationData = await response.json();
            
            // Automatically show detail view when station is touched
            if (stationData && stationData.name) {
                console.log('[JS] Station touched detected:', stationData.name);
                showStationDetailDirect(stationData);
            }
        }
    } catch (error) {
        // No current station - that's ok
    }
}

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
    updateOverallStatus(data.overall_status);

    if (data.f_train) {
        updateTransitCard('f-train', data.f_train);
    }
    if (data.weather) {
        updateWeather(data.weather);
    }
}

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

// Show detail view by fetching station data
async function showDetail(stationId, line) {
    isDetailViewOpen = true;
    
    const mainView = document.getElementById('main-view');
    const detailView = document.getElementById('detail-view');
    const detailHeader = document.getElementById('detail-header');
    const detailContent = document.getElementById('detail-content');
    
    mainView.style.display = 'none';
    detailView.style.display = 'block';
    
    // Show loading state
    detailHeader.innerHTML = `
        <h2>Loading station data...</h2>
    `;
    detailContent.innerHTML = '<p style="text-align: center; color: #888;">Fetching real-time arrivals...</p>';
    
    try {
        // Fetch station-specific data
        const response = await fetch(`/api/station/${stationId}/${line}`);
        const data = await response.json();
        
        if (data && data.next_trains) {
            showStationDetailDirect(data);
        } else {
            detailContent.innerHTML = '<p style="text-align: center; color: #e74c3c;">Unable to load station data</p>';
        }
    } catch (error) {
        console.error('Error fetching station detail:', error);
        detailContent.innerHTML = '<p style="text-align: center; color: #e74c3c;">Connection error</p>';
    }
}

// Show station detail directly (used by both manual clicks and automatic touch detection)
function showStationDetailDirect(data) {
    isDetailViewOpen = true;
    
    const mainView = document.getElementById('main-view');
    const detailView = document.getElementById('detail-view');
    const detailHeader = document.getElementById('detail-header');
    const detailContent = document.getElementById('detail-content');
    
    mainView.style.display = 'none';
    detailView.style.display = 'block';
    
    // Create header with station info
    detailHeader.innerHTML = `
        <div class="transit-icon f-train-icon" style="width: 60px; height: 60px; font-size: 30px; margin: 0 auto 15px;">
            <span>${data.line}</span>
        </div>
        <h2>${data.name}</h2>
        <p class="status-label ${data.status}">${getStatusText(data.status)}</p>
    `;
    
    // Group trains by direction
    const trainsByDirection = {};
    
    if (data.next_trains && data.next_trains.length > 0) {
        data.next_trains.forEach(train => {
            const dir = train.direction;
            if (!trainsByDirection[dir]) {
                trainsByDirection[dir] = [];
            }
            trainsByDirection[dir].push(train);
        });
    }
    
    // Build trains HTML grouped by direction
    let trainsHTML = '<div class="upcoming-trains">';
    
    if (Object.keys(trainsByDirection).length > 0) {
        // Show each direction as a group
        Object.keys(trainsByDirection).forEach(direction => {
            const trains = trainsByDirection[direction];
            
            trainsHTML += `<h3 style="margin-top: 20px; margin-bottom: 10px; color: #fff; font-size: 18px;">${direction}</h3>`;
            
            trains.forEach((train, index) => {
                trainsHTML += `
                    <div class="train-item ${index === 0 ? 'next' : ''}">
                        <div class="train-time">${train.minutes} min</div>
                        <div class="train-info">${train.route || data.line} train</div>
                    </div>
                `;
            });
        });
    } else {
        trainsHTML += '<p style="color: #888; text-align: center;">No upcoming trains</p>';
    }
    
    trainsHTML += '</div>';
    
    // Add service alerts section
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
    
    detailContent.innerHTML = trainsHTML + alertsHTML;
}

// Hide detail view
function hideDetail() {
    isDetailViewOpen = false;
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