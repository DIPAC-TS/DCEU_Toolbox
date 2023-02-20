def getMCA(load, v=200., ph=1):
  import math
  if ph == 1:
    return load / v * 1.25
  else:
    return load / v / math.sqrt(3.) * 1.25
 
def getMOB(load, v=200., ph=1):
  import math
  if ph == 1:
    return load / v * 1.4
  else:
    return load / v / math.sqrt(3.) * 1.4