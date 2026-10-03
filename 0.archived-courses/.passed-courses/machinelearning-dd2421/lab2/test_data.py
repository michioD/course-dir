import numpy
import matplotlib.pyplot as plt


classA = numpy.concatenate(
        (numpy.random.randn(100, 2) * 0.2 + [1.5, 0.5], 
         numpy.random.randn(100, 2) * 0.25 + [-1.5, 0.5]))


classB = numpy.random.randn(2000, 2) * 0.2 + [0.0, -0.5]


inputs = numpy.concatenate((classA, classB))


targets = numpy.concatenate(
        (numpy.ones(classA.shape[0]),
         -numpy.ones(classB.shape[0])))

N = inputs.shape[0] 

permute = list(range(N))

numpy.random.shuffle(permute)

inputs = inputs[permute, :]

targets = targets[permute]



# plt.plot([p[0] for p in classA], [p[1] for p in classA],'b.')
# plt.plot([p[0] for p in classB], [p[1] for p in classB],'r.')



# xgrid = numpy.linspace(-5,5)
# xgrid = numpy.linspace(-4,4)
# grid = numpy.array([[indicator(x,y) for x in xgrid] for y in ygrid])
# plt.contour(xgrid, ygrid, grid, (-1.0,0.0,1.0), colors = ('red', 'black', 'blue'),
# linewidths = (1,3,1))



# lt.show()
