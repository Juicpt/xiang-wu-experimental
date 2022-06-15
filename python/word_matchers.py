import re

from typing import Iterable, List, Optional, Tuple, Union

from . import utils


def extract_words(s: str) -> List[str]:
    return re.findall(r"[a-zA-Z]+|[0-9.]+%*|\$+(?![a-zA-Z0-9])", s)


def split_at_capital(s: str) -> List[str]:
    return re.sub(r"([a-z])([A-Z])", r"\1 \2", s).split()


def tokenize(s: str) -> List[str]:
    return [x.lower() for y in extract_words(s) for x in split_at_capital(y)]


class BaseMatcher:
    def match(self, i: int, tokens: List[str]) -> Optional[Tuple[int, int]]:
        if i < 0 or not tokens or i >= len(tokens):
            return None
        else:
            return self._match_impl(i, tokens)

    def post(
        self,
        positive_matcher: "Optional[BaseMatcher]" = None,
        negative_matcher: "Optional[BaseMatcher]" = None,
        padding_start: int = 0,
        padding_stop: int = 0,
    ) -> "PostMatcher":
        return PostMatcher(
            self,
            post_positive=positive_matcher,
            post_negative=negative_matcher,
            padding_start=padding_start,
            padding_stop=padding_stop,
        )


def match_all(matcher: BaseMatcher, tokens: List[str]) -> Iterable[Tuple[int, int]]:
    i = 0
    while i < len(tokens):
        match = matcher.match(i, tokens)
        if match is not None:
            yield match
            i = match[1]
        else:
            i += 1


class PostMatcher(BaseMatcher):
    def __init__(
        self,
        matcher,
        post_positive: Optional[BaseMatcher] = None,
        post_negative: Optional[BaseMatcher] = None,
        padding_start: int = 0,
        padding_stop: int = 0,
    ):
        assert post_positive is None or post_negative is None
        self._matcher = cast_to_matcher(matcher)
        self._post_positive = post_positive
        self._post_negative = post_negative
        self._padding_start = padding_start
        self._padding_stop = padding_stop

    def _match_impl(self, i: int, tokens: List[str]) -> Optional[Tuple[int, int]]:
        match = self._matcher.match(i, tokens)
        if match is None:
            return None
        start = max(0, match[0] - self._padding_start)
        stop = min(len(tokens), match[1] + self._padding_stop)
        if self._post_positive is not None and not utils.consume_first(
            match_all(self._post_positive, tokens[start:stop])
        ):
            return None
        if self._post_negative is not None and utils.consume_first(
            match_all(self._post_negative, tokens[start:stop])
        ):
            return None
        return match


class SingleWordMatcher(BaseMatcher):
    def __init__(self, word: str):
        assert isinstance(word, str)
        self._word = word

    def _match_impl(self, i: int, tokens: List[str]) -> Optional[Tuple[int, int]]:
        return (i, i + 1) if tokens[i] == self._word else None


class MultiWordMatcher(BaseMatcher):
    def __init__(self, *words):
        self._words = set(words)

    def _match_impl(self, i: int, tokens: List[str]) -> Optional[Tuple[int, int]]:
        return (i, i + 1) if tokens[i] in self._words else None

    def extend(self, *new_words):
        new_words = self._words | set(new_words)
        return MultiWordMatcher(*new_words)

    def __or__(self, matcher: "MultiWordMatcher") -> "MultiWordMatcher":
        assert isinstance(matcher, MultiWordMatcher)
        return MultiWordMatcher(*(self._words | matcher._words))


def cast_to_matcher(matcher: Union[str, Iterable[str], BaseMatcher]) -> BaseMatcher:
    if isinstance(matcher, str):
        return SingleWordMatcher(matcher)
    try:
        if all(isinstance(x, str) for x in matcher):
            return MultiWordMatcher(*matcher)
    except TypeError:
        pass
    return matcher


class SeqMatcher(BaseMatcher):
    def __init__(self, *matchers):
        self._matchers = [cast_to_matcher(matcher) for matcher in matchers]

    def _match_impl(self, i: int, tokens: List[str]) -> Optional[Tuple[int, int]]:
        start = i
        j = 0
        while i < len(tokens):
            match = self._matchers[j].match(i, tokens)
            if match is None:
                return None
            i = match[1]
            j += 1
            if j == len(self._matchers):
                return start, match[1]
        return None


class DistanceMatcher(BaseMatcher):
    def __init__(
        self,
        distances: List[int],
        matcher1: Union[str, BaseMatcher],
        matcher2: Union[str, BaseMatcher],
    ):
        assert all(x < y for x, y in zip(distances[:-1], distances[1:]))
        self._distances = distances
        self._matcher1 = cast_to_matcher(matcher1)
        self._matcher2 = cast_to_matcher(matcher2)

    def _match_impl(self, i: int, tokens: List[str]) -> Optional[Tuple[int, int]]:
        match1 = self._matcher1.match(i, tokens)
        if match1 is None:
            return None
        for j in self._distances:
            k = match1[1] + j
            if k >= len(tokens):
                break
            match2 = self._matcher2.match(k, tokens)
            if match2 is not None:
                return i, match2[1]
        return None


def make_distance_matcher(
    max_distance: int,
    matcher1: Union[str, BaseMatcher],
    matcher2: Union[str, BaseMatcher],
    min_distance: int = 0,
) -> DistanceMatcher:
    return DistanceMatcher(
        list(range(min_distance, max_distance + 1)), matcher1, matcher2
    )


class FirstMatcher(BaseMatcher):
    def __init__(self, *matchers):
        self._matchers = [cast_to_matcher(matcher) for matcher in matchers]

    def _match_impl(self, i: int, tokens: List[str]) -> Optional[Tuple[int, int]]:
        for matcher in self._matchers:
            match = matcher.match(i, tokens)
            if match is not None:
                return match
        return None
