"""Tool for looking up customer information from PostgreSQL."""

from typing import Type, Optional
from langchain.tools import BaseTool
from pydantic import Field, BaseModel

from libs.database.tabular.sql.base import BaseSQLClient
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class CustomerLookupInput(BaseModel):
    """Input schema for customer lookup tool."""

    customer_id: str = Field(description="Customer ID to look up")


class CustomerLookupTool(BaseTool):
    """Look up customer information from PostgreSQL.

    Retrieves customer details including plan type, tenure,
    region, seats, and notes using customer_id from the ticket.

    Attributes:
        name: Tool name for LangChain.
        description: Tool description for the LLM.
        db_client: SQL database client for queries.
    """

    name: str = "customer_lookup"
    description: str = (
        "Look up customer information including plan type, tenure, "
        "region, seats, and account notes. Use customer_id from the ticket."
    )
    args_schema: Type[BaseModel] = CustomerLookupInput
    db_client: Optional[BaseSQLClient] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, db_client: BaseSQLClient, **kwargs):
        """Initialize customer lookup tool.

        Args:
            db_client: SQL database client for queries.
            **kwargs: Additional arguments passed to BaseTool.
        """
        super().__init__(**kwargs)
        self.db_client = db_client
        logger.info("CustomerLookupTool initialized with PostgreSQL client")

    def _run(self, customer_id: str) -> str:
        """Look up customer by ID from PostgreSQL.

        Args:
            customer_id: Customer ID to look up.

        Returns:
            Formatted string with customer information.
        """
        logger.info(f"Looking up customer: {customer_id}")

        try:
            result = self.db_client.fetch_one(
                """
                SELECT id, name, email, plan, tenure_months, region, seats, notes
                FROM customers
                WHERE id = %s
                """,
                (customer_id,)
            )

            if not result:
                return f"Customer {customer_id} not found."

            return (
                f"**Customer:** {result['name']}\n"
                f"**Email:** {result['email']}\n"
                f"**Plan:** {result['plan']}\n"
                f"**Tenure:** {result['tenure_months']} months\n"
                f"**Region:** {result['region'] or 'N/A'}\n"
                f"**Seats:** {result.get('seats', 1)}\n"
                f"**Notes:** {result.get('notes') or 'None'}"
            )

        except Exception as e:
            logger.error(f"Failed to query customer: {e}")
            return f"Error looking up customer: {str(e)}"
