"""
Path Optimization using Gradient Descent
Finds the optimal path from start to goal while avoiding obstacles
"""

import numpy as np
from typing import List, Tuple, Dict


class PathOptimizer:
    """
    Optimizes a path from start to goal using gradient descent.
    Minimizes a cost function that balances path length, smoothness, and obstacle avoidance.
    """
    
    def __init__(
        self,
        start: Tuple[float, float],
        goal: Tuple[float, float],
        obstacles: List[Dict],
        n_points: int = 20,
        safety_margin: float = 5.0,
        weights: Dict[str, float] = None
    ):
        """
        Initialize the path optimizer.
        
        Args:
            start: Starting point (x, y)
            goal: Goal point (x, y)
            obstacles: List of obstacles, each with 'center' (x, y) and 'radius'
            n_points: Number of waypoints in the path
            safety_margin: Additional safety distance around obstacles
            weights: Dictionary with keys 'length', 'smoothness', 'obstacle'
        """
        self.start = np.array(start)
        self.goal = np.array(goal)
        self.obstacles = obstacles
        self.n_points = n_points
        self.safety_margin = safety_margin
        
        # Initialize velocity for momentum
        self.velocity = None
        
        # Default weights
        if weights is None:
            weights = {'length': 1.0, 'smoothness': 50.0, 'obstacle': 1000.0}
        self.w_len = weights.get('length', 1.0)
        self.w_smooth = weights.get('smoothness', 50.0)
        self.w_obs = weights.get('obstacle', 1000.0)
        
        # Initialize path with linear interpolation
        self.path = self._initialize_path()
        
        # Store cost history
        self.cost_history = []
    
    def _initialize_path(self) -> np.ndarray:
        """
        Initialize path as a straight line from start to goal.
        
        Returns:
            Array of shape (n_points, 2) representing the initial path
        """
        path = np.zeros((self.n_points, 2))
        for i in range(self.n_points):
            t = i / (self.n_points - 1)
            path[i] = self.start * (1 - t) + self.goal * t
        return path
    
    def cost_length(self, path: np.ndarray) -> float:
        """
        Calculate the length cost of the path.
        Sum of squared distances between consecutive waypoints.
        
        Args:
            path: Array of waypoints (n_points, 2)
            
        Returns:
            Length cost value
        """
        diff = path[1:] - path[:-1]
        return np.sum(diff ** 2)
    
    def cost_smoothness(self, path: np.ndarray) -> float:
        """
        Calculate the smoothness cost of the path.
        Sum of squared accelerations (second derivatives).
        
        Args:
            path: Array of waypoints (n_points, 2)
            
        Returns:
            Smoothness cost value
        """
        if self.n_points < 3:
            return 0.0
        
        # Acceleration at each intermediate point
        acceleration = path[2:] - 2 * path[1:-1] + path[:-2]
        return np.sum(acceleration ** 2)
    
    def cost_obstacle(self, path: np.ndarray) -> float:
        """
        Calculate the obstacle avoidance cost using the penalty method.
        
        Args:
            path: Array of waypoints (n_points, 2)
            
        Returns:
            Obstacle cost value
        """
        total_cost = 0.0
        
        # Check intermediate points (not start and goal)
        for i in range(1, self.n_points - 1):
            point = path[i]
            
            for obstacle in self.obstacles:
                center = np.array(obstacle['center'])
                radius = obstacle['radius']
                
                # Squared distance from point to obstacle center
                d_sq = np.sum((point - center) ** 2)
                
                # Squared effective radius (including safety margin)
                R_sq = (radius + self.safety_margin) ** 2
                
                # Violation amount
                violation = R_sq - d_sq
                
                # Penalty if inside safety zone
                if violation > 0:
                    total_cost += violation ** 2
        
        return total_cost
    
    def total_cost(self, path: np.ndarray) -> float:
        """
        Calculate the total weighted cost of the path.
        
        Args:
            path: Array of waypoints (n_points, 2)
            
        Returns:
            Total cost value
        """
        f_len = self.cost_length(path)
        f_smooth = self.cost_smoothness(path)
        f_obs = self.cost_obstacle(path)
        
        # Clip individual costs to prevent overflow
        f_len = min(f_len, 1e12)
        f_smooth = min(f_smooth, 1e12)
        f_obs = min(f_obs, 1e12)
        
        total = self.w_len * f_len + self.w_smooth * f_smooth + self.w_obs * f_obs
        
        # Return finite value
        return total if np.isfinite(total) else 1e15
    
    def gradient_length(self, path: np.ndarray, i: int) -> np.ndarray:
        """
        Calculate the gradient of the length cost with respect to point i.
        
        Args:
            path: Current path
            i: Index of the point
            
        Returns:
            Gradient vector (2,)
        """
        grad = np.zeros(2)
        
        # Contribution from segment (i-1) to i
        if i > 0:
            grad += 2 * (path[i] - path[i-1])
        
        # Contribution from segment i to (i+1)
        if i < self.n_points - 1:
            grad += 2 * (path[i] - path[i+1])
        
        return grad
    
    def gradient_smoothness(self, path: np.ndarray, i: int) -> np.ndarray:
        """
        Calculate the gradient of the smoothness cost with respect to point i.
        
        Args:
            path: Current path
            i: Index of the point
            
        Returns:
            Gradient vector (2,)
        """
        if self.n_points < 3:
            return np.zeros(2)
        
        grad = np.zeros(2)
        
        # Point i appears in three acceleration terms:
        # a_{i-1} = p_i - 2*p_{i-1} + p_{i-2}  (coefficient: +1)
        # a_i = p_{i+1} - 2*p_i + p_{i-1}       (coefficient: -2)
        # a_{i+1} = p_{i+2} - 2*p_{i+1} + p_i   (coefficient: +1)
        
        # Contribution from a_{i-1}
        if i >= 2:
            accel = path[i] - 2 * path[i-1] + path[i-2]
            grad += 2 * accel
        
        # Contribution from a_i
        if 1 <= i <= self.n_points - 2:
            accel = path[i+1] - 2 * path[i] + path[i-1]
            grad += 2 * (-2) * accel
        
        # Contribution from a_{i+1}
        if i <= self.n_points - 3:
            accel = path[i+2] - 2 * path[i+1] + path[i]
            grad += 2 * accel
        
        return grad
    
    def gradient_obstacle(self, path: np.ndarray, i: int) -> np.ndarray:
        """
        Calculate the gradient of the obstacle cost with respect to point i.
        
        Args:
            path: Current path
            i: Index of the point
            
        Returns:
            Gradient vector (2,)
        """
        grad = np.zeros(2)
        point = path[i]
        
        for obstacle in self.obstacles:
            center = np.array(obstacle['center'])
            radius = obstacle['radius']
            
            # Squared distance
            d_sq = np.sum((point - center) ** 2)
            
            # Squared effective radius
            R_sq = (radius + self.safety_margin) ** 2
            
            # Violation
            violation = R_sq - d_sq
            
            if violation > 0:
                # Gradient of d_sq with respect to point
                grad_d_sq = 2 * (point - center)
                
                # Chain rule: d/dp (max(0, R_sq - d_sq)^2)
                grad += 2 * violation * (-grad_d_sq)
        
        return grad
    
    def gradient_total(self, path: np.ndarray, i: int) -> np.ndarray:
        """
        Calculate the total gradient at point i.
        
        Args:
            path: Current path
            i: Index of the point
            
        Returns:
            Total gradient vector (2,)
        """
        grad_len = self.gradient_length(path, i)
        grad_smooth = self.gradient_smoothness(path, i)
        grad_obs = self.gradient_obstacle(path, i)
        
        return (self.w_len * grad_len + 
                self.w_smooth * grad_smooth + 
                self.w_obs * grad_obs)
    
    def optimize_step(self, learning_rate: float = 0.001, momentum: float = 0.9) -> Tuple[np.ndarray, float]:
        """
        Perform one gradient descent step with momentum.
        
        Args:
            learning_rate: Step size for gradient descent
            momentum: Momentum coefficient (0.0 to 1.0)
            
        Returns:
            Tuple of (updated_path, current_cost)
        """
        # Initialize velocity if first step
        if self.velocity is None:
            self.velocity = np.zeros_like(self.path)
        
        # Create a copy of the path
        new_path = self.path.copy()
        
        # Update only intermediate points (not start and goal)
        for i in range(1, self.n_points - 1):
            # Calculate gradient
            grad = self.gradient_total(self.path, i)
            
            # Gradient clipping to prevent overflow (reduced for smoother optimization)
            grad_norm = np.linalg.norm(grad)
            max_grad_norm = 50.0  # Reduced from 1000 to prevent vibration
            if grad_norm > max_grad_norm:
                grad = grad * (max_grad_norm / grad_norm)
            
            # Check for NaN or Inf
            if not np.all(np.isfinite(grad)):
                grad = np.zeros_like(grad)
            
            # Update velocity with momentum
            self.velocity[i] = momentum * self.velocity[i] - learning_rate * grad
            
            # Update path using velocity
            new_path[i] = self.path[i] + self.velocity[i]
            
            # Ensure the updated point is finite
            if not np.all(np.isfinite(new_path[i])):
                new_path[i] = self.path[i]  # Keep old value if overflow
                self.velocity[i] = np.zeros(2)  # Reset velocity if overflow
        
        # Calculate cost
        cost = self.total_cost(new_path)
        
        # Check for overflow in cost
        if not np.isfinite(cost):
            cost = 1e15  # Large but finite number
        
        self.cost_history.append(cost)
        
        # Update path
        self.path = new_path
        
        return new_path, cost
    
    def optimize(self, n_iterations: int = 500, learning_rate: float = 0.001, momentum: float = 0.9) -> List[Dict]:
        """
        Run the full optimization process.
        
        Args:
            n_iterations: Number of gradient descent iterations
            learning_rate: Step size for gradient descent
            momentum: Momentum coefficient (0.0 to 1.0)
            
        Returns:
            List of dictionaries, each containing 'path' and 'cost' for that iteration
        """
        results = []
        
        # Add initial path
        initial_cost = self.total_cost(self.path)
        self.cost_history = [initial_cost]
        results.append({
            'iteration': 0,
            'path': self.path.tolist(),
            'cost': initial_cost
        })
        
        # Run optimization
        for iteration in range(1, n_iterations + 1):
            new_path, cost = self.optimize_step(learning_rate, momentum)
            
            results.append({
                'iteration': iteration,
                'path': new_path.tolist(),
                'cost': cost
            })
        
        return results
    
    def get_path(self) -> List[List[float]]:
        """Get the current path as a list of [x, y] coordinates."""
        return self.path.tolist()
    
    def get_cost_history(self) -> List[float]:
        """Get the history of cost values."""
        return self.cost_history
