from _ast import If
from ast import *
from typing import Any
from core.rewriter import RewriterCommand


# Clases que permiten transformar if ternarios que puedan ser simplificados usando la condicion o su negacion.

class SimplifiedIfTransformer(NodeTransformer):

    # def __init__(self):
    #     super().__init__()

    def visit_If(self, node):
        NodeTransformer.generic_visit(self, node)
        if isinstance(node.test, Compare) and len(node.test.ops) == 1 and len(node.test.comparators) == 1:
            operand = node.test.ops[0]
            left = node.test.left
            right = node.test.comparators[0]

            if isinstance(operand, (Eq, NotEq, Lt, LtE, Gt, GtE)):
                if isinstance(operand, (Eq, NotEq)):
                    return Compare(left, [operand], [right])
                elif isinstance(operand, Lt):
                    return Compare(left, [GtE()], [right])
                elif isinstance(operand, LtE):
                    return Compare(left, [Gt()], [right])
                elif isinstance(operand, Gt):
                    return Compare(left, [LtE()], [right])
                elif isinstance(operand, GtE):
                    return Compare(left, [Lt()], [right])
            elif isinstance(operand, IsNot):
                return UnaryOp(Not(), node.test.left)
        
        return self.generic_visit(node)


    # def visit_If(self, node):
    #     NodeTransformer.generic_visit(self, node)
    #     statements = node
    #     if isinstance(node.test, UnaryOp):
    #         if isinstance(node.test.op, Not):
    #             return If(test=node.test.operand, body=node.orelse, orelse=node.body)
    #     return statements
        

class SimplifiedIfCommand(RewriterCommand):

    def apply(self, ast):
        # print(dump(ast))   #imprime el árbol AST
        new_tree = fix_missing_locations(SimplifiedIfTransformer().visit(ast))
        return new_tree
        # transformed = SimplifiedIfTransformer()
        # return transformed

