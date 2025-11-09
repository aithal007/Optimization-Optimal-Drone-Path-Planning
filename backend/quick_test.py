"""
Quick test to verify the optimizer works
"""
import sys
sys.path.insert(0, 'C:/Users/Lenovo/Documents/optmisation/backend')

from optimizer import PathOptimizer
import numpy as np

# Test scenario matching what you see in browser
start = (150, 400)
goal = (580, 190)
obstacles = [{'center': [460, 310], 'radius': 80}]

print("Creating optimizer...")
optimizer = PathOptimizer(
    start=start,
    goal=goal,
    obstacles=obstacles,
    n_points=20,
    safety_margin=5.0,
    weights={'length': 1.0, 'smoothness': 50.0, 'obstacle': 1000.0}
)

print(f"Initial cost: {optimizer.total_cost(optimizer.path):.2f}")
print(f"Initial obstacle cost: {optimizer.cost_obstacle(optimizer.path):.2f}")

# Run a few iterations
for i in range(10):
    path, cost = optimizer.optimize_step(learning_rate=0.001)
    obs_cost = optimizer.cost_obstacle(path)
    print(f"Iteration {i+1}: Total={cost:.2f}, Obstacle={obs_cost:.2f}")

print("\nRunning full optimization...")
results = optimizer.optimize(n_iterations=500, learning_rate=0.001)

final_cost = results[-1]['cost']
final_obs_cost = optimizer.cost_obstacle(optimizer.path)

print(f"\nFinal cost: {final_cost:.2f}")
print(f"Final obstacle cost: {final_obs_cost:.2f}")

if final_obs_cost < 1:
    print("✅ SUCCESS: Path avoids obstacle!")
else:
    print("❌ FAILED: Path still violates obstacle zone")
    print(f"   Try increasing obstacle weight or learning rate")
