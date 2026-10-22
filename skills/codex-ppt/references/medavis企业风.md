# medavis企业风

**适用场景:**
- medavis 及 synava Group 内部汇报、管理层汇报、团队介绍
- 产品介绍、产品路线图、项目复盘
- 面向医院、放射科诊所和合作伙伴的方案介绍
- 医疗 IT、放射科软件、云产品相关的业务与技术分享
- 需要“品牌一致 + 冷静专业 + 医疗科技质感”的正式演示
- 可与 medavis 输出模板（封面页、Logo、结束页）搭配使用，但两者相互独立

**GPT-Image-2 风格 Brief:**
```json
{
  "type": "16:9 full-slide PowerPoint image",
  "style_name": "medavis企业风",
  "best_for": "medavis and synava Group corporate decks: management and executive briefings, team and product introductions, roadmaps, project reviews, and healthcare-IT / radiology software presentations for customers and partners",
  "visual_direction": "official medavis corporate look: calm, premium, trustworthy healthcare-IT; light sage background, titles in medavis petrol blue, medavis green as the single bright accent, clean geometric sans-serif typography, generous white space, rounded cards, thin lines and simple flat line icons; facts and clear structure instead of decoration",
  "canvas": {
    "aspect_ratio": "16:9",
    "background": "light sage #EFF3E8 for the slide, lighter panels and cards in #F9FAF6 or white; no dark slides except a rare full-petrol emphasis band",
    "composition": "title top left, one clear content zone below with a strong focal element; asymmetric layouts are welcome; keep the top-right corner (about 14% of the width by 14% of the height) calm and completely empty so a logo can be placed there later",
    "density": "low to medium; one message per slide, few words, generous margins; prefer one strong diagram over many small boxes"
  },
  "color_palette": {
    "primary": "medavis petrol blue #005674 for titles, key shapes, main lines and primary chart series",
    "secondary": "slate grey-blue #44637B for secondary text, supporting shapes, inactive steps and comparison series",
    "accent": "medavis green #79AA00 for the single most important element per slide: a highlighted step, a key number, an arrow, a marker or a call-out",
    "neutral": "near-black #1C2226 for small body text, sage #EFF3E8 background, light panel #F9FAF6, soft divider lines in a pale petrol or grey tint",
    "rule": "petrol carries structure, green carries emphasis; use green sparingly (usually one focal element per slide); no other strong hues; no neon, no gold, no red except a small warning sign when the content requires it; gradients only very subtle"
  },
  "typography": {
    "title": "Titillium Web style geometric sans-serif, bold, petrol blue, left-aligned, short and confident (one line where possible)",
    "body": "the same sans-serif family in regular weight, near-black or slate, left-aligned, short phrases rather than paragraphs",
    "labels": "small but presentation-readable labels in slate or petrol; key numbers large and bold in petrol or green",
    "text_quality": "all visible text must be exact, correctly spelled, horizontal and readable at presentation size; English and German umlauts (ä, ö, ü, ß) must render correctly; never invent filler text"
  },
  "layout_patterns": [
    "opening or section slide: large petrol title, short subtitle, one calm visual (photo, simple illustration or a green accent shape)",
    "timeline or ascending steps with one highlighted milestone in green",
    "two-column comparison (before / after, what fades / what grows) on light cards",
    "parallel swimlanes or process flow with continuous arrows and short stage labels",
    "key-number slide: two to four large figures with one-line explanations",
    "journey map: people on simple lanes, the product highlighted where it touches them",
    "closing slide with three short statements and one photo or illustration"
  ],
  "layout_usage_rule": "Use layout_blueprints as candidate starting points only. Choose and adapt the composition according to each slide's semantic role; vary layouts across the deck while keeping the same palette, typography, icon language and calm density; avoid repeating the same blueprint on adjacent slides unless it is a deliberate sequence.",
  "layout_blueprints": [
    {
      "name": "highlighted timeline",
      "sections": [
        {"position": "top-left", "count": 1, "labels": ["slide title"]},
        {"position": "center", "count": 5, "labels": ["milestones on a rising line or staircase, years in bold"]},
        {"position": "one milestone", "count": 1, "labels": ["the key milestone highlighted in medavis green"]},
        {"position": "open space", "count": 1, "labels": ["optional short quote or takeaway in large petrol type"]}
      ]
    },
    {
      "name": "two-column comparison",
      "sections": [
        {"position": "top-left", "count": 1, "labels": ["slide title"]},
        {"position": "left card", "count": 1, "labels": ["muted slate column: the old or fading side, 3-4 short items"]},
        {"position": "right card", "count": 1, "labels": ["petrol and green column: the new or growing side, 3-4 short items"]},
        {"position": "bottom", "count": 1, "labels": ["one-sentence takeaway"]}
      ]
    },
    {
      "name": "parallel lanes",
      "sections": [
        {"position": "top-left", "count": 1, "labels": ["slide title"]},
        {"position": "left two thirds", "count": 3, "labels": ["horizontal lanes, each with icon, name, small tag pill and one continuous arrow with short stage labels"]},
        {"position": "under the lanes", "count": 1, "labels": ["green bracket for a shared function across all lanes"]},
        {"position": "right third", "count": 1, "labels": ["light side panel for supporting facts"]}
      ]
    },
    {
      "name": "key numbers",
      "sections": [
        {"position": "top-left", "count": 1, "labels": ["slide title"]},
        {"position": "center row", "count": 3, "labels": ["large figure with a one-line label each; the most important figure in green"]},
        {"position": "bottom", "count": 1, "labels": ["short source or context line in slate"]}
      ]
    }
  ],
  "visual_elements": {
    "allowed": "rounded cards (about 10px radius), thin lines, simple flat line icons in petrol, small pill tags, continuous arrows, timelines and staircases, swimlanes, brackets, numbered circles, very soft shadows at most, generous white space",
    "avoid": "playful or cartoon styles, clip art, stock-photo clichés (handshakes, glowing brains, robots), heavy shadows, 3D effects, busy textures, neon or rainbow colors, dense tables, decorative noise, page numbers, footers, watermarks"
  },
  "image_treatment": {
    "photos": "real, calm, natural-light photos of people at work or clinical/office settings; show them wide and uncropped where faces matter, with the title above rather than on top; no heavy filters",
    "screenshots": "place in clean white frames with a thin border and a short label; keep interface details readable",
    "charts": "flat and simple: petrol as the main series, slate for comparison, green for the one highlight; direct labels instead of legends; no 3D",
    "illustrations": "simple flat line icons and minimal geometric shapes in petrol, slate and green; healthcare-IT themes (calendar, monitor, cloud, document, stethoscope, scan) drawn neutrally"
  },
  "rendering_constraints": [
    "The slide must look like an official, professional medavis presentation suitable for executives, customers and partners.",
    "Keep the top-right corner (about 14% of the width by 14% of the height) completely empty; do not draw any logo, wordmark, brand name mark or page number anywhere.",
    "Never invent or approximate logos, certification badges, product marks or partner brands; leave an empty panel when real marks will be added later.",
    "Keep all text horizontal; avoid small rotated or vertical text, which renders unreliably.",
    "Use only the exact visible text provided; no filler words, lorem ipsum, invented labels or extra numbers.",
    "Use medavis green for one focal element per slide; petrol carries the structure.",
    "No watermark, no unrelated logo, no slide number unless explicitly requested."
  ]
}
```
