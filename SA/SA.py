from Req import Map
from gen_new_path import simple_swap
def SA(map, t0 = 100, alpha, int_its):
    number_of_points = len(map1.points)
    coordinates = []
    for i in range(number_of_points):
        coordinates.append(np.array([map1.points[i][0], map1.points[i][1]]))
    def getdistmat(coordinates):
        num = len(coordinates)
        distmat = np.zeros((num,num))
        for i in range(num):
            for j in range(i,num):
                distmat[i][j] = distmat[j][i]=np.linalg.norm(coordinates[i]-coordinates[j])
        return distmat

    

    num = number_of_points
    distmat = getdistmat(coordinates) """get the distance matrix"""

    solutionnew = np.arange(num)

    solutioncurrent = solutionnew.copy()
    valuecurrent = 99000 

    solutionbest = solutionnew.copy()
    valuebest = 99000

    t2 = (10**(-5), t0)

    t = t2[1]
    ext_its = 0
    result = [] """here its for the optimal solution"""
    while t > t2[0] and ext_its < (np.log(t2[0] / t0) / np.log(alpha)):
        for n in range(int_its):
            if np.random.rand() > 0.5:
                    simple_swap(solutionnew)

            valuenew = 0
            for i in range(num-1):"""calculate new value"""
                valuenew += distmat[solutionnew[i]][solutionnew[i+1]]
            valuenew += distmat[solutionnew[0]][solutionnew[51]]
            if valuenew<valuecurrent: """then accept this value"""
            
                """update current value and current solution"""
                valuecurrent = valuenew
                solutioncurrent = solutionnew.copy()
    
                if valuenew < valuebest:
                    valuebest = valuenew
                    solutionbest = solutionnew.copy()
            else:"""accept this value with some prob"""
                if np.random.rand() < np.exp(-(valuenew-valuecurrent)/t):
                    valuecurrent = valuenew
                    solutioncurrent = solutionnew.copy()
                else:
                    solutionnew = solutioncurrent.copy()
        t = alpha*t
        ext_its += 1
        result.append(valuebest)
