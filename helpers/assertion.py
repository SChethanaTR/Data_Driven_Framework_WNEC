def validate_dictionary_data(response, case_sensitive=False, **kwarg):
    if not case_sensitive:
        response.update({k: v.lower() for k, v in response.items() if isinstance(v, str)})
        kwarg.update({k: v.lower() for k, v in kwarg.items() if isinstance(v, str)})
    res = [item in response.items() for item in kwarg.items()]
    assert all(res)
