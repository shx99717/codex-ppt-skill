#!/usr/bin/env python3
"""
PPT 组装脚本

将一个目录中的幻灯片图片组装成 PowerPoint 演示文稿。
默认模式：每张图片插入为一页空白幻灯片，按锁定比例均匀 contain。
可选 medavis 模板模式：匹配比例的 3 页模板 + 内容页整页贴图 + 小 logo 叠加。
"""

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from slide_image_ratio import RATIO_BY_LABEL, require_image_ratio, uniform_picture_box

MEDAVIS_LOGO_MARGIN_EMU = 95250
MEDAVIS_LOGO_WIDTH_EMU = 1362456
MEDAVIS_LOGO_HEIGHT_EMU = 274320
PPT_TITLE_TOKEN = "<PPT-Title>"
SLIDE_EMU = {
    "16:9": (9144000, 5143500),
    "4:3": (9144000, 6858000),
    "3:2": (9144000, 6096000),
}
MEDAVIS_TEMPLATE_NAME = {
    "16:9": "medavis_ppt_template_2026_en_16-9.pptx",
    "4:3": "medavis_ppt_template_2026_en_4-3.pptx",
    "3:2": "medavis_ppt_template_2026_en_3-2.pptx",
}


def skill_root_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def medavis_template_path(aspect_ratio: str = "16:9") -> str:
    name = MEDAVIS_TEMPLATE_NAME.get(aspect_ratio)
    if not name:
        raise KeyError(aspect_ratio)
    return os.path.join(skill_root_dir(), "assets", "templates", name)


def medavis_logo_path() -> str:
    return os.path.join(skill_root_dir(), "assets", "templates", "medavis-logo-small.png")


def dependency_hint() -> str:
    runtime_home = os.path.expanduser(os.environ.get("CODEX_PPT_HOME", "~/.codex-ppt-skill"))
    python = os.path.join(
        runtime_home,
        ".venv",
        "Scripts" if os.name == "nt" else "bin",
        "python.exe" if os.name == "nt" else "python",
    )
    runtime_script = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "codex_ppt_runtime.py",
    )
    return (
        f"请运行: python3 {runtime_script} bootstrap\n"
        f"或直接运行: {python} -m pip install -r "
        f"{os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'requirements.txt')}"
    )


def get_slide_images(ppt_project_dir: str) -> List[str]:
    """
    获取幻灯片图片文件列表，按页码排序

    Args:
        ppt_project_dir: PPT 项目目录（包含 origin_image 子目录）

    Returns:
        按顺序排列的图片文件路径列表
    """
    # 从 origin_image 子目录读取
    origin_image_dir = os.path.join(ppt_project_dir, "origin_image")

    if not os.path.exists(origin_image_dir):
        print(f"错误：origin_image 目录不存在: {origin_image_dir}")
        return []

    print(f"从 origin_image 目录读取图片: {origin_image_dir}")

    # 支持的图片格式
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}

    # 只获取正式幻灯片图片，避免 sample_slide.png、草稿图或参考图被误装入 PPT。
    slide_name_pattern = re.compile(r"^slide_(\d+)\.(png|jpe?g|gif|bmp)$", re.IGNORECASE)
    image_files = []
    for file in os.listdir(origin_image_dir):
        file_path = os.path.join(origin_image_dir, file)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower()
            if ext in image_extensions and slide_name_pattern.match(file):
                image_files.append(file_path)

    def slide_sort_key(path: str) -> Tuple[int, str]:
        filename = os.path.basename(path)
        stem = os.path.splitext(filename)[0]
        return (int(re.search(r"^slide_(\d+)", stem).group(1)), filename.lower())

    # 按页码排序，避免 slide_10 排在 slide_2 前面。
    # 同页码多文件时按文件名稳定排序。
    image_files.sort(key=slide_sort_key)

    return image_files


def load_speaker_notes(ppt_project_dir: str) -> Dict[int, str]:
    """
    从 speech.md 读取每页演讲备注。

    支持以下标题格式：
    - ## Slide 1: 标题
    - ### Slide 1: 标题
    - ## 第 1 页：标题
    """
    speech_path = os.path.join(ppt_project_dir, "speech.md")
    if not os.path.exists(speech_path):
        return {}

    with open(speech_path, "r", encoding="utf-8") as f:
        content = f.read()

    notes: Dict[int, str] = {}
    current_slide: Optional[int] = None
    current_lines: List[str] = []
    heading_pattern = re.compile(r"^#{2,4}\s*(?:Slide\s*(\d+)|第\s*(\d+)\s*页)\b.*$", re.IGNORECASE)

    def flush_current() -> None:
        if current_slide is None:
            return
        text = "\n".join(current_lines).strip()
        if text:
            notes[current_slide] = text

    for line in content.splitlines():
        match = heading_pattern.match(line.strip())
        if match:
            flush_current()
            current_slide = int(match.group(1) or match.group(2))
            current_lines = []
            continue

        if current_slide is not None:
            current_lines.append(line)

    flush_current()
    return notes


def compress_image_if_needed(
    image_path: str,
    max_size_mb: float = 2.0,
    quality_step: int = 5
) -> Optional[str]:
    """
    如果图片超过指定大小，压缩图片并返回临时文件路径

    Args:
        image_path: 原始图片路径
        max_size_mb: 最大文件大小（MB）
        quality_step: 每次降低的质量步进

    Returns:
        str: 如果需要压缩，返回临时文件路径；否则返回 None
    """
    max_size_bytes = max_size_mb * 1024 * 1024

    # 检查原始文件大小
    file_size = os.path.getsize(image_path)

    if file_size <= max_size_bytes:
        # 不需要压缩
        return None

    print(f"  图片大小 {file_size / 1024 / 1024:.2f}MB，需要压缩...")

    try:
        from PIL import Image

        # 打开图片
        img = Image.open(image_path)

        # 转换 RGBA 到 RGB（如果需要保存为 JPEG）
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background

        # 创建临时文件
        temp_fd, temp_path = tempfile.mkstemp(suffix='.jpg')
        os.close(temp_fd)

        # 从高质量开始尝试压缩
        quality = 95
        while quality > 20:
            img.save(temp_path, 'JPEG', quality=quality, optimize=True)
            compressed_size = os.path.getsize(temp_path)

            if compressed_size <= max_size_bytes:
                print(f"  压缩成功: {compressed_size / 1024 / 1024:.2f}MB (质量: {quality})")
                return temp_path

            quality -= quality_step

        # 如果还是太大，尝试调整尺寸
        print(f"  质量压缩不足，尝试缩小尺寸...")
        scale = 0.9
        while scale > 0.3:
            new_width = int(img.width * scale)
            new_height = int(img.height * scale)
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            resized_img.save(temp_path, 'JPEG', quality=85, optimize=True)
            compressed_size = os.path.getsize(temp_path)

            if compressed_size <= max_size_bytes:
                print(f"  压缩成功: {compressed_size / 1024 / 1024:.2f}MB (缩放: {scale:.0%})")
                return temp_path

            scale -= 0.1

        # 实在压不下去了，返回最后的结果
        print(f"  警告：无法压缩到 {max_size_mb}MB 以下，使用最小尺寸版本")
        return temp_path

    except ImportError:
        print("错误：未安装 Pillow 库")
        print(dependency_hint())
        return None
    except Exception as e:
        print(f"  警告：图片压缩失败: {e}")
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        return None


def _validate_images_for_ratio(image_files: List[str], aspect_ratio: str) -> None:
    if aspect_ratio not in RATIO_BY_LABEL:
        raise ValueError(f"unsupported aspect_ratio: {aspect_ratio}")
    expected = RATIO_BY_LABEL[aspect_ratio]
    for image_path in image_files:
        if not os.path.exists(image_path):
            raise ValueError(f"图片文件不存在: {image_path}")
        require_image_ratio(image_path, expected, aspect_ratio)


def add_content_picture(slide, image_path: str, prs, aspect_ratio: str) -> None:
    expected = RATIO_BY_LABEL[aspect_ratio]
    width, height = require_image_ratio(image_path, expected, aspect_ratio)
    left, top, box_w, box_h = uniform_picture_box(
        width, height, int(prs.slide_width), int(prs.slide_height)
    )
    slide.shapes.add_picture(image_path, left=left, top=top, width=box_w, height=box_h)


def add_medavis_logo(slide, prs) -> None:
    logo = medavis_logo_path()
    if not os.path.exists(logo):
        raise FileNotFoundError(logo)
    left = int(prs.slide_width) - MEDAVIS_LOGO_WIDTH_EMU - MEDAVIS_LOGO_MARGIN_EMU
    slide.shapes.add_picture(
        logo,
        left=left,
        top=MEDAVIS_LOGO_MARGIN_EMU,
        width=MEDAVIS_LOGO_WIDTH_EMU,
        height=MEDAVIS_LOGO_HEIGHT_EMU,
    )


def set_medavis_landing_title(slide, title: str) -> None:
    for shape in slide.shapes:
        if not getattr(shape, "has_text_frame", False):
            continue
        if PPT_TITLE_TOKEN not in (shape.text_frame.text or ""):
            continue
        replaced = False
        for paragraph in shape.text_frame.paragraphs:
            runs = paragraph.runs
            if not runs:
                continue
            if not replaced:
                runs[0].text = title
                replaced = True
                for extra in runs[1:]:
                    extra.text = ""
            else:
                for run in runs:
                    run.text = ""
        if not replaced:
            shape.text_frame.paragraphs[0].text = title
        return
    raise RuntimeError("medavis landing page is missing the <PPT-Title> placeholder")


def move_slide(prs, old_index: int, new_index: int) -> None:
    sld_id_lst = prs.slides._sldIdLst
    elements = list(sld_id_lst)
    el = elements[old_index]
    sld_id_lst.remove(el)
    sld_id_lst.insert(new_index, el)


def _cleanup_temp_files(temp_files: List[str]) -> None:
    for temp_file in temp_files:
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except Exception as e:
            print(f"警告：清理临时文件失败 {temp_file}: {e}")


def create_presentation(
    image_files: List[str],
    output_path: str,
    aspect_ratio: str = "16:9",
    speaker_notes: Optional[Dict[int, str]] = None,
) -> bool:
    """
    创建 PowerPoint 演示文稿

    Args:
        image_files: 幻灯片图片文件列表
        output_path: 输出 PPT 文件路径
        aspect_ratio: 幻灯片宽高比（16:9、4:3 或 3:2）

    Returns:
        bool: 成功返回 True，失败返回 False
    """
    temp_files_to_cleanup: List[str] = []
    try:
        try:
            from pptx import Presentation
        except ImportError:
            print("错误：未安装 python-pptx 库")
            print(dependency_hint())
            return False

        try:
            _validate_images_for_ratio(image_files, aspect_ratio)
        except ValueError as exc:
            print(f"错误：{exc}")
            return False

        prs = Presentation()
        slide_width, slide_height = SLIDE_EMU[aspect_ratio]
        prs.slide_width = slide_width
        prs.slide_height = slide_height

        speaker_notes = speaker_notes or {}
        blank_slide_layout = prs.slide_layouts[6]

        for i, image_path in enumerate(image_files, 1):
            compressed_path = compress_image_if_needed(image_path, max_size_mb=2.0)
            image_to_use = compressed_path if compressed_path else image_path
            if compressed_path:
                temp_files_to_cleanup.append(compressed_path)

            slide = prs.slides.add_slide(blank_slide_layout)
            add_content_picture(slide, image_to_use, prs, aspect_ratio)

            note_text = speaker_notes.get(i)
            if note_text:
                notes_frame = slide.notes_slide.notes_text_frame
                notes_frame.clear()
                notes_frame.text = note_text

            print(f"✓ 已添加第 {i} 页: {os.path.basename(image_path)}")

        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        prs.save(output_path)
        print(f"\n✓ PPT 文件已保存: {output_path}")
        print(f"  总页数: {len(image_files)}")
        if speaker_notes:
            matched_notes = sum(1 for i in range(1, len(image_files) + 1) if speaker_notes.get(i))
            print(f"  已写入备注: {matched_notes}/{len(image_files)} 页")

        _cleanup_temp_files(temp_files_to_cleanup)
        return True

    except ValueError as exc:
        print(f"错误：{exc}")
        _cleanup_temp_files(temp_files_to_cleanup)
        return False
    except Exception as e:
        print(f"错误：创建 PPT 失败: {e}")
        import traceback
        traceback.print_exc()
        _cleanup_temp_files(temp_files_to_cleanup)
        return False


def create_medavis_presentation(
    image_files: List[str],
    output_path: str,
    landing_title: str,
    speaker_notes: Optional[Dict[int, str]] = None,
    aspect_ratio: str = "16:9",
) -> bool:
    """Build a medavis-templated PPTX: landing + N content + ending."""
    temp_files_to_cleanup: List[str] = []
    try:
        try:
            from pptx import Presentation
        except ImportError:
            print("错误：未安装 python-pptx 库")
            print(dependency_hint())
            return False

        try:
            _validate_images_for_ratio(image_files, aspect_ratio)
        except ValueError as exc:
            print(f"错误：{exc}")
            return False

        template = medavis_template_path(aspect_ratio)
        if not os.path.exists(template):
            print(f"错误：未找到 medavis 模板: {template}")
            return False

        # Open for reading only; never save back to the bundled asset.
        prs = Presentation(template)
        if len(prs.slides) != 3:
            print(f"错误：medavis 模板必须恰好 3 页（落地页 + 空白内容 + 结束页），实际 {len(prs.slides)}")
            return False

        set_medavis_landing_title(prs.slides[0], landing_title)
        blank_layout = prs.slides[1].slide_layout
        speaker_notes = speaker_notes or {}

        for i, image_path in enumerate(image_files):
            compressed_path = compress_image_if_needed(image_path, max_size_mb=2.0)
            image_to_use = compressed_path if compressed_path else image_path
            if compressed_path:
                temp_files_to_cleanup.append(compressed_path)

            if i == 0:
                slide = prs.slides[1]
            else:
                slide = prs.slides.add_slide(blank_layout)
                move_slide(prs, len(prs.slides) - 1, 1 + i)

            add_content_picture(slide, image_to_use, prs, aspect_ratio)
            add_medavis_logo(slide, prs)

            note_text = speaker_notes.get(i + 1)
            if note_text:
                notes_frame = slide.notes_slide.notes_text_frame
                notes_frame.clear()
                notes_frame.text = note_text

            print(f"✓ 已添加 medavis 内容页 {i + 1}: {os.path.basename(image_path)}")

        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if os.path.abspath(output_path) == os.path.abspath(template):
            print("错误：拒绝覆盖捆绑的 medavis 模板文件")
            return False

        prs.save(output_path)
        print(f"\n✓ medavis PPT 已保存: {output_path}")
        print(f"  总页数: {2 + len(image_files)} (1 落地页 + {len(image_files)} 内容页 + 1 结束页)")
        if speaker_notes:
            matched_notes = sum(1 for i in range(1, len(image_files) + 1) if speaker_notes.get(i))
            print(f"  已写入备注: {matched_notes}/{len(image_files)} 内容页")

        _cleanup_temp_files(temp_files_to_cleanup)
        return True

    except ValueError as exc:
        print(f"错误：{exc}")
        _cleanup_temp_files(temp_files_to_cleanup)
        return False
    except Exception as e:
        print(f"错误：创建 medavis PPT 失败: {e}")
        import traceback
        traceback.print_exc()
        _cleanup_temp_files(temp_files_to_cleanup)
        return False


def assemble_managed(deck, ppt_name, template, aspect_ratio, landing_title):
    """Assemble approved immutable inputs and publish outputs only after revalidation."""
    from planning_contract import (planning_lock,require_managed_ready,read_contract_json,
                                   inside_path,file_digest,ContractError,load_managed_spec,slide_id)
    from record_plan_approval import snapshot_file,atomic_group
    with planning_lock(deck):
        require_managed_ready(deck,template,aspect_ratio,landing_title)
        jobs=read_contract_json(deck/"slide_jobs.json","managed jobs")
        notes=load_speaker_notes(str(deck))
        with tempfile.TemporaryDirectory(prefix=".assembly-",dir=deck) as scratch:
            scratch_path=Path(scratch).resolve()
            if not scratch_path.is_relative_to(deck.resolve()):
                raise ContractError("Assembly scratch directory escaped the deck")
            images=[]
            checks=[]
            by_id={slide["slide_id"]:slide for slide in jobs["slides"]}
            for approved_slide in load_managed_spec(deck)["slides"]:
                slide=by_id[slide_id(approved_slide)]
                expected=slide["qa"]["image_sha256"]
                path=scratch_path/f"{slide['slide_id']}.png"
                snapshot_file(inside_path(deck,slide["out"]),path,expected)
                images.append(str(path))
                checks.append((path,expected))
            outputs={}
            if template in {"none","both"}:
                path=scratch_path/f"{ppt_name}.pptx"
                if not create_presentation(images,str(path),aspect_ratio,notes):
                    return False
                outputs[path.name]=path.read_bytes()
            if template in {"medavis","both"}:
                path=scratch_path/f"{ppt_name}-medavis.pptx"
                if not create_medavis_presentation(images,str(path),landing_title.strip(),notes,aspect_ratio):
                    return False
                outputs[path.name]=path.read_bytes()
            for path,expected in checks:
                if file_digest(path)!=expected:
                    raise ContractError("Approved assembly snapshot changed")
            require_managed_ready(deck,template,aspect_ratio,landing_title)
            atomic_group(deck,outputs)
        return True

def main():
    # Windows consoles on a non-UTF-8 locale (e.g. GBK/cp936) can't encode the
    # Chinese status text and check-mark symbols this script prints; force UTF-8
    # so the process doesn't crash regardless of the ambient console code page.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description='将幻灯片图片组装成 PowerPoint 演示文稿',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例用法:
  # 基本用法（无模板，整页贴图）
  python assemble_ppt.py /path/to/base/ MyPresentation.pptx

  # medavis 模板（输出 MyPresentation-medavis.pptx）
  python assemble_ppt.py /path/to/base/ MyPresentation.pptx \\
    --template medavis --landing-title "Deck Title"

  # 同时输出无模板与 medavis 两个文件
  python assemble_ppt.py /path/to/base/ MyPresentation.pptx \\
    --template both --landing-title "Deck Title"

  # 指定 4:3 / 3:2 宽高比（none 与 medavis 均生效）
  python assemble_ppt.py /path/to/base/ MyPresentation.pptx --aspect-ratio 4:3

  # 只初始化目录，不生成 PPT
  python assemble_ppt.py /path/to/base/ MyPresentation.pptx --init

文件夹结构要求:
  /path/to/base/MyPresentation/
  ├── origin_image/
  │   ├── slide_01.png
  │   ├── slide_02.png
  │   └── ...
  ├── speech.md (可选，将写入 PPT 备注)
  ├── MyPresentation.pptx (none / both 时生成)
  └── MyPresentation-medavis.pptx (medavis / both 时生成)

注意：
  - 图片文件必须放在 origin_image 子目录中
  - 只会读取 slide_01.png、slide_02.png 这类正式图片，其他图片会被忽略
  - 图片文件按页码排序
  - none 模式：按锁定比例均匀 contain，不拉伸
  - medavis 模式：匹配比例的 3 页模板（落地页 + 内容 + 结束页）；内容页整页贴图并叠加小 logo
  - 如果项目目录下存在 speech.md，会按 Slide N 标题写入内容页备注（结束页不写）
        '''
    )

    parser.add_argument('base_dir', help='基础目录（PPT 项目文件夹的父目录）')
    parser.add_argument('output', help='输出 PPT 文件名 (.pptx)')
    parser.add_argument('--aspect-ratio', '--ar',
                        choices=['16:9', '4:3', '3:2'],
                        default='16:9',
                        help='幻灯片宽高比 (默认: 16:9；none 与 medavis 均使用)')
    parser.add_argument('--template',
                        choices=['none', 'medavis', 'both'],
                        default='none',
                        help='组装模板：none=无模板整页贴图；medavis=medavis 公司模板；both=两者都生成')
    parser.add_argument('--landing-title',
                        default=None,
                        help='medavis/both 落地页标题（必填）')
    parser.add_argument('--init',
                        action='store_true',
                        help='只创建 PPT 项目目录和 origin_image 子目录，不生成 PPT')
    parser.add_argument('--legacy-unmanaged', action='store_true', help='Explicit unmanaged/manual assembly; cannot bypass managed markers')

    args = parser.parse_args()

    # 确保输出文件有 .pptx 扩展名
    output_filename = args.output
    if not output_filename.lower().endswith('.pptx'):
        output_filename += '.pptx'

    # 获取 PPT 名称（不含扩展名）
    ppt_name = os.path.splitext(os.path.basename(output_filename))[0]

    # 构建 PPT 项目目录
    ppt_project_dir = os.path.join(args.base_dir, ppt_name)
    origin_image_dir = os.path.join(ppt_project_dir, "origin_image")

    if args.init:
        os.makedirs(origin_image_dir, exist_ok=True)
        print(f"✓ PPT 项目目录已准备好: {ppt_project_dir}")
        print(f"✓ 幻灯片图片目录已准备好: {origin_image_dir}")
        sys.exit(0)

    if args.template in ('medavis', 'both') and not (args.landing_title and args.landing_title.strip()):
        print("错误：--template medavis/both 需要提供非空的 --landing-title")
        sys.exit(1)

    if not os.path.exists(ppt_project_dir):
        print(f"错误：PPT 项目目录不存在: {ppt_project_dir}")
        print("如需初始化目录，请添加 --init 参数")
        sys.exit(1)

    if not os.path.exists(origin_image_dir):
        print(f"错误：origin_image 目录不存在: {origin_image_dir}")
        print("如需初始化目录，请添加 --init 参数")
        sys.exit(1)

    plain_output_path = os.path.join(ppt_project_dir, f"{ppt_name}.pptx")
    from planning_contract import require_legacy_allowed, ContractError
    deck_path=Path(ppt_project_dir).resolve()
    try:
        if args.legacy_unmanaged:
            require_legacy_allowed(deck_path)
        else:
            success=assemble_managed(deck_path,ppt_name,args.template,args.aspect_ratio,args.landing_title)
            sys.exit(0 if success else 1)
    except (ContractError,ValueError,OSError) as exc:
        print(f"Error: {exc}",file=sys.stderr)
        sys.exit(1)
    medavis_output_path = os.path.join(ppt_project_dir, f"{ppt_name}-medavis.pptx")

    # 获取幻灯片图片
    print(f"正在扫描 PPT 项目目录: {ppt_project_dir}")
    image_files = get_slide_images(ppt_project_dir)

    if not image_files:
        print("错误：未找到任何图片文件")
        print("支持的格式: .png, .jpg, .jpeg, .gif, .bmp")
        print(f"\n请将幻灯片图片放置在: {origin_image_dir}/")
        sys.exit(1)

    print(f"找到 {len(image_files)} 张幻灯片图片\n")
    speaker_notes = load_speaker_notes(ppt_project_dir)
    if speaker_notes:
        print(f"找到 {len(speaker_notes)} 页备注: {os.path.join(ppt_project_dir, 'speech.md')}\n")

    success = True

    if args.template in ('none', 'both'):
        print(f"正在创建 PPT (模板: none, 宽高比: {args.aspect_ratio})...")
        print("-" * 50)
        success = create_presentation(
            image_files, plain_output_path, args.aspect_ratio, speaker_notes
        ) and success

    if args.template in ('medavis', 'both'):
        print(f"正在创建 PPT (模板: medavis, 宽高比: {args.aspect_ratio}, 落地标题: {args.landing_title})...")
        print("-" * 50)
        success = create_medavis_presentation(
            image_files,
            medavis_output_path,
            args.landing_title.strip(),
            speaker_notes,
            args.aspect_ratio,
        ) and success

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
