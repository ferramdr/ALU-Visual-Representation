import pymongo
from datetime import datetime

# 1. Configuración de la Conexión
URI = "mongodb://localhost:27017/"

try:
    print("🔌 Conectando a MongoDB...")
    client = pymongo.MongoClient(URI, serverSelectionTimeoutMS=2000)
    
    # Forzar verificación de conexión
    client.server_info()
    print("Conexión Exitosa al Servidor.")

    # 2. Definir Base de Datos y Colección
    db_name = "alu_simulator"
    collection_name = "operation_logs"
    
    db = client[db_name]
    collection = db[collection_name]

    # 3. Crear un documento de prueba (Genesis Log)
    test_log = {
        "timestamp": datetime.now(),
        "tipo": "Proyecto Final",
        "mensaje": "Base de datos inicializada correctamente",
        "version_alu": "1.0",
        "autor": "Fernando Ramírez"
    }

    # 4. Insertar el documento
    result = collection.insert_one(test_log)
    
    print(f"Base de Datos '{db_name}' creada.")
    print(f"Colección '{collection_name}' creada.")
    print(f"ID del documento de prueba: {result.inserted_id}")
    
    collection.create_index([("timestamp", -1)])
    print("Índice de búsqueda por fecha creado.")

except pymongo.errors.ServerSelectionTimeoutError:
    print("ERROR: No se pudo conectar a MongoDB.")
    print("Asegúrate de que el servicio esté corriendo en Windows Services.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
finally:
    if 'client' in locals():
        client.close()
        print("Conexión cerrada.")