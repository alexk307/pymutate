import ast
import codegen
from types import MethodType


class Mutator(object):
    """
    Class to mutate Python code
    """

    def __init__(self, mutations):
        self.opposite_tokens = mutations
        self.transformers = []

    def generate_transformers(self):
        """
        Generates the transformers to mutate the code
        """
        for token in self.opposite_tokens:
            transformer = type('%sTransformer' % token.__name__, (ast.NodeTransformer,), {})
            opposite = self.opposite_tokens[token]

            def closure(opposite):
                def wrap(self, node):
                    self.generic_visit(node)
                    return opposite()
                return wrap
            func_name = 'visit_%s' % token.__name__
            closure.__name__ = func_name
            setattr(transformer, func_name, MethodType(closure(opposite), None, transformer))
            self.transformers.append(transformer)

    def apply_transformations(self, code):
        """
        Applies the created transformers to the given code segment
        :param code: Python code to transform
        :return: Transformed Python code with mutations applied
        """
        tree = ast.parse(code)
        for transformation in self.transformers:
            transformation().visit(tree)
        return codegen.to_source(tree)
