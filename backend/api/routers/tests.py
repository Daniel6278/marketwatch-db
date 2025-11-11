from fastapi import APIRouter
import pymysql

from ..dependencies import DB_CONNECT_CONFIG

router = APIRouter()


@router.get("/")
async def sanity_check():
    return "FastAPI Is Responding"


@router.get("/test/rds")
async def check_aws_can_connect():
    def pymysql_connect_using_dotenv_vars():
        try:
            with pymysql.connect(**DB_CONNECT_CONFIG) as conn:
                print("Test : Connection Successful")
            return True
        except:
            return False

    return (
        "RDS Connection Successful"
        if pymysql_connect_using_dotenv_vars()
        else "Problem with RDS Connection"
    )


@router.get("/test/alpha-vantage")
async def check_alphaVantage_can_connect():
    def alphaVantage_auth():
        return True

    return "Success" if alphaVantage_auth() else "Error"


@router.get("/test/yahoo-finance")
async def check_yFinance_can_connect():
    def yahooFinance_connect():
        return True

    return "Success" if yahooFinance_connect() else "Error"
