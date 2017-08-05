##
# File:  TableContainer.py
# Date:  16-Nov-2012  jdw
#
# Example of table container created by subclassing UserList.
#
# Update - -
#   15-Dec-2013 jdw add support slices and other functions
#
##


from __future__ import absolute_import
from __future__ import print_function
import sys
from six.moves import UserList
from six.moves import range
from six.moves import zip


class TableContainer(UserList):

    def __init__(self, name, attributeNameList=None, rowList=None):
        self._name = name
        self._attributeNameList = attributeNameList if attributeNameList is not None else []
        self.data = rowList if rowList is not None else []
        self._itemNameList = []
        self.__mappingType = "DATA"
        #
        self.__super = super(TableContainer, self)
        self.__super.__init__(self.data)

    def __updateItemLabels(self):
        self._itemNameList = []
        for aL in self._attributeNameList:
            self._itemNameList.append("_" + str(self._name) + "." + aL)

    def __alignLabels(self, row):
        if len(row) > len(self._attributeNameList):
            for i in range(len(self._attributeNameList), len(row) - 1):
                self._attributeNameList.insert(i, "unlabeled_" + str(i))
            if self.__mappingType == "ITEM":
                self.__updateItemLabels()

    def setMapping(self, mType):
        if mType in ['DATA', 'ATTRIBUTE', 'ITEM']:
            self.__mappingType = mType
            return True
        else:
            return False

    def __str__(self):
        ans = '%r' % (list(self),)
        return ans

    def __repr__(self):
        return self.__class__.__name__ + '(' + str(self) + ')'

    def dump(self):
        print(self.data)

    def __iter__(self):
        for d in self.data:
            yield self.__applyMapping(d)

    def __getitem__(self, idx):
        return self.__applyMapping(self.data[idx])

    def __setitem__(self, idx, value):
        dL = self.__extractMapping(value)
        self.data[idx] = dL

    def __applyMapping(self, d):
        if self.__mappingType == "DATA":
            return d
        elif self.__mappingType == "ATTRIBUTE":
            self.__alignLabels(d)
            return dict(list(zip(self._attributeNameList, d)))
        elif self.__mappingType == "ITEM":
            self.__alignLabels(d)
            self.__updateItemLabels()
            return dict(list(zip(self._itemNameList, d)))

    def __extractMapping(self, d):
        try:
            if self.__mappingType == "DATA":
                return d
            elif self.__mappingType == "ATTRIBUTE":
                rL = []
                for k, v in d.items():
                    rL.insert(self._attributeNameList.index(k), v)
                return rL
            elif self.__mappingType == "ITEM":
                rL = []
                for k, v in d.items():
                    rL.insert(self._itemNameList.index(k), v)
                return rL
        except:
            raise IndexError

    def __returnWith(self, rowList=None):
        return self.__class__(name=self._name, attributeNameList=self._attributeNameList, rowList=rowList)

    def __getslice__(self, i, j):
        i = max(i, 0)
        j = max(j, 0)
        return self.__returnWith(self.data[i:j])

    def __setslice__(self, i, j, other):
        i = max(i, 0)
        j = max(j, 0)
        if isinstance(other, self.__class__):
            self.data[i:j] = other.data
        elif isinstance(other, type(self.data)):
            self.data[i:j] = other
        else:
            self.data[i:j] = list(other)

    def __delslice__(self, i, j):
        i = max(i, 0)
        j = max(j, 0)
        del self.data[i:j]

    def __delitem__(self, idx):
        del self.data[idx]

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__returnWith(self.data + other.data)
        elif isinstance(other, type(self.data)):
            return self.__returnWith(self.data + other)
        else:
            return self.__returnWith(self.data + list(other))

    def __iadd__(self, other):
        if isinstance(other, self.__class__):
            self.data += other.data
        elif isinstance(other, type(self.data)):
            self.data += other
        else:
            self.data += list(other)
        return self

    def __mul__(self, n):
        return self.__returnWith(self.data * n)

    def __imul__(self, n):
        self.data *= n
        return self

    def __contains__(self, item):
        return item in self.data

    def append(self, item):
        self.data.append(item)

    def insert(self, i, item):
        self.data.insert(i, item)

    def pop(self, i=-1):
        return self.data.pop(i)

    def remove(self, item):
        self.data.remove(item)

    def count(self, item):
        return self.data.count(item)

    def index(self, item, *args):
        return self.data.index(item, *args)

    def reverse(self):
        self.data.reverse()

    def sort(self, *args, **kwds):
        self.data.sort(*args, **kwds)

    def extend(self, other):
        if isinstance(other, self.__class__):
            self.data.extend(other.data)
        else:
            self.data.extend(other)


if __name__ == '__main__':

    sys.stdout.write("\n\n --------------------------------------------------------------\n")
    tc = TableContainer('test', attributeNameList=['a', 'b', 'c', 'd'])

    tc.append([1, 2, 3, 0])
    tc.append([2, 2, 3, 4])
    tc.append([3, 2, 3, 4])
    tc.append([4, 2, 3, 4, 5, 6, 7])
    tc.append([5, 2, 3, 10])

    sys.stdout.write("First %r\n" % tc[0])
    sys.stdout.write("Last  %r\n" % tc[-1])

    sys.stdout.write("Length %d\n" % len(tc))
    sys.stdout.write("Length slice %d\n" % len(tc[1:]))

    del tc[0]
    del tc[1]
    sys.stdout.write("Length %d\n" % len(tc))
    sys.stdout.write("Length slice %d\n" % len(tc[1:]))

    sys.stdout.write("First after del %r\n" % tc[0])
    sys.stdout.write("Last  after del %r\n" % tc[-1])

    sys.stdout.write("Slice type [1:]  %r\n" % tc[1:])

    tc.insert(0, [4, 3, 2, 101])
    tc.insert(0, [4, 3, 2, 102])
    tc.insert(0, [4, 3, 2, 103])

    sys.stdout.write("contains valid   --   %r\n" % ([4, 3, 2, 103] in tc))
    sys.stdout.write("contains invalid --   %r\n" % ([4, 3, 2, 10000] in tc))

    sys.stdout.write("Full %r\n" % tc)

    sys.stdout.write("slice %r\n" % tc[2:4])

    sys.stdout.write("last  %r\n" % tc[-1])

    sys.stdout.write("Current full %r\n" % tc)

    sys.stdout.write("Add test  %r\n" % (tc + tc))

    tc += [(10, 10, 10, 10, 10)]
    sys.stdout.write("iAdd test  %r\n" % tc)

    tL = [(5, 4, 3, 2, 1), (5, 4, 3, 2, 1)]
    tc.extend(tL)
    sys.stdout.write("Extend test  %r\n" % tc)

    sys.stdout.write("Rows as data\n")
    tc.setMapping('DATA')
    for r in tc:
        print(r)

    sys.stdout.write("Rows as attributes\n")
    tc.setMapping('ATTRIBUTE')
    for r in tc:
        print(r)

    sys.stdout.write("Rows as items\n")
    tc.setMapping('ITEM')
    for r in tc:
        print(r)
    #

    tc.setMapping('DATA')
    print(tc[3])
    tmp = tc[3]
    tc[3] = []
    print(tc[3])
    tc[3] = tmp
    print(tc[3])

    tc.setMapping('ATTRIBUTE')
    print(tc[3])
    tmp = tc[3]
    dt = {}
    for k, v in tmp.items():
        dt[k] = 10000
    print(dt)
    tc[3] = dt
    print(tc[3])
    tc[3] = tmp

    tc.setMapping('ITEM')
    print(tc[3])
    tmp = tc[3]
    dt = {}
    for k, v in tmp.items():
        dt[k] = 10000
    print(dt)
    tc[3] = dt
    print(tc[3])

    tc.dump()
