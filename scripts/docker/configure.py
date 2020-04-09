import os

def main():
    
    content = []
    properties_file = "./config/application.properties"
    properties = [
        "source.base_url",
        "source.sequence_path",
        "source.metadata_path",
        "server.port"
    ]
    for prop in properties:
        envvar_name = prop.replace(".", "_").upper()
        envvar_value = os.getenv(envvar_name)
        if envvar_value:
            content.append(prop + "=" + envvar_value)

    open(properties_file, "w").write("\n".join(content) + "\n")

if __name__ == "__main__":
    main()