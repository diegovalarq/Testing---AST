from _ast import FunctionDef, If, IfExp
from ast import *
from typing import Any
from core.rewriter import RewriterCommand


# Clases que permiten transformar if ternarios que puedan ser simplificados usando la condicion o su negacion.

class SimplifiedIfTransformer(NodeTransformer):

    def __init__(self):
        super().__init__()
        self.parent_node_type = None



    def visit_IfExp(self, node: IfExp):

        if isinstance(node.test, Compare):
            return self.simplify_compare(node) 
        elif isinstance(node.test, BoolOp):
            return self.simplify_boolop(node)
        elif isinstance(node.test, UnaryOp) and isinstance(node.test.op, Not):
            return self.simplify_unarynot(node)
        else:
            return self.generic_visit(node)
        
    def simplify_compare(self, node: IfExp):
        if isinstance(node.test.ops[0], (Eq, NotEq, Lt, LtE, Gt, GtE)):
            return node.body
        else:
            return self.generic_visit(node)
    
    def simplify_boolop(self, node: IfExp):
        if isinstance(node.test.op, (And, Or)):
            return node.body
        else:
            return self.generic_visit(node)
        
    def simplify_unarynot(self, node: IfExp):
        return node.orelse



class SimplifiedIfCommand(RewriterCommand):

    def apply(self, ast):
        # print(dump(ast))   #imprime el árbol AST
        new_tree = fix_missing_locations(SimplifiedIfTransformer().visit(ast))
        return new_tree
        # transformed = SimplifiedIfTransformer()
        # return transformed

