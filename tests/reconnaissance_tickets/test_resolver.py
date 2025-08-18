import logging
import pytest
import os

from app.schemas.ticket_interprete import TicketInterprete
from app.services.tickets.reconnaissance_tickets.resolver import extrait_ticket_scanne


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SOURCE = "tests/reconnaissance_tickets/data/source"
TARGET = "tests/reconnaissance_tickets/data/expected"


def load_test_cases():
    testfiles = [
        ("sample-crf-city.md", "sample-crf-city.json"),
        ("sample-crf-market.md", "sample-crf-market.json"),
        (
            "sample-crf-market-plusieurs-produits.md",
            "sample-crf-market-plusieurs-produits.json",
        ),
        ("autre.md", None),  # pas de JSON attendu car résultat attendu = None
    ]
    cases = []
    for mdfile, jsonfile in testfiles:
        with open(os.path.join(SOURCE, mdfile), encoding="utf-8") as f:
            md_content = f.read()
        expected_TicketScanne = None
        if jsonfile:
            try:
                with open(os.path.join(TARGET, jsonfile), encoding="utf-8") as f:
                    expected_TicketScanne = TicketInterprete.model_validate_json(
                        f.read()
                    )
            except Exception as e:
                logger.error(e)
                pass  # on ne fait rien, expected_TicketScanne est déjà à None
        cases.append((md_content, expected_TicketScanne))
    return cases


@pytest.mark.parametrize("markdown,expected_TicketScanne", load_test_cases())
def test_extrait_ticket_scanne(markdown, expected_TicketScanne):
    resultat = extrait_ticket_scanne(markdown)
    if expected_TicketScanne is None:
        assert resultat is None
    else:
        assert resultat.model_dump() == expected_TicketScanne.model_dump()
