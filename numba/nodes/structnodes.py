from numba.nodes import *

class StructAttribute(ExtTypeAttribute):

    _fields = ['value']

    def __init__(self, value, attr, ctx, struct_type, **kwargs):
        super(ExtTypeAttribute, self).__init__(**kwargs)
        self.value = value
        self.attr = attr
        self.ctx = ctx
        self.struct_type = struct_type

        self.attr_type = struct_type.fielddict[attr]
        self.field_idx = struct_type.fields.index((attr, self.attr_type))

        self.type = self.attr_type
        self.variable = Variable(self.type, promotable_type=False)


class StructVariable(Node):
    """
    Tells the type inferencer that the node is actually a valid struct that
    we can mutate. For instance

        func().a = 2

    is wrong if func() returns a struct by value. So we only allow references
    like struct.a = 2 and array[i].a = 2.
    """

    _fields = ['node']

    def __init__(self, node, **kwargs):
        super(StructVariable, self).__init__(**kwargs)
        self.node = node
        self.type = node.type

class ComplexNode(Node):
    _fields = ['real', 'imag']
    type = complex128
    variable = Variable(type)

