#!/usr/bin/env python3
"""
CryptoMind IA - Sistema de Gestão de Risco
==========================================
Implementa gestão de risco diferenciada por tipo de Trading System.
Inclui cálculo de parciais, trailing stop e exposição máxima.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class TSType(Enum):
    """Tipos de Trading Systems."""
    TS1 = "TS1"  # Rompimento
    TS2 = "TS2"  # Continuação
    TS3 = "TS3"  # Reversão


@dataclass
class RiskConfig:
    """Configuração de risco por TS."""
    ts_type: TSType
    name: str
    color: str
    risk_percent: float      # % da banca por operação
    max_leverage: int        # Alavancagem máxima
    min_rr: float           # Risco/Retorno mínimo
    expected_winrate: str   # Taxa de acerto esperada
    
    # Parciais
    partial_1_target_rr: float  # R:R para primeira parcial
    partial_1_size: float       # % da posição
    partial_2_target_rr: float  # R:R para segunda parcial
    partial_2_size: float       # % da posição
    
    # Trailing
    trailing_activation_rr: float  # R:R para ativar trailing
    trailing_percent: float        # % do trailing stop


# Configurações de risco por TS
RISK_CONFIGS = {
    TSType.TS1: RiskConfig(
        ts_type=TSType.TS1,
        name="Rompimento",
        color="#3B82F6",  # Azul
        risk_percent=2.0,
        max_leverage=10,
        min_rr=2.0,
        expected_winrate="45-55%",
        partial_1_target_rr=2.0,
        partial_1_size=50,
        partial_2_target_rr=3.0,
        partial_2_size=30,
        trailing_activation_rr=2.0,
        trailing_percent=1.0
    ),
    TSType.TS2: RiskConfig(
        ts_type=TSType.TS2,
        name="Continuação",
        color="#22C55E",  # Verde
        risk_percent=3.0,
        max_leverage=7,
        min_rr=1.5,
        expected_winrate="55-65%",
        partial_1_target_rr=1.5,
        partial_1_size=60,
        partial_2_target_rr=2.5,
        partial_2_size=30,
        trailing_activation_rr=1.5,
        trailing_percent=0.8
    ),
    TSType.TS3: RiskConfig(
        ts_type=TSType.TS3,
        name="Reversão",
        color="#F97316",  # Laranja
        risk_percent=1.0,
        max_leverage=5,
        min_rr=4.0,
        expected_winrate="30-40%",
        partial_1_target_rr=4.0,
        partial_1_size=40,
        partial_2_target_rr=6.0,
        partial_2_size=30,
        trailing_activation_rr=4.0,
        trailing_percent=1.5
    )
}

# Exposição máxima total
MAX_TOTAL_EXPOSURE = 5.0  # 5% da banca em risco simultâneo


@dataclass
class PartialOrder:
    """Representa uma ordem de parcial."""
    target_price: float
    size_percent: float
    rr_ratio: float
    action: str  # "REALIZAR" ou "TRAILING"


@dataclass
class RiskPlan:
    """Plano completo de gestão de risco para um setup."""
    symbol: str
    direction: str
    ts_type: str
    ts_name: str
    color: str
    
    # Entrada
    entry_min: float
    entry_max: float
    entry_avg: float
    
    # Stop Loss
    stop_loss: float
    stop_distance_percent: float
    
    # Gestão
    risk_percent: float
    max_leverage: int
    suggested_leverage: int
    
    # Parciais
    partials: List[Dict]
    
    # Trailing
    trailing_activation: float
    trailing_percent: float
    
    # Métricas
    risk_reward: float
    expected_winrate: str
    
    def to_dict(self) -> Dict:
        """Converte para dicionário."""
        return {
            'symbol': self.symbol,
            'direction': self.direction,
            'ts_type': self.ts_type,
            'ts_name': self.ts_name,
            'color': self.color,
            'entry': {
                'min': self.entry_min,
                'max': self.entry_max,
                'avg': self.entry_avg
            },
            'stop_loss': {
                'price': self.stop_loss,
                'distance_percent': self.stop_distance_percent
            },
            'risk_management': {
                'risk_percent': self.risk_percent,
                'max_leverage': self.max_leverage,
                'suggested_leverage': self.suggested_leverage,
                'max_exposure': MAX_TOTAL_EXPOSURE
            },
            'partials': self.partials,
            'trailing': {
                'activation_price': self.trailing_activation,
                'percent': self.trailing_percent
            },
            'metrics': {
                'risk_reward': self.risk_reward,
                'expected_winrate': self.expected_winrate
            }
        }


class RiskManager:
    """Gerenciador de risco para setups."""
    
    def __init__(self, setup: Dict):
        """
        Inicializa o gerenciador.
        
        Args:
            setup: Dicionário com dados do setup
        """
        self.setup = setup
        self.ts_type = TSType(setup.get('ts_type', 'TS1'))
        self.config = RISK_CONFIGS[self.ts_type]
        self.direction = setup.get('direction', 'LONG')
        self.is_long = self.direction == 'LONG'
    
    def create_risk_plan(self) -> RiskPlan:
        """Cria plano completo de gestão de risco."""
        entry_zone = self.setup.get('entry_zone', {})
        entry_min = entry_zone.get('min', 0)
        entry_max = entry_zone.get('max', 0)
        entry_avg = (entry_min + entry_max) / 2
        
        stop_loss = self.setup.get('stop_loss', 0)
        
        # Calcular distância do stop
        if self.is_long:
            stop_distance = (entry_avg - stop_loss) / entry_avg * 100
        else:
            stop_distance = (stop_loss - entry_avg) / entry_avg * 100
        
        # Calcular alavancagem sugerida baseada no stop
        # Regra: risco máximo = risk_percent, então leverage = risk_percent / stop_distance
        if stop_distance > 0:
            suggested_leverage = min(
                int(self.config.risk_percent / stop_distance * 100),
                self.config.max_leverage
            )
        else:
            suggested_leverage = 1
        
        suggested_leverage = max(1, suggested_leverage)
        
        # Calcular parciais
        partials = self._calculate_partials(entry_avg, stop_loss)
        
        # Calcular preço de ativação do trailing
        risk = abs(entry_avg - stop_loss)
        if self.is_long:
            trailing_activation = entry_avg + (risk * self.config.trailing_activation_rr)
        else:
            trailing_activation = entry_avg - (risk * self.config.trailing_activation_rr)
        
        # Calcular R:R
        targets = self.setup.get('targets', [])
        if targets and risk > 0:
            first_target = targets[0]
            if self.is_long:
                rr = (first_target - entry_avg) / risk
            else:
                rr = (entry_avg - first_target) / risk
        else:
            rr = self.config.min_rr
        
        return RiskPlan(
            symbol=self.setup.get('symbol', ''),
            direction=self.direction,
            ts_type=self.ts_type.value,
            ts_name=self.config.name,
            color=self.config.color,
            entry_min=round(entry_min, 2),
            entry_max=round(entry_max, 2),
            entry_avg=round(entry_avg, 2),
            stop_loss=round(stop_loss, 2),
            stop_distance_percent=round(stop_distance, 2),
            risk_percent=self.config.risk_percent,
            max_leverage=self.config.max_leverage,
            suggested_leverage=suggested_leverage,
            partials=partials,
            trailing_activation=round(trailing_activation, 2),
            trailing_percent=self.config.trailing_percent,
            risk_reward=round(rr, 2),
            expected_winrate=self.config.expected_winrate
        )
    
    def _calculate_partials(self, entry: float, stop: float) -> List[Dict]:
        """Calcula os níveis de parciais."""
        partials = []
        risk = abs(entry - stop)
        
        # Parcial 1
        if self.is_long:
            target_1 = entry + (risk * self.config.partial_1_target_rr)
        else:
            target_1 = entry - (risk * self.config.partial_1_target_rr)
        
        partials.append({
            'number': 1,
            'target_price': round(target_1, 2),
            'size_percent': self.config.partial_1_size,
            'rr_ratio': self.config.partial_1_target_rr,
            'action': 'REALIZAR',
            'after_action': [
                'Subir stop para entrada (breakeven)',
                f'Ativar trailing stop de {self.config.trailing_percent}%'
            ]
        })
        
        # Parcial 2
        if self.is_long:
            target_2 = entry + (risk * self.config.partial_2_target_rr)
        else:
            target_2 = entry - (risk * self.config.partial_2_target_rr)
        
        partials.append({
            'number': 2,
            'target_price': round(target_2, 2),
            'size_percent': self.config.partial_2_size,
            'rr_ratio': self.config.partial_2_target_rr,
            'action': 'REALIZAR',
            'after_action': [
                'Manter trailing stop ativo'
            ]
        })
        
        # Restante (trailing)
        remaining = 100 - self.config.partial_1_size - self.config.partial_2_size
        partials.append({
            'number': 3,
            'target_price': 'TRAILING',
            'size_percent': remaining,
            'rr_ratio': 'VARIÁVEL',
            'action': 'TRAILING STOP',
            'after_action': [
                f'Deixar trailing de {self.config.trailing_percent}% até ser stopado'
            ]
        })
        
        return partials


def calculate_position_size(account_balance: float, risk_percent: float, 
                           entry_price: float, stop_loss: float,
                           leverage: int = 1) -> Dict:
    """
    Calcula o tamanho da posição baseado no risco.
    
    Args:
        account_balance: Saldo da conta
        risk_percent: % de risco por operação
        entry_price: Preço de entrada
        stop_loss: Preço do stop loss
        leverage: Alavancagem
    
    Returns:
        Dicionário com detalhes da posição
    """
    # Valor em risco
    risk_amount = account_balance * (risk_percent / 100)
    
    # Distância do stop em %
    stop_distance_percent = abs(entry_price - stop_loss) / entry_price * 100
    
    # Tamanho da posição sem alavancagem
    if stop_distance_percent > 0:
        position_size_base = risk_amount / (stop_distance_percent / 100)
    else:
        position_size_base = 0
    
    # Tamanho com alavancagem
    position_size = position_size_base
    margin_required = position_size / leverage
    
    # Quantidade do ativo
    quantity = position_size / entry_price
    
    return {
        'account_balance': account_balance,
        'risk_percent': risk_percent,
        'risk_amount': round(risk_amount, 2),
        'stop_distance_percent': round(stop_distance_percent, 2),
        'position_size': round(position_size, 2),
        'margin_required': round(margin_required, 2),
        'leverage': leverage,
        'quantity': round(quantity, 6),
        'entry_price': entry_price,
        'stop_loss': stop_loss
    }


def check_exposure_limit(current_exposure: float, new_risk: float) -> Tuple[bool, str]:
    """
    Verifica se a nova operação excede o limite de exposição.
    
    Args:
        current_exposure: Exposição atual em %
        new_risk: Risco da nova operação em %
    
    Returns:
        Tuple com (pode_operar, mensagem)
    """
    total_exposure = current_exposure + new_risk
    
    if total_exposure > MAX_TOTAL_EXPOSURE:
        return False, f"Exposição total ({total_exposure:.1f}%) excede limite de {MAX_TOTAL_EXPOSURE}%"
    
    remaining = MAX_TOTAL_EXPOSURE - total_exposure
    return True, f"Exposição total: {total_exposure:.1f}% (restante: {remaining:.1f}%)"


def format_risk_plan_for_display(risk_plan: RiskPlan) -> str:
    """
    Formata o plano de risco para exibição.
    
    Args:
        risk_plan: Plano de risco
    
    Returns:
        String formatada
    """
    lines = []
    
    # Cabeçalho
    emoji = "🟦" if risk_plan.ts_type == "TS1" else "🟩" if risk_plan.ts_type == "TS2" else "🟧"
    lines.append(f"{emoji} {risk_plan.direction} {risk_plan.symbol} - {risk_plan.ts_name}")
    lines.append("")
    
    # Entrada
    lines.append(f"📍 Entrada: ${risk_plan.entry_min:.2f} - ${risk_plan.entry_max:.2f}")
    lines.append(f"🛑 Stop Loss: ${risk_plan.stop_loss:.2f} ({risk_plan.stop_distance_percent:.2f}%)")
    lines.append("")
    
    # Gestão
    lines.append("⚙️ Gestão de Risco:")
    lines.append(f"   • Risco: {risk_plan.risk_percent}% da banca")
    lines.append(f"   • Alavancagem sugerida: {risk_plan.suggested_leverage}x (máx: {risk_plan.max_leverage}x)")
    lines.append(f"   • R:R: {risk_plan.risk_reward:.1f}")
    lines.append("")
    
    # Parciais
    lines.append("📊 Plano de Parciais:")
    for p in risk_plan.partials:
        if p['target_price'] == 'TRAILING':
            lines.append(f"   {p['number']}. Trailing Stop ({p['size_percent']:.0f}%)")
        else:
            lines.append(f"   {p['number']}. ${p['target_price']:.2f} ({p['rr_ratio']}R) → Realizar {p['size_percent']:.0f}%")
        for action in p.get('after_action', []):
            lines.append(f"      └─ {action}")
    
    lines.append("")
    lines.append(f"📈 Taxa de acerto esperada: {risk_plan.expected_winrate}")
    
    return "\n".join(lines)


# Teste do módulo
if __name__ == "__main__":
    # Setup de teste
    test_setup = {
        'symbol': 'BTC',
        'ts_type': 'TS1',
        'direction': 'LONG',
        'entry_zone': {'min': 90000, 'max': 90500},
        'stop_loss': 88000,
        'targets': [93000, 95000, 97000]
    }
    
    print("=" * 60)
    print("CryptoMind IA - Sistema de Gestão de Risco")
    print("=" * 60)
    
    # Criar plano de risco
    manager = RiskManager(test_setup)
    plan = manager.create_risk_plan()
    
    # Exibir plano formatado
    print(format_risk_plan_for_display(plan))
    
    print("\n" + "=" * 60)
    print("Cálculo de Tamanho de Posição")
    print("=" * 60)
    
    # Calcular tamanho da posição
    position = calculate_position_size(
        account_balance=10000,
        risk_percent=plan.risk_percent,
        entry_price=plan.entry_avg,
        stop_loss=plan.stop_loss,
        leverage=plan.suggested_leverage
    )
    
    print(f"Saldo da conta: ${position['account_balance']:.2f}")
    print(f"Risco: {position['risk_percent']}% = ${position['risk_amount']:.2f}")
    print(f"Tamanho da posição: ${position['position_size']:.2f}")
    print(f"Margem necessária: ${position['margin_required']:.2f}")
    print(f"Quantidade: {position['quantity']:.6f} BTC")
    
    print("\n" + "=" * 60)
    print("Verificação de Exposição")
    print("=" * 60)
    
    # Verificar exposição
    can_trade, msg = check_exposure_limit(current_exposure=2.0, new_risk=plan.risk_percent)
    print(f"Pode operar: {can_trade}")
    print(f"Mensagem: {msg}")
    
    print("\n✅ Sistema de gestão de risco funcionando")
