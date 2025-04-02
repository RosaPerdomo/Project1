class Perro:
	def __init__(self, nombre, color, edad):
		self.nombre=nombre
		self.color=color
		self.edad=edad
perro1 = Perro("Manolo", "azul", 8)
print (perro1.__dict__)