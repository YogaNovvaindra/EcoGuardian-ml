import logging
from app.db import use_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

def get_ispu_clean():
    engine = use_engine()
    connection = engine.connect()
    
    try:
        query = text(
            """
            DELETE FROM ispu WHERE createdAt < NOW() - INTERVAL 30 DAY
        """
        )
        connection.execute(query)
        connection.commit()
    except SQLAlchemyError as e:
        logging.error(e)
        return f"Error when updating ispu table : {str(e)}"
    else:
        return "Success updating ispu table"
    finally:
        connection.close()