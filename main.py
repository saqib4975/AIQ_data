import pandas as pd
import requests
import psycopg2 

user_data_API = "https://jsonplaceholder.typicode.com/users"

# PostgreSQL connection details
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "sales_db"
POSTGRES_USER = "postgres_user"
POSTGRES_PASSWORD = "password123"
TABLE_NAME = "user_sales_data"


def get_user_data():
    
    try:
        response = requests.get(user_data_API)
        response.raise_for_status()
        data = response.json()
        user_data = [
            {
                "id": user["id"],
                "name": user["name"],
                "username": user["username"],
                "email": user["email"],
                "lat": user.get("address", {}).get("geo", {}).get("lat"),
                "lng": user.get("address", {}).get("geo", {}).get("lng"),
                "city": user.get("address", {}).get("city"),
            }
            for user in data
        ]
        return pd.DataFrame(user_data)  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user data: {e}")
        return None


def load_sales_data():
    """Loads sales data from CSV."""
    try:
        sales_df = pd.read_csv("sales_data.csv")
        return sales_df
    except FileNotFoundError:
        print("Error: sales_data.csv file not found.")
        return None


def merge_sales_with_user_data(sales_df, user_data):
    
    sales_df["customer_id"] = sales_df["customer_id"].astype(int)  
    merged_df = pd.merge(sales_df, user_data, how="left", left_on="customer_id", right_on="id")
    return merged_df


def insert_data_to_postgres(merged_df):
    

    try:
        
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cur = conn.cursor()

        
        cur.execute(f"DROP TABLE IF EXISTS {TABLE_NAME};")
        conn.commit()

        
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                price FLOAT,
                order_date DATE,  -- Add the order_date column
                name VARCHAR(255),
                username VARCHAR(255),
                email VARCHAR(255),
                lat FLOAT,
                lng FLOAT,
                city VARCHAR(255)
            );
        """
        cur.execute(create_table_query)

        # Insert data into the table
        for _, row in merged_df.iterrows():
            cur.execute(
                f"""
                INSERT INTO {TABLE_NAME} (customer_id, product_id, quantity, price, order_date,
                                           name, username, email, lat, lng, city)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (row['customer_id'], row['product_id'], row['quantity'], row['price'], row['order_date'],
                 row['name'], row['username'], row['email'], row['lat'], row['lng'], row['city'])
            )

        
        conn.commit()
        print("Data inserted successfully into PostgreSQL table.")

    except (Exception, psycopg2.Error) as e:
        print("Error inserting data into PostgreSQL table:", e)
    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection closed.")


def main():
    # Fetch user data
    user_data = get_user_data()
    if user_data is None:
        print("Failed to fetch user data. Exiting...")
        return

    # Load sales data
    sales_df = load_sales_data()
    if sales_df is None:
        print("Failed to load sales data. Exiting...")
        return

   
    merged_df = merge_sales_with_user_data(sales_df, user_data)

    
    insert_data_to_postgres(merged_df)


if __name__ == "__main__":
    main()
