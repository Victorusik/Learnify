from datetime import datetime, timedelta
from typing import Optional, Tuple


def calculate_next_review(
    last_review: Optional[datetime],
    next_review: Optional[datetime],
    interval: int,
    ease_factor: float,
    is_correct: bool
) -> Tuple[datetime, int, float]:
    """
    Рассчитывает следующее повторение на основе алгоритма spaced repetition.
    Интервалы: 1, 7, 16, 35 дней
    """
    now = datetime.utcnow()
    
    if not last_review:
        # Первое повторение
        new_interval = 1
        new_ease_factor = 2.5
    else:
        new_interval = interval
        new_ease_factor = ease_factor or 2.5
        
        if is_correct:
            # Увеличиваем интервал
            new_interval = int(new_interval * new_ease_factor)
            new_ease_factor = min(new_ease_factor + 0.1, 2.5)
        else:
            # Уменьшаем интервал при ошибке
            new_interval = max(1, int(new_interval / 2))
            new_ease_factor = max(1.3, new_ease_factor - 0.2)
    
    # Ограничиваем интервалы: 1, 7, 16, 35 дней
    intervals = [1, 7, 16, 35]
    closest_interval = min(intervals, key=lambda x: abs(x - new_interval))
    new_interval = closest_interval
    
    next_review_date = now + timedelta(days=new_interval)
    
    return next_review_date, new_interval, new_ease_factor

