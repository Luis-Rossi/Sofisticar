import hashlib
import uuid

password = "teste"
salt = uuid.uuid4().hex
hashed_password = hashlib.sha512(password + salt).hexdigest()
