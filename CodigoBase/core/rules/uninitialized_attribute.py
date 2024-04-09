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
    
    def visit_FunctionDef(self, node: FunctionDef):
        # En esta funcion, se guardan todos aquellos atributos que son inicializados en el constructor
        # de la clase __init__
        # https://www.programcreek.com/python/example/4638/ast.Assign
        if self.parent_node_type == ClassDef and node.name == '__init__':
            for statement in node.body:
                if isinstance(statement, Assign) and isinstance(statement.targets[0], Attribute):
                    self.visited_names.add(statement.targets[0].attr)
        NodeVisitor.generic_visit(self, node)

    # Claude fue usado para debugear la siguiente función
    def visit_Attribute(self, node: Attribute):
        # en este metodo, se recorren los atributos de la clase
        # y se verifica si alguno de ellos no fue inicializado
        # en el constructor __init__
        # si no se encuentran en __init__, se levanta un warning
        if isinstance(node.value, Name) and node.value.id == 'self':
            if node.attr not in self.visited_names:
                self.addWarning("UninitializedAttribute", node.lineno, f"{node.attr} attribute was not initialized!")
                print(f"{node.attr} attribute was not initialized!")
        NodeVisitor.generic_visit(self, node)

class UninitializedAttributeRule(Rule):

    def analyze(self, ast):
        # print(dump(ast))
        visitor = UninitializedAttributeVisitor()
        visitor.visit(ast)
        return visitor.warningsList()

    @classmethod
    def name(cls):
        return 'uninit-attr'