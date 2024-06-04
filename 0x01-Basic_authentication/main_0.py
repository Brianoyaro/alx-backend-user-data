#!/usr/bin/env python3
""" Main 0
"""
from api.v1.auth.auth import Auth

a = Auth()

print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(a.authorization_header())
print(a.current_user())
ex = ["/api/v1/stat*"]
print(a.require_auth('/api/v1/users', ex))
print(a.require_auth('/api/v1/status', ex))
print(a.require_auth('/api/v1/stats', ex))
