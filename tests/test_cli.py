from weather_agent.cli import build_parser


def test_parser_accepts_city() -> None:
    args = build_parser().parse_args(["Berlin"])
    assert args.city == "Berlin"
    assert args.model == "gpt-4o-mini"
