import random
from collections import defaultdict
from functools import lru_cache

from PIL import Image, ImageDraw

PALETTE = {
    "sky": "#101b2a",
    "panel": "#17283a",
    "ink": "#f4dfb5",
    "muted": "#a7b7b6",
    "accent": "#e8b45d",
    "blue": "#72b5ca",
    "rule": "#395063",
    "outline": "#171d2c",
}
SCENE_SIZE = {"wide": (900, 620), "mobile": (480, 620)}


@lru_cache(maxsize=2)
def _pixels(mobile):
    w = 160 if mobile else 300
    h = 207
    im = Image.new("RGB", (w, h), PALETTE["sky"])
    d = ImageDraw.Draw(im)
    r = random.Random(502)
    cx = w // 2 if mobile else 100

    def rect(x0, y0, x1, y1, c):
        d.rectangle((x0, y0, x1, y1), fill=c)

    def poly(points, c):
        d.polygon(points, fill=c)

    def ellipse(box, c):
        d.ellipse(box, fill=c)

    for y, c in [(86, "#18253a"), (100, "#1d3043"), (113, "#23394a")]:
        rect(0, y, w, y + 16, c)
    for i in range(100 if not mobile else 55):
        x = r.randrange(w)
        y = r.randrange(5, 111)
        c = r.choice(["#697b88", "#97a49f", "#d1bb8f", "#536b7b"])
        rect(x, y, x + (i % 19 == 0), y, c)
    for x, y in [(cx - 113, 28), (cx + 105, 44), (cx - 83, 62), (cx + 54, 19)]:
        if 4 < x < w - 4:
            rect(x - 2, y, x + 2, y, "#c9c4a6")
            rect(x, y - 2, x, y + 2, "#c9c4a6")
    ellipse((cx + 39, 12, cx + 69, 42), "#e4d6ab")
    ellipse((cx + 46, 9, cx + 73, 35), PALETTE["sky"])
    for x, y, s in [
        (cx - 130, 105, 1),
        (cx + 100, 96, 1),
        (cx - 100, 129, 1),
        (cx + 130, 135, 1),
    ]:
        poly(
            [
                (x - 13, y),
                (x - 8, y - 4),
                (x + 7, y - 4),
                (x + 14, y),
                (x + 8, y + 4),
                (x - 6, y + 5),
            ],
            "#314b58",
        )
        rect(x - 7, y - 5, x + 7, y - 4, "#516b69")
    if mobile:
        poly(
            [(119, 111), (119, 73), (124, 66), (146, 66), (152, 74), (152, 111)],
            "#263442",
        )
        poly(
            [(122, 108), (122, 76), (126, 70), (144, 70), (149, 76), (149, 108)],
            "#6c6060",
        )
        poly(
            [
                (116, 75),
                (123, 64),
                (129, 61),
                (144, 63),
                (154, 74),
                (150, 76),
                (143, 69),
                (126, 68),
                (120, 77),
            ],
            "#516875",
        )
        ellipse((127, 75, 144, 92), "#3b4852")
        ellipse((130, 78, 141, 89), "#91b4ae")
        rect(135, 78, 136, 89, "#6d6b62")
        rect(130, 83, 141, 84, "#6d6b62")
        rect(126, 97, 146, 99, "#493e43")
        rect(128, 101, 133, 107, "#e6bb7d")
        rect(140, 101, 145, 107, "#e6bb7d")
        rect(135, 52, 136, 63, "#b6aa8c")
        poly([(136, 52), (146, 55), (136, 58)], "#d99a78")
    poly(
        [
            (cx - 76, 139),
            (cx - 66, 126),
            (cx + 67, 126),
            (cx + 82, 143),
            (cx + 65, 158),
            (cx + 48, 164),
            (cx + 39, 179),
            (cx + 18, 183),
            (cx + 7, 199),
            (cx - 10, 187),
            (cx - 30, 182),
            (cx - 49, 170),
            (cx - 65, 165),
        ],
        "#1a2635",
    )
    poly(
        [
            (cx - 76, 139),
            (cx - 59, 133),
            (cx + 64, 133),
            (cx + 82, 143),
            (cx + 67, 149),
            (cx + 54, 161),
            (cx + 37, 164),
            (cx + 25, 181),
            (cx + 8, 184),
            (cx - 5, 195),
            (cx - 20, 179),
            (cx - 37, 176),
            (cx - 47, 165),
            (cx - 62, 161),
        ],
        "#38404a",
    )
    poly(
        [
            (cx - 65, 147),
            (cx - 45, 149),
            (cx - 35, 160),
            (cx - 16, 159),
            (cx - 4, 170),
            (cx + 17, 169),
            (cx + 33, 159),
            (cx + 53, 156),
            (cx + 66, 146),
            (cx + 55, 165),
            (cx + 38, 168),
            (cx + 25, 181),
            (cx + 8, 184),
            (cx - 5, 195),
            (cx - 20, 179),
            (cx - 37, 176),
            (cx - 47, 165),
        ],
        "#575058",
    )
    for i in range(200):
        x = r.randrange(cx - 70, cx + 70)
        y = r.randrange(142, 185)
        if 0 <= x < w and im.getpixel((x, y)) in [(56, 64, 74), (87, 80, 88)]:
            rect(
                x,
                y,
                x + r.randrange(1, 4),
                y,
                r.choice(["#404652", "#68605e", "#303a47", "#777069"]),
            )
    poly(
        [
            (cx - 79, 137),
            (cx - 69, 130),
            (cx - 52, 125),
            (cx + 56, 125),
            (cx + 75, 134),
            (cx + 80, 141),
            (cx + 59, 145),
            (cx + 30, 140),
            (cx + 1, 146),
            (cx - 30, 142),
            (cx - 56, 146),
        ],
        "#718777",
    )
    poly(
        [
            (cx - 79, 137),
            (cx - 65, 132),
            (cx - 48, 129),
            (cx + 58, 129),
            (cx + 75, 136),
            (cx + 59, 140),
            (cx + 31, 136),
            (cx + 1, 142),
            (cx - 30, 138),
            (cx - 56, 142),
        ],
        "#a0a38a",
    )
    poly(
        [
            (cx - 37, 123),
            (cx - 36, 58),
            (cx - 29, 53),
            (cx - 27, 40),
            (cx - 18, 34),
            (cx + 21, 36),
            (cx + 28, 49),
            (cx + 34, 54),
            (cx + 37, 123),
            (cx + 25, 136),
            (cx - 23, 138),
        ],
        "#2b303b",
    )
    poly(
        [
            (cx - 31, 122),
            (cx - 30, 59),
            (cx - 24, 55),
            (cx - 23, 43),
            (cx - 16, 39),
            (cx + 18, 41),
            (cx + 22, 53),
            (cx + 29, 58),
            (cx + 31, 121),
            (cx + 22, 131),
            (cx - 23, 132),
        ],
        "#8c7168",
    )
    poly(
        [
            (cx - 42, 59),
            (cx - 36, 53),
            (cx - 34, 37),
            (cx - 28, 27),
            (cx - 22, 20),
            (cx - 14, 19),
            (cx - 3, 24),
            (cx + 12, 29),
            (cx + 24, 37),
            (cx + 32, 49),
            (cx + 41, 56),
            (cx + 39, 62),
            (cx + 28, 58),
            (cx + 18, 50),
            (cx + 13, 42),
            (cx - 22, 40),
            (cx - 28, 53),
            (cx - 37, 64),
        ],
        "#1b2838",
    )
    poly(
        [
            (cx - 37, 57),
            (cx - 33, 40),
            (cx - 28, 30),
            (cx - 21, 25),
            (cx - 14, 24),
            (cx - 4, 29),
            (cx + 12, 34),
            (cx + 22, 42),
            (cx + 31, 54),
            (cx + 25, 52),
            (cx + 17, 44),
            (cx + 12, 39),
            (cx - 21, 37),
            (cx - 28, 51),
        ],
        "#4e5e66",
    )
    for y in [33, 37, 41, 45, 49, 53]:
        for x in range(cx - 28 + (y - 33) // 2, cx + 21 - (y - 33) // 3, 6):
            if im.getpixel((x, y)) == (78, 94, 102):
                rect(x, y, x + 3, y, "#73817a" if (x + y) % 3 else "#a0a292")
    rect(cx - 4, 16, cx + 2, 27, "#384551")
    rect(cx - 3, 13, cx + 1, 17, "#c9a378")
    for x in [cx - 31, cx - 8, cx + 27]:
        rect(x, 57, x + 3, 126, "#3c343b")
        rect(x + 1, 57, x + 1, 125, "#b18b72")
    for y in [61, 88, 120]:
        rect(cx - 30, y, cx + 29, y + 3, "#403942")
        rect(cx - 30, y, cx + 29, y, "#c09a79")
    for x, y in [(cx - 25, 68), (cx + 9, 96)]:
        rect(x - 2, y - 2, x + 14, y + 17, "#41373a")
        rect(x, y, x + 12, y + 14, "#edb86e")
        rect(x + 1, y + 1, x + 11, y + 7, "#ffe3a0")
        rect(x + 6, y, x + 7, y + 14, "#775b4b")
        rect(x, y + 8, x + 12, y + 9, "#775b4b")
        rect(x - 3, y + 16, x + 15, y + 18, "#b39677")
    rect(cx - 26, 95, cx - 10, 114, "#494249")
    rect(cx - 24, 97, cx - 12, 112, "#736559")
    for yy in (101, 107, 112):
        rect(cx - 25, yy, cx - 11, yy + 1, "#c09e7c")
    for xx, yy, col in [
        (cx - 23, 97, "#d9a989"),
        (cx - 19, 98, "#9fb3a0"),
        (cx - 16, 96, "#e2c38c"),
        (cx - 23, 103, "#bac2a4"),
        (cx - 18, 103, "#e1c990"),
        (cx - 14, 104, "#bd8f7b"),
        (cx - 22, 109, "#dab98b"),
        (cx - 16, 108, "#9aafa2"),
    ]:
        rect(xx, yy, xx + 2, yy + 3, col)
    ellipse((cx + 2, 66, cx + 20, 84), "#4a4044")
    ellipse((cx + 4, 68, cx + 18, 82), "#e1b77e")
    ellipse((cx + 6, 70, cx + 16, 80), "#83a6a0")
    rect(cx + 10, 70, cx + 11, 80, "#6c6156")
    rect(cx + 6, 74, cx + 16, 75, "#6c6156")
    rect(cx - 30, 87, cx + 26, 87, "#dabd96")
    for xx, yy, col in [
        (cx - 25, 87, "#d6b0a0"),
        (cx - 18, 87, "#a6bcb0"),
        (cx + 15, 87, "#ead9ae"),
        (cx + 21, 87, "#cda994"),
    ]:
        rect(xx, yy, xx + 3, yy + 4, col)
        rect(xx + 1, yy - 1, xx + 1, yy, "#6d5a51")
    ellipse((cx - 9, 44, cx + 9, 62), "#403943")
    ellipse((cx - 7, 46, cx + 7, 60), "#ffd995")
    rect(cx - 1, 46, cx + 1, 60, "#856953")
    rect(cx - 7, 52, cx + 7, 54, "#856953")
    rect(cx - 6, 100, cx + 6, 130, "#3a3135")
    rect(cx - 4, 102, cx + 4, 128, "#73574e")
    rect(cx + 2, 116, cx + 3, 117, "#f2cc85")
    for i in range(4):
        rect(
            cx - 9 - i * 2,
            130 + i * 3,
            cx + 10 + i * 2,
            132 + i * 3,
            ["#bdac8d", "#817e71"][i % 2],
        )
    rect(cx + 36, 92, cx + 50, 128, "#665b58")
    rect(cx + 33, 88, cx + 53, 93, "#373a43")
    rect(cx + 37, 97, cx + 48, 111, "#e8b978")
    rect(cx + 42, 97, cx + 43, 111, "#55454a")
    poly([(cx + 35, 89), (cx + 43, 78), (cx + 53, 89)], "#647579")
    rect(cx + 43, 68, cx + 45, 81, "#ad9573")
    poly([(cx + 43, 72), (cx + 54, 64), (cx + 56, 67), (cx + 45, 75)], "#e0be80")

    def tree(x, y, scale=1):
        rect(x - 2, y - 24, x + 2, y, "#5e514c")
        poly(
            [
                (x - 14, y - 14),
                (x - 12, y - 24),
                (x - 7, y - 27),
                (x - 8, y - 34),
                (x - 1, y - 40),
                (x + 7, y - 36),
                (x + 9, y - 29),
                (x + 14, y - 26),
                (x + 15, y - 17),
                (x + 10, y - 12),
                (x + 2, y - 13),
                (x - 5, y - 10),
            ],
            "#304b4c",
        )
        for j in range(22):
            xx = x + r.randrange(-11, 12)
            yy = y - r.randrange(16, 35)
            if 0 <= xx < w and im.getpixel((xx, yy)) == (48, 75, 76):
                rect(
                    xx, yy, xx + 3, yy + 2, r.choice(["#48685f", "#58766a", "#728873"])
                )
        for xx, yy in [(x - 8, y - 23), (x + 5, y - 29), (x + 9, y - 17)]:
            rect(xx, yy, xx + 1, yy + 1, "#e5b77e")

    tree(cx - 58, 132)
    tree(cx + 65, 137)
    for x in range(cx - 70, cx + 72, 7):
        y = 140 + ((x // 7) % 3)
        if 0 < x < w:
            rect(x, y - 4, x + 1, y, "#d1bd93")
            rect(x - 2, y - 3, x + 3, y - 3, "#d1bd93")
    for x, y in [
        (cx - 48, 134),
        (cx - 42, 136),
        (cx + 53, 136),
        (cx + 58, 138),
        (cx - 17, 141),
        (cx + 20, 142),
    ]:
        rect(x, y - 5, x, y, "#566d58")
        rect(x - 1, y - 7, x + 1, y - 6, "#edc38d")
        rect(x - 2, y - 5, x, y - 4, "#cd8d7a")
    poly(
        [
            (cx - 16, 160),
            (cx - 16, 153),
            (cx - 12, 149),
            (cx + 12, 149),
            (cx + 16, 153),
            (cx + 16, 160),
        ],
        "#2b2932",
    )
    poly(
        [
            (cx - 13, 160),
            (cx - 13, 154),
            (cx - 10, 152),
            (cx + 10, 152),
            (cx + 13, 154),
            (cx + 13, 160),
        ],
        "#e8b574",
    )
    rect(cx - 1, 152, cx + 1, 160, "#73574c")
    rect(cx - 13, 157, cx + 13, 158, "#73574c")
    rect(cx - 34, 54, cx - 32, 96, "#493f40")
    rect(cx - 43, 56, cx - 32, 58, "#71594f")
    poly(
        [(cx - 47, 51), (cx - 43, 47), (cx - 39, 51), (cx - 39, 58), (cx - 47, 58)],
        "#9e866e",
    )
    ellipse((cx - 46, 49, cx - 40, 55), "#d4b488")
    rect(cx - 43, 43, cx - 42, 49, "#b19c80")
    rect(cx - 44, 59, cx - 44, 84, "#c3b092")
    rect(cx - 47, 83, cx - 41, 89, "#65554b")
    rect(cx - 46, 84, cx - 42, 88, "#edc37e")
    rect(cx - 45, 82, cx - 43, 90, "#ffdf9b")
    poly(
        [(cx + 6, 35), (cx + 6, 25), (cx + 11, 20), (cx + 19, 23), (cx + 22, 35)],
        "#3c4b54",
    )
    poly(
        [(cx + 8, 34), (cx + 8, 26), (cx + 12, 23), (cx + 18, 25), (cx + 20, 34)],
        "#9b8273",
    )
    rect(cx + 11, 27, cx + 16, 32, "#efc78a")
    rect(cx + 13, 27, cx + 13, 32, "#7f695c")
    rect(cx - 20, 21, cx - 16, 31, "#58656a")
    rect(cx - 22, 19, cx - 15, 22, "#a08a78")
    for xx, yy in [
        (cx - 21, 17),
        (cx - 23, 15),
        (cx - 21, 13),
        (cx - 17, 12),
        (cx - 15, 10),
        (cx - 17, 8),
    ]:
        rect(xx, yy, xx + 2, yy + 1, "#4f6170")
    poly([(cx - 50, 105), (cx - 33, 99), (cx - 29, 104), (cx - 46, 111)], "#303944")
    poly([(cx - 49, 104), (cx - 34, 99), (cx - 32, 102), (cx - 47, 108)], "#9b7667")
    for i in range(4):
        x = cx - 47 + i * 4
        rect(x, 104 - i, x + 1, 107 - i, "#d7ab86")
    rect(cx - 48, 109, cx - 47, 129, "#65534a")
    rect(cx - 45, 117, cx - 33, 118, "#473e3d")
    for x, c in [(cx - 44, "#9cb4a0"), (cx - 40, "#e6c885"), (cx - 36, "#a4b1ad")]:
        rect(x, 113, x + 2, 116, c)
        rect(x + 1, 111, x + 1, 112, "#d6c19c")
    for x, y in [
        (cx + 27, 121),
        (cx + 26, 115),
        (cx + 29, 109),
        (cx + 26, 104),
        (cx + 30, 98),
        (cx + 27, 92),
        (cx + 29, 85),
        (cx - 29, 90),
        (cx - 31, 84),
        (cx - 28, 79),
    ]:
        rect(x, y, x + 1, y + 5, "#506958")
        rect(x - 2, y + 1, x, y + 2, "#738671")
        rect(x + 2, y - 1, x + 4, y, "#71846c")
    rect(cx + 33, 104, cx + 36, 105, "#343941")
    rect(cx + 36, 105, cx + 36, 112, "#b6a184")
    rect(cx + 34, 112, cx + 38, 118, "#51464a")
    rect(cx + 35, 113, cx + 37, 116, "#ffe1a0")
    rect(cx + 41, 124, cx + 60, 126, "#6b574e")
    rect(cx + 43, 126, cx + 44, 132, "#4d4441")
    rect(cx + 57, 126, cx + 58, 132, "#4d4441")
    rect(cx + 46, 119, cx + 52, 123, "#9ab0a1")
    rect(cx + 47, 117, cx + 51, 118, "#b6c3aa")
    rect(cx + 52, 120, cx + 54, 121, "#d0c6a4")
    for x, y in [
        (cx - 63, 138),
        (cx - 36, 141),
        (cx + 32, 139),
        (cx + 49, 141),
        (cx - 7, 144),
        (cx + 12, 144),
    ]:
        rect(x, y, x + 4, y + 1, "#c4c0a2")
        rect(x + 1, y - 1, x + 3, y - 1, "#e0cfaa")
    for x, y in [(cx - 68, 134), (cx - 54, 138), (cx + 59, 133), (cx + 69, 137)]:
        rect(x, y - 4, x, y, "#597b63")
        rect(x - 2, y - 3, x + 2, y - 2, "#92a783")
        rect(x - 1, y - 6, x + 1, y - 5, "#e9d29a")
    if not mobile:
        for i in range(18):
            x = 160 + i * 3
            yy = 125 - i // 3
            rect(x, yy, x + 2, yy + 1, "#d0ad7e")
            rect(x, yy + 3, x + 1, yy + 5, "#574c4b")
            if i % 3 == 0:
                rect(x, yy - 5, x, yy + 4, "#c6ab86")
        poly(
            [
                (180, 139),
                (193, 130),
                (250, 128),
                (270, 137),
                (258, 151),
                (245, 155),
                (232, 173),
                (219, 161),
                (204, 160),
                (191, 153),
            ],
            "#293542",
        )
        poly(
            [
                (183, 137),
                (195, 131),
                (248, 130),
                (267, 136),
                (256, 145),
                (239, 145),
                (228, 151),
                (213, 146),
                (198, 148),
            ],
            "#879783",
        )
        poly(
            [
                (187, 141),
                (206, 144),
                (218, 143),
                (229, 149),
                (242, 144),
                (257, 144),
                (248, 156),
                (233, 159),
                (229, 170),
                (219, 157),
                (205, 156),
            ],
            "#58565a",
        )
        for i in range(85):
            xx = r.randrange(188, 258)
            yy = r.randrange(142, 164)
            if im.getpixel((xx, yy)) == (88, 86, 90):
                rect(
                    xx,
                    yy,
                    xx + r.randrange(1, 4),
                    yy,
                    r.choice(["#6e6662", "#444b53", "#837568"]),
                )
        poly(
            [
                (207, 133),
                (207, 90),
                (211, 84),
                (210, 65),
                (216, 56),
                (244, 59),
                (248, 68),
                (247, 89),
                (253, 93),
                (252, 132),
                (242, 140),
                (218, 141),
            ],
            "#293341",
        )
        poly(
            [
                (211, 131),
                (211, 93),
                (216, 88),
                (214, 68),
                (218, 61),
                (240, 64),
                (243, 70),
                (242, 91),
                (249, 95),
                (248, 130),
                (240, 135),
                (219, 136),
            ],
            "#826b63",
        )
        poly(
            [
                (207, 68),
                (211, 57),
                (217, 51),
                (241, 55),
                (249, 67),
                (245, 69),
                (238, 63),
                (216, 60),
                (211, 70),
            ],
            "#445964",
        )
        for y in (96, 116):
            rect(211, y, 248, y + 2, "#473d40")
            rect(211, y, 248, y, "#c8a384")
        for x in (212, 229, 246):
            rect(x, 92, x + 2, 132, "#4b3e41")
            rect(x, y - 17, x, y + 10, "#b39479")
        ellipse((217, 66, 240, 89), "#384451")
        ellipse((220, 69, 237, 86), "#c9ad80")
        ellipse((222, 71, 235, 84), "#77a5a5")
        ellipse((225, 73, 233, 81), "#d8d9ba")
        rect(228, 69, 229, 86, "#786d61")
        rect(221, 77, 236, 78, "#786d61")
        poly([(216, 101), (226, 99), (226, 115), (216, 117)], "#eec589")
        rect(219, 103, 223, 111, "#fff0b2")
        poly([(215, 101), (211, 99), (211, 117), (215, 115)], "#513d3b")
        rect(237, 101, 245, 112, "#eec589")
        rect(240, 101, 241, 112, "#715749")
        rect(228, 41, 230, 54, "#b4a38a")
        poly([(230, 42), (243, 45), (230, 48)], "#d99674")
        rect(250, 105, 255, 106, "#5b514d")
        rect(255, 106, 255, 112, "#c6ad84")
        rect(253, 112, 257, 118, "#594d49")
        rect(254, 113, 256, 116, "#ffe29d")
        for xx, yy in [(192, 122), (201, 115), (257, 89), (263, 102), (190, 95)]:
            rect(xx, yy, xx + 1, yy + 1, "#e8cf9b")
        for i in range(5):
            rect(192 + i * 3, 143 + i * 3, 198 + i * 3, 144 + i * 3, "#d3b894")
        rect(217, 151, 235, 157, "#373238")
        rect(220, 152, 232, 156, "#e5b477")
        rect(225, 152, 226, 156, "#786155")
        poly(
            [
                (162, 178),
                (181, 169),
                (199, 174),
                (216, 169),
                (235, 178),
                (219, 184),
                (199, 181),
                (180, 185),
            ],
            "#2b3440",
        )
        poly(
            [
                (166, 175),
                (182, 168),
                (199, 173),
                (216, 168),
                (232, 175),
                (216, 181),
                (199, 177),
                (182, 182),
            ],
            "#d5c3a0",
        )
        poly([(168, 175), (182, 170), (197, 174), (197, 178), (182, 180)], "#ede0bd")
        poly([(201, 174), (216, 170), (230, 175), (216, 179), (201, 178)], "#ede0bd")
        for x, y in [(175, 174), (180, 173), (210, 174), (215, 175)]:
            rect(x, y, x + 5, y, "#9e9b88")
        rect(199, 174, 199, 181, "#a88c74")
        rect(274, 117, 291, 121, "#5b6870")
        poly([(272, 120), (293, 120), (289, 127), (278, 127)], "#c18f70")
        rect(280, 109, 286, 119, "#eacb95")
        rect(282, 106, 283, 109, "#786f6a")
        rect(277, 122, 289, 123, "#ead2a3")
        for xx, yy in [(278, 129), (286, 132), (291, 130)]:
            rect(xx, yy, xx + 1, yy + 1, "#e9c68e")
    if mobile:
        poly(
            [
                (2, 178),
                (13, 173),
                (24, 176),
                (34, 173),
                (44, 179),
                (34, 183),
                (24, 181),
                (13, 184),
            ],
            "#2b3440",
        )
        poly(
            [
                (3, 177),
                (13, 172),
                (24, 175),
                (34, 172),
                (43, 177),
                (34, 181),
                (24, 178),
                (13, 182),
            ],
            "#e3d5b3",
        )
        rect(24, 175, 24, 181, "#a88c74")
        rect(9, 177, 17, 177, "#a39d88")
        rect(29, 176, 36, 176, "#a39d88")
        poly([(135, 158), (156, 158), (152, 165), (141, 165)], "#c18f70")
        rect(142, 149, 148, 157, "#eacb95")
        rect(144, 146, 145, 149, "#786f6a")
        rect(140, 160, 152, 161, "#ead2a3")
        for xx, yy in [(140, 168), (149, 170), (155, 167)]:
            rect(xx, yy, xx + 1, yy + 1, "#e9c68e")
    return im


def render_scene(mobile=False, motion="ambient"):
    if motion not in ("none", "ambient", "character"):
        raise ValueError("unknown motion")
    width, height = SCENE_SIZE["mobile" if mobile else "wide"]
    im = _pixels(mobile)
    paths = defaultdict(list)
    for y in range(im.height):
        x = 0
        while x < im.width:
            color = im.getpixel((x, y))
            end = x + 1
            while end < im.width and im.getpixel((end, y)) == color:
                end += 1
            paths[color].append(f"M{x} {y}h{end - x}v1H{x}z")
            x = end
    art = "".join(
        f'<path fill="#{c[0]:02x}{c[1]:02x}{c[2]:02x}" d="{"".join(p)}"/>'
        for c, p in paths.items()
    )
    animations = """<style>@keyframes pw-glow{0%,100%{opacity:.2}50%{opacity:.85}}@keyframes pw-walk{0%,100%{transform:translateX(0)}50%{transform:translateX(6px)}}@keyframes pw-drift{0%,100%{transform:translate(0,0)}50%{transform:translate(2px,-3px)}}@media (prefers-reduced-motion:no-preference){.pw-glow{animation:pw-glow 4s ease-in-out infinite}.pw-fly{animation:pw-drift 5s ease-in-out infinite}.pw-walk{animation:pw-walk 4s steps(6) infinite}}@media (prefers-reduced-motion:reduce){.pw-glow,.pw-fly,.pw-walk{animation:none}}</style>"""
    cx = im.width // 2 if mobile else 100
    lights = "".join(
        f'<rect class="pw-glow" x="{cx + x}" y="{y}" width="2" height="2" fill="#fff1b2"/>'
        for x, y in [(-55, 118), (58, 120), (-33, 99), (52, 82)]
    )
    keeper = f'''<g transform="translate({cx - 42} 127)"><g class="{"pw-walk" if motion == "character" else "pw-keeper"}"><path fill="#d0c7ad" d="M-4-9h1v4h-1z M4-9h1v4h-1z"/><path fill="#e2d2ad" d="M-5-5l2-2h6l2 2v6l-3 2h-5l-2-2z"/><path fill="#303544" d="M-3-3h2v2h-2z M2-3h2v2h-2z"/><path fill="#665958" d="M-2 3h2v2h-2z M2 3h2v2h-2z"/></g></g>'''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {im.width} 207" shape-rendering="crispEdges"><title>A tiny midnight workshop on a floating island</title>{animations if motion != "none" else ""}{art}{keeper}{lights if motion != "none" else ""}</svg>'


if __name__ == "__main__":
    from pathlib import Path

    out = Path("/Volumes/RAID0/Codex/profile-typography/pixel-scene-prototypes")
    out.mkdir(parents=True, exist_ok=True)
    for mobile in (False, True):
        name = "mobile" if mobile else "wide"
        preview = _pixels(mobile).copy()
        d = ImageDraw.Draw(preview)
        x = (preview.width // 2 if mobile else 100) - 42
        y = 127
        d.rectangle((x - 4, y - 9, x - 3, y - 5), fill="#d0c7ad")
        d.rectangle((x + 4, y - 9, x + 5, y - 5), fill="#d0c7ad")
        d.polygon(
            [
                (x - 5, y - 5),
                (x - 3, y - 7),
                (x + 3, y - 7),
                (x + 5, y - 5),
                (x + 5, y + 1),
                (x + 2, y + 3),
                (x - 3, y + 3),
                (x - 5, y + 1),
            ],
            fill="#e2d2ad",
        )
        d.rectangle((x - 3, y - 3, x - 2, y - 2), fill="#303544")
        d.rectangle((x + 2, y - 3, x + 3, y - 2), fill="#303544")
        preview.resize(SCENE_SIZE[name], Image.Resampling.NEAREST).save(
            out / f"{name}.png"
        )
        for motion in ("none", "ambient", "character"):
            (out / f"{name}-{motion}.svg").write_text(render_scene(mobile, motion))
    for mobile in (False, True):
        name = "mobile" if mobile else "wide"
        base = _pixels(mobile)
        cx = base.width // 2 if mobile else 100
        for mode in ("ambient", "character"):
            frames = []
            for frame in range(12):
                pic = base.copy()
                d = ImageDraw.Draw(pic)
                shift = (
                    (frame if frame < 6 else 12 - frame) if mode == "character" else 0
                )
                x = cx - 42 + shift
                y = 127
                d.rectangle((x - 4, y - 9, x - 3, y - 5), fill="#d0c7ad")
                d.rectangle((x + 4, y - 9, x + 5, y - 5), fill="#d0c7ad")
                d.polygon(
                    [
                        (x - 5, y - 5),
                        (x - 3, y - 7),
                        (x + 3, y - 7),
                        (x + 5, y - 5),
                        (x + 5, y + 1),
                        (x + 2, y + 3),
                        (x - 3, y + 3),
                        (x - 5, y + 1),
                    ],
                    fill="#e2d2ad",
                )
                d.rectangle((x - 3, y - 3, x - 2, y - 2), fill="#303544")
                d.rectangle((x + 2, y - 3, x + 3, y - 2), fill="#303544")
                if frame in range(3, 10):
                    for dx, yy in [(-55, 118), (58, 120), (-33, 99), (52, 82)]:
                        d.rectangle((cx + dx, yy, cx + dx + 1, yy + 1), fill="#fff1b2")
                frames.append(pic.resize(SCENE_SIZE[name], Image.Resampling.NEAREST))
            frames[0].save(
                out / f"{name}-{mode}.gif",
                save_all=True,
                append_images=frames[1:],
                duration=330,
                loop=0,
                optimize=True,
            )
