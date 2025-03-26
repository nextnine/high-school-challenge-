from config.settings import settings
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from database.crud import save_chat_record
from database.session import get_db
from typing import AsyncGenerator
from utils.logger import APILogger
from pathlib import Path

logger = APILogger("QaEngine")

class QaEngine:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.offload_folder = Path("offload")  # 新增卸载目录配置
        self.offload_folder.mkdir(exist_ok=True)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    async def initialize(self):
        """异步初始化模型"""
        try:
            logger.info("正在加载语言模型...")
            self.tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME)
            self.model = AutoModelForCausalLM.from_pretrained(
                settings.MODEL_NAME,
                torch_dtype=getattr(torch, settings.MODEL_PRECISION),
                device_map="auto",
                # 新增以下参数
                offload_folder=settings.MODEL_OFFLOAD_FOLDER,
                use_safetensors=settings.USE_SAFETENSORS,
                low_cpu_mem_usage=settings.LOW_CPU_MEM_USAGE
            )
            logger.info("模型加载完成")
        except Exception as e:
            logger.error(f"模型加载失败: {str(e)}")
            raise RuntimeError("模型初始化失败") from e
    
    async def generate_answer(
        self, 
        question: str,
        user_id: int,
        session_id: str
    ) -> AsyncGenerator[str, None]:
        """生成回答并保存记录"""
        try:
            # 准备输入
            inputs = self.tokenizer(
                question, 
                return_tensors="pt"
            ).to(self.device)
            
            # 生成回答
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=500,
                    temperature=0.7,
                    top_p=0.9
                )
            
            answer = self.tokenizer.decode(
                outputs[0], 
                skip_special_tokens=True
            )
            
            # 保存到数据库
            async for session in get_db():
                await save_chat_record(
                    session=session,
                    user_id=user_id,
                    question=question,
                    answer=answer,
                    session_id=session_id
                )
            
            yield answer
            
        except Exception as e:
            logger.error(f"生成失败: {str(e)}")
            raise