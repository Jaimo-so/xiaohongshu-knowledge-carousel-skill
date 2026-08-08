# Complete RAG eight-page example

This example preserves the full definitions, meanings, mechanisms, limitations, and verification requirements used in the original series. Use it unchanged when reproducing the same lesson; expand it rather than deleting points if more detail is requested.

## 01 Cover

- Eyebrow: `AI回答前，为什么要先翻资料？`
- Main title: `RAG`
- Core line: `让 AI 先查资料，再回答`
- Supporting line: `不是重学一遍，是临时开卷`
- Meaning: visually establish “look up material before answering.”

## 02 Exact definition

- Title: `RAG 是什么？`
- English: `RETRIEVAL-AUGMENTED GENERATION`
- Definition: RAG 的全称是“检索增强生成”。在生成回答之前，系统先从外部知识库检索相关资料，再把资料和用户问题一起交给大模型。
- Meaning: 模型不必只依赖参数中的记忆，也能临时利用较新、私有或特定领域的资料。
- Boundary: RAG 能补充上下文，但不会让答案天然正确。

## 03 Why RAG is needed

- Title: `为什么需要 RAG？`
- Knowledge cutoff: 模型参数中的知识有训练截止时间，不能自动知道之后发生的新变化。
- Private knowledge: 模型通常不知道企业内部文档、个人笔记或受权限保护的私有资料。
- Unsupported answers: 只靠参数记忆回答时，模型可能把不确定的内容组织成听起来合理但没有证据的说法。
- Meaning: RAG 不必重新训练或修改模型参数，而是在每次回答时临时补充相关上下文。
- Boundary: 补充资料能降低风险，但不能消除错误。

## 04 Retrieve

- Title: `第一步：检索`
- English: `RETRIEVE`
- Definition: 用户提问后，系统从文档、网页或数据库中寻找最相关的内容片段。
- Boundary: 相关，不代表天然正确或权威。

## 05 Augment

- Title: `第二步：增强`
- English: `AUGMENT`
- Definition: 系统把检索到的内容片段与用户问题按规则整理，组成提供给大模型的提示上下文。
- Metadata: 上下文还可以包含来源、时间、权限或其他元数据，帮助模型判断资料能否使用以及如何使用。
- Boundary: 上下文不是越多越好；无关、重复或冲突的片段会形成噪声并干扰回答。

## 06 Generate

- Title: `第三步：生成`
- English: `GENERATE`
- Definition: 大模型读取用户问题和检索上下文，再根据这些材料组织回答。
- Controls: 系统可以要求模型标注来源、在资料不足时明确说明，并避免给出超出证据范围的结论。
- Boundary: 模型仍可能误解资料、忽略冲突或编造细节；重要结论仍需核验。

## 07 Prepare searchable material

- Title: `资料怎样变得可检索？`
- English: `INDEX & RETRIEVE`
- Chunking: 先把长文档切分成适合检索的内容片段；片段太大容易混入无关信息，太小则可能丢失上下文。
- Embedding: 嵌入模型把每个片段转换成表示语义特征的数值向量。
- Indexing: 系统把向量和原片段、来源等信息保存到向量数据库或其他检索索引中。
- Query and reranking: 用户提问时，系统也把问题转换成向量，根据相似度寻找候选片段，必要时再进行重排。
- Boundary: 语义相似表示内容可能相关，不等于资料事实正确，也不等于它一定能回答问题。

## 08 Complete recap and checklist

- Title: `记住：RAG 是“带资料回答”`
- Flow: 用户提问后，系统先检索相关片段，再把问题与片段组成上下文，最后让大模型依据上下文生成答案。
- Suitable scenarios: 企业知识库问答、产品与技术文档助手、需要频繁更新资料的问答，以及要求答案能够追溯来源的场景。
- Failure sources: 原始资料可能过时或错误；检索可能漏掉关键片段；上下文可能混入噪声；权限控制可能不完善；模型也可能没有忠实使用证据。
- Usage checks: 检查资料来源与更新时间；保留引用或可追溯依据；资料不足时允许模型说不知道；对重要结论进行人工核验；对私有资料设置访问权限。
