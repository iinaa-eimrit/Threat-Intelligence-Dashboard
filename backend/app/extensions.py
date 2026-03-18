from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

# ...existing code...

def configure_extensions(app):
    CORS(app)
    Limiter(key_func=get_remote_address, default_limits=["100 per hour"]).init_app(app)
