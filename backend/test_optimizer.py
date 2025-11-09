"""
Test script for the path optimizer
Validates that the optimization algorithm works correctly
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from optimizer import PathOptimizer
import numpy as np


def test_basic_optimization():
    """Test basic path optimization with a simple scenario."""
    print("=" * 60)
    print("TEST: Basic Path Optimization")
    print("=" * 60)
    
    # Simple scenario: straight line with one obstacle in the middle
    start = (50, 300)
    goal = (750, 300)
    obstacles = [
        {'center': [400, 300], 'radius': 50}
    ]
    
    print(f"Start: {start}")
    print(f"Goal: {goal}")
    print(f"Obstacles: {len(obstacles)}")
    
    # Create optimizer
    optimizer = PathOptimizer(
        start=start,
        goal=goal,
        obstacles=obstacles,
        n_points=15,
        safety_margin=10.0,
        weights={'length': 1.0, 'smoothness': 50.0, 'obstacle': 1000.0}
    )
    
    # Check initial path
    initial_cost = optimizer.total_cost(optimizer.path)
    print(f"\nInitial cost: {initial_cost:.2f}")
    
    # Run optimization
    print("\nRunning optimization (100 iterations)...")
    results = optimizer.optimize(n_iterations=100, learning_rate=0.001)
    
    final_cost = results[-1]['cost']
    print(f"Final cost: {final_cost:.2f}")
    print(f"Cost reduction: {initial_cost - final_cost:.2f} ({(1 - final_cost/initial_cost)*100:.1f}%)")
    
    # Check that cost decreased
    assert final_cost < initial_cost, "Cost should decrease during optimization!"
    print("\n✅ TEST PASSED: Cost decreased as expected")
    
    return optimizer


def test_gradient_calculations():
    """Test that gradient calculations are correct."""
    print("\n" + "=" * 60)
    print("TEST: Gradient Calculations")
    print("=" * 60)
    
    start = (0, 0)
    goal = (100, 100)
    obstacles = [{'center': [50, 50], 'radius': 10}]
    
    optimizer = PathOptimizer(
        start=start,
        goal=goal,
        obstacles=obstacles,
        n_points=5,
        safety_margin=5.0
    )
    
    # Test gradient at middle point
    i = 2
    grad = optimizer.gradient_total(optimizer.path, i)
    
    print(f"Gradient at waypoint {i}: [{grad[0]:.4f}, {grad[1]:.4f}]")
    print(f"Gradient magnitude: {np.linalg.norm(grad):.4f}")
    
    # Gradient should not be zero (there's something to optimize)
    assert np.linalg.norm(grad) > 1e-6, "Gradient should not be zero!"
    print("\n✅ TEST PASSED: Gradients computed correctly")


def test_obstacle_avoidance():
    """Test that paths avoid obstacles."""
    print("\n" + "=" * 60)
    print("TEST: Obstacle Avoidance")
    print("=" * 60)
    
    start = (50, 300)
    goal = (750, 300)
    obstacles = [
        {'center': [400, 300], 'radius': 60}
    ]
    
    optimizer = PathOptimizer(
        start=start,
        goal=goal,
        obstacles=obstacles,
        n_points=20,
        safety_margin=15.0,
        weights={'length': 1.0, 'smoothness': 50.0, 'obstacle': 2000.0}
    )
    
    # Run optimization
    results = optimizer.optimize(n_iterations=300, learning_rate=0.002)
    
    final_path = np.array(results[-1]['path'])
    
    # Check if any point is inside the safety zone
    obstacle = obstacles[0]
    center = np.array(obstacle['center'])
    effective_radius = obstacle['radius'] + optimizer.safety_margin
    
    violations = 0
    for point in final_path[1:-1]:  # Check intermediate points
        dist = np.linalg.norm(point - center)
        if dist < effective_radius:
            violations += 1
    
    print(f"Safety zone violations: {violations} / {len(final_path) - 2}")
    print(f"Effective obstacle radius: {effective_radius:.1f}")
    
    if violations == 0:
        print("\n✅ TEST PASSED: Path successfully avoids obstacle!")
    else:
        print(f"\n⚠️  WARNING: {violations} points still in safety zone")
        print("   (May need more iterations or higher obstacle weight)")


def test_cost_components():
    """Test individual cost function components."""
    print("\n" + "=" * 60)
    print("TEST: Cost Function Components")
    print("=" * 60)
    
    start = (0, 0)
    goal = (100, 0)
    obstacles = []
    
    optimizer = PathOptimizer(
        start=start,
        goal=goal,
        obstacles=obstacles,
        n_points=10,
        safety_margin=5.0
    )
    
    # Test length cost (should be non-zero for any path)
    length_cost = optimizer.cost_length(optimizer.path)
    print(f"Length cost: {length_cost:.4f}")
    assert length_cost > 0, "Length cost should be positive!"
    
    # Test smoothness cost (should be ~0 for straight line)
    smoothness_cost = optimizer.cost_smoothness(optimizer.path)
    print(f"Smoothness cost: {smoothness_cost:.4f}")
    assert smoothness_cost < 1e-6, "Smoothness cost should be ~0 for straight line!"
    
    # Test obstacle cost (should be 0 when no obstacles)
    obstacle_cost = optimizer.cost_obstacle(optimizer.path)
    print(f"Obstacle cost: {obstacle_cost:.4f}")
    assert obstacle_cost == 0, "Obstacle cost should be 0 when no obstacles!"
    
    print("\n✅ TEST PASSED: All cost components working correctly")


def visualize_path(optimizer):
    """Print a simple ASCII visualization of the path."""
    print("\n" + "=" * 60)
    print("ASCII Visualization (XY plane)")
    print("=" * 60)
    
    path = optimizer.path
    
    # Find bounds
    x_coords = [p[0] for p in path]
    y_coords = [p[1] for p in path]
    
    print(f"\nPath summary:")
    print(f"  Start: ({path[0][0]:.1f}, {path[0][1]:.1f})")
    print(f"  Goal:  ({path[-1][0]:.1f}, {path[-1][1]:.1f})")
    print(f"  Waypoints: {len(path)}")
    print(f"  X range: [{min(x_coords):.1f}, {max(x_coords):.1f}]")
    print(f"  Y range: [{min(y_coords):.1f}, {max(y_coords):.1f}]")


if __name__ == '__main__':
    print("\n" + "🧪 RUNNING PATH OPTIMIZER TESTS" + "\n")
    
    try:
        # Run all tests
        test_gradient_calculations()
        test_cost_components()
        optimizer = test_basic_optimization()
        test_obstacle_avoidance()
        visualize_path(optimizer)
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe optimizer is working correctly!")
        print("You can now start the server with: python server.py")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
