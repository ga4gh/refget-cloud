# Getting Started - Native Setup

## Installation

As a prerequesite, the refget-cloud application requires Python 3.6 or higher.

The refget web server can be installed natively on your OS. Execute the following commands to clone the repository and build the application:
```
https://github.com/ga4gh/refget-cloud.git
cd refget-cloud
python setup.py
```

This will build the commandline utility `refget-server`

## Usage

To run the server, execute the following command:
```
refget-server
```

Running the service like this is not necessarily very useful, as the server is configured with all default parameters. This means it will run on the default port (8888), and only serve reference sequences from the AWS INSDC public dataset.

To configure the service with custom properties (e.g. port, data source, etc.), you may pass the path to a properties file on the commandline:

```
refget-server --properties-file /path/to/properties/file
```

Click [here](../other/RefgetServerProperties.md) to view the format and allowed properties of a properties file
