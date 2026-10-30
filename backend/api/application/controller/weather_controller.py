from datetime import datetime
import pyodbc
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from application.configs.pyodbc_configs import GetConnectionString

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/clima/climaAtual")
def read_clima_atual():
    try:
        connectionString = GetConnectionString()
        conn = pyodbc.connect(connectionString)
        cursor = conn.cursor()
            
        query = f"""SELECT TOP 1 IDClima, Temperatura as 'temperatura', umidade as umidade, indiceUV, DataClima as 'data' 
        FROM TBclima ORDER BY DataClima DESC"""
            
        cursor.execute(query)
        colunas = [column[0] for column in cursor.description]
        result = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()

        return {
            "status" : "sucesso",
            "total" : len(result),
            "climaAtual" : result
        }
                
    except Exception as e:
        print(f"Ocorreu um erro ao buscar os dados do clima. \n{e}")

@app.get("/clima/climaSemanal")
def read_clima_semanal():
    try:
        connectionString = GetConnectionString()
        conn = pyodbc.connect(connectionString)
        cursor = conn.cursor()
        
        query = f"""
            WITH MediasDiarias AS (
                SELECT
                    CAST(DataClima AS DATE) AS DataDia,
                    AVG(Temperatura) AS MediaTemperatura
                FROM TBclima
                GROUP BY CAST(DataClima AS DATE)
            )
            SELECT 
                r.IDResumo as id,
                r.DataDia as data,
                ISNULL(m.MediaTemperatura, 0) as media,
                r.TemperaturaMaxima as temp_maxima,
                r.TemperaturaMinima as temp_minima
            FROM TBResumoClima r
            LEFT JOIN MediasDiarias m
                ON r.DataDia = m.DataDia
            WHERE r.DataDia >= CAST(DATEADD(DAY, -7, GETDATE()) AS DATE)
            ORDER BY 
                r.DataDia DESC;"""
        
        cursor.execute(query)
        colunas = [column[0] for column in cursor.description]
        raw_results = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        results = []
        
        for result in raw_results:
            dt = result["data"]
            if isinstance(dt, datetime):
                dt = dt.date()
            
            dia_semana_str = dias_semana[dt.weekday()] if dt else ""
            
            results.append({
                "id" : result["id"],
                "data" : dt.strftime("%d/%m/%y"),
                "dia_semana" : dia_semana_str,
                "media" : result["media"],
                "temp_maxima" : result["temp_maxima"],
                "temp_minima" : result["temp_minima"]
            })
            
        return {
           "status" : "sucesso",
            "total" : len(results),
            "dados" : results
        }
            
    except Exception as e:
        print(f"Ocorreu um erro ao buscar os dados do clima. \n{e}")
        

@app.get("/climas")
def read_climas(pageInput : int, pageSizeInput : int):
    try:
        page = pageInput
        pageSize = pageSizeInput
        
        connectionString = GetConnectionString()
        conn = pyodbc.connect(connectionString)
        cursor = conn.cursor()
        
        query = f"SELECT * FROM TBclima ORDER BY DataClima DESC OFFSET ((? - 1) * ?) ROWS FETCH NEXT ? ROWS ONLY"
        parameters = (
            page,
            pageSize,
            pageSize
        )
        # print(query, parameters)
        cursor.execute(query, parameters)
        
        colunas = [column[0] for column in cursor.description]
        results = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return {
            "status" : "sucesso",
            "total" : len(results),
            "dados" : results,
            "page": page,
            "pageSize": pageSize
        }
        
        
    except Exception as e:
        print(f"Ocorreu um erro ao buscar os dados do clima. \n{e}")

@app.get("/clima/{clima_id}")
def read_clima_id(clima_id : int):
    if clima_id <= 0:
        raise HTTPException(status_code=400, detail="ID inválido.")
    try:
        
        connectionString = GetConnectionString()
        conn = pyodbc.connect(connectionString)
        cursor = conn.cursor()
        
        query = f"SELECT * FROM TBclima WHERE IDClima = ? ORDER BY DataClima DESC"
        cursor.execute(query, clima_id)
        
        colunas = [column[0] for column in cursor.description]
        results = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        
        if not results:
            raise HTTPException(status_code=404, detail="Nenhum resultado encontrado. ID não existente.")
        
        cursor.close()
        conn.close()
       
        return {
            "status" : "sucesso",
            "total" : len(results),
            "dados" : results
        }
        
    except Exception as e:
        print(f"Ocorreu um erro ao buscar os dados do clima {clima_id}. \n{e}")
        
