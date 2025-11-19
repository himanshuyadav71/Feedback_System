from django.http import JsonResponse
from django.db import connections
from django.db.utils import DatabaseError
from django.views.decorators.http import require_GET

@require_GET
def list_tables(request):
    """
    GET /tables/ -> returns JSON with list of schema.table names or an error.
    """
    try:
        with connections['default'].cursor() as cur:
            cur.execute("""
                SELECT TABLE_SCHEMA + '.' + TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_SCHEMA, TABLE_NAME
            """)
            rows = cur.fetchall()
            tables = [r[0] for r in rows]
            return JsonResponse({'status': 'ok', 'tables': tables})
    except DatabaseError as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)

@require_GET
def list_users(request):
    """
    GET /users/ -> returns JSON list of rows from Users_Student.
    """
    try:
        with connections['default'].cursor() as cur:
            cur.execute("""
                SELECT EnrollmentNo, FullName, Gender, Email, Branch, Year, Section, IsActive
                FROM Users_Student
                ORDER BY EnrollmentNo
            """)
            rows = cur.fetchall()
            users = []
            for r in rows:
                users.append({
                    'EnrollmentNo': r[0],
                    'FullName': r[1],
                    'Gender': r[2],
                    'Email': r[3],
                    'Branch': r[4],
                    'Year': r[5],
                    'Section': r[6],
                    'IsActive': bool(r[7]),
                })
            return JsonResponse({'status': 'ok', 'users': users})
    except DatabaseError as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)

def check_db_connection_and_list_tables():
    try:
        with connections['default'].cursor() as cur:
            # lightweight check
            cur.execute("SELECT 1")
        print("database connection successful")
    except DatabaseError:
        print("connection failed")

check_db_connection_and_list_tables()