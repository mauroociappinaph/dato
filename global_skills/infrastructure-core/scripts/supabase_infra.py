"""
Supabase Infrastructure Abstractions
Provides reusable functions for common Supabase operations.
"""

import os
import logging
from typing import Dict, List, Any, Optional
from supabase import create_client, Client

logger = logging.getLogger(__name__)

# Singleton client
_supabase_client: Optional[Client] = None

def get_client() -> Client:
    """Get or create Supabase client singleton."""
    global _supabase_client
    if _supabase_client is None:
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
        _supabase_client = create_client(url, key)
    return _supabase_client


# ============================================================================
# CRUD Operations
# ============================================================================

async def store_result(table: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Insert a record into a Supabase table.

    Args:
        table: Table name
        data: Record data

    Returns:
        Inserted record with ID

    Raises:
        Exception: If insert fails
    """
    try:
        client = get_client()
        result = client.table(table).insert(data).execute()
        logger.info(f"Inserted record into {table}: {result.data[0].get('id')}")
        return result.data[0]
    except Exception as e:
        logger.error(f"Failed to insert into {table}: {str(e)}")
        raise


async def load_by_id(table: str, record_id: str) -> Optional[Dict[str, Any]]:
    """
    Load a record by ID.

    Args:
        table: Table name
        record_id: Record ID

    Returns:
        Record data or None if not found
    """
    try:
        client = get_client()
        result = client.table(table).select("*").eq('id', record_id).execute()
        if result.data:
            return result.data[0]
        return None
    except Exception as e:
        logger.error(f"Failed to load {record_id} from {table}: {str(e)}")
        raise


async def query_by_filter(table: str, filters: Dict[str, Any], limit: int = 100) -> List[Dict[str, Any]]:
    """
    Query records with filters.

    Args:
        table: Table name
        filters: Key-value filters (e.g., {'status': 'active'})
        limit: Max records to return

    Returns:
        List of matching records
    """
    try:
        client = get_client()
        query = client.table(table).select("*")

        for key, value in filters.items():
            query = query.eq(key, value)

        result = query.limit(limit).execute()
        logger.info(f"Query {table} with {filters}: {len(result.data)} results")
        return result.data
    except Exception as e:
        logger.error(f"Failed to query {table}: {str(e)}")
        raise


async def update_by_id(table: str, record_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a record by ID.

    Args:
        table: Table name
        record_id: Record ID
        updates: Fields to update

    Returns:
        Updated record
    """
    try:
        client = get_client()
        result = client.table(table).update(updates).eq('id', record_id).execute()
        logger.info(f"Updated {record_id} in {table}")
        return result.data[0]
    except Exception as e:
        logger.error(f"Failed to update {record_id} in {table}: {str(e)}")
        raise


async def delete_by_id(table: str, record_id: str) -> bool:
    """
    Delete a record by ID.

    Args:
        table: Table name
        record_id: Record ID

    Returns:
        True if deleted
    """
    try:
        client = get_client()
        client.table(table).delete().eq('id', record_id).execute()
        logger.info(f"Deleted {record_id} from {table}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete {record_id} from {table}: {str(e)}")
        raise


# ============================================================================
# Context Management
# ============================================================================

async def load_user_context(user_id: str) -> Dict[str, Any]:
    """
    Load complete user context (profile, preferences, history).

    Args:
        user_id: User ID

    Returns:
        User context dictionary
    """
    try:
        client = get_client()

        # Load profile
        profile = client.table('users').select("*").eq('id', user_id).execute()

        # Load preferences
        prefs = client.table('user_preferences').select("*").eq('user_id', user_id).execute()

        context = {
            'profile': profile.data[0] if profile.data else {},
            'preferences': prefs.data[0] if prefs.data else {}
        }

        logger.info(f"Loaded context for user {user_id}")
        return context
    except Exception as e:
        logger.error(f"Failed to load context for {user_id}: {str(e)}")
        raise


async def save_agent_state(agent_id: str, state: Dict[str, Any]) -> bool:
    """
    Save agent execution state.

    Args:
        agent_id: Agent identifier
        state: State dictionary

    Returns:
        True if saved
    """
    try:
        client = get_client()

        # Upsert agent state
        client.table('agent_states').upsert({
            'agent_id': agent_id,
            'state': state,
            'updated_at': 'now()'
        }).execute()

        logger.info(f"Saved state for agent {agent_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to save state for {agent_id}: {str(e)}")
        raise


# ============================================================================
# Batch Operations
# ============================================================================

async def bulk_insert(table: str, records: List[Dict[str, Any]]) -> int:
    """
    Insert multiple records in a single operation.

    Args:
        table: Table name
        records: List of records to insert

    Returns:
        Number of records inserted
    """
    try:
        client = get_client()
        result = client.table(table).insert(records).execute()
        count = len(result.data)
        logger.info(f"Bulk inserted {count} records into {table}")
        return count
    except Exception as e:
        logger.error(f"Failed to bulk insert into {table}: {str(e)}")
        raise


async def bulk_update(table: str, updates: List[Dict[str, Any]]) -> int:
    """
    Update multiple records (requires 'id' in each update dict).

    Args:
        table: Table name
        updates: List of update dicts with 'id' field

    Returns:
        Number of records updated
    """
    try:
        client = get_client()
        count = 0

        for update in updates:
            record_id = update.pop('id')
            client.table(table).update(update).eq('id', record_id).execute()
            count += 1

        logger.info(f"Bulk updated {count} records in {table}")
        return count
    except Exception as e:
        logger.error(f"Failed to bulk update {table}: {str(e)}")
        raise
