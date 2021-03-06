from typing import Dict

from . import word_matchers

_MONEY_MATCHER = word_matchers.MultiWordMatcher(
    "$",
    "$$",
    "$$$",
    "bitcoin",
    "bitcoins",
    "btc",
    "btcs",
    "cash",
    "dollar",
    "dollars",
    "money",
    "moneys",
    "usd",
    "usds",
)

_INTEREST_MATCHER = word_matchers.MultiWordMatcher(
    "coupon",
    "coupons",
    "disimbursement",
    "disimbursements",
    "distribution",
    "distributions",
    "dividend",
    "dividends",
    "interest",
    "interests",
    "royalties",
    "royalty",
    "yield",
    "yields",
)

_PROFIT_MATCHER = word_matchers.MultiWordMatcher(
    "gain",
    "gains",
    "income",
    "incomes",
    "payment",
    "payments",
    "payout",
    "payouts",
    "profit",
    "profits",
    "upside",
    "upsides",
)

_GET_MATCHER = word_matchers.MultiWordMatcher("get", "gets", "getting", "got")

_GUARANTEE_MATCHER = word_matchers.MultiWordMatcher(
    "guarantee", "guarantees", "guaranteeing", "guaranteed"
)

_MAKE_MATCHER = word_matchers.MultiWordMatcher("make", "makes", "making", "made")

_PAY_MATCHER = word_matchers.MultiWordMatcher("pay", "pays", "paying", "paid")

_RECEIVE_MATCHER = word_matchers.MultiWordMatcher(
    "receive", "receives", "receiving", "received"
)

_SEND_MATCHER = word_matchers.MultiWordMatcher("send", "sends", "sending", "sent")

_TAKE_MATCHER = word_matchers.MultiWordMatcher(
    "take", "takes", "taking", "took", "taken"
)

_PASSIVE_GET_MATCHER = word_matchers.MultiWordMatcher(
    "guaranteed", "made", "paid", "received", "sent", "taken"
)

_NEGATE_POST_MATCHER = word_matchers.MultiWordMatcher("no", "none", "not")

_WHAT_TO_INCREASE_MATCHER = word_matchers.MultiWordMatcher(
    "investment", "investments", "money", "moneys"
)

_SECURITY_MATCHER = word_matchers.MultiWordMatcher(
    "bond",
    "bonds",
    "commodities",
    "commodity",
    "currencies",
    "currency",
    "derivative",
    "derivatives",
    "option",
    "options",
    "securities",
    "security",
    "stock",
    "stocks",
)

LABEL_AND_MATCHER: Dict[str, word_matchers.BaseMatcher] = {}

LABEL_AND_MATCHER["GET_MONEY"] = word_matchers.make_distance_matcher(
    4,
    _GET_MATCHER
    | _GUARANTEE_MATCHER
    | _MAKE_MATCHER
    | _PAY_MATCHER
    | _RECEIVE_MATCHER
    | _SEND_MATCHER
    | _TAKE_MATCHER,
    _MONEY_MATCHER,
).post(negative_matcher=_NEGATE_POST_MATCHER, padding_start=2)

LABEL_AND_MATCHER["GET_INTEREST"] = word_matchers.make_distance_matcher(
    4,
    _GET_MATCHER | _GUARANTEE_MATCHER | _PAY_MATCHER | _RECEIVE_MATCHER,
    _INTEREST_MATCHER,
).post(negative_matcher=_NEGATE_POST_MATCHER, padding_start=2)

LABEL_AND_MATCHER["GET_PROFIT"] = word_matchers.make_distance_matcher(
    4,
    _GET_MATCHER
    | _GUARANTEE_MATCHER
    | _MAKE_MATCHER
    | _RECEIVE_MATCHER
    | _SEND_MATCHER
    | _TAKE_MATCHER,
    _PROFIT_MATCHER,
).post(negative_matcher=_NEGATE_POST_MATCHER, padding_start=2)

LABEL_AND_MATCHER["MONEY_GOT"] = word_matchers.make_distance_matcher(
    2, _MONEY_MATCHER, _PASSIVE_GET_MATCHER
).post(negative_matcher=_NEGATE_POST_MATCHER, padding_start=2)

LABEL_AND_MATCHER["INTEREST_GOT"] = word_matchers.make_distance_matcher(
    2, _INTEREST_MATCHER, _PASSIVE_GET_MATCHER
).post(negative_matcher=_NEGATE_POST_MATCHER, padding_start=2)

LABEL_AND_MATCHER["PROFIT_GOT"] = word_matchers.make_distance_matcher(
    2, _PROFIT_MATCHER, _PASSIVE_GET_MATCHER
).post(negative_matcher=_NEGATE_POST_MATCHER, padding_start=2)

LABEL_AND_MATCHER["FINANCIAL_FREEDOM"] = word_matchers.make_distance_matcher(
    2,
    ["finance", "financial", "financially", "money"],
    ["free", "freedom"],
)

LABEL_AND_MATCHER["RETIRE_EARLY"] = word_matchers.make_distance_matcher(
    2,
    ["retire", "retires", "retiring", "retired"],
    ["early", "now", "soon", "tomorrow"],
)

LABEL_AND_MATCHER["SECURITY_UNIGRAM"] = word_matchers.MultiWordMatcher(
    "apy",
    "cusip",
    "forex",
    "ico",
    "ido",
    "ieo",
    "ipo",
    "roi",
)

LABEL_AND_MATCHER["IS_INVESTMENT"] = word_matchers.make_distance_matcher(
    4,
    ["be", "been", "is", "are", "was", "were"],
    word_matchers.FirstMatcher(
        [
            "investing",
            "investment",
            "investments",
            "lucrative",
            "profitable",
        ],
        word_matchers.SeqMatcher(
            ["money", "profit", "income", "interest"],
            ["making", "generating", "bearing"],
        ),
    ),
).post(negative_matcher=_NEGATE_POST_MATCHER, padding_start=2)

LABEL_AND_MATCHER["INCREASE_INVESTMENT"] = word_matchers.make_distance_matcher(
    4,
    [
        "double",
        "doubling",
        "doubled",
        "grow",
        "growing",
        "grew",
        "increase",
        "increasing",
        "increased",
        "multiply",
        "multiplying",
        "multiplied",
        "triple",
        "tripling",
        "tripled",
    ],
    _WHAT_TO_INCREASE_MATCHER,
)

LABEL_AND_MATCHER["INVESTMENT_INCREASED"] = word_matchers.make_distance_matcher(
    2,
    _WHAT_TO_INCREASE_MATCHER,
    [
        "doubled",
        "grown",
        "increased",
        "multiplied",
        "tripled",
    ],
)

LABEL_AND_MATCHER["CRYPTO_OFFERING"] = word_matchers.make_distance_matcher(
    2,
    _SECURITY_MATCHER.extend("coin", "crypto"),
    ["listing", "offering"],
)

LABEL_AND_MATCHER["REVENUE_SHARE"] = word_matchers.SeqMatcher(
    ["profit", "rev", "revenue"],
    ["share", "sharing"],
)

LABEL_AND_MATCHER["PASSIVE_INCOME"] = word_matchers.SeqMatcher(
    [
        "passive",
        "stable",
        "daily",
        "weekly",
        "monthly",
        "yearly",
        "timely",
        "recurring",
        "diversified",
    ],
    (_INTEREST_MATCHER | _PROFIT_MATCHER).extend("investment"),
)

LABEL_AND_MATCHER["TRADE_SECURITY"] = word_matchers.make_distance_matcher(
    4,
    [
        "buy",
        "buying",
        "bought",
        "sell",
        "selling",
        "sold",
        "trade",
        "trading",
        "traded",
        "transact",
        "transacting",
        "transacted",
    ],
    _SECURITY_MATCHER,
)

LABEL_AND_MATCHER["SECURITY_TRADED"] = word_matchers.make_distance_matcher(
    2,
    _SECURITY_MATCHER,
    ["bought", "sold", "traded", "transacted"],
)

LABEL_AND_MATCHER["I_WILL_BUY"] = word_matchers.make_distance_matcher(
    2,
    word_matchers.SeqMatcher(
        ["i", "we"],
        ["will", "ll", "would", "d"],
    ),
    ["buy", "buyback"],
)

LABEL_AND_MATCHER["CASINO_UNIGRAM"] = word_matchers.MultiWordMatcher(
    "casino", "casinos", "gamble", "gambles", "gambling", "gambled"
)

LABEL_AND_MATCHER["CASINO_BETTING"] = word_matchers.make_distance_matcher(
    4,
    ["bet", "betting", "play", "playing"],
    word_matchers.make_distance_matcher(
        1,
        ["to", "for"],
        (_MONEY_MATCHER | _PROFIT_MATCHER).extend("win", "winning"),
    ),
)
