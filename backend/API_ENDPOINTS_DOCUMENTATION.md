# FastAPI  
**Version:** 0.1.0  
## `/`
### GET
*Sanity Check*  
**Responses:**  
- `200` — Successful Response  

## `/test/rds`
### GET
*Check Aws Can Connect*  
**Responses:**  
- `200` — Successful Response  

## `/test/alpha-vantage`
### GET
*Check Alphavantage Can Connect*  
**Responses:**  
- `200` — Successful Response  

## `/test/yahoo-finance`
### GET
*Check Yfinance Can Connect*  
**Responses:**  
- `200` — Successful Response  

## `/tickers`
### GET
*Tickers Overview*  
**Parameters:**  
- `search_query` () —   
- `limit` (integer) —   
- `offset` (integer) —   
- `name` (string) —   
**Responses:**  
- `200` — Successful Response  
- `422` — Validation Error  

## `/ticker/{symbol}`
### GET
*Ticker Details And Price History*  
**Parameters:**  
- `symbol` (string) —   
**Responses:**  
- `200` — Successful Response  
- `422` — Validation Error  

## `/admin/setup`
### POST
*Sitewide Setup*  
**Parameters:**  
- `name` (string) —   
**Responses:**  
- `200` — Successful Response  
- `422` — Validation Error  

## `/admin/fill`
### PUT
*Insert Static Data Into Db*  
**Parameters:**  
- `name` (string) —   
**Responses:**  
- `200` — Successful Response  
- `422` — Validation Error  

## `/admin/tables`
### GET
*List Tables*  
**Responses:**  
- `200` — Successful Response  

## `/admin/table/{table_name}`
### GET
*View Table*  
**Parameters:**  
- `table_name` (string) —   
- `limit` (integer) —   
- `offset` (integer) —   
**Responses:**  
- `200` — Successful Response  
- `422` — Validation Error  

## `/admin/metrics/storage`
### GET
*Check Db Size*  
**Responses:**  
- `200` — Successful Response  

## `/admin/signin`
### POST
*Signin*  
**Parameters:**  
- `name` (string) —   
**Responses:**  
- `200` — Successful Response  
- `422` — Validation Error  

## `/admin/me`
### GET
*Admin Frontend User Info*  
**Parameters:**  
- `name` (string) —   
**Responses:**  
- `200` — Successful Response  
- `422` — Validation Error  

## `/register`
### POST
*Register New User*  
**Parameters:**  
- `name` (string) —   
**Responses:**  
- `200` — Successful Response  
- `422` — Validation Error  

## `/signin`
### POST
*Signin*  
**Parameters:**  
- `email` (string) —   
- `password` (string) —   
**Responses:**  
- `200` — Successful Response  
- `422` — Validation Error  

## `/me`
### GET
*User Me Shortcut*  
**Parameters:**  
- `domain` (string) —   
**Responses:**  
- `200` — Successful Response  
- `422` — Validation Error  

## `/users/{id}`
### GET
*User Profile Details*  
**Parameters:**  
- `id` (integer) —   
**Responses:**  
- `200` — Successful Response  
- `422` — Validation Error  

## `/users/{id}/portfolios`
### GET
*User Portfolios Basic Info*  
**Parameters:**  
- `id` (integer) —   
- `return_descriptions` (boolean) —   
**Responses:**  
- `200` — Successful Response  
- `422` — Validation Error  

## `/users/{id}/portfolios/holdings`
### GET
*User Portfolios And Contained Holdings*  
**Parameters:**  
- `id` (integer) —   
**Responses:**  
- `200` — Successful Response  
- `422` — Validation Error  

## `/users/{id}/portfolios/new`
### POST
*Create Portfolio*  
**Parameters:**  
- `id` (integer) —   
- `name` (string) —   
- `description` (string) —   
- `demo_mode` (boolean) —   
**Responses:**  
- `200` — Successful Response  
- `422` — Validation Error  

