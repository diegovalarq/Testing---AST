from ast import *
from core.rewriter import RewriterCommand

# Clases que permiten transformar codigo que contiene x = x <operador_aritmetico_binario> z a x <operador_aritmetico_binario>= z.

class OperatorEqualsTransformer(NodeTransformer):

    def __init__(self):
        super().__init__()

    def visit_Assign(self, node: Assign):
        statements = node
        if len(node.targets) == 1:
            assign_target = node.targets[0]
            aug_assign_value_node = None
            if node.value.left.id == assign_target.id:
               aug_assign_value_node = node.value.right
            elif node.value.right.id == assign_target.id:
                aug_assign_value_node = node.value.left
            
        if aug_assign_value_node != None:
            aug_assign_target_node = assign_target
            aug_assign_operation_node = node.value.op
            return AugAssign(
                    target=aug_assign_target_node,
                    op=aug_assign_operation_node,
                    value=aug_assign_value_node
                    )
        
        return statements


class OperatorEqualsCommand(RewriterCommand):

    def apply(self, ast):
        #print(dump(ast))
        new_tree = fix_missing_locations(OperatorEqualsTransformer().visit(ast))
        return new_tree