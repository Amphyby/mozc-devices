import math
import svgwrite


class SvgGenerator:

  def __init__(self, width, height):
    self.dwg = svgwrite.Drawing(
        size=(f"{width}mm", f"{height}mm"), profile="full"
    )
    self.dwg.viewbox(0, 0, width, height)

  def circle(self, center_x, center_y, size, stroke="black", fill="none"):
    radius = size / 2
    self.dwg.add(
        self.dwg.circle(
            center=(center_x, center_y), r=radius, stroke=stroke, fill=fill
        )
    )

  def text(self, center_x, center_y, label, font_size=5):
    self.dwg.add(
        self.dwg.text(
            label,
            insert=(center_x, center_y),
            text_anchor="middle",
            dominant_baseline="central",
            font_size=font_size,
            fill="black",
        )
    )

  def save(self, filename):
    self.dwg.saveas(filename)


# PROJECT.mdから変換したデータ
# [id, 直径, x, y, keys, bits, pcbの回転量]
DIALS = [
    ["a", 150, 125, 84, 35, 6, 0],
    ["b", 41, 27, 45, 3, 2, 180 - 90],
    ["c", 44, 29, 125, 4, 3, 180],
    ["d", 37, 234, 87, 1, 3, 45],
    ["e", 59, 290, 54, 6, 3, 45],
    ["f", 59, 290, 118, 4, 3, 0],
    ["g", 41, 345, 49, 3, 2, 10],
    ["h", 41, 405, 49, 3, 2, 0],
    ["i", 82, 378, 112, 10, 4, -45],
]

LABELS = {
    "a": [
        "@",
        ":",
        "_",
        "p",
        ";",
        "/",
        "o",
        "l",
        ".",
        "i",
        "k",
        ",",
        "u",
        "j",
        "m",
        "y",
        "h",
        "n",
        "t",
        "g",
        "b",
        "r",
        "f",
        "v",
        "e",
        "d",
        "c",
        "w",
        "s",
        "x",
        "q",
        "a",
        "z",
        "<SPACE>",
        "<CAPS>",
    ],
    "b": ["^", "<ESC>", "<TAB>"],
    "c": ["<SHIFT>", "<CTRL>", "<ALT>", "<FN>"],
    "d": ["Ent"],
    "e": ["<END>", "<PAGE DOWN>", "<PAGE UP>", "<HOME>", "<INS>", "<DEL>"],
    "f": ["<RIGHT>", "<UP>", "<LEFT>", "<DOWN>"],
    "g": ["*", "/", "."],
    "h": ["+", "-", "="],
    "i": ["9", "8", "7", "6", "5", "4", "3", "2", "1", "0"],
}


if __name__ == "__main__":
  # 全体のサイズを計算 (paddingを追加)
  padding = 10
  max_x = max(d[2] + d[1] / 2 for d in DIALS) + padding
  max_y = max(d[3] + d[1] / 2 for d in DIALS) + padding

  generator = SvgGenerator(max_x, max_y)

  for dial_data in DIALS:
    dial_id, diameter, x, y, keys, _, _ = dial_data

    # 大円を描画
    generator.circle(x, y, diameter)

    # 小円とラベルを描画
    if keys > 0:
      labels = LABELS.get(dial_id, [])
      large_radius = diameter / 2
      small_diameter = 13
      small_radius = small_diameter / 2

      # 小円の中心が並ぶ円の半径
      inner_circle_radius = large_radius - small_radius

      # 小円は270度の範囲に配置し、右下(0〜90度)を開ける
      start_angle_rad = 0  # 0度(右)から開始
      angle_span_rad = 1.5 * math.pi  # 270度の範囲

      for i in range(keys):
        # 角度を計算 (ラジアン) - 減算して反時計回りにする
        sector_angle = angle_span_rad / keys
        angle = start_angle_rad - sector_angle * (i + 0.5)

        # ダイヤル 'a' のみ3列に配置
        current_inner_radius = inner_circle_radius
        if dial_id == "a":
          offset = (i % 3) * 12
          current_inner_radius -= offset

        # 小円の中心座標を計算
        small_x = x + current_inner_radius * math.cos(angle)
        small_y = y + current_inner_radius * math.sin(angle)

        generator.circle(small_x, small_y, small_diameter)

        if i < len(labels):
          label = labels[i]
          # ラベルの長さに応じてフォントサイズを調整
          if len(label) > 8:
            font_size = 2.0
          elif len(label) > 4:
            font_size = 3.0
          else:
            font_size = 4.0
          generator.text(small_x, small_y, label, font_size=font_size)

  output_filename = "keymap.svg"
  generator.save(output_filename)
  print(f"SVG file '{output_filename}' has been generated.")
