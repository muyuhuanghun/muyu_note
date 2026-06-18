"""测试辅助：共享 Sanic 测试客户端。"""
from sanic_testing.testing import SanicTestClient as TestClient

from app.server import app

# 所有测试类共享同一个客户端实例，避免 Windows 端口复用冲突
shared_client = TestClient(app, port=0)
