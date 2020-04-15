# -*- coding: utf-8 -*-
"""Helper for docker containers. Writes environment variables to properties file

This script is run when running the refget tornado server in a docker container.
It writes environment variables to a properties file, which is then loaded 
as the runtime properties object in the Tornado context. Passing environment
variables to the docker container modifies what cloud storage service the 
refget server points to.
"""

import os

def main():
    """Write refget-specific environment variables to properties file"""
    
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