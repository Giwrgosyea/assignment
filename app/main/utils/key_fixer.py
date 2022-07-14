def key_fix(result: dict):
    try:
        # cant store result with $ as part of key therefore replace $ with .
        return {k.replace("$", "."): v for k, v in result.items()}
    except Exception as ex:
        raise ex


def original_key_fix(result: dict):
    # cant store result with $ as part of key therefore replace $ with . and return it
    # in original shape
    try:
        return {k.replace(".", "$"): v for k, v in result.items()}
    except Exception as ex:
        raise ex
