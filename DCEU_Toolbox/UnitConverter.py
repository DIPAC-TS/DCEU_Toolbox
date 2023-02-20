def toLps(flow, mode="CFM"):
  if (mode == "CFM"):
    return flow * 1000. / 2118.88
  elif (mode == "CMM"):
    return flow * 1000. / 60.
  else: #m3s
    return flow * 1000. 
    
def toCFM(flow, mode="Lps"):
  if (mode == "Lps"):
    return flow * 2118.88 / 1000.
  elif (mode == "CMM"):
    return flow * 2118.88 / 60.
  else: #m3s
    return flow * 2118.88
  
def toM(length, mode="in"):
  if (mode == "in"):
    return length * 0.0254
  else: #ft
    return length * .3048
  
def toFt(length, mode="m"):
  if (mode == "m"):
    return length / .3048
  else: #in
    return length / 12.

def toIn(length, mode="m"):
  if (mode == "m"):
    return length / .3048
  else: #ft
    return length * 12.
  
def toKg(lb):
  return lb * 453.592 / 1000.
  
def toLb(kg):
  return kg * 1000. / 453.592
  
def toC(F):
  return (F - 32.) * 5. / 9.
  
def toF(C):
  return C * 9. / 5. + 32.
  
def toK(R):
  return 5. / 9. * R

def toR(K):
  return 9. / 5. * K
  
def toMps(FPM):
  return FPM * 5.08 / 1000.
  
def toFPM(Mps):
  return Mps * 1000. / 5.08
  
def toinWC(Pa):
  return Pa * 4.01865 / 1000.
    
def toPSI(Pa):
  return Pa * 1. / 6894.76
  
def toPa(value, mode="PSI"):
  if mode == "PSI":
    return value * 6894.76
  else: #inWC
    return value * 1000. / 4.01865
  
def toTR(value, mode="W"):
  if (mode == "W"):
    return value * 3412.142 / 1000. / 12000.
  elif(mode == "Bph"):
    return value / 12000.

def toBph(value, mode="W"):
  if (mode == "W"):
    return value * 3412.142 / 1000.
  elif (mode == "TR"):
    return value * 12000

def toW(value, mode="Bph"):
  if (mode == "Bph"):
    return value * 1000. / 3412.142
  elif (mode == "TR"):
    return value * 1000. / 3412.142 * 12000
  else: #HP
    return value * 745.699872
  
def toHP(value):
  return value / 745.699872  