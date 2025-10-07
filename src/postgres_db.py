import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class VectorDB:
    def __init__(self, dbname="vectordb", user="postgres", password="postgres", host="localhost", port="5432"):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor()

    def init_db(self, dim=1536):
        """Initialize database with pgvector and a documents table"""
        try:
            self.cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            self.cur.execute(f"""
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    content TEXT,
                    embedding VECTOR({dim})
                );
            """)
            print("✅ Database initialized successfully!")
        except Exception as e:
            print("❌ Error initializing database:", e)

    def delete_db(self):
        """Delete the entire database"""
        try:
            self.cur.execute("DROP TABLE IF EXISTS documents;")
            print("✅ Database deleted successfully!")
        except Exception as e:
            print("❌ Error deleting database:", e)

    def insert_document(self, content, embedding):
        """Insert a document and its embedding"""
        try:
            self.cur.execute(
                "INSERT INTO documents (content, embedding) VALUES (%s, %s);",
                (content, embedding)
            )
        except Exception as e:
            print("❌ Error inserting document:", e)

    def search_similar(self, query_embedding, top_k=5):
        """Search for top_k most similar documents"""
        try:
            self.cur.execute(
                """
                SELECT id, content, embedding <-> %s::vector AS distance,
                       1 - (embedding <-> %s::vector) AS similarity
                FROM documents
                ORDER BY embedding <-> %s::vector
                LIMIT %s;
                """,
                (query_embedding, query_embedding, query_embedding, top_k)
            )
            results = self.cur.fetchall()
            return results
        except Exception as e:
            print("❌ Error searching documents:", e)
            return []

    def close(self):
        """Close connection"""
        self.cur.close()
        self.conn.close()