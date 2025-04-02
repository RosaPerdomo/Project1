class Worker:
    def __init__(self, name, salary, age):
        self.name=''
        self.salary = salary
        self.age = age
jefe = Worker('Manolito', 4500, 55)
Worker1 = Worker('Pepito', 1100, 26)
Worker2 = Worker('Paca', 2200, 27)
Worker3 = Worker('Manolita', 3000, 52)
class Company:
    def __init__(self):
        self.name =''
        self.boss = jefe
        self.employees= []
cp=Company()
cp.employees.extend([Worker1, Worker2, Worker3])
cp.name='Cocacola'
jefe.salary= jefe.salary*0.5
print(cp.__dict__)