// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Application State
const state = {
    mode: 'start',
    start: null,
    goal: null,
    obstacles: [],
    currentPath: null,
    isOptimizing: false,
    animationId: null,
    costHistory: [],
    currentIteration: 0,
    
    // Temp state for obstacle drawing
    tempObstacle: null,
    isDrawingObstacle: false,
    
    // Zoom and Pan state
    scale: 1,
    offsetX: 0,
    offsetY: 0,
    isPanning: false,
    lastMouseX: 0,
    lastMouseY: 0
};

// Canvas Setup
const canvas = document.getElementById('pathCanvas');
const ctx = canvas.getContext('2d');

// Graph Setup
const graphCanvas = document.getElementById('costGraph');
const graphCtx = graphCanvas.getContext('2d');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    updateStatus('Ready - Click to set start point');
    drawCanvas();
});

// Event Listeners
function initializeEventListeners() {
    // Mode buttons
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            state.mode = e.target.dataset.mode;
            updateStatus(`Mode: ${state.mode}`);
        });
    });
    
    // Action buttons
    document.getElementById('btnClear').addEventListener('click', clearAll);
    document.getElementById('btnOptimize').addEventListener('click', runOptimization);
    document.getElementById('btnStop').addEventListener('click', stopOptimization);
    
    // Canvas events
    canvas.addEventListener('mousedown', handleCanvasMouseDown);
    canvas.addEventListener('mousemove', handleCanvasMouseMove);
    canvas.addEventListener('mouseup', handleCanvasMouseUp);
    canvas.addEventListener('wheel', handleWheel, { passive: false });
    
    // Zoom button events
    document.getElementById('btnZoomIn').addEventListener('click', () => zoomAt(canvas.width/2, canvas.height/2, 1.2));
    document.getElementById('btnZoomOut').addEventListener('click', () => zoomAt(canvas.width/2, canvas.height/2, 0.8));
    document.getElementById('btnResetZoom').addEventListener('click', resetZoom);
}

// Canvas Mouse Handlers
function handleCanvasMouseDown(e) {
    const pos = getMousePos(e);
    
    // Middle mouse button or Ctrl+Left click for panning
    if (e.button === 1 || (e.button === 0 && e.ctrlKey)) {
        state.isPanning = true;
        state.lastMouseX = e.clientX;
        state.lastMouseY = e.clientY;
        canvas.style.cursor = 'grabbing';
        e.preventDefault();
        return;
    }
    
    if (state.mode === 'start') {
        state.start = pos;
        updateStatus('Start point set - Now set goal point');
        drawCanvas();
    } else if (state.mode === 'goal') {
        state.goal = pos;
        updateStatus('Goal point set - Ready to add obstacles or run optimization');
        drawCanvas();
    } else if (state.mode === 'obstacle') {
        state.isDrawingObstacle = true;
        state.tempObstacle = { center: pos, radius: 0 };
    }
}

function handleCanvasMouseMove(e) {
    if (state.isPanning) {
        const dx = e.clientX - state.lastMouseX;
        const dy = e.clientY - state.lastMouseY;
        state.offsetX += dx;
        state.offsetY += dy;
        state.lastMouseX = e.clientX;
        state.lastMouseY = e.clientY;
        drawCanvas();
        return;
    }
    
    if (state.isDrawingObstacle && state.tempObstacle) {
        const pos = getMousePos(e);
        const dx = pos.x - state.tempObstacle.center.x;
        const dy = pos.y - state.tempObstacle.center.y;
        state.tempObstacle.radius = Math.sqrt(dx * dx + dy * dy);
        drawCanvas();
    }
}

function handleCanvasMouseUp(e) {
    if (state.isPanning) {
        state.isPanning = false;
        canvas.style.cursor = 'default';
        return;
    }
    
    if (state.isDrawingObstacle && state.tempObstacle) {
        if (state.tempObstacle.radius > 5) {
            state.obstacles.push({
                center: [state.tempObstacle.center.x, state.tempObstacle.center.y],
                radius: state.tempObstacle.radius
            });
            updateStatus(`Obstacle added (${state.obstacles.length} total)`);
        }
        state.tempObstacle = null;
        state.isDrawingObstacle = false;
        drawCanvas();
    }
}

function getMousePos(e) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    
    const canvasX = (e.clientX - rect.left) * scaleX;
    const canvasY = (e.clientY - rect.top) * scaleY;
    
    // Transform to world coordinates
    return {
        x: (canvasX - state.offsetX) / state.scale,
        y: (canvasY - state.offsetY) / state.scale
    };
}

// Transform world coordinates to canvas coordinates
function worldToCanvas(x, y) {
    return {
        x: x * state.scale + state.offsetX,
        y: y * state.scale + state.offsetY
    };
}

// Drawing Functions
function drawCanvas() {
    // Clear canvas
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Save context and apply transformations
    ctx.save();
    ctx.translate(state.offsetX, state.offsetY);
    ctx.scale(state.scale, state.scale);
    
    // Draw grid
    drawGrid();
    
    // Draw obstacles
    state.obstacles.forEach(obs => {
        drawObstacle(obs.center[0], obs.center[1], obs.radius);
    });
    
    // Draw temp obstacle
    if (state.tempObstacle) {
        drawObstacle(
            state.tempObstacle.center.x,
            state.tempObstacle.center.y,
            state.tempObstacle.radius,
            true
        );
    }
    
    // Draw current path
    if (state.currentPath && state.currentPath.length > 0) {
        drawPath(state.currentPath);
    }
    
    // Draw start and goal
    if (state.start) {
        drawPoint(state.start.x, state.start.y, '#28a745', 10);
        ctx.fillStyle = '#000';
        ctx.font = 'bold 14px Arial';
        ctx.fillText('START', state.start.x + 15, state.start.y + 5);
    }
    
    if (state.goal) {
        drawPoint(state.goal.x, state.goal.y, '#dc3545', 10);
        ctx.fillStyle = '#000';
        ctx.font = 'bold 14px Arial';
        ctx.fillText('GOAL', state.goal.x + 15, state.goal.y + 5);
    }
    
    // Restore context
    ctx.restore();
}

function drawGrid() {
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 1 / state.scale; // Keep line width constant
    
    const gridSize = 50;
    const startX = Math.floor(-state.offsetX / state.scale / gridSize) * gridSize;
    const startY = Math.floor(-state.offsetY / state.scale / gridSize) * gridSize;
    const endX = startX + (canvas.width / state.scale) + gridSize;
    const endY = startY + (canvas.height / state.scale) + gridSize;
    
    // Vertical lines
    for (let x = startX; x < endX; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, startY);
        ctx.lineTo(x, endY);
        ctx.stroke();
    }
    
    // Horizontal lines
    for (let y = startY; y < endY; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(startX, y);
        ctx.lineTo(endX, y);
        ctx.stroke();
    }
}

function drawPoint(x, y, color, radius = 5) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, 2 * Math.PI);
    ctx.fill();
    
    // Outline
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 2;
    ctx.stroke();
}

function drawObstacle(x, y, radius, isTemp = false) {
    const safetyMargin = parseFloat(document.getElementById('safetyMargin').value);
    
    // Draw actual obstacle
    ctx.fillStyle = isTemp ? 'rgba(255, 99, 71, 0.3)' : 'rgba(255, 99, 71, 0.5)';
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, 2 * Math.PI);
    ctx.fill();
    
    ctx.strokeStyle = '#ff6347';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Draw safety zone
    ctx.strokeStyle = '#ff6347';
    ctx.lineWidth = 1;
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.arc(x, y, radius + safetyMargin, 0, 2 * Math.PI);
    ctx.stroke();
    ctx.setLineDash([]);
}

function drawPath(path) {
    if (path.length < 2) return;
    
    // Draw path line
    ctx.strokeStyle = '#667eea';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(path[0][0], path[0][1]);
    
    for (let i = 1; i < path.length; i++) {
        ctx.lineTo(path[i][0], path[i][1]);
    }
    ctx.stroke();
    
    // Draw waypoints
    path.forEach((point, i) => {
        if (i === 0 || i === path.length - 1) return; // Skip start and goal
        drawPoint(point[0], point[1], '#667eea', 4);
    });
}

// Cost Graph
function drawCostGraph() {
    if (state.costHistory.length === 0) return;
    
    const width = graphCanvas.width;
    const height = graphCanvas.height;
    const padding = 40;
    
    // Clear
    graphCtx.fillStyle = '#fff';
    graphCtx.fillRect(0, 0, width, height);
    
    // Find min and max
    const maxCost = Math.max(...state.costHistory);
    const minCost = Math.min(...state.costHistory);
    const costRange = maxCost - minCost || 1;
    
    // Draw axes
    graphCtx.strokeStyle = '#333';
    graphCtx.lineWidth = 2;
    graphCtx.beginPath();
    graphCtx.moveTo(padding, padding);
    graphCtx.lineTo(padding, height - padding);
    graphCtx.lineTo(width - padding, height - padding);
    graphCtx.stroke();
    
    // Draw labels
    graphCtx.fillStyle = '#333';
    graphCtx.font = '12px Arial';
    graphCtx.fillText('Cost', 5, padding);
    graphCtx.fillText('Iteration', width - padding - 30, height - 10);
    
    // Draw cost line
    graphCtx.strokeStyle = '#667eea';
    graphCtx.lineWidth = 2;
    graphCtx.beginPath();
    
    state.costHistory.forEach((cost, i) => {
        const x = padding + (i / (state.costHistory.length - 1)) * (width - 2 * padding);
        const y = height - padding - ((cost - minCost) / costRange) * (height - 2 * padding);
        
        if (i === 0) {
            graphCtx.moveTo(x, y);
        } else {
            graphCtx.lineTo(x, y);
        }
    });
    
    graphCtx.stroke();
    
    // Draw current position marker
    const currentX = padding + (state.currentIteration / (state.costHistory.length - 1)) * (width - 2 * padding);
    const currentY = height - padding - ((state.costHistory[state.currentIteration] - minCost) / costRange) * (height - 2 * padding);
    
    graphCtx.fillStyle = '#dc3545';
    graphCtx.beginPath();
    graphCtx.arc(currentX, currentY, 5, 0, 2 * Math.PI);
    graphCtx.fill();
}

// Optimization
async function runOptimization() {
    // Validation
    if (!state.start || !state.goal) {
        alert('Please set both start and goal points!');
        return;
    }
    
    if (state.isOptimizing) {
        return;
    }
    
    // Get parameters
    const params = {
        start: [state.start.x, state.start.y],
        goal: [state.goal.x, state.goal.y],
        obstacles: state.obstacles,
        n_points: parseInt(document.getElementById('nPoints').value),
        safety_margin: parseFloat(document.getElementById('safetyMargin').value),
        weights: {
            length: parseFloat(document.getElementById('weightLength').value),
            smoothness: parseFloat(document.getElementById('weightSmooth').value),
            obstacle: parseFloat(document.getElementById('weightObstacle').value)
        },
        n_iterations: parseInt(document.getElementById('nIterations').value),
        learning_rate: parseFloat(document.getElementById('learningRate').value),
        momentum: parseFloat(document.getElementById('momentum').value)
    };
    
    // UI updates
    state.isOptimizing = true;
    document.getElementById('btnOptimize').style.display = 'none';
    document.getElementById('btnStop').style.display = 'inline-block';
    updateStatus('Optimizing...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/optimize`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
        });
        
        if (!response.ok) {
            throw new Error('Optimization failed');
        }
        
        const data = await response.json();
        
        // Animate the results
        animateOptimization(data.results);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error running optimization. Make sure the backend server is running!');
        stopOptimization();
    }
}

function animateOptimization(results) {
    let index = 0;
    
    const animate = () => {
        if (!state.isOptimizing || index >= results.length) {
            stopOptimization();
            return;
        }
        
        const result = results[index];
        state.currentPath = result.path;
        state.currentIteration = result.iteration;
        state.costHistory = results.slice(0, index + 1).map(r => r.cost);
        
        // Update UI
        document.getElementById('iterationText').textContent = result.iteration;
        document.getElementById('costText').textContent = result.cost.toFixed(2);
        
        // Update cost breakdown
        document.getElementById('costTotal').textContent = result.cost.toFixed(2);
        
        // Draw
        drawCanvas();
        drawCostGraph();
        
        index++;
        
        // Continue animation
        state.animationId = setTimeout(animate, 10); // 10ms between frames
    };
    
    animate();
}

function stopOptimization() {
    state.isOptimizing = false;
    
    if (state.animationId) {
        clearTimeout(state.animationId);
        state.animationId = null;
    }
    
    document.getElementById('btnOptimize').style.display = 'inline-block';
    document.getElementById('btnStop').style.display = 'none';
    updateStatus('Optimization complete!');
}

// Zoom and Pan Functions
function handleWheel(e) {
    e.preventDefault();
    
    const rect = canvas.getBoundingClientRect();
    const mouseX = (e.clientX - rect.left) * (canvas.width / rect.width);
    const mouseY = (e.clientY - rect.top) * (canvas.height / rect.height);
    
    const zoomFactor = e.deltaY < 0 ? 1.1 : 0.9;
    zoomAt(mouseX, mouseY, zoomFactor);
}

function zoomAt(x, y, factor) {
    const oldScale = state.scale;
    state.scale *= factor;
    
    // Limit zoom range
    state.scale = Math.max(0.1, Math.min(5, state.scale));
    
    const actualFactor = state.scale / oldScale;
    
    // Adjust offset to zoom towards the point
    state.offsetX = x - (x - state.offsetX) * actualFactor;
    state.offsetY = y - (y - state.offsetY) * actualFactor;
    
    drawCanvas();
    updateZoomDisplay();
}

function resetZoom() {
    state.scale = 1;
    state.offsetX = 0;
    state.offsetY = 0;
    drawCanvas();
    updateZoomDisplay();
}

function updateZoomDisplay() {
    const zoomPercent = Math.round(state.scale * 100);
    const zoomElement = document.getElementById('zoomLevel');
    if (zoomElement) {
        zoomElement.textContent = `${zoomPercent}%`;
    }
}

function clearAll() {
    if (state.isOptimizing) {
        stopOptimization();
    }
    
    state.start = null;
    state.goal = null;
    state.obstacles = [];
    state.currentPath = null;
    state.costHistory = [];
    state.currentIteration = 0;
    
    // Clear cost display
    document.getElementById('iterationText').textContent = '0';
    document.getElementById('costText').textContent = 'N/A';
    document.getElementById('costTotal').textContent = 'N/A';
    document.getElementById('costLength').textContent = 'N/A';
    document.getElementById('costSmooth').textContent = 'N/A';
    document.getElementById('costObstacle').textContent = 'N/A';
    
    updateStatus('Cleared - Click to set start point');
    drawCanvas();
    
    // Clear graph
    graphCtx.fillStyle = '#fff';
    graphCtx.fillRect(0, 0, graphCanvas.width, graphCanvas.height);
}

function updateStatus(message) {
    document.getElementById('statusText').textContent = message;
}
