from _ast import Attribute
from typing import Any
from ..rule import *

# Clases que permiten detectar si algun atributo no fue inicializado.
# A veces se usan algunos atributos que no estan inicializados y esto genera errores.

class UninitializedAttributeVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()
        self.parent_node_type = None
        self.visited_names = set()

    def visit_ClassDef(self, node: ClassDef):
        self.parent_node_type = ClassDef
        NodeVisitor.generic_visit(self, node)
        self.parent_node_type = None
    
    def visit_Assign(self, node: Assign):
        if self.parent_node_type == ClassDef:
            for target in node.targets:
                if isinstance(target, Name):
                    self.visited_names.add(target.id)
        NodeVisitor.generic_visit(self, node)
    
    def visit_Attribute(self, node: Attribute):
        if isinstance(node.value, Name) and node.value.id == 'self':
            if node.attr not in self.visited_names:
                self.addWarning("UninitializedAttribute", node.lineno, f"{node.attr} attribute was not initialized!")
        NodeVisitor.generic_visit(self, node)

class UninitializedAttributeRule(Rule):

    def analyze(self, ast):
        visitor = UninitializedAttributeVisitor()
        visitor.visit(ast)

    @classmethod
    def name(cls):
        return 'uninit-attr'