from backend.database import engine, Base
from backend import models
import os
import sys

def reset_database():
    """
    מוחק את כל הטבלאות במסד נתונים ויוצר אותן מחדש עם המבנה החדש
    """
    print("\n🔄 איפוס מסד הנתונים...")
    
    # מחיקת כל הטבלאות
    print("🗑️ מוחק טבלאות קיימות...")
    Base.metadata.drop_all(bind=engine)
    
    # יצירת הטבלאות מחדש
    print("🏗️ יוצר טבלאות חדשות...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ איפוס מסד הנתונים הושלם בהצלחה!")
    print("ℹ️ כעת תוכל להשתמש במערכת עם המבנה החדש של הטבלאות.")

if __name__ == "__main__":
    # Add the parent directory to sys.path to allow absolute imports
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # אישור מהמשתמש
    confirm = input("⚠️ אזהרה: פעולה זו תמחק את כל הנתונים במסד הנתונים! להמשיך? (כ/ל): ")
    if confirm.lower() in ['כ', 'y', 'yes', 'כן']:
        reset_database()
    else:
        print("❌ הפעולה בוטלה. לא בוצעו שינויים במסד הנתונים.") 