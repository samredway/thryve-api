from decimal import Decimal
from enum import Enum
from typing import Optional

from plaid.model.account_balance import AccountBalance  # type: ignore
from pydantic import BaseModel


class IsoCurrencyCode(str, Enum):
    GBP = "GBP"


class PlaidAccountBalance(BaseModel):
    available: Optional[Decimal]
    current: Decimal
    iso_currency_code: IsoCurrencyCode
    limit: Optional[Decimal]
    unofficial_currency_code: Optional[str]


class PlaidAccountSubType(str, Enum):
    NONE = "None"  # Not sure about if none comes as string or obj maybe this is wrong
    _401A = "401a"
    _401K = "401k"
    _403B = "403B"
    _457B = "457b"
    _529 = "529"
    BROKERAGE = "brokerage"
    CASH_ISA = "cash isa"
    CRYPTO_EXCHANGE = "crypto exchange"
    EDUCATION_SAVINGS_ACCOUNT = "education savings account"
    EBT = "ebt"
    FIXED_ANNUITY = "fixed annuity"
    GIC = "gic"
    HEALTH_REIMBURSEMENT_ARRANGEMENT = "health reimbursement arrangement"
    HSA = "hsa"
    ISA = "isa"
    IRA = "ira"
    LIF = "lif"
    LIFE_INSURANCE = "life insurance"
    LIRA = "lira"
    LRIF = "lrif"
    LRSP = "lrsp"
    NON_CUSTODIAL_WALLET = "non-custodial wallet"
    NON_TAXABLE_BROKERAGE_ACCOUNT = "non-taxable brokerage account"
    OTHER = "other"
    OTHER_INSURANCE = "other insurance"
    OTHER_ANNUITY = "other annuity"
    PRIF = "prif"
    RDSP = "rdsp"
    RESP = "resp"
    RLIF = "rlif"
    RRIF = "rrif"
    PENSION = "pension"
    PROFIT_SHARING_PLAN = "profit sharing plan"
    RETIREMENT = "retirement"
    ROTH = "roth"
    ROTH_401K = "roth 401k"
    RRSP = "rrsp"
    SEP_IRA = "sep ira"
    SIMPLE_IRA = "simple ira"
    SIPP = "sipp"
    STOCK_PLAN = "stock plan"
    THRIFT_SAVINGS_PLAN = "thrift savings plan"
    TFSA = "tfsa"
    TRUST = "trust"
    UGMA = "ugma"
    UTMA = "utma"
    VARIABLE_ANNUITY = "variable annuity"
    CREDIT_CARD = "credit card"
    PAYPAL = "paypal"
    CD = "cd"
    CHECKING = "checking"
    SAVINGS = "savings"
    MONEY_MARKET = "money market"
    PREPAID = "prepaid"
    AUTO = "auto"
    BUSINESS = "business"
    COMMERCIAL = "commercial"
    CONSTRUCTION = "construction"
    CONSUMER = "consumer"
    HOME_EQUITY = "home equity"
    LOAN = "loan"
    MORTGAGE = "mortgage"
    OVERDRAFT = "overdraft"
    LINE_OF_CREDIT = "line of credit"
    STUDENT = "student"
    CASH_MANAGEMENT = "cash management"
    KEOGH = "keogh"
    MUTUAL_FUND = "mutual fund"
    RECURRING = "recurring"
    REWARDS = "rewards"
    SAFE_DEPOSIT = "safe deposit"
    SARSEP = "sarsep"
    PAYROLL = "payroll"
    NULL = "null"


class PlaidAccountType(str, Enum):
    INVESTMENT = "investment"
    CREDIT = "credit"
    DEPOSITORY = "depository"
    LOAN = "loan"
    BROKERAGE = "brokerage"
    OTHER = "other"


class PlaidAccount(BaseModel):
    account_id: str
    balances: PlaidAccountBalance
    mask: str
    name: str
    official_name: Optional[str]
    subtype: PlaidAccountSubType
    type: PlaidAccountType

    @classmethod
    def from_plaid_account_balance_raw(cls, account: AccountBalance) -> "PlaidAccount":
        return cls(
            account_id=account.account_id,
            balances=PlaidAccountBalance(
                available=account.balances.available,
                current=account.balances.current,
                iso_currency_code=account.balances.iso_currency_code,
                limit=account.balances.limit,
                unofficial_currency_code=account.balances.unofficial_currency_code,
            ),
            mask=account.mask,
            name=account.name,
            official_name=account.official_name,
            subtype=PlaidAccountSubType(str(account.subtype)),
            type=PlaidAccountType(str(account.type)),
        )


# Responses and requests


class GetPlaidLinkTokenResponse(BaseModel):
    plaid_link_token: str


class GetPlaidAccountsResponse(BaseModel):
    accounts: list[PlaidAccount]


class PlaidPublicTokenExchangePostRequest(BaseModel):
    public_token: str
