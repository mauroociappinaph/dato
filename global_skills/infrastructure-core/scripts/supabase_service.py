"""
Supabase Service - The Dude S.A.S.
Centralized Supabase client with connection pooling and error handling.
"""
from functools import lru_cache
from typing import Any, Dict, Optional
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
from ..config import get_config


class SupabaseService:
    """Supabase service with singleton pattern"""
    
    _instance: Optional["SupabaseService"] = None
    _client: Optional[Client] = None
    
    def __new__(cls) -> "SupabaseService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is not None:
            return
            
        config = get_config()
        self._client = create_client(
            config.supabase.url,
            config.supabase.anon_key,
            options=ClientOptions(
                postgrest_client_timeout=30,
                storage_client_timeout=30,
                schema="public"
            )
        )
    
    @property
    def client(self) -> Client:
        """Get Supabase client"""
        if self._client is None:
            self.__init__()
        return self._client


@lru_cache(maxsize=1)
def get_supabase() -> Client:
    """Get Supabase client singleton (cached)"""
    return SupabaseService().client


def get_supabase_service() -> SupabaseService:
    """Get Supabase service instance"""
    return SupabaseService()


class Table:
    """Base table class for type-safe access"""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
        self._supabase_service = get_supabase_service()
    
    def select(self, *columns: str) -> Any:
        return self._supabase_service.client.table(self.table_name).select(*columns)
    
    def insert(self, data: Dict[str, Any]) -> Any:
        return self._supabase_service.client.table(self.table_name).insert(data)
    
    def update(self, data: Dict[str, Any]) -> Any:
        return self._supabase_service.client.table(self.table_name).update(data)
    
    def delete(self) -> Any:
        return self._supabase_service.client.table(self.table_name).delete()
    
    def upsert(self, data: Dict[str, Any], on_conflict: Optional[str] = None) -> Any:
        return self._supabase_service.client.table(self.table_name).upsert(data, on_conflict=on_conflict)


class LeadsTable(Table):
    """Leads table access"""
    
    def __init__(self):
        super().__init__("leads")
    
    def get_new_leads(self) -> list:
        """Get leads with status NEW"""
        return self.select("*").eq("status", "NEW").execute().data
    
    def get_enriched_leads(self) -> list:
        """Get leads with status ENRICHED"""
        return self.select("*").eq("status", "ENRICHED").execute().data
    
    def get_contacted_leads(self) -> list:
        """Get leads with status CONTACTED"""
        return self.select("*").eq("status", "CONTACTED").execute().data
    
    def get_interested_leads(self) -> list:
        """Get leads with status INTERESTED"""
        return self.select("*").eq("status", "INTERESTED").execute().data


class MemoryTable(Table):
    """Memory/Knowledge table access"""
    
    def __init__(self):
        super().__init__("memory")


class SuccessVaultTable(Table):
    """Success vault table access"""
    
    def __init__(self):
        super().__init__("success_vault")
