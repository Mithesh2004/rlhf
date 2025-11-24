from utils.mongodb_config import test_connection, get_conversations_collection

def main():
    print("Testing MongoDB Atlas connection...")
    
    if test_connection():
        print("\n✅ Connection successful!")
        
        # Test insert
        collection = get_conversations_collection()
        if collection is not None:  # FIXED: Use 'is not None' instead of 'if collection:'
            test_doc = {
                "test": "atlas_connection",
                "message": "Hello from Atlas!"
            }
            result = collection.insert_one(test_doc)
            print(f"✅ Test document inserted with ID: {result.inserted_id}")
            
            # Verify
            found = collection.find_one({"_id": result.inserted_id})
            print(f"✅ Test document retrieved: {found}")
            
            # Clean up
            collection.delete_one({"_id": result.inserted_id})
            print("✅ Test document deleted")
            print("\n🎉 All tests passed!")
        else:
            print("❌ Could not get collection")
    else:
        print("\n❌ Connection failed!")

if __name__ == "__main__":
    main()
