from ..rule import *

# Clases que permiten detectar si un argumento no fue usado

class UnusedArgumentVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()
        self.parent_node_type = None
        self.child_nodes_ids = []

    def visit_FunctionDef(self, node: FunctionDef):
        self.parent_node_type = FunctionDef
        NodeVisitor.generic_visit(self, node)
        self.update_unused_argument_warning(node)
        self.parent_node_type = None
        self.child_nodes_ids = []

    def visit_Name(self, node: Name):
        if self.parent_node_type == FunctionDef:
            self.child_nodes_ids.append(node.id)

    def update_unused_argument_warning(self, node: FunctionDef):
        function_arguments = self.get_function_arguments(node)
        for function_argument in function_arguments:
            if function_argument not in self.child_nodes_ids:
                 self.addWarning('UnusedArgument', node.lineno, f'{function_argument} argument has not been used!')
    
    def get_function_arguments(self, node: FunctionDef):
        function_arguments = []
        for arg in node.args.args:
            function_arguments.append(arg.arg)
        return function_arguments


class UnusedArgumentRule(Rule):

    def analyze(self, ast):
        visitor = UnusedArgumentVisitor()
        #print(dump(ast))   #imprime el árbol AST
        visitor.visit(ast)
        return visitor.warningsList()


    @classmethod
    def name(cls):
        return 'unused-arg'