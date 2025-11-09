"""
Flask server for path optimization
Provides REST API for the frontend to interact with the optimizer
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from optimizer import PathOptimizer
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication


@app.route('/api/optimize', methods=['POST'])
def optimize():
    """
    Endpoint to optimize a path.
    
    Expected JSON body:
    {
        "start": [x, y],
        "goal": [x, y],
        "obstacles": [{"center": [x, y], "radius": r}, ...],
        "n_points": 20,
        "safety_margin": 5.0,
        "weights": {"length": 1.0, "smoothness": 50.0, "obstacle": 1000.0},
        "n_iterations": 500,
        "learning_rate": 0.001
    }
    
    Returns:
    {
        "results": [
            {"iteration": 0, "path": [[x1, y1], [x2, y2], ...], "cost": 123.45},
            ...
        ],
        "final_cost": 10.5,
        "initial_cost": 500.0
    }
    """
    try:
        data = request.get_json()
        
        # Extract parameters
        start = tuple(data['start'])
        goal = tuple(data['goal'])
        obstacles = data['obstacles']
        n_points = data.get('n_points', 20)
        safety_margin = data.get('safety_margin', 5.0)
        weights = data.get('weights', {'length': 1.0, 'smoothness': 50.0, 'obstacle': 1000.0})
        n_iterations = data.get('n_iterations', 500)
        learning_rate = data.get('learning_rate', 0.001)
        momentum = data.get('momentum', 0.9)
        
        # Create optimizer
        optimizer = PathOptimizer(
            start=start,
            goal=goal,
            obstacles=obstacles,
            n_points=n_points,
            safety_margin=safety_margin,
            weights=weights
        )
        
        # Run optimization
        results = optimizer.optimize(n_iterations=n_iterations, learning_rate=learning_rate, momentum=momentum)
        
        return jsonify({
            'results': results,
            'final_cost': results[-1]['cost'],
            'initial_cost': results[0]['cost'],
            'cost_history': optimizer.get_cost_history()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/single_step', methods=['POST'])
def single_step():
    """
    Endpoint to perform a single optimization step.
    Useful for real-time animation.
    
    Expected JSON body:
    {
        "current_path": [[x1, y1], [x2, y2], ...],
        "start": [x, y],
        "goal": [x, y],
        "obstacles": [{"center": [x, y], "radius": r}, ...],
        "safety_margin": 5.0,
        "weights": {"length": 1.0, "smoothness": 50.0, "obstacle": 1000.0},
        "learning_rate": 0.001
    }
    
    Returns:
    {
        "path": [[x1, y1], [x2, y2], ...],
        "cost": 123.45
    }
    """
    try:
        data = request.get_json()
        
        # Extract parameters
        current_path = np.array(data['current_path'])
        start = tuple(data['start'])
        goal = tuple(data['goal'])
        obstacles = data['obstacles']
        safety_margin = data.get('safety_margin', 5.0)
        weights = data.get('weights', {'length': 1.0, 'smoothness': 50.0, 'obstacle': 1000.0})
        learning_rate = data.get('learning_rate', 0.001)
        momentum = data.get('momentum', 0.9)
        
        # Create optimizer with current path
        n_points = len(current_path)
        optimizer = PathOptimizer(
            start=start,
            goal=goal,
            obstacles=obstacles,
            n_points=n_points,
            safety_margin=safety_margin,
            weights=weights
        )
        
        # Set current path
        optimizer.path = current_path
        
        # Perform one step
        new_path, cost = optimizer.optimize_step(learning_rate=learning_rate, momentum=momentum)
        
        return jsonify({
            'path': new_path.tolist(),
            'cost': cost
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/calculate_cost', methods=['POST'])
def calculate_cost():
    """
    Endpoint to calculate the cost of a given path.
    
    Expected JSON body:
    {
        "path": [[x1, y1], [x2, y2], ...],
        "obstacles": [{"center": [x, y], "radius": r}, ...],
        "safety_margin": 5.0,
        "weights": {"length": 1.0, "smoothness": 50.0, "obstacle": 1000.0}
    }
    
    Returns:
    {
        "total_cost": 123.45,
        "length_cost": 10.0,
        "smoothness_cost": 5.0,
        "obstacle_cost": 108.45
    }
    """
    try:
        data = request.get_json()
        
        # Extract parameters
        path = np.array(data['path'])
        obstacles = data['obstacles']
        safety_margin = data.get('safety_margin', 5.0)
        weights = data.get('weights', {'length': 1.0, 'smoothness': 50.0, 'obstacle': 1000.0})
        
        # Create optimizer (start and goal are just the path endpoints)
        n_points = len(path)
        optimizer = PathOptimizer(
            start=tuple(path[0]),
            goal=tuple(path[-1]),
            obstacles=obstacles,
            n_points=n_points,
            safety_margin=safety_margin,
            weights=weights
        )
        
        # Calculate individual costs
        length_cost = optimizer.cost_length(path)
        smoothness_cost = optimizer.cost_smoothness(path)
        obstacle_cost = optimizer.cost_obstacle(path)
        total_cost = optimizer.total_cost(path)
        
        return jsonify({
            'total_cost': total_cost,
            'length_cost': length_cost,
            'smoothness_cost': smoothness_cost,
            'obstacle_cost': obstacle_cost
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    # For production (Render)
    if os.environ.get('RENDER'):
        print(f"Starting Path Optimization Server on port {port}...")
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        # For local development
        print("Starting Path Optimization Server...")
        print("Server running on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
