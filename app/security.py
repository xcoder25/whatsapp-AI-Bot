import hmac, hashlib, base64

def verify_x_hub_signature_256(app_secret: str, payload: bytes, signature_header: str | None) -> bool:
    if not app_secret or not signature_header:
        return True  # If not configured, skip verification.
    try:
        # header format: sha256=<hexdigest>
        algo, provided_sig = signature_header.split("=", 1)
        if algo != "sha256":
            return False
        mac = hmac.new(app_secret.encode(), msg=payload, digestmod=hashlib.sha256)
        expected = mac.hexdigest()
        # Constant-time compare
        return hmac.compare_digest(expected, provided_sig)
    except Exception:
        return False
