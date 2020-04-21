# -*- coding: utf-8 -*-
"""Methods for resolving urls from system properties

The Properties object holds properties that reference a cloud storage service
containing reference sequences. These property keys should hold specific info:
    source.base_url -> base url to cloud storage service
    source.sequence_path -> url path to access sequences from cloud storage.
        The path should contain the parameter {seqid} for sequence identifier
    source.metadata_path -> url path to access sequence metadata from cloud
        storage. The path should contain the parameter {seqid} for sequence
        identifier

These methods resolve refget requests to cloud storage urls to access the
requested sequence or metadata from cloud storage
"""

def resolve_url(properties, seqid, path_type):
    """Resolves a refget request to a cloud storage object url

    Arguments:
        properties (Properties): runtime properties containing cloud storage
            base url, and url paths to sequences and metadata
        seqid (str): Requested sequence (checksum identifier)
        path_type (str): 'sequence' for sequence requests, 
            'metadata' for metadata requests
    
    Returns:
        (str): url pointing to requested object in cloud storage
    """

    path_props = {
        "sequence": "source.sequence_path",
        "metadata": "source.metadata_path"
    }

    base_url = properties.get("source.base_url")
    url_path = properties.get(path_props[path_type])
    template = base_url + url_path
    url = template.format(seqid=seqid)
    return url

def resolve_sequence_url(properties, seqid):
    """Resolves a refget sequence request to cloud storage object url

    Arguments:
        properties (Properties): runtime properties with cloud storage base url,
            url paths
        seqid (str): Requested sequence (checksum identifier)
    
    Returns:
        (str): url pointing to requested sequence in cloud storage
    """

    return resolve_url(properties, seqid, "sequence")

def resolve_metadata_url(properties, seqid):
    """Resolves a refget metadata request to cloud storage object url

    Arguments:
        properties (Properties): runtime properties with cloud storage base url,
            url paths
        seqid (str): Requested sequence (checksum identifier)
    
    Returns:
        (str): url pointing to requested sequence metadata in cloud storage
    """

    return resolve_url(properties, seqid, "metadata")
