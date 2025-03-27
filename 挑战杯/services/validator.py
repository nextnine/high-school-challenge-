import re
from fastapi import HTTPException
from config.settings import settings

class InputValidator:
    def __init__(self):
        self.banned_words = ["暴力", "色情", "政治敏感词"]
        
    def validate_question(self, text: str):
        # 长度验证
        if len(text) > settings.MAX_QUESTION_LENGTH:
            raise HTTPException(400, "问题过长")
        
        # 敏感词验证
        if any(word in text for word in self.banned_words):
            raise HTTPException(403, "包含违规内容")
        
        # 特殊字符验证
        if not re.match(r'^[\w\u4e00-\u9fa5\s\.,?!@#$%^&*()\-+=]+$', text):
            raise HTTPException(400, "包含非法字符")

validator = InputValidator()