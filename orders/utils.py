import uuid

def generate_ref_code():
    code = str(uuid.uuid4()).replace("-", "")[:12]
    return code

def generate_pass_code():
    code = str(uuid.uuid4()).replace("-", "")[:12]
    return code
