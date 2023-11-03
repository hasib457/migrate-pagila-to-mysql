# pylint:  disable-all

class SqlQueries:
    create_db_database = "CREATE DATABASE IF NOT EXISTS db;"
    create_actor = """
        CREATE TABLE IF NOT EXISTS db.actor (
            actor_id SMALLINT ,
            first_name VARCHAR(45),
            last_name VARCHAR(45),
            last_update TIMESTAMP,
             batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
    
    create_address="""
        CREATE TABLE IF NOT EXISTS db.address (
            address_id SMALLINT,
            address VARCHAR(50),
            address2 VARCHAR(50),
            district VARCHAR(20),
            city_id SMALLINT,
            postal_code VARCHAR(10),
            phone VARCHAR(20),
            last_update TIMESTAMP ,
             batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

    create_category = """
        CREATE TABLE IF NOT EXISTS db.category (
            category_id TINYINT,
            name VARCHAR(25),
            last_update TIMESTAMP ,
             batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    create_city="""
        CREATE TABLE IF NOT EXISTS db.city (
            city_id SMALLINT ,
            city VARCHAR(50),
            country_id SMALLINT,
            last_update TIMESTAMP,
             batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""

    create_country = """
        CREATE TABLE IF NOT EXISTS db.country (
            country_id SMALLINT,
            country VARCHAR(50),
            last_update TIMESTAMP ,
             batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""

    create_customer = """
        CREATE TABLE IF NOT EXISTS db.customer (
            customer_id SMALLINT ,
            store_id TINYINT ,
            first_name VARCHAR(45),
            last_name VARCHAR(45),
            email VARCHAR(50),
            address_id SMALLINT,
            activebool BOOLEAN,
            create_date DATETIME,
            last_update TIMESTAMP,
            active BOOLEAN ,
             batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""

    create_film = """
        CREATE TABLE IF NOT EXISTS db.film (
            film_id SMALLINT,
            title VARCHAR(255),
            description TEXT,
            release_year YEAR,
            language_id TINYINT,
            original_language_id TINYINT,
            rental_duration TINYINT,
            rental_rate DECIMAL(4,2),
            length SMALLINT,
            replacement_cost DECIMAL(5,2),
            rating VARCHAR(5),
            last_update TIMESTAMP, 
            special_features TEXT,
            full_text TEXT,
             batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""

    create_film_actor = """
        CREATE TABLE IF NOT EXISTS db.film_actor (
            actor_id SMALLINT, 
            film_id SMALLINT, 
            last_update TIMESTAMP, 
             batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""

    create_film_category = """
        CREATE TABLE IF NOT EXISTS db.film_category (
            film_id SMALLINT, 
            category_id TINYINT , 
            last_update TIMESTAMP, 
            batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""

    create_inventory = """
        CREATE TABLE IF NOT EXISTS db.inventory (
            inventory_id MEDIUMINT, 
            film_id SMALLINT , 
            store_id TINYINT, 
            last_update TIMESTAMP, 
             batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""


    create_language = """
        CREATE TABLE IF NOT EXISTS db.language (
            language_Id TINYINT, 
            name CHAR(20), 
            last_update TIMESTAMP, 
             batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
    
    create_payment = """
        CREATE TABLE IF NOT EXISTS db.payment (
            payment_Id SMALLINT, 
            customer_Id SMALLINT, 
            staff_Id TINYINT, 
            rental_Id INT, 
            amount DECIMAL(5,2), 
            payment_date DATETIME, 
             batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
    
    create_rental = """
        CREATE TABLE IF NOT EXISTS db.rental (
            rental_id INT ,
            rental_date DATETIME ,
            inventory_id MEDIUMINT  ,
            customer_id SMALLINT  ,
            return_date DATETIME ,
            staff_id TINYINT  ,
            last_update TIMESTAMP  ,
             batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
    
    create_staff = """
        CREATE TABLE IF NOT EXISTS db.staff (
            staff_id TINYINT,
            first_name VARCHAR(45) ,
            last_name VARCHAR(45) ,
            address_id SMALLINT  ,
            email VARCHAR(50) ,
            store_id TINYINT  ,
            active BOOLEAN,
            username VARCHAR(16) ,
            password VARCHAR(40) ,
            last_update TIMESTAMP  ,
            picture BLOB ,
             batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
    
    create_store = """
        CREATE TABLE IF NOT EXISTS db.store (
            store_id TINYINT,
            manager_staff_id TINYINT ,
            address_id SMALLINT,
            last_update TIMESTAMP  ,
             batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""

    
    last_update = """SELECT COALESCE(MAX({}), '1970-01-01 00:00:00') FROM db.{};"""
    select_statement = """ SELECT * FROM {} WHERE {} > '{}' ;"""
    insert_statement = """ INSERT INTO db.{} VALUES {};"""

