def resolve_url(properties, seqid, path_type):

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
    return resolve_url(properties, seqid, "sequence")

def resolve_metadata_url(properties, seqid):
    return resolve_url(properties, seqid, "metadata")
