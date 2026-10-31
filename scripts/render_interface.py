from pathlib import Path

ROOT = Path(__file__).parents[1]


def svg(width, height, body, title, background="#101010"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
    <title>{title}</title><rect width="{width}" height="{height}" fill="{background}"/>
    <g font-family="Arial,sans-serif">{body}</g></svg>'''


def chapter(number, title, subtitle):
    return svg(
        900,
        150,
        f"""<path d="M0 0H900" stroke="#f04416" stroke-width="9"/>
    <text x="24" y="106" fill="#f04416" font-size="104" font-weight="900">{number}</text>
    <text x="183" y="84" fill="#f4f1e9" font-size="63" font-weight="900">{title}</text>
    """,
        f"{title}. {subtitle}",
    )


def destination(name, subtitle, accent, width=440):
    lines = name.split() if name == "NUMBER THEORY" else [name]
    labels = "".join(
        f'<text x="24" y="{72 + index * 58 if len(lines) > 1 else 105}" fill="#f4f1e9" font-size="56" font-weight="900">{line}</text>'
        for index, line in enumerate(lines)
    )
    return svg(
        width,
        170,
        f'''<path d="M0 0H{width}" stroke="{accent}" stroke-width="12"/>
    {labels}
    <path d="M{width - 70} 137H{width - 26}m-14 -13 14 13-14 13" fill="none" stroke="{accent}" stroke-width="4"/>''',
        f"{name}. {subtitle}",
    )


def main():
    assets = ROOT / "assets"
    for number, name, title, subtitle in [
        ("01", "math", "MATHEMATICS", "NOTES / PROOFS / EXPERIMENTS"),
        ("02", "software", "SOFTWARE", "TOOLS FOR MY DEGREE AND RESEARCH"),
        ("03", "public-work", "PUBLIC WORK", "PUBLIC RECORDS / EXPLICIT DEFINITIONS"),
    ]:
        (assets / f"chapter-{name}.svg").write_text(chapter(number, title, subtitle))
    for name, title, subtitle, accent in [
        ("algebra", "ALGEBRA", "Structure + symmetry", "#f04416"),
        ("calculus", "CALCULUS", "Change + geometry", "#dfff00"),
        ("probability", "PROBABILITY", "Reason about uncertainty", "#dfff00"),
        ("numbertheory", "NUMBER THEORY", "Patterns in the integers", "#f04416"),
        ("calculator", "CALCULATOR", "Notebooks / sign-in required", "#f04416"),
    ]:
        (assets / f"enter-{name}.svg").write_text(
            destination(title, subtitle, accent, 900 if name == "calculator" else 440)
        )
    for name, title, number in [
        ("explore", "EXPLORE", "01"),
        ("build", "BUILD", "02"),
        ("contribute", "CONTRIBUTE", "03"),
    ]:
        body = f'<text x="16" y="42" font-size="25" fill="#101010">{number}</text><text x="16" y="99" fill="#101010" font-size="43" font-weight="900">{title}</text>'
        (assets / f"nav-{name}.svg").write_text(svg(300, 130, body, title, "#f04416"))
    exit_body = '<text x="28" y="102" fill="#101010" font-size="85" font-weight="900">JEROME QUECK</text><path d="M790 96H866m-25 -25 25 25-25 25" fill="none" stroke="#101010" stroke-width="7"/>'
    (assets / "exit.svg").write_text(
        svg(900, 145, exit_body, "Jerome Queck. Explore the website.", "#f04416")
    )


if __name__ == "__main__":
    main()
