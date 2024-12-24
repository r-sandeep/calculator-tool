import json
import sys

def evaluate_expression(input_data, config_data):
    """
    Evaluates an expression found in input_data["query"], returning a JSON string.
    Optionally, config_data can be used to determine how the expression is evaluated.
    """
    try:
        # Extract the expression from the input
        expression = input_data.get("query", "")
        if not expression:
            return json.dumps({"error": "No expression provided."})

        # For safety, block builtins unless config explicitly allows them
        allow_builtins = config_data.get("allowBuiltins", False)
        builtins_dict = {"__builtins__": None} if not allow_builtins else {}

        print("Evaluating expression: {expression}")

        # Evaluate the expression securely (if allowBuiltins = false, we don't allow them)
        result = eval(expression, builtins_dict, {})
        return json.dumps({"result": result})

    except Exception as e:
        return json.dumps({"error": str(e)})

def main():
    """
    Expects two command-line arguments:
      1) input_json  (string)
      2) config_json (string)
    
    Example: 
      python src/evaluator.py '{"query":"2+3"}' '{"allowBuiltins":true}'
    """
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Not enough arguments. Expected input JSON and config JSON."}))
        sys.exit(1)

    input_json = sys.argv[1]
    config_json = sys.argv[2]

    try:
        input_data = json.loads(input_json)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid input JSON: {e}"}))
        sys.exit(1)

    try:
        config_data = json.loads(config_json)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid config JSON: {e}"}))
        sys.exit(1)

    # Evaluate and print final result in JSON
    print(evaluate_expression(input_data, config_data))

if __name__ == "__main__":
    main()
