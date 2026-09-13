class Robot:
    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery

r2 = Robot("R2")
c3 = Robot("C3, battery=50")
print(r2.name, r2.battery)
print(c3.name, c3.battery)