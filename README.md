# pymutate
Mutation Testing Using The AST

```python
import ast
from mutator import Mutator

# Define tokens to mutate
mutations = {ast.Eq: ast.NotEq}
mut = Mutator(mutations)
mut.generate_transformers()

# Read code to mutate
with file('code.py', 'r') as f:
    code = f.read()

mutated_code = mut.apply_transformers()
```
