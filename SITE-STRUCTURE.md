# China Pins Factory（CPF）站点结构规划

> 目标：面向 Google 与 AI 搜索场景的 B2B 批发外贸站。纯批发，不做零售。
> 品牌：China Pins Factory，标识缩写 CPF。域名：`chinapinsfactory.com`。
> 报价策略：全站不公开价格，采用国际 B2B 工厂的 Quote only 做法，价格走询价。
> 语言：仅纯英文站，不做中文版。
> 本文件是实施的唯一依据。改结构前先改这里。

---

## 〇、实施状态（2026-10-24 更新）

**18 个页面已全部建成并通过全站校验。** Phase 1-3 完成，Phase 4 待办。

| 页面 | 状态 | 主词 | JSON-LD |
|---|---|---|---|
| index.html | 已重写 | custom lapel pins wholesale | Organization + WebSite + WebPage + ItemList + HowTo + FAQPage |
| wholesale-custom-pins.html | 已重写 | wholesale custom enamel pins | BreadcrumbList + ItemList + Product×5 + FAQPage |
| custom-metal-swag.html | 已重写 | wholesale custom challenge coins | BreadcrumbList + ItemList + Product×6 |
| bulk-order-guide.html | 已建 | bulk order lapel pins | BreadcrumbList + Service + OfferCatalog + FAQPage |
| china-pin-factory.html | 已重写 | china lapel pin factory | BreadcrumbList + Organization + LocalBusiness |
| wholesale-quote.html | 已重写 | custom lapel pin quote | BreadcrumbList + ContactPage + Service + OfferCatalog |
| blog.html | 已建 | 内容中枢 | BreadcrumbList + Blog + ItemList |
| blog-how-to-order-custom-lapel-pins-from-china.html | 已建 | how to order custom lapel pins from china | BreadcrumbList + BlogPosting + FAQPage |
| blog-hard-enamel-vs-soft-enamel-pins.html | 已建 | hard enamel vs soft enamel pins | BreadcrumbList + BlogPosting + FAQPage |
| blog-lapel-pin-sizes-guide.html | 已建 | lapel pin sizes | BreadcrumbList + BlogPosting + FAQPage |
| blog-custom-challenge-coin-sizes-guide.html | 已建 | custom challenge coin sizes | BreadcrumbList + BlogPosting + FAQPage |
| privacy-policy.html | 已建 | 无 | BreadcrumbList + WebPage |
| custom-metal-badges.html | 已建 | custom metal badges | Organization + Service |
| samples.html | 已建 | custom lapel pin samples | Organization + Service |
| faq.html | 已建 | lapel pin faq | FAQPage（27 问） |
| contact.html | 已建 | contact lapel pin factory | Organization + ContactPage + LocalBusiness |
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

采用**扁平 URL**，全部落在根目录，文章用 `blog-` 前缀而非子目录。

理由有三个：一是静态托管零配置，任何主机（Cloudflare Pages / Netlify / Nginx / 虚拟主机）直接丢进去就能跑；二是 `file://` 双击就能预览，不用起服务；三是避免尾斜杠、canonical、相对路径三件套打架。以后要换 `/blog/slug/` 干净 URL，一张 301 映射表就能迁走。

```
/  (index.html)                                        首页 · 工厂定位 + 信任锚 + 规格速配器 + FAQ + RFQ
│
├── wholesale-custom-pins.html                         核心品类 · 5 种工艺 + 电镀 + 背扣 + 包装
├── custom-metal-swag.html                             延伸品类 · 挑战币 / 奖牌 / 钥匙扣 / 皮带扣 / 袖扣
├── custom-metal-badges.html                           延伸品类 · 徽章类目（服务徽章 / 盾形 / 机构徽章）
├── bulk-order-guide.html                              ★ 批量下单指南 · 长尾承接页，无任何金额
├── china-pin-factory.html                             工厂与品控 · E-E-A-T 信任页
├── wholesale-quote.html                               询价页 · 全站唯一转化落地页
├── blog.html                                          ★ 内容中枢 · 文章索引
│
├── blog-how-to-order-custom-lapel-pins-from-china.html   长尾 · 采购流程
├── blog-hard-enamel-vs-soft-enamel-pins.html             长尾 · 工艺对比
├── blog-lapel-pin-sizes-guide.html                      长尾 · 尺寸规格
├── blog-custom-challenge-coin-sizes-guide.html           长尾 · 挑战币规格
│
├── samples.html                                       ★ 打样与原型 · 四类样品 / 成本 / 交期
├── faq.html                                           ★ 独立 FAQ · 27 问长尾承接
├── contact.html                                       ★ 联系页 · 联系方式 / 工厂档案 / 联系表单
├── privacy-policy.html                                ★ 信任与合规
├── 404.html                                           ★ 兜底页
└── thank-you.html                                     ◦ 表单提交后展示 · 不挂链接、不进 sitemap
```

**最终 18 个页面**（原 5 + 新增 13）。文件名相对旧版的三处变化：

| 旧文件名 | 新文件名 | 变化原因 |
|---|---|---|
| `bulk-pricing.html` | `bulk-order-guide.html` | 页面不再承载价格表，改为批量下单流程与贸易条款指南 |
| `blog-lapel-pin-sizes-and-pricing-guide.html` | `blog-lapel-pin-sizes-guide.html` | 去掉价格字眼，主词收敛到 lapel pin sizes |
| `blog-custom-challenge-coin-sizes-and-price-guide.html` | `blog-custom-challenge-coin-sizes-guide.html` | 去掉价格字眼，主词收敛到 custom challenge coin sizes |

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
| wholesale-custom-pins.html | 工艺选型与规格决策 | wholesale custom enamel pins | 跳询价页 |
| custom-metal-swag.html | 承接徽章之外的金属品类 | wholesale custom challenge coins | 跳询价页 |
| bulk-order-guide.html | 教买家怎么批量下单、怎么谈贸易条款 | bulk order lapel pins | 跳询价页 |
| china-pin-factory.html | 证明是工厂不是贸易商 | china lapel pin factory | 跳询价页 |
| wholesale-quote.html | 收表单 | custom lapel pin quote | 表单提交 |
| blog.html + 4 篇 | 吃信息型长尾，建主题集群 | how to order lapel pins from china 等 | 跳品类页 / 批量下单指南 / 询价页 |
| custom-metal-badges.html | 承接徽章类目的独立采购意图 | custom metal badges | 跳询价页 |
| samples.html | 讲清打样流程，化解"先买样品"的顾虑 | custom lapel pin samples | 跳询价页 |
| faq.html | 27 问承接疑问型长尾 | lapel pin faq | 跳品类页 / 询价页 |
| contact.html | 联系方式与工厂档案，补 E-E-A-T 信任 | contact lapel pin factory | 跳询价页 |
| privacy-policy.html | 合规与信任 | 无 | 无 |
| 404.html | 留住误入流量 | 无 | 跳首页 |

### 2.2 bulk-order-guide.html 内容大纲

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
| wholesale custom enamel pins | wholesale-custom-pins.html | hard enamel pin, soft enamel pin, die struck pin |
| wholesale custom challenge coins | custom-metal-swag.html | custom medals, metal keychains, belt buckles |
| bulk order lapel pins | bulk-order-guide.html | how to order in bulk, bulk lapel pin order process, bulk pin order guide |
| china lapel pin factory | china-pin-factory.html | OEM lapel pin manufacturer, factory direct pins, custom pin manufacturer china |
| custom lapel pin quote | wholesale-quote.html | get lapel pin quote, lapel pin supplier quote, request pin quote |
| how to order custom lapel pins from china | blog-how-to-order-custom-lapel-pins-from-china.html | import lapel pins, China pin supplier, sourcing pins from china |
| hard enamel vs soft enamel pins | blog-hard-enamel-vs-soft-enamel-pins.html | cloisonne vs soft enamel, enamel finish comparison |
| lapel pin sizes | blog-lapel-pin-sizes-guide.html | lapel pin size chart, lapel pin dimensions |
| custom challenge coin sizes | blog-custom-challenge-coin-sizes-guide.html | challenge coin diameter chart, coin thickness |
| custom metal badges | custom-metal-badges.html | service badges, shield badges, organisation badges |
| custom lapel pin samples | samples.html | lapel pin sample order, prototype sample, sample kit finishes |
| lapel pin faq | faq.html | enamel pin questions, custom pin minimum order, pin lead time |
| contact lapel pin factory | contact.html | contact china pin supplier, kunshan pin factory contact |

四篇文章互相不抢词，每篇都往品类页、批量下单指南与询价页导流。

**关键词层面的取舍**：主动放弃 pricing、price list、cost、how much 这一类词的落地页，把它们降级为询价页与批量下单指南里的支撑语义，页面照常能被相关词命中，但不做专门的比价型落地页。

---

## 四、内链枢纽

```
                    index.html
        ┌───────────┼───────────┬────────────┐
        ▼           ▼           ▼            ▼
   品类页       金属周边页   批量下单指南    工厂页
        │           │           │            │
        └───────────┴─────┬─────┘            │
                          ▼                  │
                       blog.html             │
                          │                  │
              文章 ×4 ─────┴──────────────────┘
             （每篇 → 品类页 / 批量下单指南 / 询价页，3 条内链起步）

                     wholesale-quote.html
                    （全站唯一转化落地页，被以上所有节点指向）
```

规则：

1. 每页页头导航固定 6 个链接（品类页 / 金属周边页 / 批量下单指南 / 工厂页 / 博客 / 询价），保证任意两页之间 ≤2 跳。
2. 文章正文里出现的品类词必须链到对应品类页，**不做锚文本堆砌**，用自然句做锚。
3. 面包屑只在子页出现，首页不出现（首页本身就是根）。
4. 批量下单指南是第二强承接页，至少被首页、文章、品类页各链一次。
5. 每页页脚固定"批量下单指南 + 询价"双 CTA，链接到 `bulk-order-guide.html` 与 `wholesale-quote.html`。

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
| wholesale-custom-pins.html | `BreadcrumbList` + `ItemList` + `Product` × 5（只写材质、尺寸、工艺属性） |
| custom-metal-swag.html | `BreadcrumbList` + `ItemList` + `Product` × 6（只写材质、尺寸、工艺属性） |
| bulk-order-guide.html | `BreadcrumbList` + `Service` + `OfferCatalog`（catalog 只列服务项目，不带金额） |
| china-pin-factory.html | `BreadcrumbList` + `Organization` + `LocalBusiness`（geo 坐标） |
| wholesale-quote.html | `BreadcrumbList` + `ContactPage` + `Service` + `OfferCatalog`（服务项，无金额） |
| blog.html | `BreadcrumbList` + `Blog` + `ItemList` |
| 文章页 | `BlogPosting` + `BreadcrumbList` + `FAQPage`（有 FAQ 段落的文章） |
| privacy-policy.html | `WebPage` + `BreadcrumbList` |
| 404.html | `WebPage` + `noindex` |

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
| 顶部公告条 | 全站 | No minimum order quantity · 免费 2D/3D CAD 图 12 小时出 · ISO 9001:2015，一句话说清供应商性质 |
| 页头询价 CTA | 页头右侧 | 所有页面固定 |
| 浮动咨询条 | 右下角 | WhatsApp + 邮件，桌面端常驻 |
| 移动端吸底条 | 底部 | WhatsApp / 邮件 / 询价三按钮，中国出口站标配 |
| 规格速配器 Spec Builder | index.html | 选工艺 × 尺寸 × 数量，输出推荐交期 / 开模费是否免除 / 建议包装 / 工艺说明 / 预计生产排期，全站零金额输出，卡片底部内嵌询价表单，提交后原地返回结果，不跳转页面 |
| 数量档位与排期表 | bulk-order-guide.html | 数量区间对应的排期影响、包装建议、打样安排，无金额 |
| RFQ 表单 | wholesale-quote.html | 10 个字段（必填 5 + 选填 5），带成功态 |
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

**提交询价（原地，不跳转）**：卡片底部内嵌 Web3Forms 表单 —— 姓名、邮箱、公司三个可见字段，加工艺、尺寸、数量、表面处理、留言五个隐藏字段。点击 "Send this spec for a quote" 不离开当前页面，fetch 提交到 `https://api.web3forms.com/submit`，成功与失败都在原地提示。提交成功后 `form.reset()` 会清空隐藏字段，由 `renderSpec()` 重新写回当前规格，重复提交不丢规格。需要更长说明（预算、交期）时，卡片底部保留 "Open the full quote form" 入口跳到 `wholesale-quote.html`。

**Query 预填仍保留**：`wholesale-custom-pins.html` 等产品页继续用 `wholesale-quote.html?process=...&size=...&qty=...&finish=...` 直接跳询价页并自动预填，首页不再走这条链路。

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
6. 新建 `bulk-order-guide.html`、`blog.html`、`privacy-policy.html`、`404.html`
7. 组装 4 篇文章（2 篇改名：`blog-lapel-pin-sizes-guide.html`、`blog-custom-challenge-coin-sizes-guide.html`），全文清除价格表述
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
| 价格相关内容 | 单价、阶梯价、MOQ、免模门槛 | 已决定全部删除 | 按第九章禁用词清单扫描 |

**域名一旦最终确认，`canonical`、`og:url`、`sitemap.xml`、`robots.txt` 里的绝对 URL 需要全局替换一次。**

---

## 十四、后续可扩展项

第一阶段上线后，按数据表现决定是否加：

1. 更多工艺页：软珐琅单独页、挑战币单独页（把长尾词各自拆出来）
2. 案例页：按买家类型分的项目案例（能吃到大量长尾）
3. 询价表单接后端（Formspree / Cloudflare Worker / 邮件转发），并做询盘入库与跟进状态管理
4. GA4 + Search Console 接入与事件埋点，重点跟踪速配器配置次数与表单提交率
5. 下载型物料：产品目录 PDF、工艺对照表 PDF、尺寸对照表 PDF，走 gated download 收线索
6. 数字样品册：把 12 种电镀与 5 种工艺做成可点击的在线样品册
7. 独立域名策略评估：是否需要为 challenge coins 或 keychains 单开子域
