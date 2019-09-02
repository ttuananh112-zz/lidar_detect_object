import numpy as np

a = [1,2,3,4,5]
a_np = np.array(a)
a_np[a_np>2]=0
print(a_np)