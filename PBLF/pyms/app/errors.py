ERROR_MESSAGES = {
    0: "ok",
    1001: "invalid parameters",
    1002: "url is invalid or forbidden",
    1003: "unsupported command",
    1004: "unauthorized",
    2001: "task not found",
    2002: "invalid state transition",
    3001: "wordcloud generation failed",
    5000: "internal server error",
}


class AppError(Exception):
    def __init__(self, code: int, message: str | None = None) -> None:
        self.code = code
        self.message = message or ERROR_MESSAGES.get(code, "unknown error")
        super().__init__(self.message)
