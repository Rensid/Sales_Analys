
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import log_decorator
from app.schemas import AnalysSchema
from app.services.llm_analys import get_data_for_prompt, get_result, load_response_to_db, make_prompt, make_request_to_llm
from app.services.xml_parser import load_products, parse_product_data
from app.db.base import main_db_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await main_db_manager.init_models()
    yield

app = FastAPI()


@log_decorator
@app.get('/analys_results/{prompt_id}')
async def get_analys_result(session: AsyncSession = Depends(main_db_manager.get_async_session), prompt_id) -> AnalysSchema:
    result = await get_result(session, prompt_id)
    return result


@log_decorator
@app.post('/upload-xml/')
async def load_file(session: AsyncSession = Depends(main_db_manager.get_async_session),
                    file: UploadFile = File(...)):
    result = await parse_product_data(file)
    await load_products(result['products'], session)
    data = await get_data_for_prompt(result['date'], session)
    prompt = await make_prompt(data)
    response = await make_request_to_llm(prompt)
    await load_response_to_db(session, response)
