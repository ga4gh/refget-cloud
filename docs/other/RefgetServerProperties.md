# Refget Server Properties

The refget web service can be configured with modifiable properties to serve data from different cloud resources, and adjust the behaviour of the web server.

## How to Modify Server Properties 

### Natively

When running the server natively via commandline, properties are written to a `.properties` file, which is then passed as an argument to the program. Each line in the properties file contains a single property, in the format `{property_key}={property_value}`. The following example could be used as a valid properties file:

```
source.base_url=https://example-refget.com
source.sequence_path=/{seqid}
source.metadata_path=/meta/{seqid}
server.port=9999
```

The server will use default values for any properties not specified in the file.

### Docker Container / Serverless

When running the server either via docker container or serverless architecture, properties are passed via **environment variables**. 

## Properties

The following table shows all modifiable properties. It shows the required property name (whether specified via properties file or environment variable), and the default value.

| Properties File Key | Environment Variable | Default Value |
|---------------------|----------------------|---------------|
| source.base_url | SOURCE_BASE_URL | http://insdc-mirror.s3-website-us-west-2.amazonaws.com |
| source.sequence_path | SOURCE_SEQUENCE_PATH | /sequence/{seqid} |
| source.metadata_path | SOURCE_METADATA_PATH | /metadata/json/{seqid}.json |
| server.port | SERVER_PORT | 8888 |
| local.openapi_file | LOCAL_OPENAPI_FILE | None |

The following sections explain each modifiable property

### source.base_url / SOURCE_BASE_URL

The base url to a cloud-based resource that contains the sequence and metadata objects you'd like to serve via Refget. This could be the base url to an AWS S3 bucket, Google Cloud Storage, or any other scalable file/object storage accessible via http(s).

### source.sequence_path / SOURCE_SEQUENCE_PATH

The url path template to where reference sequences are stored in cloud storage. The template **MUST** include exactly '`{seqid}`' somewhere in the path to allow the refget service to resolve incoming requested sequence ids and request them from cloud storage.

The refget service will construct sequence request urls from the base url and sequence path template, formatting the path template's `{seqid}` with the `id` passed to it.

### source.metadata_path / SOURCE_METADATA_PATH

The url path template to where reference sequence metadata objects are stored in cloud storage. The template **MUST** include exactly '`{seqid}`' somewhere in the path to allow the refget service to resolve incoming requested sequence ids and request them from cloud storage.

The refget service will construct metadata request urls from the base url and metadata path template, formatting the path template's `{seqid}` with the `id` passed to it.

### server.port / SERVER_PORT

The port the web server runs on.

### local.openapi_file / LOCAL_OPENAPI_FILE

Enables `SwaggerUI` html pages for the server. 

By default, this property is set to `None`, and will therefore not set up any routes serving `SwaggerUI` documentation. If the path to an OpenAPI `.yaml` file is specified, this file will copied to the `public/html` directory and served. The server's `SwaggerUI` documentation will be available at `/index.html`
