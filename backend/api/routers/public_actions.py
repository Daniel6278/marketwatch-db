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
import pymysql

from ..dependencies import DB_CONNECT_CONFIG

router = APIRouter()


@router.get("/tickers", tags=["public"])
async def tickers_overview(
    search_query: str | None = Query(None),
    pagination_params: LimitOffsetParams = Depends(),
):
    MAX_PAGE_SIZE = 100
    if search_query is None:
        search_query = ""
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
                            "offset": pagination_params.offset,  # type: ignore
                            "limit": pagination_params.limit,
                            "starts_with": search_query,
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to fetch tickers",
        )


@router.get("/ticker/{symbol}", tags=["public"])
async def ticker_details_and_price_history(symbol: str):
    # TODO
    return
