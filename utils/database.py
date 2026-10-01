import psycopg2

class DatabaseUtil:

    def __init__(self, db_config):
        self.db_config = db_config

        try:
            self.connection = psycopg2.connect(**db_config)

        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            self.connection = None

    def schema_details(self, schema_name):
        try:
            schema_info_context = ""
            
            connection = self.connection
            cursor = connection.cursor()

            schema_info_context = f"Database Schema: {schema_name}\n"
            cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", (schema_name,))
            tables_list = cursor.fetchall()

            for table in tables_list:
                table_name = table[0]
                schema_info_context += f"{schema_info_context}\nTable: {table_name}\n"

                # Adding columns and data types
                cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = %s", (schema_name,))
                columns_list = cursor.fetchall()

                for column in columns_list:
                    column_name = column[0]
                    data_type = column[1]
                    schema_info_context += f" Column: {column_name}, Data Type: {data_type}\n"

                cursor.execute(f"SELECT * FROM {schema_name}.{table_name} LIMIT 5;")
                sample_data = cursor.fetchall()
                schema_info_context += f"{schema_info_context} Sample Data:\n"
                for row in sample_data:
                    schema_info_context += f"{schema_info_context}   {row}\n"
        
        except Exception as e:
            print(f"Error occurred while fetching schema details: {e}")
            schema_info_context = f"Error occurred while fetching schema details: {e}"

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        
        return schema_info_context
