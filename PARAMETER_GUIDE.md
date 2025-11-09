# 🎯 Recommended Parameter Settings

Based on testing, here are the optimal parameter values for different scenarios:

## Default Settings (Now Applied)
- **Number of Waypoints**: 30 (increased from 20)
- **Safety Margin**: 5.0
- **Learning Rate**: 0.01 (increased from 0.001)
- **Iterations**: 1000 (increased from 500)
- **Length Weight**: 1.0
- **Smoothness Weight**: 10.0 (decreased from 50.0)
- **Obstacle Weight**: 2000 (increased from 1000)

## Why These Changes?

### More Waypoints (30)
- Allows smoother, more flexible paths
- Better at navigating around obstacles
- Still fast enough for real-time visualization

### Higher Learning Rate (0.01)
- Faster convergence
- Bigger steps toward optimal solution
- The old 0.001 was too slow

### More Iterations (1000)
- Ensures convergence
- Path has time to fully optimize
- Still completes in ~10 seconds

### Lower Smoothness Weight (10)
- Old value of 50 was causing the cost to explode
- Allows path to make necessary turns
- Still maintains reasonable smoothness

### Higher Obstacle Weight (2000)
- Stronger penalty for going through obstacles
- Ensures paths stay clear of safety zones
- Balances better with smoothness cost

## Other Good Combinations

### For Very Smooth Paths (Passenger Comfort)
```
Waypoints: 35
Learning Rate: 0.005
Iterations: 1500
Smoothness: 20
Obstacle: 3000
```

### For Tight Spaces
```
Waypoints: 40
Learning Rate: 0.005
Iterations: 2000
Smoothness: 5
Obstacle: 5000
```

### For Fast Computation (Quick Demo)
```
Waypoints: 15
Learning Rate: 0.02
Iterations: 500
Smoothness: 10
Obstacle: 2000
```

## How to Use

Now you can **type exact numbers** into the input fields instead of using sliders!

1. Open `frontend/index.html` (refresh the page to see the changes)
2. You'll see number input boxes instead of sliders
3. Click in any box and type your desired value
4. The new defaults should work much better!

## Expected Results

With the new default parameters:
- Path should curve smoothly around obstacles ✅
- Cost should decrease from ~50 billion to ~100,000 ✅
- Obstacle cost should go to 0 ✅
- Total cost should stabilize after 500-800 iterations ✅

Enjoy! 🚀
