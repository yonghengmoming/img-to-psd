# -*- coding: utf-8 -*-
"""N 层 PSD 生成模板（已知可跑通，2026-09-21 验证）

用法：改 SPECS 后运行。每层给 (图层名, PIL.Image 或 RGBA numpy 数组)。
依赖: pytoshop 1.2.1, Pillow, numpy
注意: 必须用 Compression.raw（wheel 未编译 packbits，rle 会 NameError）
"""
import sys
import numpy as np
import pytoshop
from PIL import Image
from pytoshop import layers as psdl
from pytoshop.enums import ColorMode, ChannelId, Compression


def to_rgba_array(img):
    if isinstance(img, Image.Image):
        return np.asarray(img.convert("RGBA"), dtype=np.uint8)
    return np.asarray(img, dtype=np.uint8)


def make_layer(name, arr, top=0, left=0):
    """arr: (h,w,4) uint8，占满 (top,left) 起的自身尺寸区域"""
    h, w = arr.shape[:2]
    chans = {
        ChannelId.red:   psdl.ChannelImageData(image=arr[:, :, 0], compression=Compression.raw),
        ChannelId.green: psdl.ChannelImageData(image=arr[:, :, 1], compression=Compression.raw),
        ChannelId.blue:  psdl.ChannelImageData(image=arr[:, :, 2], compression=Compression.raw),
        ChannelId.transparency: psdl.ChannelImageData(image=arr[:, :, 3], compression=Compression.raw),
    }
    return psdl.LayerRecord(channels=chans, top=top, left=left, bottom=top + h, right=left + w, name=name)


def build_psd(width, height, specs, out_path):
    """specs: [(图层名, PIL.Image/numpy RGBA)] — 顺序 = 从底到顶"""
    psd = pytoshop.core.PsdFile(num_channels=3, height=height, width=width)
    psd.color_mode = ColorMode.rgb
    records = psd.layer_and_mask_info.layer_info.layer_records
    for name, img in specs:
        arr = to_rgba_array(img)
        full = np.zeros((height, width, 4), dtype=np.uint8)
        full[:arr.shape[0], :arr.shape[1]] = arr  # 左上对齐；需要定位就改这里
        records.append(make_layer(name, full))
    with open(out_path, "wb") as f:
        psd.write(f)
    return out_path


def verify(out_path, expected_names):
    psd2 = pytoshop.core.PsdFile.read(open(out_path, "rb"))
    names = [l.name for l in psd2.layer_and_mask_info.layer_info.layer_records]
    ok = names == expected_names
    print("回读图层:", names, "| 预期:", expected_names, "|", "OK" if ok else "MISMATCH")
    return ok


if __name__ == "__main__":
    W, H = 800, 600
    from PIL import ImageDraw

    bg = Image.new("RGBA", (W, H), "white")
    circle = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(circle)
    d.ellipse([400 - 120, 300 - 120, 400 + 120, 300 + 120], fill=(220, 0, 0, 255))
    bar = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(bar)
    d2.rectangle([80, 420, 600, 560], fill=(0, 0, 200, 255))

    out = sys.argv[1] if len(sys.argv) > 1 else "测试_三层.psd"
    build_psd(W, H, [("背景-白", bg), ("产品-红圆", circle), ("标签-蓝条", bar)], out)
    print("已生成:", out)
    verify(out, ["背景-白", "产品-红圆", "标签-蓝条"])
