from fastapi import Request, Response
from time import time
from core.config import logger

async def log_requests(request: Request, call_next):
    """リクエストとレスポンスのログを記録"""
    start_time = time()

    # オリジナルのreceive関数を保存
    original_receive = request.receive

    # リクエストボディを収集
    body = b""
    async def receive():
        nonlocal body
        message = await original_receive()
        if message["type"] == "http.request":
            body += message.get("body", b"")
            if message.get("more_body", False):
                while message.get("more_body", False):
                    message = await original_receive()
                    body += message.get("body", b"")
        return message

    # receiveメソッドを置き換え
    request._receive = receive

    response = await call_next(request)
    end_time = time()

    # リクエストボディのログ
    if body:
        try:
            body_str = body.decode()
            logger.info(f"Request Body: {body_str}")
        except UnicodeDecodeError:
            logger.info("Request Body: <binary>")

    # レスポンスのログ
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} "
        f"Duration: {(end_time - start_time):.3f}s"
    )

    # レスポンスボディの取得とログ
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    try:
        response_str = response_body.decode()
        logger.info(f"Response Body: {response_str}")
    except UnicodeDecodeError:
        logger.info("Response Body: <binary>")

    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )
