"""Core detection and anonymization logic for French PII."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Callable, Iterable, Optional


Validator = Callable[[str], bool]


@dataclass(frozen=True)
class PIIMatch:
    """Represents one detected PII entity in a text."""

    entity_type: str
    text: str
    start: int
    end: int
    score: float = 1.0

    @property
    def type(self) -> str:
        """Backward-compatible alias for older examples."""
        return self.entity_type

    def to_dict(self) -> dict[str, object]:
        """Serialize the match to a JSON-friendly dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class _PatternRule:
    entity_type: str
    regex: re.Pattern[str]
    replacement: str
    validator: Optional[Validator] = None


def _digits(value: str) -> str:
    return re.sub(r"\D", "", value)


def _luhn_valid(value: str) -> bool:
    numbers = _digits(value)
    if len(numbers) < 13 or len(numbers) > 19:
        return False
    checksum = 0
    parity = len(numbers) % 2
    for idx, char in enumerate(numbers):
        digit = int(char)
        if idx % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def _iban_fr_valid(value: str) -> bool:
    compact = re.sub(r"\s+", "", value).upper()
    if not compact.startswith("FR") or len(compact) != 27:
        return False
    rearranged = compact[4:] + compact[:4]
    converted = []
    for ch in rearranged:
        if ch.isdigit():
            converted.append(ch)
        elif "A" <= ch <= "Z":
            converted.append(str(ord(ch) - 55))
        else:
            return False
    number = int("".join(converted))
    return number % 97 == 1


def _phone_fr_valid(value: str) -> bool:
    raw = re.sub(r"[.\s-]", "", value)
    if raw.startswith("+33"):
        return len(_digits(raw)) == 11
    if raw.startswith("0"):
        return len(_digits(raw)) == 10
    return False


RULES: tuple[_PatternRule, ...] = (
    _PatternRule(
        entity_type="EMAIL",
        regex=re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        replacement="[EMAIL]",
    ),
    _PatternRule(
        entity_type="PHONE_NUMBER",
        regex=re.compile(
            r"(?<!\w)(?:\+33[\s.-]?[1-9](?:[\s.-]?\d{2}){4}|0[1-9](?:[\s.-]?\d{2}){4})(?!\w)"
        ),
        replacement="[TELEPHONE]",
        validator=_phone_fr_valid,
    ),
    _PatternRule(
        entity_type="ADDRESS_FR",
        regex=re.compile(
            r"\b\d{1,4}\s*(?:bis|ter|quater)?\s+"
            r"(?:rue|avenue|av\.?|boulevard|bd\.?|chemin|impasse|allee|all[ée]e|route|place|quai)\s+"
            r"[A-Za-zÀ-ÖØ-öø-ÿ' -]{2,},?\s+\d{5}\s+[A-Za-zÀ-ÖØ-öø-ÿ' -]{2,}\b",
            flags=re.IGNORECASE,
        ),
        replacement="[ADRESSE]",
    ),
    _PatternRule(
        entity_type="IBAN",
        regex=re.compile(r"\bFR\d{2}(?:\s?\d{4}){5}\s?\d{3}\b", flags=re.IGNORECASE),
        replacement="[IBAN]",
        validator=_iban_fr_valid,
    ),
    _PatternRule(
        entity_type="NIR",
        regex=re.compile(r"\b[12]\s?\d{2}(?:\s?\d{2}){2}\s?\d{3}\s?\d{3}\s?\d{2}\b"),
        replacement="[NUMERO_SECURITE_SOCIALE]",
    ),
    _PatternRule(
        entity_type="SIRET",
        regex=re.compile(r"\b\d{3}\s?\d{3}\s?\d{3}\s?\d{5}\b"),
        replacement="[SIRET]",
    ),
    _PatternRule(
        entity_type="SIREN",
        regex=re.compile(r"\b\d{3}\s?\d{3}\s?\d{3}\b"),
        replacement="[SIREN]",
    ),
    _PatternRule(
        entity_type="CREDIT_CARD",
        regex=re.compile(r"\b(?:\d[ -]?){13,19}\b"),
        replacement="[CARTE_BANCAIRE]",
        validator=_luhn_valid,
    ),
    _PatternRule(
        entity_type="LICENSE_PLATE_FR",
        regex=re.compile(r"\b[A-Z]{2}-\d{3}-[A-Z]{2}\b"),
        replacement="[IMMATRICULATION]",
    ),
    _PatternRule(
        entity_type="DATE",
        regex=re.compile(
            r"\b(?:0?[1-9]|[12]\d|3[01])/(?:0?[1-9]|1[0-2])/(?:19|20)\d{2}\b"
        ),
        replacement="[DATE]",
    ),
)


def _resolve_overlaps(matches: Iterable[PIIMatch]) -> list[PIIMatch]:
    sorted_matches = sorted(matches, key=lambda m: (m.start, -(m.end - m.start)))
    resolved: list[PIIMatch] = []
    for match in sorted_matches:
        if not resolved:
            resolved.append(match)
            continue
        last = resolved[-1]
        overlap = match.start < last.end
        if not overlap:
            resolved.append(match)
            continue
        current_len = match.end - match.start
        last_len = last.end - last.start
        if current_len > last_len:
            resolved[-1] = match
    return resolved


class PIIDetector:
    """Regex-first French PII detector with deterministic anonymization."""

    def __init__(self, language: str = "fr") -> None:
        if language.lower() != "fr":
            raise ValueError("Only language='fr' is supported in this version.")
        self.language = "fr"
        self.rules = RULES

    def detect(self, text: str) -> list[PIIMatch]:
        """Detect PII entities in text."""
        candidates: list[PIIMatch] = []
        for rule in self.rules:
            for found in rule.regex.finditer(text):
                value = found.group(0)
                if rule.validator and not rule.validator(value):
                    continue
                candidates.append(
                    PIIMatch(
                        entity_type=rule.entity_type,
                        text=value,
                        start=found.start(),
                        end=found.end(),
                    )
                )
        return _resolve_overlaps(candidates)

    def anonymize(self, text: str) -> str:
        """Replace detected entities with stable placeholders."""
        matches = self.detect(text)
        if not matches:
            return text
        replacements = {rule.entity_type: rule.replacement for rule in self.rules}
        redacted = text
        for match in reversed(matches):
            placeholder = replacements.get(match.entity_type, "[PII]")
            redacted = redacted[: match.start] + placeholder + redacted[match.end :]
        return redacted
