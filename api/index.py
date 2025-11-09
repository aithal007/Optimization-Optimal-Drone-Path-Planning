"""
Vercel serverless function for path optimization API
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from optimizer import PathOptimizer

# Create Flask app
app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Path Optimization API is running'})

@app.route('/api/optimize', methods=['POST', 'OPTIONS'])
def optimize():
    """Main optimization endpoint"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        
        # Extract parameters
        start = tuple(data['start'])
        goal = tuple(data['goal'])
        obstacles = data['obstacles']
        n_points = data.get('n_points', 20)
        safety_margin = data.get('safety_margin', 5.0)
        weights = data.get('weights', {'length': 1.0, 'smoothness': 5.0, 'obstacle': 1500.0})
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

# For Vercel
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()

