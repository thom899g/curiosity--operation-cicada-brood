"""
Configuration and constants for Operation CICADA BROOD
"""
from datetime import timedelta
from typing import Dict, List, Optional
import os

# Daemon lifecycle
DAEMON_LIFETIME_HOURS = (24, 48)  # Min, max lifetime
CYCLE_INTERVAL_MINUTES = 5  # How often daemons analyze/trade

# Capital management
POOLED_CAPITAL_USDT = 1000.0  # Total pool
DAEMON_CAPITAL_MIN = 10.0     # Minimum per daemon
DAEMON_CAPITAL_MAX = 100.0    # Maximum per daemon

# Micro-cap exchange selection
MICROCAP_EXCHANGES = ['kucoin', 'gate.io', 'mexc', 'bitmart', 'huobi']
MIN_DAILY_VOLUME_USDT = 1000
MAX_DAILY_VOLUME_USDT = 50000

# Trading parameters
MAX_POSITION_SIZE = 0.1  # 10% of daily volume
SLIPPAGE_TOLERANCE = 0.02  # 2% max slippage
MAX_ACTIVE_DAEMONS = 10

# Firebase configuration
FIREBASE_COLLECTIONS = {
    'daemons': 'cicada_daemons',
    'findings': 'cicada_findings',
    'transactions': 'cicada_transactions',
    'system_state': 'cicada_system_state'
}

# Risk parameters
MAX_DRAWDOWN_PERCENT = 5.0
STOP_LOSS_PERCENT = 3.0
TAKE_PROFIT_PERCENT = 5.0

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"