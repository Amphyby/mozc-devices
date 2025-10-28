import math

class SVGGenerator:
    """SVGを作るためのクラス"""

    def __init__(self, width_mm=100, height_mm=100):
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.elements = []

    def circle(self, radius_mm):
        """半径radius_mmのなるべく細い円を書く"""
        self.elements.append(
            f'<circle cx="{self.width_mm / 2}" cy="{self.height_mm / 2}" r="{radius_mm}" stroke="black" stroke-width="0.1" fill="none" />'
        )

    def sector_ring(self, outer_radius_mm, inner_radius_mm, start_degree, end_degree):
        """outer_radius_mmの円から、inner_radius_mmの円を切り取り、start_degreeからend_degreeまでを取り出した扇形環を描く"""

        def polar_to_cartesian(radius, angle_in_degrees):
            angle_in_radians = (angle_in_degrees - 90) * math.pi / 180.0
            return (
                (self.width_mm / 2) + (radius * math.cos(angle_in_radians)),
                (self.height_mm / 2) + (radius * math.sin(angle_in_radians))
            )

        start_outer = polar_to_cartesian(outer_radius_mm, end_degree)
        end_outer = polar_to_cartesian(outer_radius_mm, start_degree)
        start_inner = polar_to_cartesian(inner_radius_mm, end_degree)
        end_inner = polar_to_cartesian(inner_radius_mm, start_degree)

        large_arc_flag = "1" if end_degree - start_degree > 180 else "0"

        path_data = [
            f"M {start_outer[0]} {start_outer[1]}",
            f"A {outer_radius_mm} {outer_radius_mm} 0 {large_arc_flag} 0 {end_outer[0]} {end_outer[1]}",
            f"L {end_inner[0]} {end_inner[1]}",
            f"A {inner_radius_mm} {inner_radius_mm} 0 {large_arc_flag} 1 {start_inner[0]} {start_inner[1]}",
            "Z"
        ]
        self.elements.append(f'<path d="{" ".join(path_data)}" stroke="none" stroke-width="0.1" fill="black"/>')

    def indicator(self, inner_radius_mm, pos_digree):
        """inner_radius_mm、0度の位置に大きさ2mm程度の三角を描く"""
        size_mm = 2

        def polar_to_cartesian(radius, angle_in_degrees):
            angle_in_radians = (angle_in_degrees - 90) * math.pi / 180.0
            return (
                (self.width_mm / 2) + (radius * math.cos(angle_in_radians)),
                (self.height_mm / 2) + (radius * math.sin(angle_in_radians))
            )

        # Tip of the triangle, pointing towards the center
        p1 = polar_to_cartesian(inner_radius_mm, 0 + pos_digree)

        # Base of the triangle is further out
        base_radius = inner_radius_mm + size_mm

        half_base_width = size_mm / 2
        half_base_angle_rad = half_base_width / base_radius
        half_base_angle_deg = half_base_angle_rad * 180 / math.pi

        p2 = polar_to_cartesian(base_radius, -half_base_angle_deg + pos_digree)
        p3 = polar_to_cartesian(base_radius, half_base_angle_deg + pos_digree)

        self.elements.append(
            f'<polygon points="{p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}" fill="black" />'
        )

    def label(self, text):
        """左上にラベルを書く"""
        self.elements.append(
            f'<text x="40" y="8" font-size="8" fill="black">{text}</text>'
        )

    def export_to_svg(self):
        """描いたデータをsvgにして出力する。"""
        svg_elements = "\n".join(self.elements)
        return (
            f'<svg width="{self.width_mm}mm" height="{self.height_mm}mm" viewBox="0 0 {self.width_mm} {self.height_mm}" xmlns="http://www.w3.org/2000/svg">\n'
            + svg_elements
            + "\n</svg>"
        )

encoders = [
    {
        "page": "one_dial",
        "x": 10,
        "y": 10,
        "name": "one_dial",
        "bits": 6,
        # ダイヤルでは最初の穴の中心が0度の位置、そこから23/3度おきに35個の穴がある。
        # コードでは最初の穴位置が20度から(20+23/2)度になってる。
        "degrees": [
            0,  # 最初の遊び
        ]+[
            (i * 23 / 3 + 20) for i in range(33+2)
        ] + [320],
        # 最初の穴の中央位置 = 23/3*.5+20
        # センサとエンドの位置のズレ = 23/3+5
        "indicator": 23/3*0.5+20 + 23/3+5,
    },
    {
        "page": "nine_dial",
        "x": 0,
        "y": 10,
        "name": "dial_a",
        "bits": 6,
        # あそびあり35穴
        "degrees": [
            0,  # 最初の遊び
        ]+[
            (i * 23 / 3 + 20) for i in range(33+2)
        ] + [320],
        "indicator": 23/3*0.5+20 + 23/3+5 + 85,
    },
    {
        "page": "nine_dial",
        "x": 70,
        "y": 10,
        "name": "dial_b",
        "bits": 2,
        # あそびなし3穴
        "degrees": [
            270/3*0,  # 穴1
            270/3*1,  # 穴2
            270/3*2,  # 穴3
            270/3*3,  # 最後
        ],
        "indicator": 75,
    },
    {
        "page": "nine_dial",
        "x": 120,
        "y": 10,
        "name": "dial_c",
        "bits": 3,
        # あそびなし4穴
        "degrees": [
            270/4*0,  # 穴1
            270/4*1,  # 穴2
            270/4*2,  # 穴3
            270/4*3,  # 穴4
            270/4*4,  # 最後
        ],
        "indicator": 75-90,
    },
    {
        "page": "nine_dial",
        "x": 0,
        "y": 110,
        "name": "dial_d",
        "bits": 3,
        # あそびあり1穴
        "degrees": [
            0,  # あそび
            20, # 1オンになる所
            300, # 最後
        ],
        "indicator": 20+75+90-90,
    },
    {
        "page": "nine_dial",
        "x": 60,
        "y": 110,
        "name": "dial_e",
        "bits": 3,
        # あそびあり6穴
        "degrees": [
            0,  # あそび
            20 + 270/6*0, # 穴1
            20 + 270/6*1, # 穴2
            20 + 270/6*2, # 穴3
            20 + 270/6*3, # 穴4
            20 + 270/6*4, # 穴5
            20 + 270/6*5, # 穴6
            20 + 270/6*6, # 最後
        ],
        "indicator": 20+75+45,
    },
    {
        "page": "nine_dial",
        "x": 120,
        "y": 110,
        "name": "dial_f",
        "bits": 3,
        # あそびあり4穴
        # 十字キーなので値がすごい変則
        "degrees": [
            0,  # あそび
            10+360/4*0, # 穴1
            10+360/4*1, # 穴2
            10+360/4*2, # 穴3
            10+360/4*3, # 穴4
            10+360/4*4-45, # 最後
        ],
        "indicator": 75+90-15,
    },
    {
        "page": "nine_dial",
        "x": 0,
        "y": 210,
        "name": "dial_g",
        "bits": 2,
        # あそびなし3穴
        "degrees": [ # degrees dial_bと同じ
            270/3*0,  # 穴1
            270/3*1,  # 穴2
            270/3*2,  # 穴3
            270/3*3,  # 最後
        ],
        "indicator": 75+80,
    },
    {
        "page": "nine_dial",
        "x": 50,
        "y": 210,
        "name": "dial_h",
        "bits": 2,
        # あそびなし3穴
        "degrees": [ # degrees dial_bと同じ
            270/3*0,  # 穴1
            270/3*1,  # 穴2
            270/3*2,  # 穴3
            270/3*3,  # 最後
        ],
        "indicator": 75+90,
    },
    {
        "page": "nine_dial",
        "x": 110,
        "y": 210,
        "name": "dial_i",
        "bits": 4,
        # あそびあり10穴
        "degrees": [
            0, # あそび
            20 + 270/10*0,  # 穴1
            20 + 270/10*1,  # 穴2
            20 + 270/10*2,  # 穴3
            20 + 270/10*3,  # 穴4
            20 + 270/10*4,  # 穴5
            20 + 270/10*5,  # 穴6
            20 + 270/10*6,  # 穴7
            20 + 270/10*7,  # 穴8
            20 + 270/10*8,  # 穴9
            20 + 270/10*9,  # 穴10
            20 + 270/10*10,  # 最後
        ],
        "indicator": 20+75+315-30,
    },
]

from collections import defaultdict

# Group encoders by page
pages = defaultdict(list)
for encoder in encoders:
    pages[encoder["page"]].append(encoder)

# A4 size in mm
A4_WIDTH_MM = 210
A4_HEIGHT_MM = 297

# Process each page
for page_name, page_encoders in pages.items():
    page_svg_elements = []
    for encoder in page_encoders:
        # SVGGeneratorは内部でwidth/height=100を想定して中心座標を計算している
        gen = SVGGenerator(width_mm=100, height_mm=100)
        bits = encoder["bits"]
        templ = encoder["degrees"]
        gen.circle(8)
        gen.circle(8 + 5 * bits)
        gen.indicator(8 + 5 * bits, encoder["indicator"])

        for i in range(len(templ)-1):
            gen.label(encoder["name"])
            num = i+1
            gray = num ^ (num>>1)
            s = f'{gray:0{bits}b}'
            # print(s)
            for j in range(bits):
                if (s[bits-j-1] == "1"):
                    gen.sector_ring(8+5+5*j, 8+5*j, templ[i], templ[i+1])

        # Get the SVG elements from the public member
        encoder_elements = "\n".join(gen.elements)

        transform_x = encoder["x"]
        transform_y = encoder["y"]
        page_svg_elements.append(
            f'<g transform="translate({transform_x}, {transform_y})">\n{encoder_elements}\n</g>'
        )

    # Combine all elements for the page into a single A4 SVG
    final_svg_content = (
        f'<svg width="{A4_WIDTH_MM}mm" height="{A4_HEIGHT_MM}mm" viewBox="0 0 {A4_WIDTH_MM} {A4_HEIGHT_MM}" xmlns="http://www.w3.org/2000/svg">\n'
        + "\n".join(page_svg_elements)
        + "\n</svg>"
    )

    # Write to the page file
    with open(f"{page_name}.svg", "w") as f:
        f.write(final_svg_content)
