def finalize_response(response):
    final_response = {}
    final_response["statusCode"] = response["statusCode"]
    final_response["headers"] = response["headers"]
    final_response["body"] = response["body"]
    return final_response