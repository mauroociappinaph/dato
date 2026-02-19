import sys
import re

def normalize_name(name):
    # Convert to lowercase
    name = name.lower()
    # Replace spaces and underscores with hyphens
    name = re.sub(r'[\s_]+', '-', name)
    # Remove any non-alphanumeric characters (except hyphens)
    name = re.sub(r'[^a-z0-9-]', '', name)
    # Remove leading/trailing hyphens
    name = name.strip('-')
    return name

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_name = " ".join(sys.argv[1:])
        print(normalize_name(input_name))
    else:
        print("Error: No name provided.")
        sys.exit(1)
