# coding: utf-8
from pycparser import c_parser, c_ast


def parse_source(preprocessed_source):
    parser = c_parser.CParser()
    ast = parser.parse(preprocessed_source, filename="<none>")
    return ast

def ast_rec_iterator(node, tag="", level=0):
    yield tag, node
    if hasattr(node, "children"):
        for tag, child in node.children():
            yield from ast_rec_iterator(child, tag, level + 1)


def find_function_definitions(ast):

    return dict(
        (node.decl.name, node)
        for _, node in ast_rec_iterator(ast)
        if isinstance(node, c_ast.FuncDef)
    )


def find_function_call_names(ast):

    fcalls = set(
        node.name.name
        for _, node in ast_rec_iterator(ast)
        if isinstance(node, c_ast.FuncCall)
    )

    ids =  set(
        node.name
        for _, node in ast_rec_iterator(ast)
        if isinstance(node, c_ast.ID)
    )

    return set.union(ids,fcalls)
