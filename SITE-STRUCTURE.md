# China Pins Factory（CPF）站点结构规划

> 目标：面向 Google 与 AI 搜索场景的 B2B 批发外贸站。纯批发，不做零售。
> 品牌：China Pins Factory，标识缩写 CPF。域名：`chinapinsfactory.com`。
> 报价策略：全站不公开价格，采用国际 B2B 工厂的 Quote only 做法，价格走询价。
> 语言：仅纯英文站，不做中文版。
> 本文件是实施的唯一依据。改结构前先改这里。

---

## 〇、实施状态（2026-10-25 更新）

**18 个页面已全部建成并通过全站校验。** Phase 1-3 完成，Phase 4 待办。

| 页面 | 状态 | 主词 | JSON-LD |
|---|---|---|---|
| index.html | 已重写 | custom lapel pins wholesale | Organization + WebSite + WebPage + ItemList + HowTo + FAQPage |
| products/custom-enamel-pins.html | 已重写 | wholesale custom enamel pins | BreadcrumbList + ItemList + Service×6 + FAQPage |
| products/custom-metal-swag.html | 已重写 | wholesale custom challenge coins | BreadcrumbList + ItemList + Service×7 |
| guides/bulk-order-guide.html | 已建 | bulk order lapel pins | BreadcrumbList + Service + OfferCatalog + FAQPage |
| company/factory.html | 已重写 | china lapel pin factory | BreadcrumbList + Organization + LocalBusiness |
| products/request-a-quote.html | 已重写 | custom lapel pin quote | BreadcrumbList + ContactPage + Service + OfferCatalog |
| blog/index.html | 已建 | 内容中枢 | BreadcrumbList + Blog + ItemList |
| blog/how-to-order-custom-lapel-pins-from-china.html | 已建 | how to order custom lapel pins from china | BreadcrumbList + BlogPosting + FAQPage |
| blog/hard-enamel-vs-soft-enamel-pins.html | 已建 | hard enamel vs soft enamel pins | BreadcrumbList + BlogPosting + FAQPage |
| blog/lapel-pin-sizes-guide.html | 已建 | lapel pin sizes | BreadcrumbList + BlogPosting + FAQPage |
| blog/custom-challenge-coin-sizes-guide.html | 已建 | custom challenge coin sizes | BreadcrumbList + BlogPosting + FAQPage |
| legal/privacy-policy.html | 已建 | 无 | BreadcrumbList + WebPage |
| products/custom-metal-badges.html | 已建 | custom metal badges | Organization + Service |
| products/samples.html | 已建 | custom lapel pin samples | Organization + Service |
| guides/faq.html | 已建 | lapel pin faq | FAQPage（27 问） |
| company/contact.html | 已建 | contact lapel pin factory | Organization + ContactPage + LocalBusiness |
| 404.html | 已建 | 无 | WebPage（noindex） |
| thank-you.html | 已建 | 无 | WebPage（noindex, nofollow）· 仅表单提交后展示，站内无任何入口链接 |

**校验结果（全部通过）**

- 禁用词扫描零命中：`$[0-9]`、`MOQ`、`price list`、`per piece`、`Free mold on`、`Sedex`、`SMETA`、`aggregateRating`、`aggregateOffer`、`priceSpecification`
- 18/18 页面：Title ≤ 60 字符、Description 140-158 字符、恰好 1 个 H1、全部图片有 alt 与 width/height
- 全部 JSON-LD 可解析；Schema 禁用字段零命中
- canonical ↔ sitemap 双向一致（16 个可索引 URL，404 与 thank-you 不入 sitemap）
- 内链零断链，锚点零失效，图片引用零缺失
- 桌面 1440px 与移动 390px（DPR 2）均无横向溢出，零断图
- Spec Builder 在首页原地提交 Web3Forms，不跳转；规格实时同步到隐藏字段，工艺参数与表单 select 值完全对齐
- Spec Builder 交期矩阵 30 组合全部自洽（数量档位只延长、不缩短工艺交期）

**Phase 4 待办（上线前）**

- [ ] 移除主题切换器（DOM、`applySkin` JS、`<head>` 内联脚本，`ink` 变量固化为 `:root`）
- [ ] 替换邮箱、电话、WhatsApp、证书编号为真实信息
- [ ] 确认 8,000 ㎡ / 240 万枚 / 22 CNC / 16 冲压 / 8 压铸 / 24 点胶 / 18 技师为真实数据
- [ ] 确认认证覆盖范围，未覆盖则删除对应声明块
- [ ] 域名 www 与否最终确认（当前全站用 `https://www.chinapinsfactory.com`）
- [ ] 询价表单接后端（Formspree / Cloudflare Worker / 邮件转发）
- [ ] GA4 / Search Console 接入

**新增样式组件**（`assets/css/styles.css` 第 23-26 节）：`.page-hero`、`.stats--dark`、`.article__*`、`.toc`、`.post-meta`、`.author-box`、`.rows__*`、`.timeline__*`、`.callout`、`.bullets`、`.split__*`、`.deflist__*`、`.linkband`。

**页面生成器**：站点的 18 个页面由同一套 chrome 模板生成（head / 公告条 / 页头 / 面包屑 / 页脚 / 浮条 / 移动端吸底条 / 主题切换器），保证风格零漂移。改公共部分时改模板再重跑，或直接改各页 HTML（结构一致，手改同样安全）。

---

## 一、定位与买家

**一句话定位**：中国昆山（江苏）的自有工厂，做定制徽章（lapel pin / enamel pin / metal badge）的批量代工，只接批发单。

**站点主张**（贯穿全站的一句话）：Factory-direct. Wholesale only. Quote on request. 你直接跟工厂谈。

### 1.1 三类买家与站内落点

| 买家 | 他在搜什么 | 他要什么证据 | 站内落点 |
|---|---|---|---|
| 进口分销商 / 批发商 | wholesale custom lapel pins, lapel pin manufacturer | 交期、产能、能否小批量、能否盲发到 ASI/PPAI 仓 | 工厂页 + 批量下单指南 + 询价页 |
| 促销品代理商 / 创意公司 | custom enamel pins bulk, promo pin supplier | 打样速度、起订门槛、能否做小批量、工艺参数 | 品类页 + 规格速配器 + 博客 |
| 终端品牌 / 企业采购 | custom challenge coins, employee recognition pins | 材质工艺、认证、交期 | 工艺目录 + 工厂页 + 博客 |

### 1.2 工厂硬数据基准（全站唯一数据源）

首页、工厂页、品类页、Schema、FAQ 里的每一个数字都必须来自这张表，任何页面出现表外的数字都算错误。

| 项目 | 设定值 |
|---|---|
| 成立年份 | 2009 年（16 年制造经验） |
| 厂房面积 | 8,000 ㎡ |
| 年产能 | 240 万枚 |
| 出口国家 | 40 多个国家 |
| CNC 雕刻机 | 22 台 |
| 液压冲压机 | 16 台（最高压力 200 吨） |
| 锌合金压铸机 | 8 台 |
| 点胶机器人 | 24 台 |
| 手工上色技师 | 18 名 |
| 车间 | 6 大车间：模具 / 冲压压铸 / 抛光 / 电镀 / 上色 / 品控包装 |
| 认证 | ISO 9001:2015、BSCI 社会责任审核、RoHS |
| 常规生产交期 | 7-10 个工作日 |
| 加急交期 | 5 个工作日（可选，需在询价时确认产能窗口） |
| 打样 | 免费 2D/3D CAD 效果图，12 小时内出 |
| 起订量 | 无最低起订量，单枚起可打样 |
| 报价方式 | 逐单询价，页面不公开单价与阶梯价 |

**认证口径**：只保留 ISO 9001:2015、BSCI 社会责任审核、RoHS 三项。Sedex 4-Pillar 与 SMETA 全站不出现。

---

## 二、信息架构

采用**分类目录 URL**，按买家路径分五组，根目录只留系统文件与入口页。

最初（2026-10-24）用的是扁平 URL，18 个页面全堆在根目录。2026-10-25 改为分类目录，理由是文件一多就没法看了，18 个平铺文件和 5 个目录在维护时的差别很大 —— 找一条产品页要在一屏长列表里扫，而目录结构本身就是给维护者看的地图。

改结构时保住了两条原扁平结构的好性质：

1. **静态托管零配置。** 子目录被静态服务器原样映射成 URL 路径，Cloudflare Pages / Netlify / Nginx / 虚拟主机都不用额外配置，GitHub Pages 直接就能跑。
2. **`file://` 双击就能预览，不用起服务。** 站内链接一律用相对路径（`../products/request-a-quote.html`），不写目录形式（`../products/`）—— 浏览器打开 `file://` 目录时显示的是文件列表而不是 `index.html`，写成目录形式会丢掉双击预览。代价是 `blog/index.html` 的对外 URL 仍由 canonical 指向干净的 `/blog/`。

```
/  (index.html)                                   首页 · 工厂定位 + 信任锚 + 规格速配器 + FAQ + RFQ
│
├── products/                                    买什么
│   ├── index.html                               ★ 目录中枢 · 5 条产品线聚合页（对外 URL /products/）
│   ├── custom-enamel-pins.html                  核心品类 · 5 种工艺 + 电镀 + 背扣 + 包装
│   ├── custom-metal-swag.html                   延伸品类 · 挑战币 / 奖牌 / 钥匙扣 / 皮带扣 / 袖扣
│   ├── custom-metal-badges.html                 延伸品类 · 徽章类目（服务徽章 / 盾形 / 机构徽章）
│   ├── samples.html                             ★ 打样与原型 · 四类样品 / 成本 / 交期
│   └── request-a-quote.html                     询价页 · 全站唯一转化落地页
│
├── guides/                                      怎么买
│   ├── index.html                               ★ 目录中枢 · 按买家任务分组（对外 URL /guides/）
│   ├── bulk-order-guide.html                    ★ 批量下单指南 · 长尾承接页，无任何金额
│   ├── design-file-specs.html                   ★ 设计文件规范 · 线宽 / 色块 / 字号 / 格式
│   ├── process-comparison.html                  ★ 五工艺对比矩阵 · 同口径横向对比
│   └── faq.html                                 ★ 独立 FAQ · 27 问长尾承接
│
├── company/                                     是不是靠谱
│   ├── index.html                               ★ 目录中枢 · 工厂 / 联系 / 样品（对外 URL /company/）
│   ├── factory.html                             工厂与品控 · E-E-A-T 信任页
│   └── contact.html                             ★ 联系页 · 联系方式 / 工厂档案 / 联系表单
│
├── blog/                                        知识
│   ├── index.html                               ★ 内容中枢 · 文章索引（对外 URL /blog/）
│   ├── how-to-order-custom-lapel-pins-from-china.html   长尾 · 采购流程
│   ├── hard-enamel-vs-soft-enamel-pins.html             长尾 · 工艺对比
│   ├── lapel-pin-sizes-guide.html                      长尾 · 尺寸规格
│   └── custom-challenge-coin-sizes-guide.html           长尾 · 挑战币规格
│
├── legal/
│   └── privacy-policy.html                      ★ 信任与合规
│
├── 404.html                                     ★ 兜底页
└── thank-you.html                               ◦ 表单提交后展示 · 不挂链接、不进 sitemap
```

**最终 23 个页面**（原 5 + 新增 18）。文件名相对旧版的三处变化：

| 旧文件名 | 新文件名 | 变化原因 |
|---|---|---|
| `bulk-pricing.html` | `guides/bulk-order-guide.html` | 页面不再承载价格表，改为批量下单流程与贸易条款指南 |
| `blog-lapel-pin-sizes-and-pricing-guide.html` | `blog/lapel-pin-sizes-guide.html` | 去掉价格字眼，主词收敛到 lapel pin sizes |
| `blog-custom-challenge-coin-sizes-and-price-guide.html` | `blog/custom-challenge-coin-sizes-guide.html` | 去掉价格字眼，主词收敛到 custom challenge coin sizes |

### 2.0.1 2026-10-25 目录重构的旧 URL 映射

重构后旧地址全部失效。`404.html` 内置了旧路径 → 新路径的跳转表，命中即自动跳走；真正的 301 需要在 Cloudflare 侧配 Bulk Redirect（规则表见 `README.md`）。完整对照：

| 旧路径 | 新路径 |
|---|---|
| `/wholesale-custom-pins.html` | `/products/custom-enamel-pins.html` |
| `/custom-metal-swag.html` | `/products/custom-metal-swag.html` |
| `/custom-metal-badges.html` | `/products/custom-metal-badges.html` |
| `/samples.html` | `/products/samples.html` |
| `/wholesale-quote.html` | `/products/request-a-quote.html` |
| `/bulk-order-guide.html` | `/guides/bulk-order-guide.html` |
| `/faq.html` | `/guides/faq.html` |
| `/china-pin-factory.html` | `/company/factory.html` |
| `/contact.html` | `/company/contact.html` |
| `/blog.html` | `/blog/` |
| `/blog-how-to-order-custom-lapel-pins-from-china.html` | `/blog/how-to-order-custom-lapel-pins-from-china.html` |
| `/blog-hard-enamel-vs-soft-enamel-pins.html` | `/blog/hard-enamel-vs-soft-enamel-pins.html` |
| `/blog-lapel-pin-sizes-guide.html` | `/blog/lapel-pin-sizes-guide.html` |
| `/blog-custom-challenge-coin-sizes-guide.html` | `/blog/custom-challenge-coin-sizes-guide.html` |
| `/privacy-policy.html` | `/legal/privacy-policy.html` |

### 2.0.2 2026-10-25 子页 hero 改为单栏居中

**改动前的问题**：`.page-hero h1` 上有 `max-width: 20ch`。`ch` 是"0"字符的宽度，h1 字号在 1440px 视口下是 49.6px，20ch 只有 668px——这是给窄栏设计的行宽约束，却被套在了 1232px 宽的容器上。后果有两个：标题被强行折行（"Notes from the workshop floor" 733px 放不下，"floor" 孤零零掉到第二行），加上 `.lede` 的 68ch = 741px，容器右边界 1336px 处**空出 491px，占可用宽度的 40%**。`.page-hero::after` 的网格纹理又用 `mask-image: radial-gradient(70% 70% at 20% 40%)` 锚在左侧 20%，往右直接淡出，所以右半边连纹理都没有，只剩背景上那一小块金色辉光。

**改成什么**：子页 hero 改为**单栏居中**。

- `.page-hero .container` 加 `text-align: center`；h1 改 `max-width: 25ch`（≈805px），`margin: 0 auto`，加 `text-wrap: balance`。
- 段落 `max-width: 68ch` 居中 + `text-wrap: pretty`；`.hero__actions`、`.post-meta` 改 `justify-content: center`。
- 背景辉光从 `at 88% 8%` 移到 `at 50% 0%`，网格纹理的 mask 锚点从 `20% 40%` 移到 `50% 36%`，左右对称。

**为什么不加右栏图片**：首页 hero 已经是"左文 + 右侧出血图"的两栏结构（`.hero__media` 绝对定位占 48%），子页是纯文字页，硬塞一张图会与首页抢戏，也会让子页的转化路径（标题→导语→按钮）被视觉噪音打断。单栏居中是"一句话抬头"的正确形态：左右留白对称，看起来是刻意的版式而不是没排满。

**首页保持不变**：`index.html` 的 `.hero` 仍是左文 + 右图的两栏。首页是形象页，子页是陈述页，两者形态不同是合理的区分。

### 2.0.3 2026-10-25 统计条与 404 页的两个修复

**统计条对齐**：`.stats` 是 5 列网格，1440px 下每格内容区只有 197px，而 `.stat__num` 是 36.8px 的展示数字。实测 `7 to 10 business days` 宽 354px，必然折成 3 行，标签比其他格子低 73px，一排数字参差不齐。

- **文案拆分**：把"单位"从数字挪到标签。`7 to 10 business days` → 数字 `7 to 10` + 标签 `Business days, standard production lead time`；`5 business days` → 数字 `5 days` + 标签 `Business days, rush option where a window allows`；`20 to 60 mm` → `20–60 mm`。事实不变，全站两种交期写法也统一了（原先 24 处写 "7 to 10 business days"、2 处写 "7 to 10 days"）。
- **组件改法**：分隔线不再用 `gap: 1px` + 容器底色，改成每个单元格的 `box-shadow: inset -1px -1px 0`。这样当列数除不尽条目数时（平板 3 列放 5 条），剩下的空格子会和格子底色融为一体，而不是露出一块灰底。
- **断点**：≤860px 统计条改 3 列（原先是 5 列，数字会被挤到折行）；≤640px 保持 2 列并把单元格内边距从 `30px 24px` 收到 `24px 14px`。

**404 页在 `file://` 下丢样式**：`404.html` 里有一段脚本，在页面被请求到子路径时把相对引用改写成站点根绝对路径。原来的守卫是 `window.location.origin !== 'null'`，但 Chrome 在 `file://` 下返回的是字符串 `"file://"` 而不是 `"null"`，守卫失效，脚本把样式表改写成了 `/assets/css/styles.css`，Windows 上被解析到磁盘根 `C:/assets/...`，整页裸奔。改成按 `location.protocol` 判断协议，并算出真正的 ROOT（`file://` 下取 404.html 所在目录），同时给 `absolute()` 加了 `file:` 前缀和幂等判断，避免二次改写时重复套 ROOT。

**头部在 861–1024px 区间溢出**：全宽导航（当时 6 项）+ wordmark + 头部按钮在 900px 视口下需要 990px，超出 115px，"Get a Quote" 按钮被推出屏幕右缘，产生横向滚动条。最初加了 `max-width: 1024px` 断点隐藏 `.header__cta`，并把导航间距从 26px 收到 16px、字号从 .92rem 收到 .85rem。

2026-10-27 导航项由 6 项减为 5 项（删除与 CTA 重复的 `Request a Quote`）后释放约 143px，隐藏断点相应放宽到 `max-width: 1000px`，1001px 起 CTA 单行完整可见。

### 2.0.4 响应式不变量（改版时的验收线）

以下三条是 2026-10-25 实测 360–1920px 全区间后固化的验收标准，改样式时不要破坏：

1. **统计数字必须单行。** `.stats` 在 ≥1101px 是 5 列，每格内容区只有 198px，`.stat__num` 是 36.8px 的展示数字。数字文本必须控制在 180px 以内（约 12 个窄字符），否则标签会被顶得比邻居低 73px。单位放到标签里（`7 to 10` + `Business days, standard production`）。
2. **hero 标题的比例稳定。** h1 用 `max-width: 25ch`，ch 随字号缩放，所以在 1440px 占列宽 65%、900px 占 71%、手机占 91%——随视口收放但始终居中，不会出现"某档宽度特别空"。
3. **任何断点都不能产生横向滚动条。** 用 `document.documentElement.scrollWidth - clientWidth` 判定。表格的 `min-width: 640px` 在 `.table-wrap` 里是安全的滚动容器，不算溢出。
4. **页头询价按钮的下断点是 880px，隐藏时必须保留占位。** 2026-10-27 实测：三个 caret 全部显示（触屏指针，hover 不存在）时，字标、导航、按钮三者在 871px 以上仍能并排不重叠，所以按钮可以一直显示到 880px。但隐藏时不能用 `display: none`，只能用 `visibility: hidden`：一旦按钮彻底离开布局，`justify-content: space-between` 会把导航推到视口右缘，230px 宽的 Guides 下拉面板就会超出屏幕 1px，整页出现横向滚动。改导航结构后重跑 `python scripts/nav_responsive.py`，它会同时验这三条。

### 2.0.5 导航三层结构与下拉分组（2026-10-27 定案）

**三层各司其职，不重复。**

| 层 | 装什么 | 当前内容 |
|---|---|---|
| 导航 | 买家意图直达 | 4 个顶级项 + 10 个二级项 |
| 面包屑 | 目录层级 | `Home / 目录 / 当前页` |
| 页脚 | 平铺实用链接 | 23 页完全一致，无目录项 |

**导航结构**

```
导航        Products            Guides                 Our Factory      Journal
            4 个二级项          4 个二级项             2 个二级项         平铺，无二级
            ├ Custom enamel pins        ├ How to order in bulk from China
            ├ Challenge coins, medals and swag  ├ Design file specifications
            ├ Custom metal badges       ├ Five processes, side by side
            └ Samples and prototyping    └ Frequently asked questions
                                         ├ Our factory and quality control
                                         └ Contact our export desk
```

**四条定案规则**

1. **顶级项是意图，不是目录。** 三个下拉组的父项本身就是通往目录中枢的真实 `<a>`（`products/index.html` / `guides/index.html` / `company/index.html`），所以脚本不运行时二级页面照样可达，父项链接不空。
2. **Journal 保持平铺。** 入口层稳态不增长：每加一篇新文章就往导航里加一项，导航会退化成文章列表。文章级入口由 `blog/index.html` 聚合页承担，导航只留一个指向聚合页的入口。
3. **二级项不进页脚。** 目录层级只出现在面包屑里。页脚三列装的是具体工艺与杂项链接，塞进目录节点会打乱层级。
4. **不重复同一功能的入口。** 导航项与紧邻的 CTA 按钮都指向 `request-a-quote.html` 就是重复。询价入口全站只有页头 `Get a Quote` 按钮、移动端吸底条与各页语境 CTA 三类。

**当前项标记规则**

- 目录组里的任意页面（hub 或二级项）→ 该组 `<li>` 加 `is-active`
- 当前页恰好是 hub → 父 `<a>` 加 `aria-current="page"`
- 当前页是某个二级项 → 该 sublink 加 `aria-current="page"`
- 全页 `is-active` 至多 1 个、`aria-current` 至多 1 个（`scripts/check.py` 强制）

**降级与无障碍**

- 父项是真链接，`<button class="nav__caret">` 只负责展开，`aria-expanded` 与展开状态同步
- 桌面端 `hover` / `focus-within` / `.is-open` 三态叠加，`:focus-within` 保证纯键盘 Tab 也能展开
- 移动端（≤860px）导航变竖排抽屉，下拉降级为手风琴。**这是本次改造最大的回归风险点**：hover 在触屏上不存在，触屏用户会一次性丢掉全部 10 个二级入口
- `Esc` 关闭当前组并把焦点还给 caret，焦点离开导航区自动收起

### 2.0 Thank You 页的规则

`thank-you.html` 是全站唯一一个"没有人会主动点进去"的页面，它只为表单提交后的落地展示服务。三条硬规则：

1. **站内没有任何链接指向它。** 全站 `<a href="thank-you.html">` 数量恒为 0，导航、页脚、内容区都不出现它。它只由 `assets/js/main.js` 在提交成功后用 `window.location.href` 程序化跳转进入。
2. **不进 sitemap，`noindex, nofollow`。** 它没有可索引价值，也不该稀释站点的页面信号。canonical 指向自身即可。
3. **只做一件事。** 确认已收到、说明下一步（12 小时内出图与报价）、给出紧急联系方式、给出少量出站链接让人继续逛。不放导航、不放页脚之外的入口、不做二次转化。

四个表单（首页 RFQ、Spec Builder、询价页、联系页）提交成功后统一跳到这里，失败时留在原地报错。

### 2.1 页面角色表

| 页面 | 页面职责 | 主关键词 | 转化目标 |
|---|---|---|---|
| index.html | 回答"这厂靠谱吗、卖什么、能做什么规格" | custom lapel pins wholesale | 跳批量下单指南 / 询价页 |
| products/custom-enamel-pins.html | 工艺选型与规格决策 | wholesale custom enamel pins | 跳询价页 |
| products/custom-metal-swag.html | 承接徽章之外的金属品类 | wholesale custom challenge coins | 跳询价页 |
| guides/bulk-order-guide.html | 教买家怎么批量下单、怎么谈贸易条款 | bulk order lapel pins | 跳询价页 |
| company/factory.html | 证明是工厂不是贸易商 | china lapel pin factory | 跳询价页 |
| products/request-a-quote.html | 收表单 | custom lapel pin quote | 表单提交 |
| blog/index.html + 4 篇 | 吃信息型长尾，建主题集群 | how to order lapel pins from china 等 | 跳品类页 / 批量下单指南 / 询价页 |
| products/custom-metal-badges.html | 承接徽章类目的独立采购意图 | custom metal badges | 跳询价页 |
| products/samples.html | 讲清打样流程，化解"先买样品"的顾虑 | custom lapel pin samples | 跳询价页 |
| guides/faq.html | 27 问承接疑问型长尾 | lapel pin faq | 跳品类页 / 询价页 |
| company/contact.html | 联系方式与工厂档案，补 E-E-A-T 信任 | contact lapel pin factory | 跳询价页 |
| legal/privacy-policy.html | 合规与信任 | 无 | 无 |
| 404.html | 留住误入流量 | 无 | 跳首页 |

### 2.2 guides/bulk-order-guide.html 内容大纲

长尾 SEO 价值来自真实的采购流程知识，页面不出现任何金额、单价、阶梯价、"起订量"门槛。

1. 为什么工厂要先问数量与用途（数量区间如何影响排期与工艺选择）
2. 数量档位与生产排期的关系（档位区间表，列出对交期、包装、打样安排的影响，不写金额）
3. 从草图到出货的完整流程（草图 / 2D-3D CAD 效果图 12 小时 / 确认开模 / 打样 / 确认色稿 / 大货 / 检验 / 包装 / 出货）
4. 打样与开模流程（模具类型、修改次数、免费效果图范围）
5. 包装选项（单枚吸塑、背卡、胶头袋、礼盒、贴牌分装）
6. 付款方式与节点（定金 / 尾款节点、常见结算方式）
7. 贸易条款：FOB / CIF / DDP 的适用场景与买家责任
8. 关税与进口注意事项（HTS 编码由买家确认、进口商身份、申报责任）
9. 常见下单问题（FAQ，覆盖设计文件格式、数量灵活度、样品与量产一致性、交期变更）

---

## 三、关键词地图（防内耗）

规则：**一个页面一个主词**，主词不重复；支撑词允许交叉，但主词必须唯一。

| 主词 | 页面 | 支撑词（该页可覆盖） |
|---|---|---|
| custom lapel pins wholesale | index.html | lapel pin manufacturer, bulk enamel pins, enamel pin supplier |
| wholesale custom enamel pins | products/custom-enamel-pins.html | hard enamel pin, soft enamel pin, die struck pin |
| wholesale custom challenge coins | products/custom-metal-swag.html | custom medals, metal keychains, belt buckles |
| bulk order lapel pins | guides/bulk-order-guide.html | how to order in bulk, bulk lapel pin order process, bulk pin order guide |
| china lapel pin factory | company/factory.html | OEM lapel pin manufacturer, factory direct pins, custom pin manufacturer china |
| custom lapel pin quote | products/request-a-quote.html | get lapel pin quote, lapel pin supplier quote, request pin quote |
| how to order custom lapel pins from china | blog/how-to-order-custom-lapel-pins-from-china.html | import lapel pins, China pin supplier, sourcing pins from china |
| hard enamel vs soft enamel pins | blog/hard-enamel-vs-soft-enamel-pins.html | cloisonne vs soft enamel, enamel finish comparison |
| lapel pin sizes | blog/lapel-pin-sizes-guide.html | lapel pin size chart, lapel pin dimensions |
| custom challenge coin sizes | blog/custom-challenge-coin-sizes-guide.html | challenge coin diameter chart, coin thickness |
| custom metal badges | products/custom-metal-badges.html | service badges, shield badges, organisation badges |
| custom lapel pin samples | products/samples.html | lapel pin sample order, prototype sample, sample kit finishes |
| lapel pin faq | guides/faq.html | enamel pin questions, custom pin minimum order, pin lead time |
| contact lapel pin factory | company/contact.html | contact china pin supplier, kunshan pin factory contact |

四篇文章互相不抢词，每篇都往品类页、批量下单指南与询价页导流。

**关键词层面的取舍**：主动放弃 pricing、price list、cost、how much 这一类词的落地页，把它们降级为询价页与批量下单指南里的支撑语义，页面照常能被相关词命中，但不做专门的比价型落地页。

---

## 四、内链枢纽

```
                          index.html
        ┌───────────┼───────────┬────────────┐
        ▼           ▼           ▼            ▼
   品类页       金属周边页   批量下单指南    工厂页
   products/    products/    guides/       company/
        │           │           │            │
        └───────────┴─────┬─────┘            │
                          ▼                  │
                     blog/index.html        │
                          │                  │
              文章 ×4 ─────┴──────────────────┘
             （每篇 → 品类页 / 批量下单指南 / 询价页，3 条内链起步）

                  products/request-a-quote.html
                 （全站唯一转化落地页，被以上所有节点指向）
```

规则：

1. 每页页头导航固定 5 个链接（品类页 / 金属周边页 / 批量下单指南 / 工厂页 / 博客），保证任意两页之间 ≤2 跳。询价入口由页头 CTA 按钮与移动端吸底条承担，不占导航项。
2. 文章正文里出现的品类词必须链到对应品类页，**不做锚文本堆砌**，用自然句做锚。
3. 面包屑只在子页出现，首页不出现（首页本身就是根）。
4. 批量下单指南是第二强承接页，至少被首页、文章、品类页各链一次。
5. 每页页脚固定"批量下单指南 + 询价"双 CTA，链接到 `guides/bulk-order-guide.html` 与 `products/request-a-quote.html`。

---

## 五、每页 head 模板

所有页面统一这套结构，变量部分替换即可：

```html
<meta name="description" content="…">            <!-- 140-158 字符 -->
<link rel="canonical" href="https://chinapinsfactory.com/…">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="website">
<meta property="og:site_name" content="China Pins Factory">
<meta property="og:url" content="https://chinapinsfactory.com/…">
<meta property="og:image" content="https://chinapinsfactory.com/assets/images/og-cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" hreflang="en" href="https://chinapinsfactory.com/…">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

**规则**

- Title ≤ 60 字符，主词靠前，结尾不硬塞品牌名。
- Description 140-158 字符，带一个具体数字（来自 1.2 数据表）和一个差异化承诺。
- **删掉 `meta keywords`**（Google 2009 年起不读，留着显得不专业）。
- canonical 必须是绝对 URL，且与 sitemap 完全一致。
- 每页一个 H1，H2 分区，H3 细分，不跳级。
- 单语言站，只留 `hreflang="en"`，不写 `zh-cn`，不做多语言互指。

---

## 六、结构化数据矩阵

| 页面 | Schema 类型 |
|---|---|
| index.html | `Organization` + `WebSite` + `WebPage` + `ItemList` + `FAQPage` + `HowTo`（下单流程） |
| products/custom-enamel-pins.html | `BreadcrumbList` + `ItemList` + `Service` × 6（1 个页面级 + 5 个工艺段，只写材质、尺寸、工艺属性） |
| products/custom-metal-swag.html | `BreadcrumbList` + `ItemList` + `Service` × 7（1 个页面级 + 6 个品类段，只写材质、尺寸、工艺属性） |
| guides/bulk-order-guide.html | `BreadcrumbList` + `Service` + `OfferCatalog`（catalog 只列服务项目，不带金额） |
| company/factory.html | `BreadcrumbList` + `Organization` + `LocalBusiness`（geo 坐标） |
| products/request-a-quote.html | `BreadcrumbList` + `ContactPage` + `Service` + `OfferCatalog`（服务项，无金额） |
| blog/index.html | `BreadcrumbList` + `Blog` + `ItemList` |
| 文章页 | `BlogPosting` + `BreadcrumbList` + `FAQPage`（有 FAQ 段落的文章） |
| legal/privacy-policy.html | `WebPage` + `BreadcrumbList` |
| 404.html | `WebPage` + `noindex` |

**为什么用 `Service` 而不是 `Product`**（2026-10-26 修正）：

Search Console 报过一条严重错误「应指定 offers、review 或 aggregateRating」。根因是这两个页面各有 5 个和 6 个 `Product` 节点，而它们描述的是**工艺板块**（hard enamel、die struck、challenge coins……），不是可直接下单的商品条目，所以既没有 `offers` 也没有 `review`。

本站**不公布价格、不采集评价**，编造 `offers` 或 `aggregateRating` 属于虚假标注，处罚比缺属性更重，还会和页面正文自相矛盾。Google 对此的官方口径是：无效标记只影响对应富媒体结果的资格，不影响页面收录；不适用商品摘要时应移除 `Product` 标记。

因此这 11 个节点改为 `Service`——这才是它们的实际语义（按图生产的代工服务），也跟 `guides/bulk-order-guide.html` 里对同样五种工艺用 `Service` 的写法一致。属性映射：

| 原 `Product` 属性 | 改为 | 说明 |
|---|---|---|
| `@type: Product` | `@type: Service` | |
| `manufacturer` | `provider` | Service 的规范属性名 |
| `category` | `serviceType` | Service 的规范属性名 |
| `material` | 并入 `additionalProperty` | Service 无此属性，不丢弃而是转成 `PropertyValue` |
| — | 新增 `areaServed` | "Worldwide"，页面可如实声明 |
| — | 新增 `url` | 指向页内锚点，与 `@id` 一致 |

`name` / `description` / `image` / `brand` / `additionalProperty` 原样保留，所有 `@id` 仍指向同一页面的同一锚点，指向这些板块的站内链接不受影响。

**不变量**：全站不得出现 `Product` / `Offer` / `AggregateOffer` / `Review` 节点——除非站内真的开始公开价格或采集到真实评价。到那时才引入 `Product` + `offers`（价格须与页面可见文字完全一致）或 `aggregateRating`（须是页面上可见的真实评分）。

**OfferCatalog 的正确用法**（替代被删掉的价格表）：

```json
{
  "@context": "https://schema.org",
  "@type": "OfferCatalog",
  "name": "China Pins Factory custom lapel pin services",
  "itemListElement": [
    { "@type": "OfferCatalog", "name": "Craft services",
      "itemListElement": [
        { "@type": "Service", "name": "Hard enamel pin production" },
        { "@type": "Service", "name": "Soft enamel pin production" },
        { "@type": "Service", "name": "Die struck pin production" },
        { "@type": "Service", "name": "3D die cast pin production" },
        { "@type": "Service", "name": "Offset printed pin production" }
      ] },
    { "@type": "OfferCatalog", "name": "Tooling services",
      "itemListElement": [
        { "@type": "Service", "name": "Custom 2D and 3D CAD artwork" },
        { "@type": "Service", "name": "Steel die engraving" }
      ] },
    { "@type": "OfferCatalog", "name": "Sampling services",
      "itemListElement": [
        { "@type": "Service", "name": "Single piece sample production" },
        { "@type": "Service", "name": "Pre-production sample approval" }
      ] },
    { "@type": "OfferCatalog", "name": "Packaging services",
      "itemListElement": [
        { "@type": "Service", "name": "Backing card packing" },
        { "@type": "Service", "name": "Custom gift box packing" }
      ] }
  ]
}
```

**四条硬规矩**

1. Schema 里写的任何数字，必须在页面上肉眼可见。工厂面积、设备台数、交期、产能全部对得上 1.2 表。FAQ 同理，FAQ 里的答案必须在页面正文里逐条出现。
2. **禁止任何价格类字段**：`offers`、`priceSpecification`、`AggregateOffer`、`priceRange`、带金额的 `Offer` 一律不写。报价入口统一用 `Service` 加 `url` 指向询价页。
3. **不写 `aggregateRating`**。原站 `4.9 / 428 条评价` 配三条编造人名的证言，这是 Google 虚假评价政策的红线，真实商家有被人工处罚和降权的风险。
4. 证言改成不带虚构人名的「行业结果卡」（客群类型 + 地区 + 达成结果），真实评价等客户授权后自行填写。

---

## 七、图片资产与 alt 映射

30 张内容图已生成在 `raw-images/`（原始 PNG，含水印），压缩产物在 `assets/images/`（.webp + .jpg 双格式），另有 1 张 og-cover 社交分享图。

**命名规范**：语义化英文小写连字符，与槽位一一对应。alt 文本里不出现价格、单价、起订量类措辞。

| 文件名 | 用途 | alt 文本（最终稿） |
|---|---|---|
| hero-enamel-pins | 首页主视觉 | Wholesale custom hard enamel and soft enamel lapel pins with polished gold plating, produced in bulk at our China factory |
| pin-hard-enamel | 首页卡片 | Custom hard enamel lapel pin wholesale with flat glossy enamel fill flush to raised gold metal lines |
| pin-soft-enamel | 首页卡片 | Wholesale soft enamel lapel pin with recessed Pantone colour fill and raised black nickel border |
| pin-die-struck | 首页卡片 | Die struck all-metal antique brass lapel pin with sandblasted recess and polished relief |
| pin-3d-die-cast | 首页卡片 | 3D die cast zinc alloy lapel pin with multi-level relief and internal cutouts |
| pin-offset-printed | 首页卡片 | Offset printed lapel pin with full colour CMYK artwork under a clear epoxy dome |
| pin-glitter-glow | 首页卡片 | Wholesale trading lapel pins in glitter, glow-in-the-dark and stained glass enamel finishes |
| swag-challenge-coins | 首页卡片 | Wholesale custom challenge coins with dual-sided 3D relief and diamond-cut edges |
| swag-medals | 首页卡片 | Custom finisher medals with full colour sublimated neck ribbons, wholesale production |
| swag-keychains | 首页卡片 | Wholesale custom metal keychains including enamel, bottle opener and leather fob styles |
| swag-cufflinks-buckles | 首页卡片 | Custom wholesale cufflinks, tie bars and cast zinc alloy belt buckles |
| detail-hard-enamel-macro | 工艺页 | Macro view of a hard enamel lapel pin showing enamel polished flush with raised gold borders |
| detail-soft-enamel-recess | 工艺页 | Close-up of soft enamel recessed into the cavities of a custom lapel pin |
| detail-die-struck-antique | 工艺页 | Antique brass die struck lapel pin showing contrast between polished relief and matte recess |
| detail-3d-die-cast-mechanism | 工艺页 | 3D die cast lapel pin with working spinner mechanism and cast internal cutouts |
| detail-offset-print-epoxy | 工艺页 | Offset printed lapel pin sealed under a clear non-yellowing epoxy resin dome |
| detail-plating-finishes | 工艺页 | Twelve custom lapel pin electroplating finishes including 24K gold, black nickel and rose gold |
| detail-pin-backings | 工艺页 | Lapel pin backings including brass butterfly clutch, rubber PVC cap and locking clutch |
| detail-retail-packaging | 工艺页 | Wholesale lapel pin retail packaging with backing cards, header bags and gift boxes |
| factory-cnc-mold | 工厂页 | CNC engraving machine cutting a precision steel die for custom lapel pins |
| factory-stamping-diecast | 工厂页 | Hydraulic stamping press and zinc alloy die casting machines producing lapel pin blanks |
| factory-polishing | 工厂页 | Polishing workshop with metal lapel pins tumbled to a mirror finish |
| factory-electroplating | 工厂页 | Electroplating line with racks of lapel pin blanks entering a plating tank |
| factory-enamel-dispensing | 工厂页 | Robotic enamel dispensing machine filling Pantone colour into lapel pin cavities |
| factory-qc-inspection | 工厂页 | Quality control inspector checking lapel pins under a daylight magnifier with XRF tester |
| sample-kit-finishes | 询价页 | Free distributor sample kit showing twelve custom lapel pin plating finishes |
| blog-ordering-workflow | 博客 | Artwork, CAD proof and packed cartons showing the custom lapel pin order workflow |
| blog-enamel-comparison | 博客 | Hard enamel and soft enamel lapel pins side by side showing the difference in finish |
| blog-pin-sizes | 博客 | Six custom lapel pins arranged from 0.75 inch to 2 inch diameter beside a steel ruler |
| blog-coin-guide | 博客 | Custom challenge coins in four diameters with 3D relief and diamond-cut edges |
| og-cover | 社交分享 | China Pins Factory wholesale custom lapel pin manufacturing, factory direct |

**技术要求**

- 全部输出 WebP + JPG 双格式，用 `<picture>` 交付，WebP 优先。

```html
<picture>
  <source srcset="/assets/images/hero-enamel-pins.webp" type="image/webp">
  <img src="/assets/images/hero-enamel-pins.jpg"
       alt="Wholesale custom hard enamel and soft enamel lapel pins with polished gold plating, produced in bulk at our China factory"
       width="1200" height="630" fetchpriority="high" decoding="async">
</picture>
```

- 首屏 hero 用 `fetchpriority="high"`，其余全部 `loading="lazy" decoding="async"`。
- 每张图写死 `width` / `height` 属性，杜绝 CLS。
- CSS 统一 `aspect-ratio` + `object-fit: cover`，源图比例不同也不会变形。
- 全部图片走绝对路径 `/assets/images/…`，与 canonical 域名一致。
- WebP 全部 < 250KB。

---

## 八、转化组件

| 组件 | 位置 | 说明 |
|---|---|---|
| 顶部公告条 | 全站 | 6 个短标签：Wholesale only（徽章）· 12H Free Proof · 24/7 Customer Support · No Minimum Qty · Factory Direct · Global Shipping。徽章后 5 条用金色圆点分隔。**响应式不变量**：公告条恒为单行 44px；≤1150px 隐藏右侧联系方式（邮箱与电话在每页页脚和移动端吸底条都有），≤900px 左区改为横向滚动并加右端渐隐，绝不换行堆叠 |
| 页头询价 CTA | 页头右侧 | 所有页面固定 |
| 浮动咨询条 | 右下角 | WhatsApp + 邮件，桌面端常驻 |
| 移动端吸底条 | 底部 | WhatsApp / 邮件 / 询价三按钮，中国出口站标配 |
| 规格速配器 Spec Builder | index.html | 选工艺 × 尺寸 × 数量，输出推荐交期 / 开模费是否免除 / 建议包装 / 工艺说明 / 预计生产排期，全站零金额输出，卡片底部内嵌询价表单，提交后原地返回结果，不跳转页面 |
| 数量档位与排期表 | guides/bulk-order-guide.html | 数量区间对应的排期影响、包装建议、打样安排，无金额 |
| RFQ 表单 | products/request-a-quote.html | 10 个字段（必填 5 + 选填 5），带成功态 |
| 主题切换器 | index.html 右下角 | 仅评审期启用，上线前移除 |

### 8.1 规格速配器（Spec Builder）

替代原来的价格计算器。输入三项，输出五项决策信息，输出区永远不出现金额。

**输入**：工艺（hard enamel / soft enamel / die struck / 3D die cast / offset printed）、尺寸（inch 或 mm）、数量（件）。

**输出字段**

| 字段 | 规则 |
|---|---|
| 推荐交期 | 常规 7-10 个工作日；数量落在小批量区间时提示可加急 5 个工作日 |
| 开模费用是否免除 | 给出"免除"或"计入本次询价"的结论与理由说明，具体判定门槛以当次询价确认为准，页面不写死数量门槛 |
| 建议包装 | 按数量区间给单枚吸塑 / 卡纸 / 礼盒 / 贴牌分装 |
| 工艺说明 | 该工艺的成型方式、常见尺寸区间、耐久特性 |
| 预计生产排期 | 打样确认 → 开模 → 大货 → 检验 → 包装的时间段 |

**提交询价（原地，不跳转）**：卡片底部内嵌 Web3Forms 表单 —— 姓名、邮箱、公司三个可见字段，加工艺、尺寸、数量、表面处理、留言五个隐藏字段。点击 "Send this spec for a quote" 不离开当前页面，fetch 提交到 `https://api.web3forms.com/submit`，成功与失败都在原地提示。提交成功后 `form.reset()` 会清空隐藏字段，由 `renderSpec()` 重新写回当前规格，重复提交不丢规格。需要更长说明（预算、交期）时，卡片底部保留 "Open the full quote form" 入口跳到 `products/request-a-quote.html`。

**Query 预填仍保留**：`products/custom-enamel-pins.html` 等产品页继续用 `products/request-a-quote.html?process=...&size=...&qty=...&finish=...` 直接跳询价页并自动预填，首页不再走这条链路。

### 8.2 RFQ 表单字段（bulk 询价页）

| 字段 | 必填 | 说明 |
|---|---|---|
| 工艺类型 | 是 | 单选，五个工艺 |
| 数量 | 是 | 数字，不设下限校验 |
| 尺寸 | 是 | 英寸或毫米 |
| 联系方式（邮箱或 WhatsApp） | 是 | 唯一强制的联系方式 |
| 公司名 | 否 | 用于识别客户类型 |
| 电镀 / 表面处理 | 否 | 12 种电镀选项 |
| 目标价位区间 | 否 | 仅用于加速核价，不作为报价依据 |
| 期望交期 | 否 | 常规或加急 |
| 收货国家 / 港口 | 否 | 影响贸易条款建议 |
| 设计文件上传 | 否 | 支持 AI / EPS / PDF / PNG |

必填只有 5 项，配合 1 个工作日内回报价的承诺，构成"无公开价格"策略的转化补偿。

---

## 九、"无公开价格"策略：利弊与执行要点

### 9.1 好处

1. **避开价格战**。价格一旦公开，谈判空间被压缩到最低，只能拼成本。隐藏单价后，议价权留在工厂侧，可按工艺复杂度、数量、交期、目的地、包装逐单核算。
2. **询价成为强转化动作**。页面浏览是弱信号，提交表单是强信号。没有价格表，访客只有一条通往转化的路，落地页的转化结构更干净。
3. **防止单一页被抄走价格表**。竞品能抄页面结构，抄不走按你的实际产能核算出来的报价逻辑与配比。
4. **符合进口商预期**。B2B 进口商习惯"send details, get quote"，页面不挂价在采购圈层属于常规做法，不构成信任障碍，前提是信任模块足够强。

### 9.2 风险

1. **买家无法自筛量级**，多一轮沟通才能确认，转化周期变长，部分小买家会直接跳出。
2. **少一批 pricing 类落地页**，依赖 pricing、cost 词的搜索流量承接变弱，泛流量占比下降。
3. **缺少价格锚点时**，页面可信度完全依赖信任模块（设备、产能、认证、交期、样品）是否足够硬。
4. **销售侧压力上升**，询盘质量参差，同一份配置可能被反复问价。

### 9.3 补偿动作

1. 把交期、产能、工艺参数、免费打样、响应速度做成显性卖点，写进首屏、工厂页、FAQ 首条。
2. 在 FAQ 里明确说明为什么不挂价，位置放在报价相关问题附近，给出可验证的替代信息清单。
3. 询价表单控制在 5 个必填字段以内，提交后 1 个工作日内回报价，页面写明这个承诺。
4. 规格速配器承接原本价格计算器的决策功能，输出交期、排期、免模费判定，让访客在不看金额的情况下也能推进决策。
5. 批量下单指南给出完整的流程与贸易条款知识，用专业度替代价格透明度。
6. 询盘侧做一次筛选：数量、尺寸、工艺、目标价位区间四栏齐全的询盘进入优先队列，其余走自动回执 + 常见问题回复。

### 9.4 全站禁用词与替代表述

| 禁用表述 | 替代表述 |
|---|---|
| `$0.24-$1.85` 及任何单价、单价区间 | Quote on request / Request a quote for your configuration |
| 阶梯价表、price list、pricing tiers | Quantity tiers and production scheduling（只写档位与排期影响） |
| MOQ 100 pcs / MOQ 50 / minimum order quantity | No minimum order quantity |
| Free mold on 500+ 等与起订量绑定的免模门槛 | 速配器里逐单判定，页面不写死门槛 |
| Samples from $X | Samples from a single piece |
| 每件多少钱、per piece price | 每档数量对应的交期与包装建议 |
| Volume discount from X pieces | Volume discounts apply automatically |

上线前用 grep 全站扫描：`\$[0-9]`、`MOQ`、`minimum order`、`price list`、`per piece`、`Free mold on`，命中即视为未完成。

---

## 十、可选皮肤机制（评审用工具）

三套主题用 CSS 变量实现，靠 `<html data-theme="...">` 切换，首页右下角放一个低调的切换器，localStorage 记忆选择。

### 10.1 三套主题定义

| 主题 key | 主色 | 辅助色 | 底色 | 定位 |
|---|---|---|---|---|
| `ink` | 深墨蓝 `#0B2733` | 香槟金 `#C8A45C` | 冷白灰 | 默认主题，premium 工业质感 |
| `graphite` | 石墨灰 `#1C2126` | 钢蓝 `#4A7C94` | 冷灰白 | 工具感、工程感 |
| `porcelain` | 墨黑棕 `#2A1E1A` | 赭铜 `#B4572F` | 暖白瓷 | 工艺感、礼品感 |

### 10.2 变量表

```css
/* assets/css/themes.css */
:root,
[data-theme="ink"] {
  --brand-900: #0B2733;
  --brand-700: #123A4B;
  --brand-100: #E7EDF0;
  --accent-500: #C8A45C;
  --accent-600: #A8843F;
  --accent-spark: #C8A45C;
  --bg-page: #F7F6F3;
  --bg-surface: #FFFFFF;
  --text-900: #14262E;
  --text-600: #5C6B73;
  --line-200: #E2E0DA;
  --radius-sm: 6px;
  --radius-lg: 14px;
  --shadow-soft: 0 1px 2px rgba(11, 39, 51, .06), 0 12px 32px rgba(11, 39, 51, .08);
}

[data-theme="graphite"] {
  --brand-900: #1C2126;
  --brand-700: #2A3138;
  --brand-100: #E6E9EB;
  --accent-500: #4A7C94;
  --accent-600: #3A6478;
  --accent-spark: #C9702F;
  --bg-page: #F4F5F6;
  --bg-surface: #FFFFFF;
  --text-900: #1B2024;
  --text-600: #5E676E;
  --line-200: #DFE3E6;
  --radius-sm: 4px;
  --radius-lg: 8px;
  --shadow-soft: 0 1px 2px rgba(28, 33, 38, .07), 0 10px 28px rgba(28, 33, 38, .09);
}

[data-theme="porcelain"] {
  --brand-900: #2A1E1A;
  --brand-700: #3C2C26;
  --brand-100: #F1E7DE;
  --accent-500: #B4572F;
  --accent-600: #96431F;
  --accent-spark: #B4572F;
  --bg-page: #FBF7F2;
  --bg-surface: #FFFDFB;
  --text-900: #241A16;
  --text-600: #6B5B52;
  --line-200: #E9DFD5;
  --radius-sm: 8px;
  --radius-lg: 18px;
  --shadow-soft: 0 1px 2px rgba(42, 30, 26, .06), 0 14px 34px rgba(42, 30, 26, .10);
}
```

所有颜色、圆角、阴影一律引用变量，组件样式里不写死十六进制色值，保证换肤一处生效。

### 10.3 切换器实现

```html
<!-- index.html 右下角，默认隐藏于移动端 -->
<div class="theme-switcher" role="group" aria-label="Theme preview">
  <button type="button" data-theme-set="ink" aria-pressed="true">Ink</button>
  <button type="button" data-theme-set="graphite" aria-pressed="false">Graphite</button>
  <button type="button" data-theme-set="porcelain" aria-pressed="false">Porcelain</button>
</div>
```

```js
// assets/js/main.js
const THEME_KEY = 'cpf-theme';
const THEMES = ['ink', 'graphite', 'porcelain'];

function applyTheme(name) {
  const theme = THEMES.includes(name) ? name : 'ink';
  document.documentElement.setAttribute('data-theme', theme);
  document.querySelectorAll('[data-theme-set]').forEach((btn) => {
    btn.setAttribute('aria-pressed', String(btn.dataset.themeSet === theme));
  });
}

applyTheme(localStorage.getItem(THEME_KEY) || 'ink');

document.querySelectorAll('[data-theme-set]').forEach((btn) => {
  btn.addEventListener('click', () => {
    const theme = btn.dataset.themeSet;
    localStorage.setItem(THEME_KEY, theme);
    applyTheme(theme);
  });
});
```

`<head>` 内联一段极小脚本，防止刷新时闪回默认主题：

```html
<script>
  try {
    var t = localStorage.getItem('cpf-theme');
    if (t) document.documentElement.setAttribute('data-theme', t);
  } catch (e) {}
</script>
```

### 10.4 外观与上线要求

- 定位 `position: fixed; right: 18px; bottom: 18px`，与右下角浮动咨询条错位排布，切换器上移，两者不重叠。
- 低调处理：默认 `opacity: .5`，hover 提到 `1`，圆角胶囊，尺寸控制在 130px 宽内。
- 移动端（≤768px）隐藏切换器，避免遮挡吸底条。
- **这是评审用工具，正式上线前必须移除**：删除切换器 DOM、`applyTheme` 相关 JS、`<head>` 里的内联读取脚本，并把 `themes.css` 中 `ink` 的变量固化为 `:root` 默认值。移除后全站只剩一套配色，减少 CSS 体积与维护面。
- 移除动作列入上线前清单，不允许带着切换器上线。

---

## 十一、技术 SEO 与性能清单

- [ ] `robots.txt`：放行全部 + sitemap 指向 + 显式允许 `Googlebot-Image`
- [ ] `sitemap.xml`：16 个可索引 URL（18 个页面去掉 `404.html` 与 `thank-you.html`），逐页挂 `<image:image>`，带 `lastmod` 与优先级分层
- [ ] `canonical` / `og:url` / `sitemap.xml` / `robots.txt` 里的绝对 URL 全部指向 `https://chinapinsfactory.com`
- [ ] 全站无金额、无 MOQ、无阶梯价：grep `$[0-9]`、`MOQ`、`minimum order`、`price list`、`per piece`、`Free mold on` 全部零命中
- [ ] 全站无 `Sedex`、`SMETA`、`aggregateRating`、`aggregateOffer`、`priceSpecification`
- [ ] 单语言站：只保留 `hreflang="en"`，无 `zh-cn`，无 `x-default` 互指
- [ ] 首屏图片 `fetchpriority="high"`，其余 `loading="lazy" decoding="async"`，全部走 `<picture>` 交付 WebP + JPG
- [ ] 字体：`Manrope`（标题）+ `Inter`（正文），`display=swap`，preconnect
- [ ] 无横向滚动条，容器 `max-width` 统一
- [ ] 移动端单列，导航折叠为抽屉
- [ ] 所有内部链接用相对路径 `xxx.html`，canonical 用绝对 URL
- [ ] 外链 `rel="noopener noreferrer"`
- [ ] 图片体积：WebP 全部 < 250KB
- [ ] 主题变量集中在 `themes.css`，组件样式零硬编码色值
- [ ] 无第三方追踪脚本占位（GA4 / GTM 留位，但默认不加载，避免拖慢首屏）

---

## 十二、实施阶段

**Phase 1 · 地基**

1. 建立 CSS 变量主题系统：`assets/css/themes.css`（三套变量）+ 重写 `assets/css/styles.css`（引用变量，不写死色值）
2. 扩写 `assets/js/main.js`：规格速配器、FAQ 手风琴、抽屉导航、吸底条、表单态、主题切换器、URL query 预填
3. 建品牌 SVG favicon 与 CPF 标识，替换 `pin-placeholder.svg`
4. 全站 `<picture>` 组件与图片路径落地，WebP + JPG 双格式

**Phase 2 · 页面**

5. 重写 5 个现有页面（修 SEO 硬伤 + 换新设计 + 换真图 + 注入工厂硬数据）
6. 新建 `guides/bulk-order-guide.html`、`blog/index.html`、`legal/privacy-policy.html`、`404.html`
7. 组装 4 篇文章（2 篇改名：`blog/lapel-pin-sizes-guide.html`、`blog/custom-challenge-coin-sizes-guide.html`），全文清除价格表述
8. 首页落地规格速配器与"配置带入询价表单"链路，询价页落地 query 预填与成功态

**Phase 3 · 内容与数据校验**

9. `sitemap.xml` + `robots.txt` 重写，域名统一为 `chinapinsfactory.com`
10. 结构化数据全量校验，确认无价格类字段
11. 全站禁用词扫描（价格、MOQ、Sedex、SMETA、aggregateRating），逐条清理
12. 全站链接与断链检查，内链枢纽按第四章规则复核

**Phase 4 · 上线前**

13. **移除主题切换器**（DOM、JS、内联脚本一并清除，`ink` 变量固化为 `:root`）
14. 替换邮箱、电话、真实产能数据、认证证书编号
15. 域名与品牌名确认，canonical 与 og:url 复核，出《上线前替换清单》

---

## 十三、上线前必须替换与确认的数据

**这一节最重要。** 下表区分"已确定"与"待确认"两类。已确定的只需核对一致性，待确认的必须补真实信息后才能上线。工厂硬数据按 1.2 表的设定值写入，文案保持保守自洽。

| 位置 | 内容 | 状态 | 处理方式 |
|---|---|---|---|
| 域名 | `chinapinsfactory.com` | 已确定 | 只需确认拼写与主域/子域选择，全站绝对 URL 统一 |
| 品牌名 | China Pins Factory（标识缩写 CPF） | 已确定 | 只需确认大小写与缩写用法，Logo、alt、Schema 保持一致 |
| 认证 | ISO 9001:2015、BSCI、RoHS | 已确认持有 | 补证书编号、颁发机构、有效期到官网可查 |
| 已删除的认证 | Sedex 4-Pillar、SMETA | 已决定删除 | 全站零出现，确认无残留 |
| 通讯 | 邮箱与电话 | 待用户确认填写 | 换成真实邮箱与 WhatsApp 号码，页脚、浮条、Schema 保持一致 |
| 产能与设备 | 年产能、设备台数、厂房面积 | 待用户确认填写 | 按 1.2 表写入作为基线，最终以真实数据替换，替换后同步 Schema 与 FAQ |
| 合规声明 | CPSIA / Prop 65 / REACH / EN71-3 检测、XRF | 待用户确认 | 确认检测报告确实覆盖所售合金与表面处理，没有就删掉整块 |
| 交期与打样 | 7-10 个工作日、5 天加急、12 小时免费效果图 | 待用户确认填写 | 与实际排产能力对齐，FAQ 与 Schema 同步 |
| 起订量表述 | No minimum order quantity | 待用户确认填写 | 与实际接单政策一致，全站统一 |
| 证言 | 行业结果卡（无虚构人名） | 待用户提供 | 真实评价等客户授权后填写，结构化数据不写评分 |
| 结构化数据 | `aggregateRating` | 已删除 | 保持删除 |
| 结构化数据 | `Product` 类型 | 已改为 `Service`（2026-10-26） | Search Console 报严重错误「应指定 offers/review/aggregateRating」。本站无公开价格、无真实评价，编造这三个属性属于虚假标注，处罚更重。11 个 `Product` 节点已改为 `Service`（`manufacturer`→`provider`，`category`→`serviceType`，`material` 并入 `additionalProperty`）。**除非站内真的开始公开价格或采集到真实评价，否则不得再引入 `Product` / `Offer` 节点** |
| 价格相关内容 | 单价、阶梯价、MOQ、免模门槛 | 已决定全部删除 | 按第九章禁用词清单扫描 |

**域名一旦最终确认，`canonical`、`og:url`、`sitemap.xml`、`robots.txt` 里的绝对 URL 需要全局替换一次。**

---

## 十四、后续可扩展项

第一阶段上线后，按数据表现决定是否加：

1. 更多工艺页：软珐琅单独页、挑战币单独页（把长尾词各自拆出来）。
   过渡方案已落地：`guides/process-comparison.html` 先用同口径对比矩阵承住这批意图，拆页等该页在 GSC 里跑出查询数据再做。
2. 案例页：按买家类型分的项目案例（能吃到大量长尾）
3. 询价表单接后端（Formspree / Cloudflare Worker / 邮件转发），并做询盘入库与跟进状态管理
4. GA4 + Search Console 接入与事件埋点，重点跟踪速配器配置次数与表单提交率
5. 下载型物料：产品目录 PDF、工艺对照表 PDF、尺寸对照表 PDF，走 gated download 收线索
6. 数字样品册：把 12 种电镀与 5 种工艺做成可点击的在线样品册
7. 独立域名策略评估：是否需要为 challenge coins 或 keychains 单开子域

## 十五、内容更新机制（2026-10-27 建立）

### 15.1 先厘清一个前提

「定期更新提升 SEO」这个说法有一半不成立，落地时必须按下面的口径执行，否则会做出 Google 点名的 search-first 动作：

| 常见做法 | Google 官方口径 | 本站执行 |
|---|---|---|
| 提高发文频率换排名 | 发布频率不是排名因素。John Mueller 明确讲过每天发博客不会自动提升排名，Google 没有「内容计数器」 | 不设发文日历指标，只按意图缺口排队列 |
| 改日期让页面显得新 | helpful content 文档把「Are you changing the date of pages to make them seem fresh when the content has not substantially changed?」列为自查项，并明确这对排名没有帮助 | `dateModified` 只在正文实质变更时动 |
| `lastmod` 全站刷一遍 | `lastmod` 只有在持续可验证准确时才被采信。全站同一个日期等于告诉爬虫这字段没有信息量，整站被降级忽略 | `lastmod` 从 `git log -1 --format=%cd -- <文件>` 推导，不手写 |

判定一条内容「值不值得刷新」只有一条标准：**老读者这次会不会得到不一样的答案**。会 → 改正文并同步日期；不会 → 一个字都别动。

### 15.2 三类内容，三种节奏

更新触发源不同的内容混在一起做是最常见的错：

1. **事实会自然变质的（真时效内容）**——交期与加急窗口、年产能、设备台数、认证有效期、材料工艺边界、样品政策、海运空运时效、贸易条款与关税口径。**季度复核，只改真变了的。**
2. **意图缺口（该新增的页面）**——见 15.4 的优先级表。**以新增为主，刷新为辅。**
3. **每次都跟着动的技术层**——sitemap、JSON-LD、ItemList 计数、feed、可见日期。**由脚本同步，不靠人记得。**

### 15.3 四层展示位模型

新内容落位靠这张表，不靠「想到哪贴到哪」：

| 层 | 位置 | 规则 |
|---|---|---|
| 入口层 | 主导航（4 个顶级项 + 10 个二级项）、页头 CTA、页脚、公告栏、首页 journal 精选卡 | **稳态，不随内容量增长。** 新内容默认不进 |
| 聚合层 | `products/` `guides/` `company/` `blog/` 四个目录 index | **新内容的主展位。** 卡片网格 + `ItemList`，`numberOfItems` 必须等于可见卡片数 |
| 上下文层 | 各页底部 linkband、页内锚点、正文内链 | **每张新页至少进 2 个强相关页的 linkband**，新页自己的 linkband 4–6 条且含 1 条指回父 hub |
| 机器层 | `sitemap.xml`、各页 JSON-LD、`feed.xml`、`llms.txt` | **必须与可见内容一一对应**，手工同步是这里唯一的失分点 |

#### 15.3.1 目录层级由面包屑承担，不由页脚承担

目录级页面（`products/` `guides/` `company/`）的入口走**面包屑**，不走页脚。理由：

- **语义层级不同。** 页脚三列是「平铺的实用链接区」——Products 列装的是具体工艺的锚点（Hard enamel、Soft enamel、Die struck…），Company 列装的是杂项。往里塞目录页，等于在平铺列表里混进一层目录，用户点进去发现又是一层。
- **面包屑本来就是为此设计的。** `.crumbs` 样式自建站起就存在，`SITE-STRUCTURE` 第四章也写着「面包屑只在子页出现，首页不出现」。此前的问题是**样式建好了却没在各页填上目录层级**——全站 23 页里只有 6 页带层级，其余只有孤零零的 `Home`。现已补齐为通例：

  ```
  叶子页：Home / Products / Custom Pins      ← Products 是可点链接，指向 products/index.html
  目录页：Home / Products                     ← Products 是当前项，链接到自身
  ```

  面包屑层级与 JSON-LD `BreadcrumbList` 保持一一对应。

- **页脚保持 23 页完全一致。** 全站页脚结构只有一个变体（结构签名校验），改它必须 23 页同步改且不能只改部分页。目录入口放在面包屑后，页脚无需任何改动。

每个目录页因此获得的入口：面包屑（同目录所有兄弟页）+ 首页语境按钮 + 目录内互相引用。

入链数在导航下拉改造后已重新拉平（2026-10-27 晚）：`products/index.html` 22、`guides/index.html` 22、`company/index.html` 22，三者完全一致，均来自导航下拉 + 面包屑 + 页脚。改造前分别是 7、28、4。

#### 15.3.2 主导航改为下拉分组（2026-10-27 晚修订，推翻同日早前的「不做二级菜单」结论）

**早前的结论**：导航保持平铺，不引入 hover 展开的二级菜单。理由是空间不够、导航项是买家意图而非目录、悬停菜单在触屏与无 JS 场景不可用。

**修订原因**：这三条理由在实测后都不成立，或者可以通过别的手段解决。

1. **空间问题已经解决。** 导航从 6 项减到 4 项后，桌面布局在 871px 以上都能容纳字标、导航与询价按钮不重叠，页头按钮的隐藏断点也因此从 1000px 下调到 880px。
2. **「意图直达」不等于「只能一级」。** 顶级项仍然是买家意图（Products / Guides / Our Factory / Journal），下拉只是把同一意图下的具体页面展开，没有多加一层目录跳转。
3. **触屏与无 JS 的问题可以工程解决。** ≤860px 降级为手风琴（caret 按钮 + `aria-expanded`）；父项本身就是指向目录中枢的真实链接，脚本不运行时二级页面照样可达。

**最终结构**：

```
导航        Products            Guides                 Our Factory      Journal
            ├ Custom enamel pins        ├ How to order in bulk from China
            ├ Challenge coins, medals and swag  ├ Design file specifications
            ├ Custom metal badges       ├ Five processes, side by side
            └ Samples and prototyping    └ Frequently asked questions
                                         ├ Our factory and quality control
                                         └ Contact our export desk
```

**新增的硬约束**（写进 `scripts/check.py`）：

- 归一化后的顶级项与二级项集合在 23 页上必须完全一致
- nav 块内不得出现 `request-a-quote`（询价入口只有页头 CTA、移动端吸底条与各页语境 CTA）
- 每页 `is-active` 至多 1 个，`aria-current="page"` 至多 1 个
- 导航的唯一来源是 `scripts/nav_sync.py`，禁止手改单页 nav 块

详见 2.0.5（导航三层结构定案）与 15.9（改造实录）。

### 15.4 内容缺口优先级队列

| 优先级 | 页面 | 理由 |
|---|---|---|
| **P0** | ✅ 设计文件规范 `guides/design-file-specs.html` | GS-JJ、bulkcustom、maxemblem、pinsfun、miracle-custom 五家竞品全都有，本站全无。高意图「画图前必看」流量，离询价最近 |
| **P0** | ✅ 五工艺对比矩阵 `guides/process-comparison.html` | 五家竞品都是五方一张表，本站原来只有 hard vs soft 两方。最容易被引用和链出的类型 |
| **P1** | 材质页（锌合金 / 黄铜 / 铁 / 铜 / 铝） | 常被搜，目前完全空白 |
| **P1** | 电镀 12 色承接页 | 已有 `detail-plating-finishes` 图与 12 个选项数据，缺页面承接 |
| **P1** | 扣具页（蝴蝶扣 / PVC 胶帽 / 安全别针 / 磁扣 / 双针） | 同上，数据都在，页面没有 |
| **P2** | 钥匙扣 / 奖牌 / 皮带扣 / 袖扣 各自独立成页 | 现在全塞在 `custom-metal-swag.html`，一页扛 6 个词，主词被稀释 |
| **P2** | 贸易术语页（FOB / CIF / DDP、报关、HS 编码、关税） | 2026 年美国对华关税变动频繁，真时效内容，值得季度复核 |
| **P2** | 成本构成页（**不写单价**，写「什么决定报价」：尺寸 / 线宽 / 色数 / 镀层 / 厚度 / 数量 / 包装 / 模具 / 运费） | 与「不公开价格」不冲突：讲构成不报价，却能吃到 cost 类意图。全站最值得重新取舍的一处 |
| **P3** | 场景页（企业活动 / 校园社团 / 婚礼 / 球队 / 公益募款 / 粉丝周边）、展会页、案例页 | 搜索量大但竞争激烈，等前两档站稳再打 |

### 15.5 新内容上线清单

每加一页要走的固定动作，漏任何一步就是新的不一致：

| # | 动作 | 归属层 | 必做 |
|---|---|---|---|
| 1 | 建页面，放进对应目录 | — | 必做 |
| 2 | 补 meta / H1 / canonical / og / JSON-LD | 机器层 | 必做 |
| 3 | 加进该目录 index 的卡片网格 + `ItemList` | 聚合层 | 必做 |
| 4 | 加进 `sitemap.xml`（`lastmod` 取 git 日） | 机器层 | 必做 |
| 5 | 进 `feed.xml` 与 `llms.txt` | 机器层 | 必做 |
| 6 | 在 2 个强相关页的 linkband 或正文里加链接 | 上下文层 | 必做 |
| 7 | 新页自己底部写 4–6 条 linkband，含指回父 hub | 上下文层 | 必做 |
| 8 | 可见日期 + `datePublished` / `dateModified` 对齐 | 机器层 | 必做 |
| 9 | 页脚对应列加一条 | 入口层 | 仅目录级，且需全站同步 |
| 10 | 首页 journal 精选卡 | 入口层 | 可选，需人工挑 |

**5 分钟判据**：新页写完之后，如果第 3、6、7 步做不了，说明它不该独立成页，应该并进某个已有页面的一个 section。**先有内容缺口，再有页面**，不是反过来。

### 15.6 日期纪律

一次真实更新，日期要落在四处且完全一致：页面可见的 `Updated` 日期、JSON-LD 的 `dateModified`、`sitemap.xml` 的 `lastmod`、feed 的 `pubDate`。

- `datePublished` 永远不动
- `dateModified` 只在正文实质变更时动
- `lastmod` 与 `pubDate` 从 git 推导，不手写

配套的反查链：某个日期突然集体变化，说明当天有批量改动，可以复核是不是模板级改动污染了所有页面的 `lastmod`。

### 15.7 本轮实际执行（2026-10-27）

| 动作 | 文件 | 性质 |
|---|---|---|
| 新建目录中枢 | `products/index.html` `guides/index.html` `company/index.html` | 纯新增，`CollectionPage` + `ItemList` |
| 新建 P0 内容页 | `guides/design-file-specs.html` `guides/process-comparison.html` | 纯新增，`TechArticle` + `ItemList` |
| 新建机器层产物 | `feed.xml`（RSS 2.0）、`llms.txt` | 纯新增 |
| 补 sitemap | `sitemap.xml` | 16 → 21 条；修正 2 条失真 `lastmod`；修 3 处 `</url><url>` 连写 |
| 补入口 | `index.html` journal 区块 | +8 行 linkband |
| 补上下文层内链 | `guides/faq.html` `guides/bulk-order-guide.html` `products/custom-enamel-pins.html` `products/samples.html` `products/request-a-quote.html` | 共 +10 行 |

本轮**未创建任何新图片**，全部复用 `assets/images/` 既有资产，因此不存在图片上线风险。

### 15.8 目录入口与提交前检查（2026-10-27 补做）

补做原因：目录中枢页建好后，站内只有首页一处链接指向 `products/index.html` 和 `guides/index.html`，`company/index.html` **入链为 0**（仅出现在 `sitemap.xml` 与 `llms.txt`），属于孤岛页。首页 journal 区块末尾那一行 linkband 也不足以构成稳定入口。

| 动作 | 文件 | 性质 |
|---|---|---|
| 补全面包屑目录层级 | 17 个页面 | `Home` 一级 → `Home / 目录 / 当前页`；目录项为可点链接，指向同目录 hub |
| 补首页语境入口 | `index.html` | swag 区块加「All product lines」按钮；factory 区块加「Company overview」按钮 |
| 撤掉页脚目录入口 | 23 个页面 | 试加后判定层级错误，已全部撤销，页脚恢复全站一致 |
| 对齐 JSON-LD 与可见标题 | 3 个 hub 页 | `ItemList` 的 `name` 与页面可见卡片标题逐字一致（Google 要求结构化数据描述可见内容） |
| 建提交前检查 | `scripts/check.py` `scripts/reachability.py` `scripts/install-hooks.sh` | 新增，`pre-commit` 与 `pre-push` 自动执行 |
| 导航去重 | 23 个页面 | 删除与页头 CTA 重复的 `Request a Quote` 项，导航由 6 项减为 5 项 |
| guides hub 进导航 | 23 个页面 | `Bulk Order Guide` 项改为 `Guides` 指向 `guides/index.html` |

**目录入口的最终分布**（不靠页脚，靠面包屑 + 语境按钮）：

```
面包屑        Home / Products / Custom Pins          ← 目录项可点，指向 products/index.html
首页          swag 区块    → All product lines         ← 语境正确
              factory 区块 → Company overview
              journal 区块 → All buying guides
页脚          23 页保持完全一致，无目录项
```

**提交前检查**覆盖 10 项：JSON-LD 解析、内部链接（含站内绝对链接与 canonical）、图片引用、`ItemList` 条目数与可见性、`FAQPage` 计数、H1 与 canonical 唯一性、sitemap/feed/llms 三者一致、孤岛页检测、面包屑层级、目录 hub 入链数、行尾翻转。任一项不通过则 commit 与 push 被拦截。

新增 `scripts/reachability.py` 输出全站链接图明细：每个页面的入链数、出链数、距首页的层级，以及三个目录 hub 各自被哪些页面链接。当前 23 页中 21 页可达，`404.html` 与 `thank-you.html` 按设计例外。

### 15.9 导航下拉改造与新文章落位（2026-10-27）

**改造前的现状**：导航 5 项平铺（Custom Pins / Metal Swag / Guides / Our Factory / Journal），目录中枢页只能靠面包屑和语境按钮进入，`company/index.html` 全站只有 4 个页面直连，入口太浅、层级不清。

**改造后的结构**：三个下拉组（Products / Guides / Our Factory）+ 一个平铺项（Journal），规则见 2.0.5。

| 动作 | 文件 | 性质 |
|---|---|---|
| 建导航唯一来源 | `scripts/nav_sync.py` | 新增，定义菜单模型并批量重写 23 页 nav 块 |
| 下拉样式 | `assets/css/styles.css` | 桌面面板 + 移动手风琴，媒体查询隔离 |
| 下拉交互 | `assets/js/main.js` | 显式展开状态、`aria-expanded` 同步、`Esc` 关闭 |
| 改写 23 页导航 | 23 个 HTML | 每页 +36/-5 行，nav 块整段替换 |
| 导航校验改造 | `scripts/check.py` | 从「硬编码 5 项文本」改为「归一化链接集合全站一致」 |
| 响应式实测 | `scripts/nav_responsive.py` | 新增，CDP 驱动，10 页 × 9 断点 = 90 组合 |
| 补机器层目录入口 | `llms.txt` | 新增 `## Directories` 段，列 4 个目录 hub |
| 修页头断点 | `assets/css/styles.css` | 询价按钮断点 1000px → 880px，隐藏改为保留占位，顺带修掉 880–1000px 区间 1px 横向溢出 |

**改造后的 hub 入链数**：`products/index.html` 7 → 22，`guides/index.html` 28 → 22，`company/index.html` 4 → 22。三个中枢页入链数现在完全一致，全部来自导航下拉、面包屑与页脚。

**Bulk Order Guide 的进入路径**：`导航 → Guides → How to order in bulk from China`，一步直达，并放在 Guides 下拉第一位（它是 P0 长尾页）。`scripts/check.py` 额外禁止 `request-a-quote` 出现在任何 nav 块内，防止日后回潮。

**以后新写的文章放哪里**

1. 文件落在 `blog/<slug>.html`，与现有 4 篇同目录
2. 聚合页 `blog/index.html` 收录卡片，并同步 `ItemList` 条目
3. 机器层：`sitemap.xml`、`feed.xml`、`llms.txt` 各加一条
4. 上下文层：在 2 个强相关页（品类页或批量下单指南）加内链
5. **不进导航**。导航只保留 `Journal` 一个入口指向 `blog/index.html`，入口层稳态不增长是硬规则；每加一篇就往导航里塞一项，导航会退化成文章列表，顶级项也会被顶出首屏。

**导航的唯一来源是 `scripts/nav_sync.py`。** 要增删二级项，改脚本里的 `NAV_GROUPS` / `NAV_FLAT`，然后跑 `python scripts/nav_sync.py` 批量重写 23 页；`--check` 只报告差异不落盘。**不要手改单个页面的 nav 块**，23 页手改必然漂移，`scripts/check.py` 会在提交前把漂移拦下来。
