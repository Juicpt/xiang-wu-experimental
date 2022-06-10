from . import word_matchers

MONEY_MATCHER = word_matchers.MultiWordMatcher(
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

INTEREST_MATCHER = word_matchers.MultiWordMatcher(
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

PROFIT_MATCHER = word_matchers.MultiWordMatcher(
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

PAYMENT_MATCHER = word_matchers.FirstMatcher(MONEY_MATCHER, INTEREST_MATCHER)

GET_MATCHER = word_matchers.MultiWordMatcher("get", "gets", "getting", "got")
GUARANTEE_MATCHER = word_matchers.MultiWordMatcher(
    "guarantee", "guarantees", "guaranteeing", "guaranteed"
)
MAKE_MATCHER = word_matchers.MultiWordMatcher("make", "makes", "making", "made")
PAY_MATCHER = word_matchers.MultiWordMatcher("pay", "pays", "paying", "paid")
RECEIVE_MATCHER = word_matchers.MultiWordMatcher(
    "receive", "receives", "receiving", "received"
)
SEND_MATCHER = word_matchers.MultiWordMatcher("send", "sends", "sending", "sent")
TAKE_MATCHER = word_matchers.MultiWordMatcher(
    "take", "takes", "taking", "took", "taken"
)
NEGATE_POST_MATCHER = word_matchers.MultiWordMatcher("no", "none", "not")

ACTIVE_GET_PAYMENT_MATCHER = word_matchers.FirstMatcher(
    word_matchers.make_distance_matcher(
        4,
        word_matchers.FirstMatcher(
            GET_MATCHER,
            GUARANTEE_MATCHER,
            MAKE_MATCHER,
            PAY_MATCHER,
            RECEIVE_MATCHER,
            SEND_MATCHER,
            TAKE_MATCHER,
        ),
        MONEY_MATCHER,
    ).post(negative_matcher=NEGATE_POST_MATCHER, padding_start=2),
    word_matchers.make_distance_matcher(
        4,
        word_matchers.FirstMatcher(
            GET_MATCHER, GUARANTEE_MATCHER, PAY_MATCHER, RECEIVE_MATCHER
        ),
        INTEREST_MATCHER,
    ).post(negative_matcher=NEGATE_POST_MATCHER, padding_start=2),
    word_matchers.make_distance_matcher(
        4,
        word_matchers.FirstMatcher(
            GET_MATCHER,
            GUARANTEE_MATCHER,
            MAKE_MATCHER,
            RECEIVE_MATCHER,
            SEND_MATCHER,
            TAKE_MATCHER,
        ),
        PROFIT_MATCHER,
    ).post(negative_matcher=NEGATE_POST_MATCHER, padding_start=2),
)

PASSIVE_GET_MATCHER = word_matchers.MultiWordMatcher(
    "guaranteed", "made", "paid", "received", "sent", "taken"
)

PASSIVE_GET_PAYMENT_MATCHER = word_matchers.make_distance_matcher(
    2,
    PAYMENT_MATCHER,
    PASSIVE_GET_MATCHER,
).post(negative_matcher=NEGATE_POST_MATCHER, padding_start=2)

FINANCIAL_FREEDOM_MATCHER = word_matchers.make_distance_matcher(
    2,
    word_matchers.MultiWordMatcher("finance", "financial"),
    "freedom",
)

RETIRE_MATCHER = word_matchers.MultiWordMatcher(
    "retire", "retires", "retiring", "retired"
)

RETIRE_EARLY_MATCHER = word_matchers.make_distance_matcher(
    2,
    RETIRE_MATCHER,
    "early",
)

SECURITY_MATCHER = word_matchers.MultiWordMatcher(
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

BE_MATCHER = word_matchers.MultiWordMatcher("be", "is", "are", "was", "were")

INCREASE_MATCHER = word_matchers.MultiWordMatcher(
    "double",
    "doubling",
    "grow",
    "growing",
    "increase",
    "increasing",
    "multiply",
    "multiplying",
    "triple",
    "tripling",
)

FINANCIAL_INSTRUMENTS_MATCHER = word_matchers.FirstMatcher(
    word_matchers.MultiWordMatcher(
        "cusip",
        "forex",
        "ico",
        "ido",
        "ieo",
        "ipo",
        "roi",
    ),
    word_matchers.make_distance_matcher(
        4,
        BE_MATCHER,
        word_matchers.FirstMatcher(
            word_matchers.MultiWordMatcher(
                "investing",
                "investment",
                "investments",
                "lucrative",
                "profitable",
            ),
            word_matchers.SeqMatcher(
                word_matchers.MultiWordMatcher("money", "profit"),
                "making",
            ),
        ),
    ).post(negative_matcher=NEGATE_POST_MATCHER, padding_start=2),
    word_matchers.make_distance_matcher(
        4,
        INCREASE_MATCHER,
        word_matchers.MultiWordMatcher("investment", "investments", "money", "moneys"),
    ),
    word_matchers.make_distance_matcher(
        2,
        SECURITY_MATCHER.extend("coin", "crypto"),
        "offering",
    ),
    word_matchers.SeqMatcher(
        word_matchers.MultiWordMatcher("profit", "rev", "revenue"),
        word_matchers.MultiWordMatcher("share", "sharing"),
    ),
    word_matchers.SeqMatcher(
        word_matchers.MultiWordMatcher(
            "passive", "stable", "daily", "weekly", "monthly", "yearly"
        ),
        PROFIT_MATCHER,
    ),
)

ACTIVE_TRADE_MATCHER = word_matchers.MultiWordMatcher(
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
)

ACTIVE_TRADE_SECURITY_MATCHER = word_matchers.make_distance_matcher(
    4,
    ACTIVE_TRADE_MATCHER,
    SECURITY_MATCHER,
)

PASSIVE_TRADE_MATCHER = word_matchers.MultiWordMatcher(
    "bought", "sold", "traded", "transacted"
)

PASSIVE_TRADE_SECURITY_MATCHER = word_matchers.make_distance_matcher(
    2,
    SECURITY_MATCHER,
    PASSIVE_TRADE_MATCHER,
)
