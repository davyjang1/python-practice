"""
A class has its own iterator which only return even number
"""
class iterable_class:
  def __init__(self):
    self.list1 = []
 
  def __iter__(self):
    return my_range_iterator(self.list1)

 
class my_range_iterator:
  def __init__(self, list1):
    self.list1 = list1
    self.iterator = iter(self.list1)
 
  def __iter__(self):
    return self

  def next(self):
      try:
        i = next(self.iterator)
        while (0 != i % 2):
            i = next(self.iterator)
        print ('iterator get number:' + str(i))
        return i
      except:
        raise StopIteration()


temp = iterable_class()
temp.list1.append(1)
temp.list1.append(2)
temp.list1.append(3)
for item in temp:
  print (item)
