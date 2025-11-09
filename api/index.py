"""
Vercel serverless function for path optimization API
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

# Import optimizer from same directory
from optimizer import PathOptimizer

# Create Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
@app.route('/api')
@app.route('/api/')
def home():
    """Home endpoint"""
    return jsonify({'status': 'ok', 'message': 'Path Optimization API', 'version': '1.0'})

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'API is running'})

@app.route('/api/optimize', methods=['POST', 'OPTIONS'])
def optimize():
    """Main optimization endpoint"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response, 200
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract parameters
        start = tuple(data.get('start', [0, 0]))
        goal = tuple(data.get('goal', [100, 100]))
        obstacles = data.get('obstacles', [])
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
        results = optimizer.optimize(
            n_iterations=n_iterations, 
            learning_rate=learning_rate, 
            momentum=momentum
        )
        
        response = jsonify({
            'results': results,
            'final_cost': results[-1]['cost'],
            'initial_cost': results[0]['cost'],
            'cost_history': optimizer.get_cost_history()
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    except Exception as e:
        import traceback
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        return jsonify({'error': error_msg}), 500

# Vercel serverless function handler
app = app

