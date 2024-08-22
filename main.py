import os

# Define the folder structure
structure = {
    "microserver-admin-panel": {
        "admin-service": {
            "src/main/java/com/example/adminservice": [],
            "resources": ["application.yml"],
            "Dockerfile": None
        },
        "app-service": {
            "src/main/java/com/example/appservice": [],
            "resources": ["application.yml"],
            "Dockerfile": None
        },
        "eureka-server": {
            "src/main/java/com/example/eurekaserver": [],
            "resources": ["application.yml"],
            "Dockerfile": None
        },
        "gateway-service": {
            "src/main/java/com/example/gatewayservice": [],
            "resources": ["application.yml"],
            "Dockerfile": None
        },
        "config-server": {
            "src/main/java/com/example/configserver": [],
            "resources": ["application.yml"],
            "Dockerfile": None
        }
    }
}

# Dockerfile contents
dockerfile_templates = {
    "admin-service": """# Use an official OpenJDK runtime as a parent image
FROM openjdk:17-jdk-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY target/admin-service-0.0.1-SNAPSHOT.jar /app/admin-service.jar

# Expose the port the service runs on
EXPOSE 8081

# Run the jar file
ENTRYPOINT ["java", "-jar", "admin-service.jar"]
""",
    "app-service": """# Use an official OpenJDK runtime as a parent image
FROM openjdk:17-jdk-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY target/app-service-0.0.1-SNAPSHOT.jar /app/app-service.jar

# Expose the port the service runs on
EXPOSE 8082

# Run the jar file
ENTRYPOINT ["java", "-jar", "app-service.jar"]
""",
    "eureka-server": """# Use an official OpenJDK runtime as a parent image
FROM openjdk:17-jdk-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY target/eureka-server-0.0.1-SNAPSHOT.jar /app/eureka-server.jar

# Expose the port the Eureka server runs on
EXPOSE 8761

# Run the jar file
ENTRYPOINT ["java", "-jar", "eureka-server.jar"]
""",
    "gateway-service": """# Use an official OpenJDK runtime as a parent image
FROM openjdk:17-jdk-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY target/gateway-service-0.0.1-SNAPSHOT.jar /app/gateway-service.jar

# Expose the port the gateway runs on
EXPOSE 8080

# Run the jar file
ENTRYPOINT ["java", "-jar", "gateway-service.jar"]
""",
    "config-server": """# Use an official OpenJDK runtime as a parent image
FROM openjdk:17-jdk-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY target/config-server-0.0.1-SNAPSHOT.jar /app/config-server.jar

# Expose the port the config server runs on
EXPOSE 8888

# Run the jar file
ENTRYPOINT ["java", "-jar", "config-server.jar"]
"""
}

# Sample application.yml content
application_yml_content = {
    "admin-service": "spring:\n  application:\n    name: admin-service\nserver:\n  port: 8081\n",
    "app-service": "spring:\n  application:\n    name: app-service\nserver:\n  port: 8082\n",
    "eureka-server": "spring:\n  application:\n    name: eureka-server\nserver:\n  port: 8761\n",
    "gateway-service": "spring:\n  application:\n    name: gateway-service\nserver:\n  port: 8080\n",
    "config-server": "spring:\n  application:\n    name: config-server\nserver:\n  port: 8888\n"
}


# Function to create directory structure and files
def create_structure(base_path, structure):
    for folder, contents in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        
        for subfolder, files in contents.items():
            if isinstance(files, dict):  # If it's a nested structure
                create_structure(folder_path, {subfolder: files})
            else:
                # Create files in the folder
                subfolder_path = os.path.join(folder_path, subfolder)
                if files is None:
                    # If files is None, create just the file (e.g., Dockerfile)
                    service_name = folder.split('-')[0] + '-' + folder.split('-')[1]
                    with open(subfolder_path, 'w') as f:
                        f.write(dockerfile_templates.get(service_name, ""))
                else:
                    # If files is a list, create those files
                    os.makedirs(subfolder_path, exist_ok=True)
                    for file in files:
                        file_path = os.path.join(subfolder_path, file)
                        with open(file_path, 'w') as f:
                            # Write content to application.yml based on service name
                            service_name = folder.split('-')[0] + '-' + folder.split('-')[1]
                            f.write(application_yml_content.get(service_name, ""))


# Create the folder and file structure
base_path = "."
create_structure(base_path, structure)
print("Folder structure and files created successfully.")
