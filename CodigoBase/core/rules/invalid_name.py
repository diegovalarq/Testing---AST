from ..rule import *
from re import match
# Clases que permiten detectar el uso de un nombre invalido en clases, metodos y funciones

class InvalidNameVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()
        self.parent_node_type = None

    def visit_ClassDef(self, node: ClassDef):
        self.update_class_warnings(node)
        self.parent_node_type = ClassDef
        NodeVisitor.generic_visit(self, node)
        self.parent_node_type = None

    def visit_FunctionDef(self, node: FunctionDef):
        self.update_function_warnings(node)
        self.parent_node_type = FunctionDef
        NodeVisitor.generic_visit(self, node)
        self.parent_node_type = None

    def update_class_warnings(self, node: ClassDef):
        if not self.is_class_name_correct(node.name):
            self.addWarning('InvalidName', node.lineno, 'invalid class name ' + node.name)
    
    def update_function_warnings(self, node: FunctionDef):
        if not self.is_function_name_correct(node.name):
            warning_message = 'invalid function name '
            if self.parent_node_type is not None:
                warning_message = 'invalid method name '
            self.addWarning('InvalidName', node.lineno, warning_message + node.name)

    def is_class_name_correct(self, name):
        class_name_pattern = r'^[A-Z][a-zA-Z0-9]+$'
        return match(class_name_pattern, name)
    
    def is_function_name_correct(self, name):
        function_name_pattern = r'^[a-z_][a-z0-9_]*$'
        function_min_len = 2
        function_max_len = 30
        return match(function_name_pattern, name) and self.is_function_len_between(name, function_min_len, function_max_len)
    
    def is_function_len_between(self, name, min_len, max_len):
        return min_len <= len(name[1:]) <= max_len 
    
    
class InvalidNameRule(Rule):
    def analyze(self, ast):
        visitor = InvalidNameVisitor()
        #print(dump(ast))   #imprime el árbol AST
        visitor.visit(ast)
        return visitor.warningsList()
    
    @classmethod
    def name(cls):
        return 'invalid-name'