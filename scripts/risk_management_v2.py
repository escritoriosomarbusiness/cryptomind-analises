#!/usr/bin/env python3
"""
CryptoMind IA - Gestão de Risco v2.0
Sistema de gestão de risco profissional para day trade e scalp

Regras Fundamentais:
1. Risco Real = SL% × Alavancagem DEVE ser < 15%
2. Exposição máxima simultânea: 5% da banca
3. SL calculado do PIOR ponto de entrada
4. Range de entrada máximo: 0.5%
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    """Níveis de risco"""
    LOW = "Baixo"
    MEDIUM = "Médio"
    HIGH = "Alto"
    REJECTED = "Rejeitado"


@dataclass
class RiskValidation:
    """Resultado da validação de risco"""
    is_valid: bool
    real_risk_pct: float
    risk_level: RiskLevel
    warnings: List[str]
    rejection_reason: Optional[str] = None


class RiskManagerV2:
    """Gerenciador de risco profissional"""
    
    # Limites de risco
    MAX_REAL_RISK_PCT = 15.0  # Risco real máximo por operação
    MAX_EXPOSURE_PCT = 5.0    # Exposição máxima simultânea
    MAX_ENTRY_RANGE_PCT = 0.5 # Range de entrada máximo
    
    # Parâmetros por Trading System
    TS_RISK_PARAMS = {
        'TS1': {  # Rompimento
            'name': 'Rompimento',
            'risk_per_trade': 2.0,
            'leverage': 10,
            'sl_range': (0.5, 1.0),
            'ideal_sl': 0.75,
            'max_entry_range': 0.3,
            'min_rr': 2.0
        },
        'TS2': {  # Continuação
            'name': 'Continuação',
            'risk_per_trade': 3.0,
            'leverage': 7,
            'sl_range': (0.8, 1.5),
            'ideal_sl': 1.0,
            'max_entry_range': 0.5,
            'min_rr': 1.5
        },
        'TS3': {  # Reversão
            'name': 'Reversão',
            'risk_per_trade': 1.0,
            'leverage': 5,
            'sl_range': (1.0, 2.0),
            'ideal_sl': 1.5,
            'max_entry_range': 0.3,
            'min_rr': 4.0
        }
    }
    
    def __init__(self, account_balance: float = 10000.0):
        """
        Inicializa o gerenciador de risco
        
        Args:
            account_balance: Saldo da conta em USD
        """
        self.account_balance = account_balance
        self.open_positions: List[Dict] = []
    
    def validate_setup(self, setup: Dict) -> RiskValidation:
        """
        Valida um setup quanto ao risco
        
        Args:
            setup: Dicionário com dados do setup
            
        Returns:
            RiskValidation com resultado da validação
        """
        warnings = []
        
        ts = setup.get('ts', 'TS1')
        params = self.TS_RISK_PARAMS.get(ts, self.TS_RISK_PARAMS['TS1'])
        
        # 1. Validar range de entrada
        entry_range_pct = setup.get('entry_range_pct', 0)
        if entry_range_pct > params['max_entry_range']:
            return RiskValidation(
                is_valid=False,
                real_risk_pct=0,
                risk_level=RiskLevel.REJECTED,
                warnings=[],
                rejection_reason=f"Range de entrada ({entry_range_pct:.2f}%) excede máximo permitido ({params['max_entry_range']}%)"
            )
        
        # 2. Validar SL
        sl_pct = setup.get('sl_pct', 0)
        sl_min, sl_max = params['sl_range']
        
        if sl_pct < sl_min:
            warnings.append(f"SL muito curto ({sl_pct:.2f}%), pode ser stopado por ruído")
        elif sl_pct > sl_max:
            warnings.append(f"SL muito longo ({sl_pct:.2f}%), considere reduzir alavancagem")
        
        # 3. Calcular e validar risco real
        leverage = setup.get('leverage', params['leverage'])
        real_risk_pct = sl_pct * leverage
        
        if real_risk_pct > self.MAX_REAL_RISK_PCT:
            return RiskValidation(
                is_valid=False,
                real_risk_pct=real_risk_pct,
                risk_level=RiskLevel.REJECTED,
                warnings=[],
                rejection_reason=f"Risco real ({real_risk_pct:.1f}%) excede máximo permitido ({self.MAX_REAL_RISK_PCT}%)"
            )
        
        # 4. Validar R:R
        targets = setup.get('targets', [])
        if targets:
            first_target = targets[0]
            if first_target.get('r', 0) != 'trailing':
                rr = first_target.get('r', 0)
                if rr < params['min_rr']:
                    warnings.append(f"R:R ({rr}) abaixo do ideal ({params['min_rr']}) para {params['name']}")
        
        # 5. Verificar exposição total
        current_exposure = self._calculate_current_exposure()
        new_exposure = setup.get('risk_per_trade', params['risk_per_trade'])
        total_exposure = current_exposure + new_exposure
        
        if total_exposure > self.MAX_EXPOSURE_PCT:
            warnings.append(f"Exposição total ({total_exposure:.1f}%) próxima do limite ({self.MAX_EXPOSURE_PCT}%)")
        
        # Determinar nível de risco
        if real_risk_pct <= 8:
            risk_level = RiskLevel.LOW
        elif real_risk_pct <= 12:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.HIGH
        
        return RiskValidation(
            is_valid=True,
            real_risk_pct=real_risk_pct,
            risk_level=risk_level,
            warnings=warnings
        )
    
    def _calculate_current_exposure(self) -> float:
        """Calcula exposição atual em operações abertas"""
        return sum(pos.get('risk_per_trade', 0) for pos in self.open_positions)
    
    def calculate_position_size(self, setup: Dict) -> Dict:
        """
        Calcula tamanho da posição baseado no risco
        
        Args:
            setup: Dicionário com dados do setup
            
        Returns:
            Dicionário com tamanho da posição e valores
        """
        ts = setup.get('ts', 'TS1')
        params = self.TS_RISK_PARAMS.get(ts, self.TS_RISK_PARAMS['TS1'])
        
        risk_per_trade = setup.get('risk_per_trade', params['risk_per_trade'])
        sl_pct = setup.get('sl_pct', params['ideal_sl'])
        leverage = setup.get('leverage', params['leverage'])
        entry_price = (setup.get('entry_low', 0) + setup.get('entry_high', 0)) / 2
        
        # Valor em risco
        risk_amount = self.account_balance * (risk_per_trade / 100)
        
        # Tamanho da posição
        # risk_amount = position_size * sl_pct / 100
        position_size = risk_amount / (sl_pct / 100)
        
        # Margem necessária
        margin_required = position_size / leverage
        
        # Quantidade do ativo
        quantity = position_size / entry_price if entry_price > 0 else 0
        
        return {
            'risk_amount': round(risk_amount, 2),
            'position_size': round(position_size, 2),
            'margin_required': round(margin_required, 2),
            'quantity': round(quantity, 6),
            'leverage': leverage,
            'entry_price': round(entry_price, 2)
        }
    
    def calculate_sl_from_worst_entry(self, entry_high: float, entry_low: float,
                                       sl_pct: float, direction: str) -> Tuple[float, float]:
        """
        Calcula SL a partir do pior ponto de entrada
        
        Para LONG: pior entrada é entry_high, SL abaixo
        Para SHORT: pior entrada é entry_low, SL acima
        
        Returns:
            Tuple (sl_price, actual_sl_pct)
        """
        if direction == 'LONG':
            worst_entry = entry_high
            sl_price = worst_entry * (1 - sl_pct / 100)
            actual_sl_pct = (worst_entry - sl_price) / worst_entry * 100
        else:
            worst_entry = entry_low
            sl_price = worst_entry * (1 + sl_pct / 100)
            actual_sl_pct = (sl_price - worst_entry) / worst_entry * 100
        
        return round(sl_price, 2), round(actual_sl_pct, 2)
    
    def calculate_targets_from_risk(self, entry_price: float, sl_price: float,
                                     direction: str, ts: str) -> List[Dict]:
        """
        Calcula alvos baseados no risco (R)
        
        Args:
            entry_price: Preço médio de entrada
            sl_price: Preço do stop loss
            direction: 'LONG' ou 'SHORT'
            ts: Trading System (TS1, TS2, TS3)
            
        Returns:
            Lista de alvos com preços e percentuais
        """
        risk = abs(entry_price - sl_price)
        
        # Parciais por TS
        partials_config = {
            'TS1': [
                {'r': 2.0, 'size': 50, 'action': 'Realizar 50%, SL → entrada, ativar trailing 1%'},
                {'r': 3.0, 'size': 30, 'action': 'Realizar 30%'},
                {'r': 'trailing', 'size': 20, 'action': 'Trailing stop 1%'}
            ],
            'TS2': [
                {'r': 1.5, 'size': 60, 'action': 'Realizar 60%, SL → entrada, ativar trailing 0.8%'},
                {'r': 2.5, 'size': 30, 'action': 'Realizar 30%'},
                {'r': 'trailing', 'size': 10, 'action': 'Trailing stop 0.8%'}
            ],
            'TS3': [
                {'r': 2.0, 'size': 40, 'action': 'Realizar 40%, SL → entrada'},
                {'r': 4.0, 'size': 30, 'action': 'Realizar 30%, ativar trailing 1.5%'},
                {'r': 'trailing', 'size': 30, 'action': 'Trailing stop 1.5%'}
            ]
        }
        
        partials = partials_config.get(ts, partials_config['TS1'])
        targets = []
        
        for partial in partials:
            if partial['r'] == 'trailing':
                targets.append({
                    'price': 'Trailing',
                    'r': 'Trailing',
                    'pct_from_entry': None,
                    'size_pct': partial['size'],
                    'action': partial['action']
                })
            else:
                if direction == 'LONG':
                    target_price = entry_price + (risk * partial['r'])
                else:
                    target_price = entry_price - (risk * partial['r'])
                
                pct_from_entry = abs(target_price - entry_price) / entry_price * 100
                
                targets.append({
                    'price': round(target_price, 2),
                    'r': partial['r'],
                    'pct_from_entry': round(pct_from_entry, 2),
                    'size_pct': partial['size'],
                    'action': partial['action']
                })
        
        return targets
    
    def generate_risk_summary(self, setup: Dict) -> str:
        """Gera resumo de risco para exibição"""
        validation = self.validate_setup(setup)
        position = self.calculate_position_size(setup)
        
        lines = [
            "⚙️ **Gestão de Risco**",
            "",
            f"• Risco por operação: {setup.get('risk_per_trade', 2)}% da banca",
            f"• Valor em risco: ${position['risk_amount']:,.2f}",
            f"• Tamanho da posição: ${position['position_size']:,.2f}",
            f"• Margem necessária: ${position['margin_required']:,.2f}",
            f"• Alavancagem: {position['leverage']}x",
            f"• Risco Real: {validation.real_risk_pct:.1f}% ({validation.risk_level.value})",
            ""
        ]
        
        if validation.warnings:
            lines.append("⚠️ **Avisos:**")
            for warning in validation.warnings:
                lines.append(f"   • {warning}")
        
        return "\n".join(lines)


def test_risk_manager():
    """Testa o gerenciador de risco"""
    rm = RiskManagerV2(account_balance=10000)
    
    # Setup válido
    valid_setup = {
        'ts': 'TS1',
        'direction': 'LONG',
        'entry_low': 95000,
        'entry_high': 95285,
        'entry_range_pct': 0.30,
        'sl_pct': 0.75,
        'leverage': 10,
        'risk_per_trade': 2.0,
        'targets': [{'r': 2.0}, {'r': 3.0}]
    }
    
    # Setup inválido (range muito grande)
    invalid_range = {
        'ts': 'TS1',
        'entry_range_pct': 2.5,
        'sl_pct': 0.75,
        'leverage': 10
    }
    
    # Setup inválido (risco real muito alto)
    invalid_risk = {
        'ts': 'TS1',
        'entry_range_pct': 0.3,
        'sl_pct': 6.0,
        'leverage': 10
    }
    
    print("=" * 60)
    print("RISK MANAGER V2.0 - TESTE")
    print("=" * 60)
    
    print("\n1. Setup Válido:")
    result = rm.validate_setup(valid_setup)
    print(f"   Válido: {result.is_valid}")
    print(f"   Risco Real: {result.real_risk_pct:.1f}%")
    print(f"   Nível: {result.risk_level.value}")
    if result.warnings:
        print(f"   Avisos: {result.warnings}")
    
    position = rm.calculate_position_size(valid_setup)
    print(f"\n   Posição calculada:")
    print(f"   - Valor em risco: ${position['risk_amount']}")
    print(f"   - Tamanho posição: ${position['position_size']}")
    print(f"   - Margem: ${position['margin_required']}")
    
    print("\n2. Setup com Range Inválido:")
    result = rm.validate_setup(invalid_range)
    print(f"   Válido: {result.is_valid}")
    print(f"   Motivo: {result.rejection_reason}")
    
    print("\n3. Setup com Risco Inválido:")
    result = rm.validate_setup(invalid_risk)
    print(f"   Válido: {result.is_valid}")
    print(f"   Risco Real: {result.real_risk_pct:.1f}%")
    print(f"   Motivo: {result.rejection_reason}")
    
    print("\n4. Cálculo de Alvos (TS1 LONG):")
    targets = rm.calculate_targets_from_risk(
        entry_price=95142.50,
        sl_price=94428.50,
        direction='LONG',
        ts='TS1'
    )
    for i, t in enumerate(targets, 1):
        if t['price'] == 'Trailing':
            print(f"   Alvo {i}: Trailing Stop → {t['size_pct']}%")
        else:
            print(f"   Alvo {i}: ${t['price']:,.2f} ({t['r']}R, +{t['pct_from_entry']:.2f}%) → {t['size_pct']}%")


if __name__ == "__main__":
    test_risk_manager()
