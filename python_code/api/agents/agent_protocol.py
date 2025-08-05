from typing import List, Dict, Any, Protocol

class AgentProtocol(Protocol):
 def get_response(self, messages: List[Dict[str, Any]]) -> dict[str, Any]:
        ...

