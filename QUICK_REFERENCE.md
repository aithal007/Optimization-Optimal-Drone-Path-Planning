# 🚀 Quick Reference - Path Optimization Project

## Start the Project (2 Commands)

### Windows PowerShell
```powershell
# 1. Start backend server (in project root)
.\start_server.bat

# 2. Open frontend/index.html in your browser
```

### Alternative (Manual)
```powershell
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Start server
python server.py

# 3. Open frontend/index.html in browser
```

---

## File Structure

```
optmisation/
├── backend/
│   ├── optimizer.py          # Core optimization algorithm
│   ├── server.py             # Flask REST API
│   ├── test_optimizer.py     # Test suite
│   └── requirements.txt      # Dependencies: Flask, NumPy
├── frontend/
│   ├── index.html            # Main interface
│   ├── styles.css            # Styling
│   └── app.js                # UI logic & visualization
├── README.md                 # Project overview
├── USER_GUIDE.md             # Detailed usage guide
├── MATH_DOCUMENTATION.md     # Mathematical derivations
├── start_server.bat          # Quick start script (Windows)
└── start_server.ps1          # Quick start script (PowerShell)
```

---

## API Endpoints

### POST /api/optimize
Full optimization run
```json
{
  "start": [x, y],
  "goal": [x, y],
  "obstacles": [{"center": [x, y], "radius": r}],
  "n_points": 20,
  "safety_margin": 5.0,
  "weights": {"length": 1.0, "smoothness": 50.0, "obstacle": 1000.0},
  "n_iterations": 500,
  "learning_rate": 0.001
}
```

### GET /api/health
Health check - returns `{"status": "healthy"}`

---

## Key Formulas

### Total Cost
```
f(P) = w_len × f_len(P) + w_smooth × f_smooth(P) + w_obs × f_obs(P)
```

### Update Rule (Gradient Descent)
```
p_i_new = p_i_old - α × ∇f(p_i)
```

### Cost Components
- **Length**: `Σ ||p_{i+1} - p_i||²`
- **Smoothness**: `Σ ||p_{i+1} - 2p_i + p_{i-1}||²`
- **Obstacle**: `Σ Σ [max(0, R_j² - ||p_i - c_j||²)]²`

---

## Default Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| Waypoints | 20 | 5-50 | Number of points in path |
| Safety Margin | 5.0 | 0-20 | Extra obstacle distance |
| Learning Rate (α) | 0.001 | 0.0001-0.01 | Step size |
| Iterations | 500 | 50-2000 | Optimization steps |
| w_length | 1.0 | 0-10 | Length weight |
| w_smoothness | 50.0 | 0-200 | Smoothness weight |
| w_obstacle | 1000.0 | 0-5000 | Obstacle weight |

---

## Common Issues & Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Path through obstacles | Increase w_obstacle to 2000+ |
| Jerky path | Increase w_smoothness to 100+ |
| Unstable/oscillating | Decrease learning rate to 0.0005 |
| Too slow | Increase learning rate to 0.002 |
| Long path | Increase w_length to 2-3 |
| Backend error | Check server running: `http://localhost:5000/api/health` |

---

## Recommended Settings by Scenario

### Simple Obstacle (Default)
- Waypoints: 15-20
- Learning Rate: 0.001
- Weights: 1 / 50 / 1000

### Narrow Passage
- Waypoints: 20-25
- Learning Rate: 0.0005
- Safety Margin: 3-5
- Weights: 1 / 50 / 2000

### Many Obstacles
- Waypoints: 25-35
- Learning Rate: 0.0008
- Iterations: 800-1500
- Weights: 1 / 30 / 1500

### Smooth/Comfortable
- Waypoints: 25-30
- Weights: 0.5 / 150 / 1500

### Fast/Racing
- Waypoints: 12-18
- Weights: 3 / 20 / 800

---

## Testing

### Run Test Suite
```powershell
cd backend
python test_optimizer.py
```

### Test Individual Components
```python
from optimizer import PathOptimizer

# Create instance
opt = PathOptimizer(
    start=(0, 0),
    goal=(100, 100),
    obstacles=[{'center': [50, 50], 'radius': 10}],
    n_points=15
)

# Test gradients
grad = opt.gradient_total(opt.path, 5)
print(f"Gradient: {grad}")

# Run optimization
results = opt.optimize(n_iterations=100)
print(f"Final cost: {results[-1]['cost']:.2f}")
```

---

## Dependencies

### Python (backend)
```txt
flask==3.0.0
flask-cors==4.0.0
numpy==1.26.2
```

Install: `pip install -r backend/requirements.txt`

### Frontend
- No dependencies! Pure vanilla JavaScript
- Works in any modern browser (Chrome, Firefox, Edge, Safari)

---

## Keyboard Workflow (Example Usage)

1. **Click** "Set Start" → **Click** canvas (green point)
2. **Click** "Set Goal" → **Click** canvas (red point)
3. **Click** "Add Obstacle" → **Click-drag** canvas (orange circles)
4. **Adjust** sliders to tune parameters
5. **Click** "Run Optimization" → Watch it animate!
6. **Click** "Clear All" → Start over

---

## Performance Metrics

- **Animation Speed**: ~100 iterations/second
- **Typical Convergence**: 200-500 iterations
- **Browser**: Chrome/Edge recommended
- **Canvas**: 800×600 pixels
- **Computation**: O(N × M × K) where N=waypoints, M=obstacles, K=iterations

---

## Extending the Project

### Easy Extensions
- [ ] Add rectangle obstacles
- [ ] Export path as JSON
- [ ] Save/load scenarios
- [ ] Keyboard shortcuts
- [ ] Dark mode

### Moderate Extensions
- [ ] Adam optimizer (adaptive learning)
- [ ] Real-time step-by-step mode
- [ ] Multiple start/goal pairs
- [ ] Path animation playback
- [ ] 3D visualization

### Advanced Extensions
- [ ] Dynamic (moving) obstacles
- [ ] Velocity/acceleration constraints
- [ ] Multiple agents
- [ ] RRT* comparison
- [ ] Neural network path prediction

---

## Documentation Files

1. **README.md** - Project overview, setup, mathematical formulation
2. **USER_GUIDE.md** - Detailed usage, scenarios, troubleshooting
3. **MATH_DOCUMENTATION.md** - Complete mathematical derivations
4. **QUICK_REFERENCE.md** - This file (cheat sheet)

---

## Support Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server running (`python server.py`)
- [ ] Server accessible at `http://localhost:5000`
- [ ] Health endpoint works: `http://localhost:5000/api/health`
- [ ] Frontend opened in browser
- [ ] Browser console shows no errors (F12)
- [ ] CORS enabled (handled by flask-cors)

---

## Math Quick Reference

### Gradients (for point i)

**Length**:
```
∇f_len = 2(2p_i - p_{i-1} - p_{i+1})
```

**Smoothness**:
```
∇f_smooth = 2a_{i-1} - 4a_i + 2a_{i+1}
where a_k = p_{k+1} - 2p_k + p_{k-1}
```

**Obstacle** (if violated):
```
∇f_obs = -4v(p_i - c_j)
where v = R² - ||p_i - c_j||²
```

---

## Git Commands (If Using Version Control)

```bash
# Initialize repo
git init
git add .
git commit -m "Initial commit: Path optimization project"

# Create .gitignore
echo "__pycache__/" > .gitignore
echo "*.pyc" >> .gitignore
echo ".venv/" >> .gitignore
echo "venv/" >> .gitignore
```

---

**Quick Start**: Run `start_server.bat`, open `frontend/index.html`, enjoy! 🎉
