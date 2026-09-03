from tools.check_distribution import forbidden_reason


def test_forbidden_validation_material_is_detected():
    assert forbidden_reason("package/data/trace.csv") is not None
    assert forbidden_reason("package/literature_sources/source.pdf") is not None
    assert forbidden_reason("package/source-figure.png") is not None
    assert forbidden_reason("package/validation_data/values.json") is not None


def test_code_and_source_metadata_are_allowed():
    assert forbidden_reason("package/src/pifira/lh2/spin.py") is None
    assert forbidden_reason("package/VALIDATION_SOURCES.md") is None
    assert forbidden_reason("package/CITATION.cff") is None
