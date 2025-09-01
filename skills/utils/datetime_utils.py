from datetime import datetime, date, time
from typing import Optional, Union
from zoneinfo import ZoneInfo

# Timezone de São Paulo (Capital)
TZ_SAO_PAULO = ZoneInfo("America/Sao_Paulo")

def now_sp() -> datetime:
    """Retorna o datetime atual no timezone de São Paulo."""
    return datetime.now(TZ_SAO_PAULO)

def today_sp_start() -> datetime:
    """Retorna o início do dia atual (00:00) no timezone de São Paulo."""
    n = now_sp()
    return n.replace(hour=0, minute=0, second=0, microsecond=0)

def to_sp_aware(dt: datetime) -> datetime:
    """Converte um datetime para timezone de São Paulo, preservando a hora local.
    - Se for naive, assume que já está em horário de São Paulo.
    - Se tiver tz, converte para America/Sao_Paulo.
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=TZ_SAO_PAULO)
    return dt.astimezone(TZ_SAO_PAULO)

def ensure_sp_aware(value: Union[str, date, datetime, None]) -> Optional[datetime]:
    """Converte diferentes tipos de entrada para datetime timezone-aware em São Paulo.
    Suporta strings especiais: "today"/"hoje" e "now"/"agora".
    Também aceita ISO 8601 (YYYY-MM-DD e YYYY-MM-DDTHH:MM[:SS][Z|±HH:MM]).
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return to_sp_aware(value)
    if isinstance(value, date):
        return datetime.combine(value, time.min, tzinfo=TZ_SAO_PAULO)
    if isinstance(value, str):
        s = value.strip()
        lower = s.lower()
        if lower in {"today", "hoje"}:
            return today_sp_start()
        if lower in {"now", "agora"}:
            return now_sp()
        # Tenta datetime ISO primeiro (aceita sufixo Z)
        try:
            iso = s.replace("Z", "+00:00")
            dt = datetime.fromisoformat(iso)
            return to_sp_aware(dt)
        except ValueError:
            # Tenta apenas data (YYYY-MM-DD)
            try:
                d = date.fromisoformat(s)
                return datetime.combine(d, time.min, tzinfo=TZ_SAO_PAULO)
            except ValueError as e:
                raise ValueError(f"Invalid date/datetime string: {value}") from e
    raise TypeError("Unsupported type for date/datetime conversion")

def isoformat_sp(value: Union[str, date, datetime, None]) -> Optional[str]:
    """Retorna string ISO 8601 no timezone de São Paulo para o valor fornecido."""
    dt = ensure_sp_aware(value)
    return dt.isoformat() if dt is not None else None
