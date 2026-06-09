import asyncio, platform, socket, sys, logging

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("simple-net-diag-server")

logger = logging.getLogger("simple-net-diag-server")

@mcp.tool()
async def fetch_page(host:str, port: int=80, path:str="/", max_bytes: int=100_000) -> str:
    """
    간단한 페이지 GET(HTTP)를 통해서 가져온 결과를 반환합니다.
    - path는 기본 '/'이며 원하는 경로를 추가할 수 있습니다.
    - max_bytes 까지만 가져오며, 기본값은 100kb입니다.
    """
    from urllib.parse import quote
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError

    # Normalize/validate inputs
    if not isinstance(host, str) or not host:
        raise ValueError("host must be a non-empty string")
    if not isinstance(port, int) or port <= 0:
        raise ValueError("port must be a positive integer")
    if not isinstance(path, str):
        raise ValueError("path must be a string")
    if not isinstance(max_bytes, int) or max_bytes <= 0:
        raise ValueError("max_bytes must be a positive integer")
    
    # Ensure path starts with '/'
    if not path.startswith("/"):
        path = "/" + path

    # Quote path but keep reserved URL characters commonly used in paths/queries
    # so that users can pass e.g. "/search?q=foo&bar=baz" as path.
    safe_chars = "/:?&=#%"

    # Bracket IPv6 literals if needed
    host_for_url = host
    if ":" in host and not host.startswith("["):
        host_for_url = f"[{host}]"
    
    url = f"http://{host_for_url}:{port}{quote(path, safe=safe_chars)}"

    # Minimal headers; do not request compressed encodings to avoid manual decompression
    req = Request(url, headers={"User-Agent": "simple-net-mcp/1.0"})

    def _fetch_sync() -> str:
        try:
            with urlopen(req, timeout=10) as resp:
                # Read up to max_bytes
                remaining = max_bytes
                chunks: list[bytes] = []
                # Read in 64 KiB chunks or smaller
                while remaining > 0:
                    chunk = resp.read(min(65536, remaining))
                    if not chunk:
                        break
                    chunks.append(chunk)
                    remaining -= len(chunk)
                data = b"".join(chunks)

                # Detect charset from headers if provided
                # HTTPMessage.get_content_charset() returns None if absent
                charset = None
                try:
                    charset = resp.headers.get_content_charset()  # type: ignore[attr-defined]
                except Exception:
                    charset = None

                # If the content type is textual but no charset, default to utf-8
                try:
                    ctype = resp.headers.get_content_type()  # type: ignore[attr-defined]
                except Exception:
                    ctype = None

                if not charset and ctype:
                    if ctype.startswith("text/") or ctype in ("application/json", "application/javascript"):
                        charset = "utf-8"

                # Fallback to utf-8 with replacement to always return a string
                if not charset:
                    charset = "utf-8"

                try:
                    return data.decode(charset, errors="replace")
                except LookupError:
                    # Unknown charset name; fallback to utf-8
                    return data.decode("utf-8", errors="replace")

        except HTTPError as e:
            # Try to extract a small portion of the error body for context
            err_body = ""
            try:
                err_raw = e.read(max_bytes)
                err_body = err_raw.decode("utf-8", errors="replace")
            except Exception:
                pass
            raise RuntimeError(f"HTTPError {e.code} {e.reason} while fetching {url}. {err_body}") from e
        except URLError as e:
            raise RuntimeError(f"URLError while fetching {url}: {getattr(e, 'reason', e)}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error while fetching {url}: {e}") from e

    # Run blocking I/O in a worker thread to avoid blocking the event loop
    return await asyncio.to_thread(_fetch_sync)


@mcp.tool()
async def ping_host(host:str, count:int=3, timeout_sec:int=3) -> str:
    """
    지정한 호스트로 Ping을 보내고 결과를 반환합니다.
     - count: 1~5까지
     - timeout_sec: 1~5초 (패킷 당 타임아웃)
    """
    host = (host or "").strip()
    if not host:
        raise ValueError("호스트를 입력해주세요.")
    
    if platform.system().lower() == "windows":
        cmd = ['ping', '-n', str(count), '-w', str(timeout_sec * 1000), host]
    else:
        cmd = ['ping', '-c', str(count), '-W', str(timeout_sec), host]

    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    output, error = await proc.communicate()

    if isinstance(output, bytes):
        text = output.decode('utf-8', errors='ignore')
        if not text:
            text = error.decode("utf-8", errors='ignore')

    logger.info(f"[내 로그] ping 결과: {text}")

    return text
    
if __name__ == "__main__":
    mcp.run(transport="stdio")