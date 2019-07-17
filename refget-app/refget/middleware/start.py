def StartMidware(event, context):
    def decorator_function(func):
        def wrapper():
            partial_response = {
                "statusCode": None,
                "headers": {},
                "body": ""
            }
            return func(partial_response)
        return wrapper
    return decorator_function