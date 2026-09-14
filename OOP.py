#class Robot:
   # def __init__(self, name, battery=100):
 #       self.name = name
#        self.battery = battery

#r = Robot("R2")
#print(r.battery)



class Robot:
    count = 0
    def __init__(self):
        Robot.count += 1

Robot(), Robot(), Robot()
print(Robot.count)





