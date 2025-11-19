from fastapi import (
    APIRouter,
    Depends,
    Header,
    status,
    HTTPException,
    Depends,
    Body,
    Query,
)
from fastapi_pagination import LimitOffsetParams, Params
import pymysql, logging

from ..dependencies import DB_CONNECT_CONFIG, BAD_REQUEST_RESPONSE, get_logger

router = APIRouter()


@router.get("/tickers", tags=["public"])
async def tickers_overview(
    search_query: str | None = Query(None),
    pagination_params: LimitOffsetParams = Depends(),
    logger: logging.Logger = Depends(get_logger)
):
    MAX_PAGE_SIZE = 100
    if search_query is None:
        search_query = ""
    if pagination_params.limit > MAX_PAGE_SIZE:
        raise BAD_REQUEST_RESPONSE
    search_query = search_query.strip().lower()
    # returns all tickers if search_query is None, else tickers that contain search_query
    try:
        with pymysql.connect(**DB_CONNECT_CONFIG) as conn:
            with conn.cursor() as cursor:
                with open(
                    "api/sql/crud_ops/read/overview_tickers.sql", "r"
                ) as f_sql_overview_tickers:
                    cursor.execute(
                        f_sql_overview_tickers.read(),
                        {
                            "offset": int(pagination_params.offset),  # type: ignore
                            "limit": int(pagination_params.limit),
                            "starts_with": str(search_query),
                        },
                    )
                results = cursor.fetchall()
                listOfDicts = [
                    {
                        "tickerSymbol": ticker_symbol,
                        "company": company,
                        "lastPrice": last_price,
                    }
                    for (ticker_symbol, company, last_price) in results
                ]
        return listOfDicts
    except:
        logger.error("failed to fetch tickers ", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to fetch tickers",
        )


@router.get("/ticker/{symbol}", tags=["public"])
async def ticker_details_and_price_history(symbol: str):
    # TODO
    return
