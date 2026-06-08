from utils.helpers import _execute_query

def db_get_reservations_dashboard(inicio: str, fin: str) -> dict:
    """Retorna todos los datos necesarios para el dashboard de reservas."""

    by_period = _execute_query("""
        SELECT DATE_FORMAT(reservation_datetime, '%Y-%m-%d') as fecha, COUNT(*) as cantidad
        FROM reservations
        WHERE DATE(reservation_datetime) BETWEEN %s AND %s
        GROUP BY DATE(reservation_datetime)
        ORDER BY DATE(reservation_datetime)
    """, (inicio, fin))

    by_status = _execute_query("""
        SELECT 
            CASE 
                WHEN status_reservation IN ('Confirmed', 'Pending') 
                    AND reservation_datetime < NOW() THEN 'NoShow'
                ELSE status_reservation 
            END as estado,
            COUNT(*) as cantidad
        FROM reservations
        WHERE reservation_datetime BETWEEN %s AND %s
        GROUP BY estado
    """, (inicio, fin))

    heatmap = _execute_query("""
        SELECT 
            DAYOFWEEK(reservation_datetime) as dia,
            HOUR(reservation_datetime) as hora,
            COUNT(*) as cantidad
        FROM reservations
        WHERE reservation_datetime BETWEEN %s AND %s
        GROUP BY dia, hora
    """, (inicio, fin))

    by_weekday = _execute_query("""
        SELECT 
            DAYOFWEEK(reservation_datetime) as dia,
            COUNT(*) as cantidad
        FROM reservations
        WHERE reservation_datetime BETWEEN %s AND %s
        GROUP BY dia
        ORDER BY dia
    """, (inicio, fin))

    return {
        "by_period":  by_period,
        "by_status":  by_status,
        "heatmap":    heatmap,
        "by_weekday": by_weekday,
    }

def db_get_delivery_dashboard(inicio: str, fin: str) -> dict:
    """Retorna todos los datos necesarios para el dashboard de delivery."""

    income = _execute_query("""
        SELECT DATE_FORMAT(d.delivery_datetime, '%Y-%m-%d') as fecha, SUM(dm.quantity * m.price) as ingresos
        FROM deliveries_menus dm
        JOIN deliveries d ON d.id = dm.delivery_id
        join menus m on dm.menu_id = m.id 
        WHERE d.delivery_datetime BETWEEN %s AND %s AND d.status = 'delivered'
        GROUP BY DATE(d.delivery_datetime)
        ORDER BY DATE(d.delivery_datetime)
    """, (inicio, fin))

    top_products = _execute_query("""
        SELECT m.name, DATE_FORMAT(d.delivery_datetime, '%Y-%m-%d') as fecha, SUM(dm.quantity) as total_vendido
        FROM deliveries_menus dm
        JOIN menus m ON dm.menu_id = m.id
        JOIN deliveries d ON dm.delivery_id = d.id
        WHERE d.delivery_datetime BETWEEN %s AND %s
        GROUP BY m.id, m.name
        ORDER BY DATE(d.delivery_datetime)
    """, (inicio, fin))

    by_hour = _execute_query("""
        SELECT 
            HOUR(delivery_datetime) AS hora, 
            DAYOFWEEK(delivery_datetime) AS dia,
            COUNT(*) AS cantidad
        FROM deliveries
        WHERE delivery_datetime BETWEEN %s AND %s
        GROUP BY hora, DAYOFWEEK(delivery_datetime) 
        ORDER BY dia, hora                       
    """, (inicio, fin))

    by_status = _execute_query("""
        SELECT status, DATE_FORMAT(delivery_datetime, '%Y-%m-%d') as fecha, COUNT(*) as cantidad
        FROM deliveries
        WHERE delivery_datetime BETWEEN %s AND %s
        GROUP BY status
        ORDER BY fecha
    """, (inicio, fin))

    return {
        "income": income,
        "top_products": top_products,
        "by_hour": by_hour,
        "by_status": by_status,
    }

def db_get_reviews_dashboard(inicio: str, fin: str) -> dict:
    """Retorna todos los datos necesarios para el dashboard de reseñas."""

    stars_distribution = _execute_query("""
        SELECT stars, DATE_FORMAT(created_at, '%Y-%m-%d') as fecha, COUNT(*) as cantidad
        FROM reviews
        WHERE created_at BETWEEN %s AND %s
        GROUP BY stars
        ORDER BY DATE(created_at)
    """, (inicio, fin))

    average_evolution = _execute_query("""
        SELECT DATE_FORMAT(created_at, '%Y-%m-%d') as fecha, ROUND(AVG(stars), 2) as promedio
        FROM reviews
        WHERE created_at BETWEEN %s AND %s
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
    """, (inicio, fin))

    count_by_period = _execute_query("""
        SELECT DATE_FORMAT(created_at, '%Y-%m-%d') as fecha, COUNT(*) as cantidad
        FROM reviews
        WHERE created_at BETWEEN %s AND %s
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
    """, (inicio, fin))

    recent = _execute_query("""
        SELECT u.name, r.stars, r.description, r.created_at
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.created_at BETWEEN %s AND %s
        ORDER BY r.created_at DESC
        LIMIT 5
    """, (inicio, fin))

    return {
        "stars_distribution": stars_distribution,
        "average_evolution":  average_evolution,
        "count_by_period":    count_by_period,
        "recent":             recent,
    }