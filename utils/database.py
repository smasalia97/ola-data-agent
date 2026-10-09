import psycopg2
from psycopg2 import sql

class DatabaseUtil:

    def __init__(self, db_config):
        self.db_config = db_config

        try:
            self.connection = psycopg2.connect(**db_config)

        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            self.connection = None

    def schema_details(self, schema_name):
        connection = self.connection
        schema_info_context = f"Database Schema: {schema_name}\n"
        cursor = None

        try:
            if connection is None:
                raise psycopg2.OperationalError("Database connection is not available.")

            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = %s
                ORDER BY table_name
                """,
                (schema_name,),
            )
            tables_list = cursor.fetchall()

            for (table_name,) in tables_list:
                schema_info_context += f"\nTable: {table_name}\n"

                cursor.execute(
                    """
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema = %s AND table_name = %s
                    ORDER BY ordinal_position
                    """,
                    (schema_name, table_name),
                )
                columns_list = cursor.fetchall()

                for column in columns_list:
                    column_name = column[0]
                    data_type = column[1]
                    schema_info_context += (
                        f" Column: {column_name}, Data Type: {data_type}\n"
                    )

                cursor.execute(
                    sql.SQL("SELECT * FROM {}.{} LIMIT 5").format(
                        sql.Identifier(schema_name),
                        sql.Identifier(table_name),
                    )
                )
                sample_data = cursor.fetchall()
                schema_info_context += " Sample Data:\n"
                for row in sample_data:
                    schema_info_context += f"   {row}\n"
        
        except psycopg2.Error as e:
            print(f"Error occurred while fetching schema details: {e}")
            schema_info_context = f"Error occurred while fetching schema details: {e}"

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
        
        return schema_info_context

    def execute_sql(self, query):
        try:
            connection = self.connection
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            return str(result)
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()