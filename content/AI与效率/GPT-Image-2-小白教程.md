---
aliases:
  - "articles/AI与效率/GPT-Image-2-小白教程"
title: GPT-Image-2 小白使用教程
permalink: gpt-image-2-guide
publish: true
description: OpenAI GPT-Image-2 的零基础使用指南，覆盖免费与付费入口、提示词写法、常见用法和踩坑点，适合第一次接触 AI 画图的用户。
tags:
  - AI
  - 图像生成
  - GPT-Image-2
  - 教程
---

> 本文收录于 [[2026-AI工具推荐]] 图像生成分类
>
> OpenAI 最新发布的图像生成模型，在 LMArena 排行榜上领先第二名 200+ 分，堪称当前最强 AI 画图模型。
>
> 本文参考：[🔥【图像视频系列7】关于GPT-Image-2，你想知道的一切 - LINUX DO](https://linux.do/t/topic/2026332)

---

## 一、GPT-Image-2 是什么？

GPT-Image-2 是 OpenAI 推出的第二代图像生成模型，可以根据你的文字描述生成高质量图片。相比上一代（image-1.5），它在画面质量、文字渲染、细节还原等方面有大幅提升。

简单说：你用文字告诉它「画什么」，它就帮你画出来。

---

## 二、在哪里可以用？（四种方式，由易到难）

### 方式 1：ChatGPT 直接用（最简单，推荐新手）

- 打开 [ChatGPT](https://chat.openai.com)（网页版或 App 均可）
- 直接在对话框输入你想画的内容，比如：「画一只穿西装的柴犬，坐在办公桌前喝咖啡」
- ChatGPT 会自动调用 GPT-Image-2 生成图片

各会员等级的额度参考：

| 会员等级 | 额度（推测） |
|---------|------------|
| Pro 会员 | medium 质量不限量 |
| Plus 会员 | 3 小时几十张 medium，之后降为 low |
| 免费用户 | medium 几张，之后降为 low |

### 方式 2：LMArena 免费体验

- 打开 [LMArena Direct Chat](https://arena.ai/image/direct)
- 无需付费，直接输入提示词即可生成
- 适合想免费试效果的用户

### 方式 3：通过 API 调用（适合开发者）

如果你是开发者，可以通过以下渠道接入：

- **OpenAI 官方 API**：直接调用，模型名 `gpt-image-2`
- **OpenRouter**：第三方聚合平台，[GPT-Image-2 on OpenRouter](https://openrouter.ai/openai/gpt-5.4-image-2)
- **中转站**：国内很多中转站已上线，约 ¥0.04/张

API 调用示例（Python）：

```python
from openai import OpenAI

client = OpenAI(api_key="你的API密钥")

response = client.images.generate(
    model="gpt-image-2",
    prompt="一只穿西装的柴犬，坐在办公桌前喝咖啡，写实风格",
    size="1536x1024",   # 分辨率
    quality="medium"     # 质量：low / medium / high
)

# 获取图片 URL
print(response.data[0].url)
```

### 方式 4：Codex 中使用

OpenAI 的 Codex 平台也已上线 GPT-Image-2 支持。

---

## 三、分辨率与质量怎么选？

### 支持的比例

| 比例 | 适用场景 |
|------|---------|
| 3:2（默认） | 通用场景，类似照片比例 |
| 1:1 | 头像、社交媒体封面 |
| 16:9 | 横屏壁纸、视频封面 |
| 9:16 | 手机壁纸、短视频封面 |

### 分辨率与价格（API）

| 分辨率 | medium 价格 | high 价格 |
|-------|-----------|----------|
| 1536×1024（1.5K） | $0.04 | $0.16 |
| 2560×1440（2K） | $0.06 | $0.22 |
| 3840×2160（4K） | $0.10 | $0.40 |

> 价格为社区推算，仅供参考。官方 token 计价：输入文本 $5/百万token，输入图像 $8/百万token，输出 $30/百万token。

### 质量等级怎么选？

| 质量 | 效果 | 建议场景 |
|------|------|---------|
| low | 速度快，细节一般 | 快速草稿、批量生成 |
| medium | 平衡之选（当前默认） | 日常使用，性价比最高 |
| high | 最精细，价格最贵（medium 的 4 倍） | 商业用途、印刷品 |

---

## 四、写好提示词的技巧

### 万能公式

```
[风格/媒介] + [主体] + [环境/场景] + [光线] + [构图] + [技术参数]
```

每个元素给模型一个明确约束，越精确，模型越少「自由发挥」。

### 六条核心原则

1. **描述要具体**：不要写「画一只猫」，而是「一只橘色的英短猫，趴在窗台上晒太阳，窗外是樱花」
2. **像导演一样写**：用自然语言描述场景，而不是堆关键词。GPT-Image-2 有推理能力，能理解复杂句子
3. **指定光线**：「柔和的窗户侧光」「金色夕阳逆光」「单灯伦勃朗光」比「好看的光线」有效 100 倍
4. **说明构图**：如「特写」「俯视角度」「全景」「三分法构图」
5. **说明不要什么**：加上"no text, no watermark, no border"可以避免常见的翻车
6. **指定比例**：不指定默认正方形，记得加 "aspect ratio 16:9" 或 "aspect ratio 9:16"

### 分场景示例 Prompt（可直接复制使用）

---

#### 场景 1：人像摄影

> 35mm film photography, warm natural window light. A young woman sitting in a vintage bookshop, reading a hardcover book. Soft afternoon sunlight filtering through dusty windows, casting warm golden light across the scene. Medium shot, slightly off-center composition with shallow depth of field. Aspect ratio 3:4.

适合：社交媒体头像、个人品牌形象照

---

#### 场景 2：电影感肖像

> Cinematic portrait of a solitary figure standing in an intense orange-to-red gradient environment. Strong silhouette lighting from behind, deep shadow contrast, reflective glossy floor mirroring the figure. Symmetrical composition, minimal set design. The mood is contemplative and powerful, like a still from a Denis Villeneuve film. Aspect ratio 16:9.

适合：壁纸、视频封面、概念艺术

---

#### 场景 3：产品摄影

> Product photography of a matte black wireless speaker on a polished concrete surface. Single product, centered composition. Soft gradient studio lighting from above and camera left. Subtle reflection on the surface beneath. Background: clean warm off-white. Shot on 90mm macro lens with edge-to-edge sharpness. Commercial advertising style, Apple-level product photography. No props, no text.

适合：电商主图、产品宣传

---

#### 场景 4：城市海报（文字渲染测试）

> A striking Spring 2026 city poster for New York with a bold contemporary design. Clean off-white textured background with generous negative space. A miniature kayaker paddles across a narrow ribbon of reflective water. The wake sweeps upward in a dynamic calligraphic curve, transforming into a dreamlike hand-painted panorama of Manhattan. Inside the flowing composition: the Empire State Building, Brooklyn Bridge, Central Park canopy, yellow cabs, and the Statue of Liberty. Elegant typography reads "SPRING 2026" with a vertical slogan "NEW YORK — A CITY OF BRIDGES, DREAMS, AND REINVENTION". Aspect ratio 9:16.

适合：活动海报、宣传物料（GPT-Image-2 的文字渲染准确率 > 95%）

---

#### 场景 5：游戏角色设定

> Create a professional character reference sheet for a fantasy RPG character: a young female mage with silver hair and violet eyes, wearing an ornate dark cloak with glowing rune patterns. Include on a clean white background: a three-view turnaround (front, side, back); facial expression variations (neutral, smiling, angry, surprised); detailed costume breakdowns; a color palette swatch row. Organized grid layout, concept art style. Aspect ratio 16:9.

适合：游戏开发、角色设计、同人创作

---

#### 场景 6：美食摄影

> Overhead flat-lay food photography of a mezze spread. Multiple small bowls on a weathered wooden table. Hummus with paprika oil drizzle, baba ganoush, tabbouleh, warm pita torn into pieces, olives, sliced cucumber. Scattered fresh herbs — parsley and mint. Linen napkin tucked in one corner. Warm natural light from camera left. Rustic, abundant feel. Bon Appétit photography style. Rich warm color palette.

适合：美食博客、餐厅菜单、社交媒体

---

#### 场景 7：UI 截图 / 社交媒体 Mockup

> A hyper-realistic iPhone screenshot of a fictional Instagram profile page for Leonardo da Vinci, username @davinci_official, as if he were a modern influencer. Profile photo is a Renaissance self-portrait. Bio reads: "Artist, Engineer, Inventor | Currently dissecting things | DM for commissions". The grid shows 9 posts: the Mona Lisa as a mirror selfie, a helicopter sketch captioned "just dropped my new drone design", an anatomy study as a gym progress photo. Follower count: 12.4M. Dark mode UI. Photorealistic screenshot quality, aspect ratio 9:16.

适合：社交媒体创意、UI 展示、病毒式传播内容

---

#### 场景 8：创意 / 搞笑梗图

> Inside a museum exhibit titled "Ancient Technology: The Desktop Era", a programmer in a glass display case is live-demonstrating coding on a CRT monitor while amazed schoolchildren press their faces against the glass. The exhibit placard reads: "Homo Developerus (c. 2005) — Primitive human using keyboard-based input devices." A second display case shows a physical book labeled "Stack Overflow — Print Edition, Vol. 1 of 4,827". 2D cartoon illustration style, warm museum lighting, humorous tone. Aspect ratio 16:9.

适合：技术社区分享、梗图、轻松内容

---

### 进阶技巧

| 技巧 | 说明 | 示例 |
|------|------|------|
| 指定相机/胶片 | 传达整套美学风格 | "Shot on Hasselblad 500C""Kodak Portra 400 film" |
| 限定色板 | 防止模型用过饱和的彩虹色 | "Color palette: warm white, walnut brown, black accents" |
| 对话式迭代 | 在同一对话中追加修改 | 先生成 → 再说「把天空改成日落」「把主体移到画面左三分之一」 |
| 多语言文字 | GPT-Image-2 支持中/英/日/韩/阿拉伯文 | 直接在 prompt 中写中文标题即可 |

更多官方示例参考：[OpenAI Prompting Guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

---

## 五、免费替代方案

如果觉得 OpenAI 贵，Google 也有免费选项：

- 打开 [Google AI Studio](https://aistudio.google.com)
- Pro/Ultra 用户可免费使用 Imagen 系列模型，支持 4K 分辨率
- 不需要付费 API Key，网页端直接画图

---

## 六、常见问题

**Q：ChatGPT 免费用户能用吗？**
A：能，但额度很少，medium 质量只有几张，之后会自动降为 low 质量。

**Q：API 调用贵吗？**
A：medium 质量 1.5K 分辨率约 $0.04/张（约 ¥0.3），日常使用成本不高。国内中转站更便宜，约 ¥0.04/张。

**Q：能用来做商业项目吗？**
A：可以，但建议使用 high 质量 + 高分辨率，并注意 OpenAI 的使用条款。

**Q：和 Midjourney / Stable Diffusion 比怎么样？**
A：LMArena 盲测排行榜上 GPT-Image-2 大幅领先，尤其在文字渲染和指令遵循方面优势明显。

---

## 参考资料

- [原文：🔥【图像视频系列7】关于GPT-Image-2，你想知道的一切 - LINUX DO](https://linux.do/t/topic/2026332)
- [GPT Image 2 官方文档](https://developers.openai.com/api/docs/models/gpt-image-2)
- [Token 计算器](https://developers.openai.com/api/docs/guides/image-generation?api=responses#size-and-quality-options)
- [官方 Prompting Guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)
- [OpenAI 定价页](https://developers.openai.com/api/docs/pricing)
- [50 Best ChatGPT Image Prompts - SurePrompts](https://sureprompts.com/blog/chatgpt-image-prompts-2026)
- [GPT Image 2 Review: Prompt Guide and Use Cases - PixVerse](https://pixverse.ai/en/blog/gpt-image-2-review-and-prompt-guide)
