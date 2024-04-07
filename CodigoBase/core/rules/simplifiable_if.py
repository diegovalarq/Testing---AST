from _ast import Constant
from typing import Any
from ..rule import *

# Clases que permiten detectar el uso de if statements o if ternarios que 
# se pueden simplificar por la condición o la condición negada.

class SimplifiableIfVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()

    def visit_IfExp(self, node: IfExp):
        self.update_bool_return_inside_ternary_If_warnings(node)
        NodeVisitor.generic_visit(self, node)

    def visit_If(self, node: If):
        self.update_bool_assign_inside_If_warnings(node)
        self.update_bool_return_inside_If_warning(node)
        NodeVisitor.generic_visit(self, node)

    def update_bool_return_inside_If_warning(self, node: If):
        for object in node.body:
            if isinstance(object, Return):
                if isinstance(object.value, Constant):
                    if type(object.value.value) == bool:
                        warning_message = 'if statement can be replaced with a bool(test)'
                        self.addWarning('SimplifiableIf', node.lineno, warning_message)

    def update_bool_assign_inside_If_warnings(self, node: Assign):
        body_assingment_value = []
        orelse_assingment_value = []

        for object in node.body:
            if isinstance(object, Assign):
                if isinstance(object.value, Constant):
                    if type(object.value.value) == bool:
                        for target in object.targets:
                            body_assingment_value.append(target.id)
        
        for object in node.orelse:
            if isinstance(object, Assign):
                if isinstance(object.value, Constant):
                    if type(object.value.value) == bool:
                        for target in object.targets:
                            orelse_assingment_value.append(target.id)
        
        any_common_value = any(target_id in body_assingment_value for target_id in orelse_assingment_value)
        if any_common_value:
            warning_message = 'if statement can be replaced with a bool(test)'
            self.addWarning('SimplifiableIf', node.lineno, warning_message)

    
    def update_bool_return_inside_ternary_If_warnings(self, node: IfExp):
        if type(node.body.value) == bool and type(node.orelse.value) == bool:
            warning_message = 'if statement can be replaced with a bool(test)'
            self.addWarning('SimplifiableIf', node.lineno, warning_message)


class SimplifiableIfRule(Rule):
    def analyze(self, ast):
        visitor = SimplifiableIfVisitor()
        #print(dump(ast))   #imprime el árbol AST
        visitor.visit(ast)
        return visitor.warningsList()
    
    @classmethod
    def name(cls):
        return 'simpl-if'
