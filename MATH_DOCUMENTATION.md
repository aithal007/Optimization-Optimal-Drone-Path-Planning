# 📐 Mathematical Documentation

## Complete Derivation of Gradient Descent for Path Optimization

This document provides the detailed mathematical derivation of all gradient calculations used in the optimizer.

---

## 1. Problem Formulation

### Variables

- **Path**: $P = \{p_1, p_2, \ldots, p_N\}$ where each $p_i = (x_i, y_i) \in \mathbb{R}^2$
- **Fixed**: $p_1 = p_{start}$, $p_N = p_{goal}$
- **Optimization variables**: $\{p_2, p_3, \ldots, p_{N-1}\}$ (total of $2(N-2)$ variables)

### Obstacles

- $M$ circular obstacles
- Obstacle $j$: center $c_j = (c_{jx}, c_{jy})$, radius $r_j$
- Effective radius: $R_j = r_j + d_{safe}$ (includes safety margin)

---

## 2. Cost Functions

### 2.1 Length Cost

**Definition**: Sum of squared distances between consecutive waypoints.

$$f_{len}(P) = \sum_{i=1}^{N-1} \|p_{i+1} - p_i\|^2$$

**Expanded**:

$$f_{len}(P) = \sum_{i=1}^{N-1} \left[(x_{i+1} - x_i)^2 + (y_{i+1} - y_i)^2\right]$$

**Why squared distance?** 
- Differentiable everywhere (unlike Euclidean distance)
- Minimum occurs at same location
- Computationally efficient

### 2.2 Smoothness Cost

**Definition**: Sum of squared accelerations (second derivatives).

$$f_{smooth}(P) = \sum_{i=2}^{N-1} \|a_i\|^2$$

where the discrete acceleration at point $i$ is:

$$a_i = p_{i+1} - 2p_i + p_{i-1}$$

**Full form**:

$$f_{smooth}(P) = \sum_{i=2}^{N-1} \|p_{i+1} - 2p_i + p_{i-1}\|^2$$

**Physical interpretation**: 
- Measures how much the velocity changes between segments
- Low smoothness cost → gentle, flowing curves
- High smoothness cost → sharp turns, jerky motion

### 2.3 Obstacle Cost (Penalty Method)

**Definition**: Penalize points that violate safety constraints.

For a single point $p_i$ and obstacle $j$:

1. **Squared distance** from point to obstacle center:
   $$d_{sq} = \|p_i - c_j\|^2 = (x_i - c_{jx})^2 + (y_i - c_{jy})^2$$

2. **Squared safety radius**:
   $$R_{sq} = R_j^2 = (r_j + d_{safe})^2$$

3. **Violation amount**:
   $$v_{ij} = R_{sq} - d_{sq}$$

4. **Penalty**:
   $$\text{penalty}_{ij} = [\max(0, v_{ij})]^2$$

**Total obstacle cost**:

$$f_{obs}(P) = \sum_{i=2}^{N-1} \sum_{j=1}^{M} [\max(0, R_j^2 - \|p_i - c_j\|^2)]^2$$

**Note**: Only intermediate points are checked (not start and goal).

### 2.4 Total Cost

**Weighted sum**:

$$f(P) = w_{len} \cdot f_{len}(P) + w_{smooth} \cdot f_{smooth}(P) + w_{obs} \cdot f_{obs}(P)$$

---

## 3. Gradient Derivations

To perform gradient descent, we need:

$$\nabla_{p_i} f(P) = \left[\frac{\partial f}{\partial x_i}, \frac{\partial f}{\partial y_i}\right]$$

for each waypoint $p_i$ where $i \in \{2, 3, \ldots, N-1\}$.

### 3.1 Gradient of Length Cost

**Claim**:

$$\nabla_{p_i} f_{len}(P) = 2(p_i - p_{i-1}) + 2(p_i - p_{i+1})$$

**Proof**:

The length cost is:

$$f_{len} = \sum_{k=1}^{N-1} \|p_{k+1} - p_k\|^2$$

Point $p_i$ appears in exactly two terms:
- Term $(i-1)$: $\|p_i - p_{i-1}\|^2$
- Term $i$: $\|p_{i+1} - p_i\|^2$

For the $x$-component:

$$\frac{\partial f_{len}}{\partial x_i} = \frac{\partial}{\partial x_i}\left[(x_i - x_{i-1})^2 + (x_{i+1} - x_i)^2\right]$$

$$= 2(x_i - x_{i-1}) \cdot 1 + 2(x_{i+1} - x_i) \cdot (-1)$$

$$= 2(x_i - x_{i-1}) - 2(x_{i+1} - x_i)$$

$$= 2x_i - 2x_{i-1} - 2x_{i+1} + 2x_i$$

$$= 4x_i - 2x_{i-1} - 2x_{i+1}$$

$$= 2(2x_i - x_{i-1} - x_{i+1})$$

In vector form:

$$\nabla_{p_i} f_{len} = 2(p_i - p_{i-1}) + 2(p_i - p_{i+1}) = 2[2p_i - p_{i-1} - p_{i+1}]$$

**Alternative form**:
$$\nabla_{p_i} f_{len} = 2(p_i - p_{i-1}) - 2(p_{i+1} - p_i)$$

### 3.2 Gradient of Smoothness Cost

**Claim**:

$$\nabla_{p_i} f_{smooth}(P) = 2a_{i-1} - 4a_i + 2a_{i+1}$$

where $a_k = p_{k+1} - 2p_k + p_{k-1}$.

**Proof**:

The smoothness cost is:

$$f_{smooth} = \sum_{k=2}^{N-1} \|p_{k+1} - 2p_k + p_{k-1}\|^2$$

Point $p_i$ appears in three acceleration terms:

1. $a_{i-1} = p_i - 2p_{i-1} + p_{i-2}$ (coefficient of $p_i$ is $+1$)
2. $a_i = p_{i+1} - 2p_i + p_{i-1}$ (coefficient of $p_i$ is $-2$)
3. $a_{i+1} = p_{i+2} - 2p_{i+1} + p_i$ (coefficient of $p_i$ is $+1$)

For the $x$-component:

$$\frac{\partial f_{smooth}}{\partial x_i} = \frac{\partial}{\partial x_i}\left[\|a_{i-1}\|^2 + \|a_i\|^2 + \|a_{i+1}\|^2\right]$$

Using $\frac{\partial}{\partial x_i}\|a_k\|^2 = 2a_k \cdot \frac{\partial a_k}{\partial x_i}$:

$$= 2a_{i-1} \cdot \frac{\partial a_{i-1}}{\partial x_i} + 2a_i \cdot \frac{\partial a_i}{\partial x_i} + 2a_{i+1} \cdot \frac{\partial a_{i+1}}{\partial x_i}$$

The partial derivatives are:
- $\frac{\partial a_{i-1}}{\partial x_i} = 1$ (from the $x_i$ term in $a_{i-1}$)
- $\frac{\partial a_i}{\partial x_i} = -2$ (from the $-2x_i$ term in $a_i$)
- $\frac{\partial a_{i+1}}{\partial x_i} = 1$ (from the $x_i$ term in $a_{i+1}$)

Therefore:

$$\frac{\partial f_{smooth}}{\partial x_i} = 2a_{i-1} \cdot 1 + 2a_i \cdot (-2) + 2a_{i+1} \cdot 1$$

$$= 2a_{i-1} - 4a_i + 2a_{i+1}$$

In vector form:

$$\nabla_{p_i} f_{smooth} = 2a_{i-1} - 4a_i + 2a_{i+1}$$

**Expanded form** (showing all waypoint dependencies):

$$\nabla_{p_i} f_{smooth} = 2(p_i - 2p_{i-1} + p_{i-2}) - 4(p_{i+1} - 2p_i + p_{i-1}) + 2(p_{i+2} - 2p_{i+1} + p_i)$$

Collecting terms:

$$= 6p_i - 4p_{i-1} - 4p_{i+1} + 2p_{i-2} + 2p_{i+2}$$

**Boundary cases**:
- If $i = 2$: ignore $a_{i-1}$ term
- If $i = N-1$: ignore $a_{i+1}$ term

### 3.3 Gradient of Obstacle Cost

**Claim**:

$$\nabla_{p_i} f_{obs}(P) = \sum_{j=1}^{M} \nabla_{p_i} \text{penalty}_{ij}$$

where:

$$\nabla_{p_i} \text{penalty}_{ij} = \begin{cases}
-4v_{ij}(p_i - c_j) & \text{if } v_{ij} > 0 \\
0 & \text{if } v_{ij} \leq 0
\end{cases}$$

**Proof**:

For a single obstacle $j$ and point $i$:

$$\text{penalty}_{ij} = [\max(0, v_{ij})]^2$$

where $v_{ij} = R_j^2 - d_{sq}$ and $d_{sq} = \|p_i - c_j\|^2$.

**Case 1**: If $v_{ij} \leq 0$ (point is safe):
$$\text{penalty}_{ij} = 0 \implies \nabla_{p_i} \text{penalty}_{ij} = 0$$

**Case 2**: If $v_{ij} > 0$ (point violates safety):
$$\text{penalty}_{ij} = v_{ij}^2$$

Using the chain rule:

$$\frac{\partial \text{penalty}_{ij}}{\partial x_i} = 2v_{ij} \cdot \frac{\partial v_{ij}}{\partial x_i}$$

Now:
$$v_{ij} = R_j^2 - d_{sq} = R_j^2 - (x_i - c_{jx})^2 - (y_i - c_{jy})^2$$

$$\frac{\partial v_{ij}}{\partial x_i} = -2(x_i - c_{jx})$$

Therefore:

$$\frac{\partial \text{penalty}_{ij}}{\partial x_i} = 2v_{ij} \cdot [-2(x_i - c_{jx})] = -4v_{ij}(x_i - c_{jx})$$

In vector form:

$$\nabla_{p_i} \text{penalty}_{ij} = -4v_{ij}(p_i - c_j)$$

**Interpretation**:
- If $v_{ij} > 0$: point is inside safety zone
- Gradient points from obstacle center to the point (repulsive force)
- Magnitude proportional to violation amount $v_{ij}$

**Total gradient** (summing over all obstacles):

$$\nabla_{p_i} f_{obs}(P) = \sum_{j=1}^{M} \nabla_{p_i} \text{penalty}_{ij}$$

### 3.4 Total Gradient

Combining all components:

$$\nabla_{p_i} f(P) = w_{len} \cdot \nabla_{p_i} f_{len} + w_{smooth} \cdot \nabla_{p_i} f_{smooth} + w_{obs} \cdot \nabla_{p_i} f_{obs}$$

---

## 4. Gradient Descent Algorithm

### Update Rule

For each intermediate waypoint $p_i$ (where $i \in \{2, \ldots, N-1\}$):

$$p_i^{(k+1)} = p_i^{(k)} - \alpha \nabla_{p_i} f(P^{(k)})$$

where:
- $k$ is the iteration number
- $\alpha$ is the learning rate (step size)
- $\nabla_{p_i} f(P^{(k)})$ is the gradient at iteration $k$

### Full Algorithm

```
Input: start, goal, obstacles, N, α, max_iterations
Output: optimized path P

1. Initialize P by linear interpolation from start to goal
2. For k = 1 to max_iterations:
     For i = 2 to N-1:
         g_i ← ∇_{p_i} f(P)
         p_i ← p_i - α · g_i
     End For
   End For
3. Return P
```

### Convergence Condition

The algorithm converges when:

$$\|\nabla f(P)\| < \epsilon$$

for some small $\epsilon > 0$ (e.g., $10^{-6}$).

In practice, we run for a fixed number of iterations and monitor the cost:
- If cost decreases → making progress
- If cost plateaus → converged to local minimum
- If cost oscillates → learning rate too high

---

## 5. Numerical Considerations

### Learning Rate Selection

**Too large**: 
- Overshoots minimum
- Oscillates or diverges
- Cost increases

**Too small**:
- Very slow convergence
- May not reach minimum in given iterations

**Adaptive learning rate** (future enhancement):
- Start with larger $\alpha$
- Decrease if cost increases
- Increase if cost decreases steadily

### Stability

The smoothness term acts as a **regularizer**:
- Prevents path from becoming too erratic
- Improves numerical stability
- Similar to momentum in optimization

### Local Minima

Gradient descent finds **local minima**, not necessarily global:
- Different initializations may give different results
- Obstacle layout can create multiple local minima
- Current implementation: straight line initialization (simple, fast)
- Alternative: random perturbations, multiple restarts

---

## 6. Computational Complexity

### Per Iteration

- **Gradient computation**: $O(N \cdot M)$ where $N$ = waypoints, $M$ = obstacles
  - Length gradient: $O(N)$
  - Smoothness gradient: $O(N)$
  - Obstacle gradient: $O(N \cdot M)$ (each point checks all obstacles)

- **Path update**: $O(N)$

- **Total**: $O(N \cdot M)$ per iteration

### Full Optimization

With $K$ iterations: $O(K \cdot N \cdot M)$

**Example**:
- $N = 20$ waypoints
- $M = 5$ obstacles  
- $K = 500$ iterations
- Total operations: $500 \times 20 \times 5 = 50,000$ (very fast)

---

## 7. Extensions and Variations

### 7.1 Higher-Order Smoothness

Instead of acceleration, penalize jerk (third derivative):

$$f_{jerk}(P) = \sum_{i=2}^{N-2} \|p_{i+2} - 3p_{i+1} + 3p_i - p_{i-1}\|^2$$

### 7.2 Velocity Constraints

Add maximum speed between waypoints:

$$f_{velocity}(P) = \sum_{i=1}^{N-1} [\max(0, \|p_{i+1} - p_i\| - v_{max})]^2$$

### 7.3 Curvature Constraints

Limit maximum curvature (turning radius):

$$\kappa_i = \frac{\|a_i\|}{\|v_i\|^2}$$

where $v_i = p_{i+1} - p_i$ is the velocity.

### 7.4 Non-Circular Obstacles

For rectangular obstacle with corners $\{q_1, q_2, q_3, q_4\}$:

$$d(p, \text{rect}) = \min_{\text{edges}} d(p, \text{edge})$$

### 7.5 Dynamic Obstacles

For time-varying obstacles $c_j(t)$:

$$f_{obs}(P) = \sum_{i=2}^{N-1} \sum_{j=1}^{M} [\max(0, R_j^2 - \|p_i - c_j(t_i)\|^2)]^2$$

where $t_i$ is the time at waypoint $i$.

---

## 8. Connection to Other Methods

### Gradient Descent vs. Other Optimizers

| Method | Pros | Cons |
|--------|------|------|
| **Gradient Descent** | Simple, intuitive, fast per iteration | Can get stuck in local minima |
| **Conjugate Gradient** | Faster convergence | More complex implementation |
| **BFGS/L-BFGS** | Quasi-Newton, very fast | Requires Hessian approximation |
| **Adam** | Adaptive learning rate | Needs hyperparameter tuning |
| **Genetic Algorithm** | Global search | Very slow, many evaluations |

### Relation to Spline Fitting

The smoothness cost is similar to **cubic spline** interpolation:
- Splines minimize integrated squared second derivative
- Our discrete version approximates this
- Splines: analytical solution (solve linear system)
- Our method: iterative, handles arbitrary constraints

### Relation to Optimal Control

This is a **direct method** for trajectory optimization:
- Discretize path into waypoints (direct transcription)
- Minimize cost subject to constraints
- Alternative: indirect methods (solve Hamilton-Jacobi-Bellman)

---

## 9. Verification

### Gradient Checking (Finite Differences)

To verify gradient implementation:

$$\frac{\partial f}{\partial x_i} \approx \frac{f(x_i + h) - f(x_i - h)}{2h}$$

for small $h$ (e.g., $h = 10^{-5}$).

**Implementation**:
```python
def check_gradient(optimizer, i, component):
    h = 1e-5
    
    # Analytical gradient
    grad_analytical = optimizer.gradient_total(optimizer.path, i)[component]
    
    # Numerical gradient
    optimizer.path[i][component] += h
    f_plus = optimizer.total_cost(optimizer.path)
    
    optimizer.path[i][component] -= 2*h
    f_minus = optimizer.total_cost(optimizer.path)
    
    optimizer.path[i][component] += h  # restore
    
    grad_numerical = (f_plus - f_minus) / (2*h)
    
    error = abs(grad_analytical - grad_numerical)
    print(f"Analytical: {grad_analytical:.6f}")
    print(f"Numerical:  {grad_numerical:.6f}")
    print(f"Error:      {error:.6e}")
```

---

## 10. Summary of Key Equations

### Cost Function
$$f(P) = w_{len} \sum_{i=1}^{N-1} \|p_{i+1} - p_i\|^2 + w_{smooth} \sum_{i=2}^{N-1} \|p_{i+1} - 2p_i + p_{i-1}\|^2 + w_{obs} \sum_{i=2}^{N-1} \sum_{j=1}^{M} [\max(0, R_j^2 - \|p_i - c_j\|^2)]^2$$

### Gradients

**Length**:
$$\nabla_{p_i} f_{len} = 2(2p_i - p_{i-1} - p_{i+1})$$

**Smoothness**:
$$\nabla_{p_i} f_{smooth} = 2(p_i - 2p_{i-1} + p_{i-2}) - 4(p_{i+1} - 2p_i + p_{i-1}) + 2(p_{i+2} - 2p_{i+1} + p_i)$$

**Obstacle** (if $v_{ij} > 0$):
$$\nabla_{p_i} \text{penalty}_{ij} = -4v_{ij}(p_i - c_j)$$

### Update Rule
$$p_i \leftarrow p_i - \alpha \left[w_{len} \nabla_{p_i} f_{len} + w_{smooth} \nabla_{p_i} f_{smooth} + w_{obs} \nabla_{p_i} f_{obs}\right]$$

---

**End of Mathematical Documentation**
