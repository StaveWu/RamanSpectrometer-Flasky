class AClassWithClassProperty:
    val = 2

    def __init__(self):
        print('aClass constructed')
        self.val = 3


class SubClass1(AClassWithClassProperty):
    def __init__(self):
        super(SubClass1, self).__init__()
        print('sub class constructed')
        self.val = 4


if __name__ == '__main__':
    print(AClassWithClassProperty.val)
    print(SubClass1.val)

    print(AClassWithClassProperty().val)
    print(SubClass1().val)
