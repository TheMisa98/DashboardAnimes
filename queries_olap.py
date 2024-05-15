import streamlit as st
import pandas as pd
import mysql.connector
import json

class Queries:
    def __init__(self):
        # Conectar a la base de datos
        self.conn = self.connect_to_database()

    # Función para conectar a la base de datos
    def connect_to_database(self):
        # Cargar datos de conexión desde un archivo JSON
        with open('./psw.json') as f:
            connection_data = json.load(f)

        # Conectar a la base de datos MySQL
        try:
            conn = mysql.connector.connect(
                host=connection_data['host'],
                user=connection_data['user'],
                password=connection_data['pass'],
                database=connection_data['olap_db']
            )
            return conn
        except Exception as e:
            st.error(f"Error al conectar a la base de datos: {e}")
            return None

    # Función para ejecutar consultas SQL
    def execute_query(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            st.error(f"Error al ejecutar la consulta: {e}")
            return None

    # top 10 mejores animes segun su rating
    def get_top_10_anime(self):
        query = """
        SELECT A.ANIME_NAME, AVG(AH.RATING) AS AVERAGE_RATING
        FROM ANIME A
        JOIN ANIME_HECHOS AH ON A.ID_ANIME = AH.ID_ANIME
        GROUP BY A.ANIME_NAME
        ORDER BY AVERAGE_RATING DESC
        LIMIT 10;
        """
        result = self.execute_query(query)
        if result:
            df = pd.DataFrame(result,columns=["Nombre", "Rating"])
            return df
        else:
            return None
    
    def get_top_10_anime_genre(self):
        query = """
        SELECT GENRE, ANIME_NAME, AVERAGE_RATING
        FROM (
            SELECT G.GENRE, A.ANIME_NAME, AVG(AH.RATING) AS AVERAGE_RATING,
                ROW_NUMBER() OVER (PARTITION BY G.GENRE ORDER BY AVG(AH.RATING) DESC) AS ranking
            FROM ANIME A
            JOIN GENRE_ANIME GA ON A.ID_ANIME = GA.ID_ANIME
            JOIN GENRE G ON GA.ID_GENRE = G.ID_GENRE
            JOIN ANIME_HECHOS AH ON A.ID_ANIME = AH.ID_ANIME
            GROUP BY G.GENRE, A.ANIME_NAME
        ) AS ranked
        WHERE ranking <= 10
        ORDER BY GENRE, AVERAGE_RATING DESC;
        """
        result = self.execute_query(query)
        if result:
            df = pd.DataFrame(result,columns=['Genero','Anime','Rating'])
            return df
        else:
            return None
    
    def get_top_10_anime_class(self):
        query = """
        SELECT CLASSIFICATION, ANIME_NAME, AVERAGE_RATING
        FROM (
            SELECT C.CLASSIFICATION, A.ANIME_NAME, AVG(AH.RATING) AS AVERAGE_RATING,
                ROW_NUMBER() OVER (PARTITION BY C.CLASSIFICATION ORDER BY AVG(AH.RATING) DESC) AS ranking
            FROM ANIME A
            JOIN ANIME_HECHOS AH ON A.ID_ANIME = AH.ID_ANIME
            JOIN CLASSIFICATION C ON AH.ID_CLASSIFICATION = C.ID_CLASSIFICATION
            GROUP BY C.CLASSIFICATION, A.ANIME_NAME
        ) AS ranked
        WHERE ranking <= 10
        ORDER BY CLASSIFICATION, AVERAGE_RATING DESC;
        """
        result = self.execute_query(query)
        if result:
            df = pd.DataFrame(result,columns=['Clase','Anime','Rating'])
            return df
        else:
            return None
    
    def get_top_10_anime_source(self):
        query = """
        SELECT SOURCES, ANIME_NAME, AVERAGE_RATING
        FROM (
            SELECT S.SOURCES, A.ANIME_NAME, AVG(AH.RATING) AS AVERAGE_RATING,
                ROW_NUMBER() OVER (PARTITION BY S.SOURCES ORDER BY AVG(AH.RATING) DESC) AS ranking
            FROM ANIME A
            JOIN ANIME_HECHOS AH ON A.ID_ANIME = AH.ID_ANIME
            JOIN SOURCES S ON AH.ID_SOURCES = S.ID_SOURCES
            GROUP BY S.SOURCES, A.ANIME_NAME
            ) AS ranked
            WHERE ranking <= 10
        ORDER BY SOURCES, AVERAGE_RATING DESC;
        """
        result = self.execute_query(query)
        if result:
            df = pd.DataFrame(result,columns=['Source','Anime','Rating'])
            return df
        else:
            return None
    
    def get_top_10_anime_type(self):
        query = """
        SELECT TYPES, ANIME_NAME, AVERAGE_RATING
        FROM (
            SELECT T.TYPES, A.ANIME_NAME, AVG(AH.RATING) AS AVERAGE_RATING,
                ROW_NUMBER() OVER (PARTITION BY T.TYPES ORDER BY AVG(AH.RATING) DESC) AS ranking
            FROM ANIME A
            JOIN ANIME_HECHOS AH ON A.ID_ANIME = AH.ID_ANIME
            JOIN TYPES T ON AH.ID_TYPES = T.ID_TYPES
            GROUP BY T.TYPES, A.ANIME_NAME
        ) AS ranked
        WHERE ranking <= 10
        ORDER BY TYPES, AVERAGE_RATING DESC;
        """
        result = self.execute_query(query)
        if result:
            df = pd.DataFrame(result,columns=['Type','Anime','Rating'])
            return df
        else:
            return None
    
    def get_top_10_anime_more_completed(self):
        query = """
        SELECT A.ANIME_NAME, COUNT(*) AS COMPLETIONS
        FROM ANIME A
        JOIN ANIME_HECHOS AH ON A.ID_ANIME = AH.ID_ANIME
        WHERE AH.RATING IS NOT NULL  -- Asumiendo que solo los animes con rating son considerados completados
        GROUP BY A.ANIME_NAME
        ORDER BY COMPLETIONS DESC
        LIMIT 10;
        """
        result = self.execute_query(query)
        if result:
            df = pd.DataFrame(result,columns=['Anime','Completion'])
            return df
        else:
            return None
        
    # Método para ejecutar una consulta personalizada
    def custom_query(self, query):
        result = self.execute_query(query)
        if result:
            df = pd.DataFrame(result)
            return df
        else:
            return None

