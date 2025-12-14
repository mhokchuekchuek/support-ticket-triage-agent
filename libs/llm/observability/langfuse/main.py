"""Langfuse observability client for LLM tracing."""

import os
from typing import Any, Dict, Optional

from langfuse import Langfuse, get_client
from langfuse.langchain import CallbackHandler

from libs.logger.logger import get_logger
from libs.llm.observability.base import BaseObservability

logger = get_logger(__name__)


class LangfuseObservability(BaseObservability):
    """Langfuse client for LLM observability and tracing.

    Provides automatic tracing for LangChain/LangGraph via CallbackHandler
    and manual tracing for non-LangChain code paths.

    Example:
        >>> obs = LangfuseObservability(
        ...     public_key="pk-lf-...",
        ...     secret_key="sk-lf-...",
        ...     host="https://cloud.langfuse.com"
        ... )
        >>>
        >>> # Automatic tracing with LangGraph
        >>> handler = obs.get_callback_handler(session_id="ticket-123")
        >>> result = agent.invoke(input, config={"callbacks": [handler]})
        >>>
        >>> # Manual tracing
        >>> obs.trace_generation(
        ...     name="embedding",
        ...     input_data={"texts": texts},
        ...     output=str(len(embeddings)),
        ...     model="text-embedding-3-large"
        ... )
        >>>
        >>> obs.flush()
    """

    def __init__(
        self,
        public_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        host: Optional[str] = None,
        enabled: bool = True,
    ):
        """Initialize Langfuse observability client.

        Args:
            public_key: Langfuse public key (default: from LANGFUSE_PUBLIC_KEY env)
            secret_key: Langfuse secret key (default: from LANGFUSE_SECRET_KEY env)
            host: Langfuse host URL (default: from LANGFUSE_HOST env or cloud)
            enabled: Whether observability is enabled (for graceful disable)
        """
        self.enabled = enabled
        self._available = False
        self.client: Optional[Langfuse] = None

        if not enabled:
            logger.info("Langfuse observability disabled by configuration")
            return

        self.public_key = public_key or os.getenv("LANGFUSE_PUBLIC_KEY")
        self.secret_key = secret_key or os.getenv("LANGFUSE_SECRET_KEY")
        self.host = host or os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

        if not self.public_key or not self.secret_key:
            logger.warning(
                "Langfuse API keys not provided. Observability will be disabled. "
                "Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY environment variables."
            )
            return

        try:
            self.client = Langfuse(
                public_key=self.public_key,
                secret_key=self.secret_key,
                host=self.host,
            )

            os.environ["LANGFUSE_PUBLIC_KEY"] = self.public_key
            os.environ["LANGFUSE_SECRET_KEY"] = self.secret_key
            os.environ["LANGFUSE_HOST"] = self.host

            self._available = True
            logger.info(f"Langfuse observability initialized (host={self.host})")

        except Exception as e:
            logger.error(f"Failed to initialize Langfuse client: {e}")

    def is_available(self) -> bool:
        """Check if Langfuse is available and connected."""
        return self._available and self.client is not None

    def get_callback_handler(
        self,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[CallbackHandler]:
        """Get LangChain callback handler for automatic tracing.

        In Langfuse v3, session_id/user_id are passed via config metadata
        when invoking the chain, not in the constructor.

        Args:
            session_id: Session ID for grouping related traces (stored for reference)
            user_id: User ID for attribution (stored for reference)
            metadata: Additional metadata to attach to all traces

        Returns:
            Langfuse CallbackHandler instance, or None if unavailable
        """
        if not self.is_available():
            logger.debug("Langfuse unavailable, returning None callback handler")
            return None

        try:
            handler = CallbackHandler()
            logger.debug(f"Created CallbackHandler (session={session_id})")
            return handler

        except Exception as e:
            logger.error(f"Failed to create CallbackHandler: {e}")
            return None

    def trace_generation(
        self,
        name: str,
        input_data: Dict[str, Any],
        output: str,
        model: str,
        metadata: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
        **kwargs,
    ) -> Any:
        """Trace an LLM generation.

        Args:
            name: Name of the generation
            input_data: Input data (prompt variables, messages, etc.)
            output: Generated output
            model: Model name
            metadata: Additional metadata
            session_id: Session ID for grouping traces
            **kwargs: Additional Langfuse-specific parameters

        Returns:
            Langfuse trace object, or None if unavailable
        """
        if not self.is_available():
            logger.debug(f"Langfuse unavailable, skipping trace for '{name}'")
            return None

        try:
            # Langfuse SDK v3 uses get_client() and start_as_current_observation()
            client = get_client()
            with client.start_as_current_observation(
                as_type="generation",
                name=name,
                model=model,
            ) as generation:
                generation.update(
                    input=input_data,
                    output=output,
                    metadata=metadata or {},
                )

            logger.debug(f"Traced generation '{name}' (session={session_id})")
            return generation

        except Exception as e:
            logger.error(f"Failed to trace generation: {e}", exc_info=True)
            return None

    def flush(self):
        """Flush pending traces to Langfuse."""
        if not self.is_available():
            return

        try:
            self.client.flush()
            logger.debug("Flushed traces to Langfuse")
        except Exception as e:
            logger.warning(f"Failed to flush traces to Langfuse: {e}")
