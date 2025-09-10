import re

def mask_company(text: str) -> str:
    """
    簡易マスク: 株式会社○○ → 株式会社***
    """
    return re.sub(r"(株式会社|有限会社)(\S+)", r"\1***", text)
