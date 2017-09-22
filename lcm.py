def lcm(a, b):
   if a > b:
       value = a
   else:
       value = b
   while(True):
       if((value % a == 0) and (value % b == 0)):
           lcm = value
           break
       value += 1
   return lcm
