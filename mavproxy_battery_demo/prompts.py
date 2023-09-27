FIX_CODE_PREFIX =  """ \
SYSTEM MESSAGE:

You are an engineer working on a Formula DSL program. You are to read, write, explain, and repair Formula DSL programs.

END OF SYSTEM MESSAGE"""

EXPLAIN_QUERY_PROMPT = """ \
{explain_prompt}

This is the Formula DSL used to build a model.
```{code}```

This is the output of the Formula program using z3.
```{output}```
"""

SOLUTIONS_QUERY_PROMPT = """ \
{solutions_prompt}
"""

REPAIR_QUERY_PROMPT = """ \
{repair_prompt}

This is the Formula DSL used to build a model.
```{code}```

This is the output of the Formula program using z3.
```{output}```
"""

OUTPUT_RETURN = """ \
{explanation}

{solutions}
"""

REPAIR_OUTPUT_RETURN = """ \
{repair}
"""

FORMULA_CODE_LLM_DESC = """ \
This is a Formula debugging tool. 

To invoke this tool, make sure you call it in a JSON format in the following format:

{
    "prompt": "FORMULA REQUEST HERE",
	"code": "FORMULA CODE HERE",
    "output": "FORMULA INTERPRETER OUTPUT HERE"
}

Make sure you only call this function with a JSON format, otherwise it will not work.
"""

REPAIR_FORMULA_CODE_LLM_DESC = """ \
This is a Formula repair tool. 

To invoke this tool, make sure you call it in a JSON format in the following format:

{
    "prompt": "FORMULA REQUEST HERE",
	"code": "FORMULA CODE HERE",
    "output": "FORMULA INTERPRETER OUTPUT HERE"
}

Make sure you only call this function with a JSON format, otherwise it will not work.
"""