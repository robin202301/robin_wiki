const { Document, Paragraph, TextRun, HeadingLevel, AlignmentType, Packer, BorderStyle } = require("docx");
const fs = require("fs");
const path = require("path");

// 解析Markdown为Word段落
function parseMarkdown(content) {
  const lines = content.split("\n");
  const paragraphs = [];
  let inCodeBlock = false;
  let codeContent = [];
  let inTable = false;
  let tableRows = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // 代码块处理
    if (line.trim().startsWith("```")) {
      if (inCodeBlock) {
        // 结束代码块
        paragraphs.push(
          new Paragraph({
            children: [
              new TextRun({
                text: codeContent.join("\n"),
                font: "Consolas",
                size: 18,
                color: "2D3748",
              }),
            ],
            spacing: { before: 100, after: 100 },
            shading: { type: "clear", color: "auto", fill: "F7F9FC" },
            border: {
              left: { color: "3B7DD8", size: 12, style: BorderStyle.SINGLE },
            },
          })
        );
        codeContent = [];
        inCodeBlock = false;
      } else {
        inCodeBlock = true;
      }
      continue;
    }

    if (inCodeBlock) {
      codeContent.push(line);
      continue;
    }

    // 表格处理（简化）
    if (line.includes("|") && line.trim().startsWith("|")) {
      if (!inTable) {
        inTable = true;
        tableRows = [];
      }
      if (!line.includes("---")) {
        tableRows.push(line);
      }
      continue;
    } else if (inTable) {
      // 表格结束，转换为段落
      for (const row of tableRows) {
        const cells = row
          .split("|")
          .filter((c) => c.trim())
          .map((c) => c.trim());
        paragraphs.push(
          new Paragraph({
            children: [
              new TextRun({
                text: cells.join("  |  "),
                size: 20,
                font: "Calibri",
              }),
            ],
            spacing: { before: 60, after: 60 },
          })
        );
      }
      tableRows = [];
      inTable = false;
    }

    // 空行跳过
    if (!line.trim()) continue;

    // 标题处理
    if (line.startsWith("# ")) {
      paragraphs.push(
        new Paragraph({
          children: [
            new TextRun({
              text: line.substring(2).trim(),
              bold: true,
              size: 32,
              color: "1B2A4A",
              font: "Georgia",
            }),
          ],
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 400, after: 200 },
        })
      );
    } else if (line.startsWith("## ")) {
      paragraphs.push(
        new Paragraph({
          children: [
            new TextRun({
              text: line.substring(3).trim(),
              bold: true,
              size: 28,
              color: "2C5282",
              font: "Georgia",
            }),
          ],
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 360, after: 160 },
          border: {
            bottom: {
              color: "3B7DD8",
              space: 4,
              value: "single",
              size: 6,
            },
          },
        })
      );
    } else if (line.startsWith("### ")) {
      paragraphs.push(
        new Paragraph({
          children: [
            new TextRun({
              text: line.substring(4).trim(),
              bold: true,
              size: 24,
              color: "2D3748",
              font: "Calibri",
            }),
          ],
          heading: HeadingLevel.HEADING_3,
          spacing: { before: 280, after: 120 },
        })
      );
    } else if (line.startsWith("#### ")) {
      paragraphs.push(
        new Paragraph({
          children: [
            new TextRun({
              text: line.substring(5).trim(),
              bold: true,
              size: 22,
              color: "4A5568",
              font: "Calibri",
            }),
          ],
          spacing: { before: 200, after: 100 },
        })
      );
    }
    // 列表处理
    else if (line.trim().startsWith("- ") || line.trim().startsWith("* ")) {
      const indent = line.search(/\S/);
      const text = line.trim().substring(2);
      paragraphs.push(
        new Paragraph({
          children: [
            new TextRun({
              text: "• " + text,
              size: 21,
              font: "Calibri",
            }),
          ],
          indent: { left: indent * 200 },
          spacing: { before: 60, after: 60 },
        })
      );
    } else if (/^\d+\.\s/.test(line.trim())) {
      const text = line.trim().replace(/^\d+\.\s/, "");
      paragraphs.push(
        new Paragraph({
          children: [
            new TextRun({
              text: line.trim(),
              size: 21,
              font: "Calibri",
            }),
          ],
          spacing: { before: 60, after: 60 },
        })
      );
    }
    // 普通段落
    else {
      // 处理粗体
      const parts = [];
      let remaining = line;
      const boldRegex = /\*\*(.*?)\*\*/g;
      let lastIndex = 0;
      let match;

      while ((match = boldRegex.exec(remaining)) !== null) {
        if (match.index > lastIndex) {
          parts.push(
            new TextRun({
              text: remaining.substring(lastIndex, match.index),
              size: 21,
              font: "Calibri",
            })
          );
        }
        parts.push(
          new TextRun({
            text: match[1],
            bold: true,
            size: 21,
            font: "Calibri",
          })
        );
        lastIndex = match.index + match[0].length;
      }

      if (lastIndex < remaining.length) {
        parts.push(
          new TextRun({
            text: remaining.substring(lastIndex),
            size: 21,
            font: "Calibri",
          })
        );
      }

      if (parts.length > 0) {
        paragraphs.push(
          new Paragraph({
            children: parts,
            spacing: { before: 80, after: 80 },
          })
        );
      }
    }
  }

  return paragraphs;
}

// 生成Word文档
async function generateWordDoc(markdownFile, outputFile) {
  const content = fs.readFileSync(markdownFile, "utf-8");
  const paragraphs = parseMarkdown(content);

  const doc = new Document({
    sections: [
      {
        properties: {},
        children: paragraphs,
      },
    ],
  });

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputFile, buffer);
  console.log(`✓ 已生成: ${outputFile}`);
}

// 主函数
async function main() {
  const docs = [
    {
      input: "rag-vectordb/docs/rag-knowledge.md",
      output: "rag-vectordb/docs/RAG知识库完整指南.docx",
    },
    {
      input: "rag-vectordb/docs/vectordb-knowledge.md",
      output: "rag-vectordb/docs/向量数据库完整指南.docx",
    },
    {
      input: "aws-data-services/aws-data-knowledge.md",
      output: "aws-data-services/AWS数据服务知识体系.docx",
    },
    {
      input: "resume-bocom-credit-card.md",
      output: "交行信用卡中心电销团队经理简历.docx",
    },
  ];

  for (const doc of docs) {
    if (fs.existsSync(doc.input)) {
      await generateWordDoc(doc.input, doc.output);
    } else {
      console.log(`⚠ 文件不存在: ${doc.input}`);
    }
  }

  console.log("\n✅ 所有Word文档生成完成！");
}

main().catch(console.error);
