# 🗺️ Project Architecture & Flow

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                    (Web Browser)                             │
└────────────────┬───────────────────────────┬─────────────────┘
                 │                           │
                 ▼                           ▼
┌────────────────────────────┐   ┌──────────────────────────┐
│      FRONTEND              │   │    FRONTEND              │
│   (index.html)             │   │    (app.js)              │
│                            │   │                          │
│  ┌──────────────────────┐  │   │  ┌────────────────────┐ │
│  │  Interactive Canvas  │  │   │  │  Event Handlers    │ │
│  │  - Draw obstacles    │  │   │  │  - Mouse events    │ │
│  │  - Set start/goal    │  │   │  │  - Button clicks   │ │
│  │  - Display path      │  │   │  │  - Slider changes  │ │
│  └──────────────────────┘  │   │  └────────────────────┘ │
│                            │   │                          │
│  ┌──────────────────────┐  │   │  ┌────────────────────┐ │
│  │  Control Panel       │  │   │  │  Visualization     │ │
│  │  - Parameter sliders │  │   │  │  - Path animation  │ │
│  │  - Weight controls   │  │   │  │  - Cost graph      │ │
│  │  - Run/Stop buttons  │  │   │  │  - Real-time update│ │
│  └──────────────────────┘  │   │  └────────────────────┘ │
└────────────┬───────────────┘   └──────────┬───────────────┘
             │                               │
             │        HTTP POST              │
             │    /api/optimize              │
             └───────────┬───────────────────┘
                         ▼
             ┌───────────────────────────┐
             │      BACKEND              │
             │    (server.py)            │
             │    Flask REST API         │
             │                           │
             │  ┌─────────────────────┐  │
             │  │  API Endpoints      │  │
             │  │  - /api/optimize    │  │
             │  │  - /api/single_step │  │
             │  │  - /api/cost        │  │
             │  │  - /api/health      │  │
             │  └─────────────────────┘  │
             └───────────┬───────────────┘
                         │
                         ▼
             ┌───────────────────────────┐
             │  OPTIMIZATION ENGINE      │
             │   (optimizer.py)          │
             │   PathOptimizer class     │
             │                           │
             │  ┌─────────────────────┐  │
             │  │  Cost Functions     │  │
             │  │  - Length           │  │
             │  │  - Smoothness       │  │
             │  │  - Obstacle         │  │
             │  └─────────────────────┘  │
             │                           │
             │  ┌─────────────────────┐  │
             │  │  Gradient Calcs     │  │
             │  │  - ∇ Length        │  │
             │  │  - ∇ Smoothness    │  │
             │  │  - ∇ Obstacle      │  │
             │  └─────────────────────┘  │
             │                           │
             │  ┌─────────────────────┐  │
             │  │  Optimizer          │  │
             │  │  - Gradient Descent │  │
             │  │  - Path Update      │  │
             │  │  - Convergence      │  │
             │  └─────────────────────┘  │
             └───────────────────────────┘
```

---

## Data Flow Diagram

```
User Input
    │
    ├─► Start Point (x_s, y_s)
    ├─► Goal Point (x_g, y_g)
    ├─► Obstacles [{center, radius}, ...]
    ├─► Parameters (N, α, d_safe, weights)
    │
    ▼
┌───────────────────────────────────────┐
│  Frontend (app.js)                    │
│  Prepare JSON request                 │
└───────────────┬───────────────────────┘
                │
                │ HTTP POST
                │ {start, goal, obstacles, params}
                │
                ▼
┌───────────────────────────────────────┐
│  Backend (server.py)                  │
│  Parse request, create optimizer      │
└───────────────┬───────────────────────┘
                │
                ▼
┌───────────────────────────────────────┐
│  PathOptimizer (optimizer.py)         │
│                                       │
│  1. Initialize path (straight line)   │
│  2. For each iteration:               │
│     a. Calculate cost                 │
│     b. Calculate gradients            │
│     c. Update waypoints               │
│  3. Return results                    │
└───────────────┬───────────────────────┘
                │
                │ Return JSON
                │ {results: [{iteration, path, cost}]}
                │
                ▼
┌───────────────────────────────────────┐
│  Frontend (app.js)                    │
│  Animate results frame-by-frame       │
└───────────────┬───────────────────────┘
                │
                ▼
┌───────────────────────────────────────┐
│  Canvas Display                       │
│  - Draw optimized path                │
│  - Update cost graph                  │
│  - Show iteration count               │
└───────────────────────────────────────┘
```

---

## Optimization Algorithm Flow

```
START
  │
  ▼
[Initialize Path P₀]
P = linear interpolation from start to goal
  │
  ▼
[For k = 1 to max_iterations]
  │
  ├─► [Calculate Total Cost]
  │   f(P) = w_len·f_len + w_smooth·f_smooth + w_obs·f_obs
  │
  ├─► [For each waypoint i = 2 to N-1]
  │   │
  │   ├─► [Calculate Length Gradient]
  │   │   ∇f_len(pᵢ) = 2(2pᵢ - pᵢ₋₁ - pᵢ₊₁)
  │   │
  │   ├─► [Calculate Smoothness Gradient]
  │   │   ∇f_smooth(pᵢ) = 2aᵢ₋₁ - 4aᵢ + 2aᵢ₊₁
  │   │
  │   ├─► [Calculate Obstacle Gradient]
  │   │   ∇f_obs(pᵢ) = Σⱼ -4vᵢⱼ(pᵢ - cⱼ)  if violated
  │   │
  │   ├─► [Compute Total Gradient]
  │   │   ∇f(pᵢ) = w_len·∇f_len + w_smooth·∇f_smooth + w_obs·∇f_obs
  │   │
  │   └─► [Update Waypoint]
  │       pᵢ ← pᵢ - α·∇f(pᵢ)
  │
  ├─► [Store iteration result]
  │   {iteration: k, path: P, cost: f(P)}
  │
  └─► [Next iteration]
      │
      ▼
[Return all results]
  │
  ▼
END
```

---

## Cost Function Breakdown

```
                    Total Cost f(P)
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    w_len × f_len   w_smooth × f_smooth   w_obs × f_obs
         │               │                    │
         │               │                    │
         ▼               ▼                    ▼
    ┌─────────┐     ┌──────────┐      ┌──────────────┐
    │ Length  │     │Smoothness│      │  Obstacle    │
    │         │     │          │      │  Penalty     │
    │ Σ ||Δp||²│     │ Σ ||a||² │      │Σ Σ [max()]² │
    └─────────┘     └──────────┘      └──────────────┘
         │               │                    │
         │               │                    │
    Penalizes      Penalizes            Penalizes
    long paths     jerky paths          unsafe paths
```

---

## Gradient Calculation Components

```
For waypoint pᵢ:

         Total Gradient ∇f(pᵢ)
                │
    ┌───────────┼───────────┐
    │           │           │
    ▼           ▼           ▼
∇f_len(pᵢ)  ∇f_smooth(pᵢ)  ∇f_obs(pᵢ)
    │           │               │
    │           │               │
    ▼           ▼               ▼
Depends on: Depends on:    Depends on:
pᵢ₋₁        pᵢ₋₂            All obstacles
pᵢ          pᵢ₋₁            Distance to each
pᵢ₊₁        pᵢ              Violation amount
            pᵢ₊₁
            pᵢ₊₂
```

---

## Frontend State Machine

```
         ┌──────────┐
    ┌───►│  READY   │◄───┐
    │    └────┬─────┘    │
    │         │          │
    │         │ User clicks     │
    │         │ "Set Start"     │
    │         ▼          │
    │    ┌──────────┐   │
    │    │ SETTING  │   │
    │    │  START   │   │
    │    └────┬─────┘   │
    │         │          │
    │         │ Click canvas    │
    │         ▼          │
    │    ┌──────────┐   │
    │    │ SETTING  │   │
    │    │  GOAL    │   │
    │    └────┬─────┘   │
    │         │          │
    │         │ Click canvas    │
    │         ▼          │
    │    ┌──────────┐   │
    │    │ ADDING   │   │
    │    │OBSTACLES │   │
    │    └────┬─────┘   │
    │         │          │
    │         │ Click "Run"     │
    │         ▼          │
    │    ┌──────────┐   │
    │    │OPTIMIZING│   │
    │    │(Animated)│   │
    │    └────┬─────┘   │
    │         │          │
    │         │ Complete/Stop   │
    │         └──────────┘
    │              
    └──────────────┘
      "Clear All"
```

---

## File Dependency Graph

```
index.html
    │
    ├─► styles.css (styling)
    ├─► app.js (logic)
    │
    └─► Backend API
            │
            └─► server.py
                    │
                    └─► optimizer.py
                            │
                            └─► numpy (external)

Documentation:
    README.md
    USER_GUIDE.md
    MATH_DOCUMENTATION.md
    QUICK_REFERENCE.md
    PROJECT_SUMMARY.md

Testing:
    test_optimizer.py ──► optimizer.py

Launch Scripts:
    start_server.bat ──► server.py
    start_server.ps1 ──► server.py
```

---

## API Request/Response Flow

```
FRONTEND                   BACKEND
   │                          │
   │  POST /api/optimize      │
   ├─────────────────────────►│
   │  {                       │
   │    start: [x, y],        │
   │    goal: [x, y],         │
   │    obstacles: [...],     │
   │    n_points: 20,         │
   │    ...                   │
   │  }                       │
   │                          │
   │                          ├─► Create PathOptimizer
   │                          │
   │                          ├─► Run optimization
   │                          │   (500 iterations)
   │                          │
   │                          ├─► Collect results
   │                          │
   │  Return JSON             │
   │◄─────────────────────────┤
   │  {                       │
   │    results: [            │
   │      {iteration: 0,      │
   │       path: [[x,y],...], │
   │       cost: 123.45},     │
   │      ...                 │
   │    ],                    │
   │    final_cost: 10.5,     │
   │    initial_cost: 500     │
   │  }                       │
   │                          │
   ├─► Animate results        │
   │   (frame-by-frame)       │
   │                          │
   ▼                          ▼
```

---

## Gradient Descent Visualization

```
Cost Landscape (conceptual 3D surface)

    ^
    │           ╱╲
Cost│          ╱  ╲
    │    ╱╲   ╱    ╲
    │   ╱  ╲ ╱      ╲
    │  ╱    ╳        ╲___
    │ ╱    ╱ ╲          ╲___
    │╱____╱   ╲             ╲___
    └────────────────────────────►
              Waypoint position

Gradient Descent Path:
    Start (high cost)
      │
      ▼ -α·∇f  (move downhill)
      │
      ▼ -α·∇f
      │
      ▼ -α·∇f
      │
    Goal (low cost, local minimum)
```

---

## Typical Convergence Pattern

```
Cost
 │
 │ •
 │  ╲
 │   ╲•
 │    ╲
 │     ╲•
 │      ╲
 │       ╲•
 │        ╲
 │         •
 │          ╲•
 │           ╲___•___•___•___•___
 │                                
 └────────────────────────────────► Iteration
 0    100   200   300   400   500

Phases:
1. Rapid initial descent (0-100)
2. Steady improvement (100-300)
3. Fine-tuning (300-500)
4. Convergence (500+)
```

---

## Canvas Coordinate System

```
(0,0) ────────────────────► X (800)
  │
  │    START (green)    OBSTACLE (orange)
  │       •                 ⊗
  │        ╲               ╱
  │         ╲    PATH     ╱
  │          ╲   (blue)  ╱
  │           •─────────•
  │                    ╱
  │                   ╱
  │                  •
  │                   ╲
  │                    ╲
  │                     • GOAL (red)
  │
  ▼
  Y (600)
```

---

## Parameter Impact Map

```
           Increase Parameter
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
w_length      w_smoothness   w_obstacle
    │             │             │
    │             │             │
    ▼             ▼             ▼
Shorter       Smoother       Safer
paths         curves         paths
    │             │             │
But may       But may        But may
be jerky      be longer      be longer

Learning Rate (α)
    │
    ├─► Too High  → Oscillation, divergence
    └─► Too Low   → Slow convergence

Number of Waypoints (N)
    │
    ├─► More  → Smoother, more flexible, slower
    └─► Fewer → Simpler, faster, less flexible
```

---

## Error Handling Flow

```
User Action
    │
    ├─► Valid input
    │   └─► Process normally
    │
    └─► Invalid input
        │
        ├─► No start/goal set
        │   └─► Alert: "Please set start and goal"
        │
        ├─► Backend not running
        │   └─► Alert: "Backend server not running"
        │
        ├─► Network error
        │   └─► Alert: "Connection failed"
        │
        └─► Optimization error
            └─► Display error message
```

---

## Testing Flow

```
test_optimizer.py
    │
    ├─► Test 1: Gradient Calculations
    │   ├─► Create simple scenario
    │   ├─► Compute analytical gradients
    │   ├─► Verify non-zero
    │   └─► ✓ PASS
    │
    ├─► Test 2: Cost Components
    │   ├─► Test length cost
    │   ├─► Test smoothness cost
    │   ├─► Test obstacle cost
    │   └─► ✓ PASS
    │
    ├─► Test 3: Basic Optimization
    │   ├─► Run 100 iterations
    │   ├─► Verify cost decreases
    │   └─► ✓ PASS
    │
    └─► Test 4: Obstacle Avoidance
        ├─► Create path through obstacle
        ├─► Optimize
        ├─► Check no violations
        └─► ✓ PASS
```

---

## Deployment Checklist

```
□ Python 3.8+ installed
□ pip available
□ Install requirements: pip install -r requirements.txt
  ├─ Flask
  ├─ Flask-CORS
  └─ NumPy
□ Run tests: python test_optimizer.py
□ Start server: python server.py
□ Verify health: http://localhost:5000/api/health
□ Open frontend/index.html in browser
□ Test basic scenario
□ ✓ Ready to use!
```

---

This visualization guide provides a high-level overview of how all the components work together!
