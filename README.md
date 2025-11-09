# 🚁 Path Optimization using Gradient Descent

An interactive web application that visualizes real-time path optimization from a start point to a goal point while avoiding obstacles. This project demonstrates the mathematical formulation and implementation of gradient descent for trajectory planning.

## 🌟 Features

- **Interactive Canvas**: Click to set start/goal points and drag to create circular obstacles
- **Real-time Visualization**: Watch the path optimize step-by-step in animated fashion
- **Adjustable Parameters**: Control the number of waypoints, learning rate, and cost function weights
- **Cost Function Breakdown**: Visualize how length, smoothness, and obstacle avoidance contribute to the total cost
- **Cost vs Iteration Graph**: Track optimization convergence in real-time

## 📐 Mathematical Formulation

### Cost Function

The optimizer minimizes a weighted sum of three costs:

**Total Cost**: `f(P) = w_len × f_len(P) + w_smooth × f_smooth(P) + w_obs × f_obs(P)`

1. **Length Cost** (`f_len`): Sum of squared distances between waypoints
   ```
   f_len(P) = Σ ||p_{i+1} - p_i||²
   ```

2. **Smoothness Cost** (`f_smooth`): Sum of squared accelerations (penalizes sharp turns)
   ```
   f_smooth(P) = Σ ||p_{i+1} - 2p_i + p_{i-1}||²
   ```

3. **Obstacle Cost** (`f_obs`): Penalty method for obstacle avoidance
   ```
   f_obs(P) = Σ Σ (max(0, R_j² - ||p_i - c_j||²))²
   ```
   where `R_j = r_j + d_safe` is the effective obstacle radius

### Gradient Descent

The optimization uses gradient descent to iteratively improve the path:

```
p_i_new = p_i_old - α × ∇f(p_i)
```

where:
- `α` is the learning rate (step size)
- `∇f(p_i)` is the gradient of the total cost with respect to waypoint `i`

## 🛠️ Project Structure

```
optmisation/
├── backend/
│   ├── optimizer.py       # Core optimization algorithm with gradient calculations
│   ├── server.py          # Flask REST API server
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── index.html         # Main HTML interface
│   ├── styles.css         # Styling and responsive design
│   └── app.js             # JavaScript for UI interaction and visualization
└── README.md              # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Installation

1. **Clone or navigate to the project directory**:
   ```powershell
   cd "c:\Users\Lenovo\Documents\optmisation"
   ```

2. **Install Python dependencies**:
   ```powershell
   cd backend
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the backend server**:
   ```powershell
   cd backend
   python server.py
   ```
   
   The server will start on `http://localhost:5000`

2. **Open the frontend**:
   - Open `frontend/index.html` in your web browser
   - Or use a simple HTTP server:
     ```powershell
     cd frontend
     python -m http.server 8080
     ```
   - Then navigate to `http://localhost:8080`

## 📖 How to Use

1. **Set Start Point**: Click the "Set Start" button, then click on the canvas to place the green start point

2. **Set Goal Point**: Click the "Set Goal" button, then click on the canvas to place the red goal point

3. **Add Obstacles**: Click the "Add Obstacle" button, then click and drag on the canvas to create circular obstacles
   - The dashed circle shows the safety margin zone

4. **Adjust Parameters**:
   - **Number of Waypoints**: More points = smoother path, but slower computation
   - **Safety Margin**: Extra distance to keep from obstacles
   - **Learning Rate (α)**: Controls optimization step size (too high = unstable, too low = slow)
   - **Iterations**: Number of optimization steps
   - **Weights**: Balance between path length, smoothness, and obstacle avoidance

5. **Run Optimization**: Click "Run Optimization" to watch the path optimize in real-time!

6. **Clear All**: Reset the canvas to start over

## 🎛️ Parameter Guide

### Recommended Starting Values

- **Number of Waypoints**: 20
- **Safety Margin**: 5.0
- **Learning Rate**: 0.001
- **Iterations**: 500
- **w_length**: 1.0
- **w_smoothness**: 50.0
- **w_obstacle**: 1000.0

### Tuning Tips

- **Increase w_obstacle** if the path cuts through obstacles
- **Increase w_smoothness** for less jerky paths
- **Increase w_length** to prefer shorter paths
- **Decrease learning rate** if optimization oscillates
- **Increase learning rate** if convergence is too slow

## 🧮 Implementation Details

### Backend (Python)

- **`optimizer.py`**: Contains the `PathOptimizer` class with:
  - Cost function calculations (length, smoothness, obstacle)
  - Gradient calculations for each cost component
  - Gradient descent optimization loop
  
- **`server.py`**: Flask REST API with endpoints:
  - `POST /api/optimize`: Run full optimization
  - `POST /api/single_step`: Perform one gradient descent step
  - `POST /api/calculate_cost`: Calculate cost breakdown for a path
  - `GET /api/health`: Health check

### Frontend (JavaScript)

- **Canvas Drawing**: Interactive drawing of obstacles, start/goal points, and the optimizing path
- **Real-time Animation**: Smooth animation of the optimization process
- **Cost Graph**: Live plotting of cost vs iteration
- **API Communication**: Fetches optimization results from the backend

## 🔬 Mathematical Details

### Gradient Calculations

Each cost component contributes to the gradient at waypoint `i`:

**Length Gradient**:
```
∂f_len/∂p_i = 2(p_i - p_{i-1}) + 2(p_i - p_{i+1})
```

**Smoothness Gradient**:
```
∂f_smooth/∂p_i = 2(p_i - 2p_{i-1} + p_{i-2}) - 4(p_{i+1} - 2p_i + p_{i-1}) + 2(p_{i+2} - 2p_{i+1} + p_i)
```

**Obstacle Gradient** (for each obstacle j):
```
∂f_obs/∂p_i = 2 × violation × (-2(p_i - c_j))
where violation = max(0, R_j² - ||p_i - c_j||²)
```

## 🎓 Educational Value

This project demonstrates:

1. **Optimization Theory**: Gradient descent, cost functions, convex/non-convex optimization
2. **Numerical Methods**: Finite differences, iterative solvers
3. **Calculus**: Partial derivatives, chain rule, gradient vectors
4. **Computer Graphics**: Canvas API, real-time rendering, animation
5. **Full-Stack Development**: REST APIs, client-server architecture
6. **Trajectory Planning**: Path smoothness, obstacle avoidance, safety constraints

## 🐛 Troubleshooting

**Problem**: "Error running optimization. Make sure the backend server is running!"
- **Solution**: Ensure the Flask server is running on port 5000
- Check if `http://localhost:5000/api/health` returns `{"status": "healthy"}`

**Problem**: Path goes through obstacles
- **Solution**: Increase the `w_obstacle` weight (try 2000-5000)

**Problem**: Path is too jerky
- **Solution**: Increase the `w_smoothness` weight (try 100-200)

**Problem**: Optimization is unstable/oscillating
- **Solution**: Decrease the learning rate (try 0.0005 or lower)

**Problem**: Optimization is too slow
- **Solution**: 
  - Increase learning rate (try 0.002-0.005)
  - Reduce number of iterations
  - Reduce number of waypoints

## 📝 License

This project is provided for educational purposes.

## 🤝 Contributing

Feel free to extend this project by:
- Adding different obstacle shapes (rectangles, polygons)
- Implementing different optimization algorithms (Adam, RMSprop)
- Adding path constraints (maximum curvature, velocity profiles)
- 3D path planning
- Multiple agents

## 📧 Support

For questions or issues, please check:
1. All Python dependencies are installed
2. Flask server is running
3. Browser console for JavaScript errors
4. CORS is enabled (handled by flask-cors)

---

**Enjoy optimizing paths! 🎉**
