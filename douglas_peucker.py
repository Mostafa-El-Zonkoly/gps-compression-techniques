from rdp import rdp
from point import Point as Point
def compressTrajectory(trajectory,eps, keep= False): 
    trajectory_xy = list(map(lambda x: [x.longitude, x.latitude,x.timestamp], trajectory))
    if keep: 
        return trajectory_xy
    result = rdp(trajectory_xy, epsilon = eps)
    return result

# compressTrajectory([[1,1], [2,2], [3,3]], 0.2)