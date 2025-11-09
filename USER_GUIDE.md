# 📚 User Guide - Path Optimization Project

## Quick Start (3 Steps)

### Step 1: Start the Backend Server

**Option A - Using PowerShell script (Recommended)**:
```powershell
.\start_server.ps1
```

**Option B - Using Batch file**:
```batch
start_server.bat
```

**Option C - Manual**:
```powershell
cd backend
pip install -r requirements.txt
python server.py
```

The server will start on `http://localhost:5000`. Keep it running!

### Step 2: Open the Frontend

Simply open `frontend/index.html` in your web browser (Chrome, Firefox, Edge, or Safari).

**Alternative**: Use a local HTTP server:
```powershell
cd frontend
python -m http.server 8080
```
Then open `http://localhost:8080` in your browser.

### Step 3: Start Optimizing!

Follow the instructions in the web interface to set points and run optimization.

---

## Detailed Usage Guide

### Setting Up Your Scenario

#### 1. Set Start Point (Green)
- Click the **"Set Start"** button
- Click anywhere on the canvas to place the start point
- You'll see a green circle with "START" label

#### 2. Set Goal Point (Red)
- Click the **"Set Goal"** button  
- Click anywhere on the canvas to place the goal point
- You'll see a red circle with "GOAL" label

#### 3. Add Obstacles (Orange)
- Click the **"Add Obstacle"** button
- Click and hold on the canvas
- Drag outward to set the obstacle size
- Release to place the obstacle
- The solid circle is the obstacle, the dashed circle is the safety zone
- Repeat to add multiple obstacles

### Adjusting Parameters

#### Optimization Parameters

**Number of Waypoints** (5-50, default: 20)
- More waypoints = smoother, more flexible path
- Fewer waypoints = faster computation, simpler path
- Recommendation: 15-25 for most scenarios

**Safety Margin** (0-20, default: 5.0)
- Extra distance to maintain from obstacles
- Increase if the path gets too close to obstacles
- Decrease to allow tighter passages

**Learning Rate (α)** (0.0001-0.01, default: 0.001)
- Controls how fast the path changes each iteration
- Too high → unstable, oscillating behavior
- Too low → very slow convergence
- Sweet spot: 0.0005 - 0.002

**Iterations** (50-2000, default: 500)
- How many optimization steps to perform
- More iterations = better convergence (but slower)
- Watch the cost graph to see when it flattens

#### Cost Function Weights

These control what the optimizer prioritizes:

**Length Weight (w_len)** (0-10, default: 1.0)
- How much to penalize path length
- Higher → shorter paths (but might be less smooth)
- Lower → path length matters less

**Smoothness Weight (w_smooth)** (0-200, default: 50.0)
- How much to penalize sharp turns and jerky motion
- Higher → smoother, more graceful paths
- Lower → allows sharper corners
- Recommendation: 30-100 for realistic drone paths

**Obstacle Weight (w_obs)** (0-5000, default: 1000.0)
- How strongly to avoid obstacles
- Higher → path stays farther from obstacles
- Lower → path can get closer to obstacles
- **Important**: This should typically be much larger than the other weights
- Recommendation: 500-2000 for most cases, up to 5000 for very strict avoidance

### Running the Optimization

1. **Click "Run Optimization"**
   - The path will appear as a blue line with waypoints
   - You'll see it animate as it improves each iteration
   - The cost graph shows convergence in real-time

2. **Watch the Status Panel**
   - **Status**: Current state of the optimizer
   - **Iteration**: Which step the optimizer is on
   - **Current Cost**: Total cost value (lower is better)

3. **Monitor the Cost Graph**
   - Shows cost vs iteration number
   - Steep drop at start → rapid initial improvement
   - Flattening curve → converging to solution
   - Red dot → current position

4. **Stop if Needed**
   - Click **"Stop"** to halt the optimization early
   - Useful if you see it's converged before max iterations

5. **Clear and Retry**
   - Click **"Clear All"** to reset everything
   - Try different parameter combinations

---

## Understanding the Results

### What Makes a "Good" Path?

A good optimized path will:
1. ✅ Connect start to goal
2. ✅ Avoid all obstacles (stay outside safety zones)
3. ✅ Be reasonably short (not unnecessarily long)
4. ✅ Be smooth (no sharp, jerky turns)

### Reading the Cost Graph

- **Y-axis**: Total cost (lower is better)
- **X-axis**: Iteration number
- **Ideal curve**: Steep drop, then gradual flattening
- **Flat line**: Converged (found optimal solution)
- **Oscillating**: Learning rate too high, reduce α

### Cost Breakdown

The interface shows four values:

- **Total**: The combined weighted cost
- **Length**: Path length component
- **Smoothness**: Jerkiness/acceleration component  
- **Obstacle**: Penalty for being near obstacles

If obstacle cost is high → path is too close to obstacles → increase w_obs

---

## Common Scenarios & Solutions

### Scenario 1: Simple Obstacle Avoidance

**Setup**:
- Start: Left side
- Goal: Right side
- Obstacle: One circle in the middle

**Recommended Settings**:
- Waypoints: 15
- Safety Margin: 5
- Learning Rate: 0.001
- Iterations: 300
- Weights: Default (1, 50, 1000)

**Expected Result**: Path curves around the obstacle smoothly

### Scenario 2: Narrow Passage

**Setup**:
- Two large obstacles with narrow gap between them

**Recommended Settings**:
- Waypoints: 20-25
- Safety Margin: 3-5 (adjust to fit gap)
- Learning Rate: 0.0005 (slower, more careful)
- Iterations: 500-1000
- Weights: w_obs = 2000 (strict avoidance)

**Expected Result**: Path threads through the gap carefully

### Scenario 3: Many Obstacles (Maze-like)

**Setup**:
- Multiple obstacles creating a complex environment

**Recommended Settings**:
- Waypoints: 25-35
- Safety Margin: 5
- Learning Rate: 0.0008
- Iterations: 800-1500
- Weights: w_smooth = 30 (allow sharper turns), w_obs = 1500

**Expected Result**: Path navigates around all obstacles

---

## Troubleshooting

### Problem: Path Still Goes Through Obstacles

**Solutions**:
1. Increase `w_obstacle` to 2000-5000
2. Increase safety margin
3. Run more iterations (800-1500)
4. Decrease learning rate to 0.0005 for more careful steps

### Problem: Path is Too Jerky/Jagged

**Solutions**:
1. Increase `w_smoothness` to 100-200
2. Increase number of waypoints to 25-30
3. Decrease learning rate to 0.0005

### Problem: Optimization is Unstable (Bouncing)

**Solutions**:
1. Decrease learning rate to 0.0003-0.0005
2. Decrease w_obstacle if it's very high (try 500-1000)
3. Increase smoothness weight

### Problem: Path is Too Long/Inefficient

**Solutions**:
1. Increase `w_length` to 2-5
2. Decrease `w_smoothness` to 20-30
3. Reduce number of waypoints to 12-15

### Problem: Convergence is Too Slow

**Solutions**:
1. Increase learning rate to 0.002-0.005 (carefully!)
2. Increase iterations if it's improving but slowly
3. Reduce number of waypoints for faster computation

### Problem: Backend Error

**Solutions**:
1. Make sure Flask server is running (`python server.py`)
2. Check server terminal for error messages
3. Verify all dependencies installed: `pip install -r requirements.txt`
4. Test with: `python test_optimizer.py`

### Problem: Frontend Not Connecting

**Solutions**:
1. Check server is on `http://localhost:5000`
2. Open browser console (F12) for error messages
3. Disable browser extensions that might block requests
4. Try a different browser

---

## Advanced Tips

### Fine-Tuning for Specific Use Cases

**Drone Racing** (fast, aggressive paths):
- High w_length (2-3)
- Low w_smoothness (20-30)
- Moderate w_obs (500-800)
- Fewer waypoints (12-18)

**Passenger Comfort** (smooth, gentle paths):
- Low w_length (0.5-1)
- High w_smoothness (100-200)
- High w_obs (1500-2000)
- More waypoints (25-35)

**Tight Spaces** (precision navigation):
- Low learning rate (0.0003-0.0005)
- High w_obs (2000-3000)
- More waypoints (30-40)
- Many iterations (1000-2000)

### Understanding the Math

The optimizer minimizes:
```
f(P) = w_len × (sum of squared segment lengths)
     + w_smooth × (sum of squared accelerations)
     + w_obs × (sum of squared obstacle violations)
```

Each iteration:
1. Calculates gradient (direction of steepest cost increase)
2. Moves waypoints opposite to gradient
3. Step size controlled by learning rate

Converges when gradient ≈ 0 (local minimum found)

---

## Keyboard Shortcuts

Currently not implemented, but you could extend the code to add:
- `S` - Switch to Set Start mode
- `G` - Switch to Set Goal mode  
- `O` - Switch to Add Obstacle mode
- `Space` - Run optimization
- `Esc` - Stop optimization
- `C` - Clear all

---

## Export/Save Features (Future Enhancement)

Consider adding these features:
- Export path coordinates as JSON/CSV
- Save/load scenarios
- Export cost graph as image
- Record optimization video

---

## Performance Notes

- **Canvas size**: 800×600 pixels
- **Recommended waypoints**: 10-30 (more = slower)
- **Animation speed**: ~100 iterations/second
- **Browser**: Chrome/Edge recommended for best performance

---

## Need Help?

1. Check the **README.md** for technical details
2. Run the test suite: `python test_optimizer.py`
3. Check browser console for JavaScript errors (F12)
4. Check server terminal for Python errors
5. Verify all files are in correct locations

---

**Happy Path Planning! 🚁✨**
