import json
from pathlib import Path
from langchain.tools import BaseTool
from pydantic import Field, BaseModel
from typing import Type

from libs.logger.logger import get_logger

logger = get_logger(__name__)


class CustomerLookupInput(BaseModel):
    """Input schema for customer lookup tool."""

    customer_id: str = Field(description="Customer ID to look up")


class CustomerLookupTool(BaseTool):
    """Look up customer information.

    Retrieves customer details including plan type, tenure,
    previous tickets, and account notes using customer_id from the ticket.

    Attributes:
        name: Tool name for LangChain.
        description: Tool description for the LLM.
        customers_data: Loaded customer data dictionary.
    """

    name: str = "customer_lookup"
    description: str = (
        "Look up customer information including plan type, tenure, "
        "previous tickets, and account notes. Use customer_id from the ticket."
    )
    args_schema: Type[BaseModel] = CustomerLookupInput
    customers_data: dict = {}

    def __init__(self, data_path: str = "data/customers.json", **kwargs):
        """Initialize customer lookup tool.

        Args:
            data_path: Path to customers JSON file.
            **kwargs: Additional arguments passed to BaseTool.
        """
        super().__init__(**kwargs)
        self._load_customers(data_path)

    def _load_customers(self, data_path: str) -> None:
        """Load customers data from JSON file.

        Args:
            data_path: Path to customers JSON file.
        """
        path = Path(data_path)
        if path.exists():
            with open(path) as f:
                data = json.load(f)
                self.customers_data = {c["id"]: c for c in data.get("customers", [])}
            logger.info(f"Loaded {len(self.customers_data)} customers from {data_path}")
        else:
            logger.warning(f"Customer data file not found: {data_path}")

    def _run(self, customer_id: str) -> str:
        """Look up customer by ID.

        Args:
            customer_id: Customer ID to look up.

        Returns:
            Formatted string with customer information.
        """
        logger.info(f"Looking up customer: {customer_id}")

        customer = self.customers_data.get(customer_id)
        if not customer:
            return f"Customer {customer_id} not found."

        return (
            f"**Customer:** {customer['name']}\n"
            f"**Email:** {customer['email']}\n"
            f"**Plan:** {customer['plan']}\n"
            f"**Tenure:** {customer['tenure_months']} months\n"
            f"**Region:** {customer['region']}\n"
            f"**Seats:** {customer.get('seats', 1)}\n"
            f"**Previous Tickets:** {len(customer.get('previous_tickets', []))}\n"
            f"**Notes:** {customer.get('notes', 'None')}"
        )
