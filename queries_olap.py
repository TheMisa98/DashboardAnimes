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
    def get_top_10_anime_rating(self):
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
    
    def best_anime_genre(self):
        query = """
        SELECT GENRE, ANIME_NAME, RATING_COUNT
        FROM (
            SELECT G.GENRE, A.ANIME_NAME, COUNT(*) AS RATING_COUNT,
                ROW_NUMBER() OVER (PARTITION BY G.GENRE ORDER BY COUNT(*) DESC) AS ranking
            FROM ANIME A
            JOIN GENRE_ANIME GA ON A.ID_ANIME = GA.ID_ANIME
            JOIN GENRE G ON GA.ID_GENRE = G.ID_GENRE
            JOIN ANIME_HECHOS AH ON A.ID_ANIME = AH.ID_ANIME
            WHERE AH.RATING IS NOT NULL -- Se asume que solo se cuentan los animes con calificación
            GROUP BY G.GENRE, A.ANIME_NAME
        ) AS ranked
        WHERE ranking <= 1
        ORDER BY GENRE, RATING_COUNT DESC;
        """
        result = self.execute_query(query)
        if result:
            df = pd.DataFrame(result,columns=['Genero','Anime','Vistas'])
            return df
        else:
            return None
    
    def get_top_10_anime_class(self):
        query = """
        SELECT CLASSIFICATION, ANIME_NAME, RATING_COUNT
        FROM (
            SELECT C.CLASSIFICATION, A.ANIME_NAME, COUNT(*) AS RATING_COUNT,
                ROW_NUMBER() OVER (PARTITION BY C.CLASSIFICATION ORDER BY COUNT(*) DESC) AS ranking
            FROM ANIME A
            JOIN ANIME_HECHOS AH ON A.ID_ANIME = AH.ID_ANIME
            JOIN CLASSIFICATION C ON AH.ID_CLASSIFICATION = C.ID_CLASSIFICATION
            WHERE AH.RATING IS NOT NULL -- Se asume que solo se cuentan los animes con calificación
            GROUP BY C.CLASSIFICATION, A.ANIME_NAME
        ) AS ranked
        WHERE ranking <= 10
        ORDER BY CLASSIFICATION, RATING_COUNT DESC;
        """
        result = self.execute_query(query)
        if result:
            df = pd.DataFrame(result,columns=['Clase','Anime','Vistas'])
            return df
        else:
            return None
    
    def get_top_10_anime_source(self):
        query = """
        SELECT SOURCES, ANIME_NAME, RATING_COUNT
        FROM (
            SELECT S.SOURCES, A.ANIME_NAME, COUNT(*) AS RATING_COUNT,
                ROW_NUMBER() OVER (PARTITION BY S.SOURCES ORDER BY COUNT(*) DESC) AS ranking
            FROM ANIME A
            JOIN ANIME_HECHOS AH ON A.ID_ANIME = AH.ID_ANIME
            JOIN SOURCES S ON AH.ID_SOURCES = S.ID_SOURCES
            WHERE AH.RATING IS NOT NULL -- Se asume que solo se cuentan los animes con calificación
            GROUP BY S.SOURCES, A.ANIME_NAME
        ) AS ranked
        WHERE ranking <= 10
        ORDER BY SOURCES, RATING_COUNT DESC;
        """
        result = self.execute_query(query)
        if result:
            df = pd.DataFrame(result,columns=['Source','Anime','Rating'])
            return df
        else:
            return None
    
    def get_top_10_anime_type(self):
        query = """
        SELECT TYPES, ANIME_NAME, VIEW_COUNT
        FROM (
            SELECT T.TYPES, A.ANIME_NAME, COUNT(*) AS VIEW_COUNT,
                ROW_NUMBER() OVER (PARTITION BY T.TYPES ORDER BY COUNT(*) DESC) AS ranking
            FROM ANIME A
            JOIN ANIME_HECHOS AH ON A.ID_ANIME = AH.ID_ANIME
            JOIN TYPES T ON AH.ID_TYPES = T.ID_TYPES
            WHERE AH.RATING > 0 -- Se asume que AH.WATCHING > 0 indica que el anime ha sido visto
            GROUP BY T.TYPES, A.ANIME_NAME
        ) AS ranked
        WHERE ranking <= 10
        ORDER BY TYPES, VIEW_COUNT DESC;
        """
        result = self.execute_query(query)
        if result:
            df = pd.DataFrame(result,columns=['Type','Anime','Vistas'])
            return df
        else:
            return None
    
    def get_top_10_anime_more_watch(self):
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
            df = pd.DataFrame(result,columns=['Anime','Vistas'])
            return df
        else:
            return None
    
    def get_top_10_genre_more_watch(self):
        query = """
        SELECT G.GENRE, COUNT(*) AS VIEW_COUNT
        FROM ANIME A
        JOIN GENRE_ANIME GA ON A.ID_ANIME = GA.ID_ANIME
        JOIN GENRE G ON GA.ID_GENRE = G.ID_GENRE
        JOIN ANIME_HECHOS AH ON A.ID_ANIME = AH.ID_ANIME
        WHERE AH.RATING > 0 -- Se asume que AH.WATCHING > 0 indica que el anime ha sido visto
        GROUP BY G.GENRE
        ORDER BY VIEW_COUNT DESC
        LIMIT 10;
        """
        result = self.execute_query(query)
        if result:
            df = pd.DataFrame(result,columns=['Genero','Vistas'])
            return df
        else:
            return None
    
    def get_top_types_mor_watch(self):
        query = """
        SELECT T.TYPES, COUNT(*) AS VIEW_COUNT
        FROM ANIME A
        JOIN ANIME_HECHOS AH ON A.ID_ANIME = AH.ID_ANIME
        JOIN TYPES T ON AH.ID_TYPES = T.ID_TYPES
        WHERE AH.RATING > 0 -- Se asume que AH.WATCHING > 0 indica que el anime ha sido visto
        GROUP BY T.TYPES
        ORDER BY VIEW_COUNT DESC;
        """
        result = self.execute_query(query)
        if result:
            df = pd.DataFrame(result,columns=['Tipo','Vistas'])
            return df
        else:
            return None
    def get_top_classification_mor_watch(self):
        query = """
        SELECT C.CLASSIFICATION, COUNT(*) AS VIEW_COUNT
        FROM CLASSIFICATION C
        JOIN ANIME_HECHOS AH ON C.ID_CLASSIFICATION = AH.ID_CLASSIFICATION
        WHERE AH.RATING > 0 -- Se asume que AH.WATCHING > 0 indica que el anime ha sido visto
        GROUP BY C.CLASSIFICATION
        ORDER BY VIEW_COUNT DESC;
        """
        result = self.execute_query(query)
        if result:
            df = pd.DataFrame(result,columns=['Clase','Vistas'])
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

