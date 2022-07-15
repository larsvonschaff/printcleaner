import ast
import libcst as cst
import typer
from pathlib import Path
import os


app = typer.Typer()


class PrintTransformer(cst.CSTTransformer):
    def leave_SimpleStatementLine(self, node, updated_node):

        if isinstance(node, cst.SimpleStatementLine):
            for n in node.body:
                if isinstance(n, cst.Expr) and  isinstance(n.value, cst.Call) and isinstance(n.value.func, cst.Name) and n.value.func.value == 'print':

                    return cst.RemovalSentinel.REMOVE
    
        return node    


def remove_print_statements(file_path):
    file = open(file_path, 'r')
    code = file.read()
    tree = cst.parse_module(code)
    transformer = PrintTransformer()
    modified_tree = tree.visit(transformer)
    with open(file_path, 'w') as f:
        f.write(modified_tree.code)


def main(target: Path):
    if target.is_file():
        remove_print_statements(target)
    elif target.is_dir(): 
        for path, subdirs, files in os.walk(target):
            if 'venv' in subdirs:
                subdirs.remove('venv')
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(path, file)
                    remove_print_statements(full_path)

    elif not target.exists:
        typer.echo('invalid path')
        raise typer.Abort()





if __name__ == "__main__":
    typer.run(main)