import os

# List of class names
class_names = ["ClassOne", "ClassTwo", "ClassThree"]

# Directory to save the Java class files
output_directory = "java_classes"

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Template for the Java class file content
class_template = """public class {class_name} {{
    public {class_name}() {{
        // Constructor
    }}

    public void exampleMethod() {{
        // Example method
        System.out.println("Hello from {class_name}");
    }}

    public static void main(String[] args) {{
        {class_name} instance = new {class_name}();
        instance.exampleMethod();
    }}
}}
"""

# Create a Java class file for each class name
for class_name in class_names:
    print(class_name)
    class_content = class_template.format(class_name=class_name)
    file_path = os.path.join(output_directory, f'{class_name}.java')
    with open(file_path, "w") as java_file:
        java_file.write(class_content)

print(f"Java class files created in the '{output_directory}' directory.")
