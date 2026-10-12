import hashlib
import os

from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.server.transport_security import TransportSecuritySettings

EMAIL = "24f2005619@ds.study.iitm.ac.in"

mcp = MCPServer("Challenge Server")


@mcp.tool()
def solve_challenge(ctx: Context) -> str:
    """Solve the current exam challenge using its HTTP request header."""

    headers = ctx.headers or {}
    challenge = headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    normalized_email = EMAIL.strip().lower()

    message = f"{challenge}:{normalized_email}"
    digest = hashlib.sha256(message.encode("utf-8")).hexdigest()

    return digest[:16]


hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if hostname:
    security = TransportSecuritySettings(
        allowed_hosts=[hostname, f"{hostname}:*"]
    )
else:
    security = TransportSecuritySettings(
        allowed_hosts=[
            "localhost",
            "localhost:*",
            "127.0.0.1",
            "127.0.0.1:*",
        ]
    )

app = mcp.streamable_http_app(
    transport_security=security
)