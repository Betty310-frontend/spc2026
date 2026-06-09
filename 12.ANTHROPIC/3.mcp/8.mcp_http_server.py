from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-http-server") 

@mcp.tool()
def hello(name: str) -> str:
    """
    주어진 이름으로 인사하는 툴

    매개변수:
        - name(str): 인사할 대상의 이름

    반환값:
        - str: "Hello, {name}!" 형식의 인사말
    """
    return f"Hello, {name}!"

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    두 정수 a와 b를 더하는 툴
    매개변수:
        - a(int): 첫 번째 정수
        - b(int): 두 번째 정수

    반환값:
        - int: a와 b의 합
    """
    return a + b

@mcp.tool()
def now() -> str:
    """
    현재 시간을 한국어로 포맷하여 반환하는 도구
    """
    from datetime import datetime
    return datetime.now().strftime("지금 시간은 %Y-%m-%d %H:%M:%S 입니다.")

if __name__ == "__main__":
    mcp.run(transport="streamable-http") # <- 이 한 줄로 stdio를 http 서버로 전환