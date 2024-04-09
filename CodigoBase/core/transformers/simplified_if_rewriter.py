from _ast import FunctionDef, If, IfExp
from ast import *
from typing import Any
from core.rewriter import RewriterCommand


# Clases que permiten transformar if ternarios que puedan ser simplificados usando la condicion o su negacion.

class SimplifiedIfTransformer(NodeTransformer):


    def visit_IfExp(self, node: IfExp):
        statements = node

        # ifexp(body, test, orelse)
        # return true if x > y else false
        # return fasle if z else true
        # z = node.test -> UnaryOp

        # true = node.body
        # x > y = node.test -> Compare(>)
        # false = node.orelse

    # https://docs.python.org/3/library/ast.html#abstract-grammar
    # unaryop = Invert | Not | UAdd | USub

    # cmpop = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn

        if isinstance(node.test, Compare) or isinstance(node.test, UnaryOp):
            if isinstance(node.body, Constant):
                if node.body.value == True:
                    return node.test
                elif node.body.value == False:
                    return UnaryOp(op=Not(), operand=node.test)
    
        return statements


class SimplifiedIfCommand(RewriterCommand):

    def apply(self, ast):
        #print(dump(parse(ast.body[0])))
        new_tree = fix_missing_locations(SimplifiedIfTransformer().visit(ast))
        return new_tree

