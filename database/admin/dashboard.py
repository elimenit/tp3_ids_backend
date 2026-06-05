from utils.helpers import _execute_query

def db_get_reservations_dashboard(inicio: str, fin: str) -> dict:
    """Retorna todos los datos necesarios para el dashboard de reservas."""

    by_period = _execute_query("""
        SELECT DATE(created_at) as fecha, COUNT(*) as cantidad
        FROM reservations
        WHERE created_at BETWEEN %s AND %s
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
    """, (inicio, fin))

    by_status = _execute_query("""
        SELECT 
            CASE 
                WHEN status_reservation = 'Confirmed' 
                     AND reservation_datetime < NOW() THEN 'NoShow'
                ELSE status_reservation 
            END as estado,
            DATE(created_at) as fecha,
            COUNT(*) as cantidad
        FROM reservations
        WHERE created_at BETWEEN %s AND %s
        GROUP BY estado, DATE(created_at)
        ORDER BY DATE(created_at)
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
            DATE(reservation_datetime) as fecha,
            COUNT(*) as cantidad
        FROM reservations
        WHERE reservation_datetime BETWEEN %s AND %s
        GROUP BY dia, DATE(reservation_datetime)
        ORDER BY fecha
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
        SELECT DATE(d.delivery_datetime) as fecha, SUM(dm.quantity * dm.unit_price) as ingresos
        FROM deliveries d
        JOIN deliveries_menus dm ON d.id = dm.delivery_id
        WHERE d.delivery_datetime BETWEEN %s AND %s AND d.status = 'delivered'
        GROUP BY DATE(d.delivery_datetime)
        ORDER BY DATE(d.delivery_datetime)
    """, (inicio, fin))

    top_products = _execute_query("""
        SELECT m.name, DATE(d.delivery_datetime) as fecha, SUM(dm.quantity) as total_vendido
        FROM deliveries_menus dm
        JOIN menus m ON dm.menu_id = m.id
        JOIN deliveries d ON dm.delivery_id = d.id
        WHERE d.delivery_datetime BETWEEN %s AND %s
        GROUP BY m.id, m.name, DATE(d.delivery_datetime)
        ORDER BY DATE(d.delivery_datetime)
    """, (inicio, fin))

    by_hour = _execute_query("""
        SELECT HOUR(delivery_datetime) as hora, DATE(delivery_datetime) as fecha, COUNT(*) as cantidad
        FROM deliveries
        WHERE delivery_datetime BETWEEN %s AND %s
        GROUP BY hora, DATE(delivery_datetime)
        ORDER BY fecha
    """, (inicio, fin))

    by_status = _execute_query("""
        SELECT status, DATE(delivery_datetime) as fecha, COUNT(*) as cantidad
        FROM deliveries
        WHERE delivery_datetime BETWEEN %s AND %s
        GROUP BY status, DATE(delivery_datetime)
        ORDER BY fecha
    """, (inicio, fin))

    return {
        "income":       income,
        "top_products": top_products,
        "by_hour":      by_hour,
        "by_status":    by_status,
    }

def db_get_reviews_dashboard(inicio: str, fin: str) -> dict:
    """Retorna todos los datos necesarios para el dashboard de reseñas."""

    stars_distribution = _execute_query("""
        SELECT stars, DATE(created_at) as fecha, COUNT(*) as cantidad
        FROM reviews
        WHERE created_at BETWEEN %s AND %s
        GROUP BY stars, DATE(created_at)
        ORDER BY DATE(created_at)
    """, (inicio, fin))

    average_evolution = _execute_query("""
        SELECT DATE(created_at) as fecha, ROUND(AVG(stars), 2) as promedio
        FROM reviews
        WHERE created_at BETWEEN %s AND %s
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
    """, (inicio, fin))

    count_by_period = _execute_query("""
        SELECT DATE(created_at) as fecha, COUNT(*) as cantidad
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
        LIMIT 20
    """, (inicio, fin))

    return {
        "stars_distribution": stars_distribution,
        "average_evolution":  average_evolution,
        "count_by_period":    count_by_period,
        "recent":             recent,
    }