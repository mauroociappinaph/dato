"""
MCP Cost Controller
Manages quotas and rate limiting for premium MCP servers.
"""

import os
import json
import logging
from typing import Dict, Optional
from datetime import datetime, date
from pathlib import Path

# Import redis_infra from infrastructure-core
import sys
sys.path.append(str(Path(__file__).parent.parent.parent / 'infrastructure-core' / 'scripts'))
from redis_infra import increment_counter, get_counter, cache_set, cache_get

logger = logging.getLogger(__name__)


class MCPCostController:
    """
    Manages quotas and rate limiting for MCP servers.
    Uses Redis for distributed tracking.
    """

    # Premium servers with multi-level costs and limits
    PREMIUM_SERVERS = {
        'exa': {
            'cost_per_call': 0.01,
            'global_daily_limit': 10000,
            'tenant_daily_limit': 1000,
            'agent_daily_limit': 100
        },
        'gemini-vision': {
            'cost_per_call': 0.05,
            'global_daily_limit': 5000,
            'tenant_daily_limit': 500,
            'agent_daily_limit': 50
        },
        'firecrawl': {
            'cost_per_call': 0.02,
            'global_daily_limit': 20000,
            'tenant_daily_limit': 2000,
            'agent_daily_limit': 200
        },
        'e2b': {
            'cost_per_call': 0.03,
            'global_daily_limit': 10000,
            'tenant_daily_limit': 1000,
            'agent_daily_limit': 100
        },
        'context7': {
            'cost_per_call': 0.01,
            'global_daily_limit': 15000,
            'tenant_daily_limit': 1500,
            'agent_daily_limit': 150
        },
        'browserbase': {
            'cost_per_call': 0.04,
            'global_daily_limit': 8000,
            'tenant_daily_limit': 800,
            'agent_daily_limit': 80
        }
    }

    def __init__(self, fallback_policies_path: Optional[str] = None, tenant_config_path: Optional[str] = None):
        """
        Initialize cost controller.

        Args:
            fallback_policies_path: Path to fallback policies JSON
            tenant_config_path: Path to tenant configuration JSON
        """
        if fallback_policies_path is None:
            fallback_policies_path = str(
                Path(__file__).parent.parent / 'fallback_policies.json'
            )

        if tenant_config_path is None:
            tenant_config_path = str(
                Path(__file__).parent.parent / 'tenant_config.json'
            )

        self.fallback_policies = self._load_fallback_policies(fallback_policies_path)
        self.tenant_config = self._load_tenant_config(tenant_config_path)

    def _load_fallback_policies(self, path: str) -> Dict:
        """Load fallback policies from JSON file."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Fallback policies not found at {path}, using defaults")
            return {}

    def _load_tenant_config(self, path: str) -> Dict:
        """Load tenant configuration from JSON file."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Tenant config not found at {path}, using defaults")
            return {
                'cost_limits': {
                    'daily_cost_limit': 10.0,
                    'global_daily_limit': 1000.0
                },
                'quota_limits': {
                    'agent_daily_limit': 100,
                    'tenant_daily_limit': 1000
                }
            }

    async def check_quota(self, server: str, agent_id: str) -> bool:
        """
        Check if agent can use the server based on quota.

        Args:
            server: MCP server name
            agent_id: Agent identifier

        Returns:
            True if quota available, False otherwise
        """
        if server not in self.PREMIUM_SERVERS:
            # Free servers always allowed
            return True

        try:
            today = date.today().isoformat()
            key = f"mcp:usage:{server}:{agent_id}:{today}"

            current_usage = await get_counter(key)
            limit = self.PREMIUM_SERVERS[server]['daily_limit']

            if current_usage >= limit:
                logger.warning(
                    f"Quota exceeded for {server} by {agent_id}: "
                    f"{current_usage}/{limit}"
                )
                return False

            return True
        except Exception as e:
            logger.error(f"Error checking quota: {str(e)}")
            # Fail open - allow usage if check fails
            return True

    async def record_usage(self, server: str, agent_id: str, cost: Optional[float] = None) -> None:
        """
        Record usage of a server by an agent.

        Args:
            server: MCP server name
            agent_id: Agent identifier
            cost: Actual cost (uses default if not provided)
        """
        try:
            today = date.today().isoformat()

            # Increment usage counter
            usage_key = f"mcp:usage:{server}:{agent_id}:{today}"
            await increment_counter(usage_key, 1)

            # Track cost
            if cost is None and server in self.PREMIUM_SERVERS:
                cost = self.PREMIUM_SERVERS[server]['cost_per_call']

            if cost:
                cost_key = f"mcp:cost:{agent_id}:{today}"
                current_cost = await get_counter(cost_key)
                await cache_set(cost_key, current_cost + cost, ttl=86400 * 7)  # 7 days

            logger.info(f"Recorded usage: {server} by {agent_id}, cost: ${cost:.4f}")
        except Exception as e:
            logger.error(f"Error recording usage: {str(e)}")

    async def get_usage_stats(self, agent_id: Optional[str] = None, days: int = 7) -> Dict:
        """
        Get usage statistics.

        Args:
            agent_id: Agent identifier (None for all agents)
            days: Number of days to look back

        Returns:
            Usage statistics dictionary
        """
        try:
            stats = {
                'total_calls': 0,
                'total_cost': 0.0,
                'by_server': {},
                'by_agent': {}
            }

            # Implementation would query Redis for historical data
            # For now, return current day stats
            today = date.today().isoformat()

            for server in self.PREMIUM_SERVERS:
                if agent_id:
                    key = f"mcp:usage:{server}:{agent_id}:{today}"
                    usage = await get_counter(key)
                    if usage > 0:
                        stats['by_server'][server] = usage
                        stats['total_calls'] += usage

            if agent_id:
                cost_key = f"mcp:cost:{agent_id}:{today}"
                stats['total_cost'] = await get_counter(cost_key)

            return stats
        except Exception as e:
            logger.error(f"Error getting usage stats: {str(e)}")
            return {}

    def get_fallback(self, server: str) -> Optional[str]:
        """
        Get fallback server for a premium server.

        Args:
            server: Primary server name

        Returns:
            Fallback server name or None
        """
        policy = self.fallback_policies.get(server, {})
        fallbacks = policy.get('fallback', [])

        if fallbacks:
            # Return first fallback
            return fallbacks[0]

        return None

    async def should_use_fallback(self, server: str, agent_id: str) -> bool:
        """
        Determine if fallback should be used based on threshold.

        Args:
            server: MCP server name
            agent_id: Agent identifier

        Returns:
            True if fallback should be used
        """
        if server not in self.PREMIUM_SERVERS:
            return False

        policy = self.fallback_policies.get(server, {})
        threshold = policy.get('fallback_threshold', 0.8)

        try:
            today = date.today().isoformat()
            key = f"mcp:usage:{server}:{agent_id}:{today}"

            current_usage = await get_counter(key)
            limit = self.PREMIUM_SERVERS[server]['daily_limit']

            usage_ratio = current_usage / limit if limit > 0 else 0

            if usage_ratio >= threshold:
                logger.info(
                    f"Fallback triggered for {server}: "
                    f"usage {usage_ratio:.1%} >= threshold {threshold:.1%}"
                )
                return True

            return False
        except Exception as e:
            logger.error(f"Error checking fallback threshold: {str(e)}")
            return False

    async def get_skill_cost_estimate(self, skill_id: str) -> float:
        """Obtiene el costo estimado de un skill desde el registry."""
        try:
            with open('/Users/mauroociappina/.gemini/anti_gravity/global_skills/skill_registry.json', 'r') as f:
                skills = json.load(f)

            for skill in skills:
                if skill.get('id') == skill_id:
                    cost_estimate = skill.get('cost_estimate', {})
                    return cost_estimate.get('per_execution', 0.0)

            return 0.0
        except Exception as e:
            logger.error(f"Error obteniendo costo del skill {skill_id}: {e}")
            return 0.0

    async def check_skill_cost_quota(self, agent_id: str, skill_id: str) -> bool:
        """Verifica si un agente puede usar un skill basado en su costo."""
        cost = await self.get_skill_cost_estimate(skill_id)
        return await self.check_quota_by_cost(agent_id, cost)

    async def check_quota_by_cost(self, agent_id: str, cost: float) -> bool:
        """Verifica si un agente tiene presupuesto para un costo específico."""
        try:
            today = date.today().isoformat()
            cost_key = f"mcp:cost:{agent_id}:{today}"

            current_cost = await get_counter(cost_key)
            tenant_config = self.tenant_config.get('cost_limits', {})
            daily_limit = tenant_config.get('daily_cost_limit', 10.0)  # Default $10/day

            if current_cost + cost > daily_limit:
                logger.warning(
                    f"Cost limit exceeded for {agent_id}: "
                    f"${current_cost + cost:.2f} > ${daily_limit:.2f}"
                )
                return False

            return True
        except Exception as e:
            logger.error(f"Error checking cost quota: {str(e)}")
            return True  # Fail open
