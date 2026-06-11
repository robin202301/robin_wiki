const { Document, Paragraph, TextRun, AlignmentType, Packer } = require("docx");
const fs = require("fs");

// Helper functions
function sectionTitle(text) {
  return new Paragraph({
    children: [
      new TextRun({ text, bold: true, size: 26, color: "1B2A4A", font: "Georgia" })
    ],
    spacing: { before: 360, after: 160 },
    border: { bottom: { color: "3B7DD8", space: 4, value: "single", size: 6 } }
  });
}

function expHeader(role, company, date) {
  return [
    new Paragraph({
      children: [
        new TextRun({ text: role, bold: true, size: 24, color: "1B2A4A", font: "Calibri" }),
      ],
      spacing: { before: 200, after: 40 }
    }),
    new Paragraph({
      children: [
        new TextRun({ text: company, size: 22, color: "3B7DD8", font: "Calibri" }),
        new TextRun({ text: "    " + date, size: 20, color: "718096", font: "Calibri" }),
      ],
      spacing: { after: 80 }
    })
  ];
}

function bullet(text, last = false) {
  return new Paragraph({
    children: [
      new TextRun({ text: "▸ ", color: "B8860B", size: 20, font: "Calibri" }),
      new TextRun({ text, size: 21, color: "4A5568", font: "Calibri" }),
    ],
    indent: { left: 280 },
    spacing: { after: last ? 180 : 40 }
  });
}

function projBlock(title, meta, desc, result) {
  const children = [
    new Paragraph({
      children: [
        new TextRun({ text: "▸ ", color: "3B7DD8", size: 20 }),
        new TextRun({ text: title, bold: true, size: 22, color: "1B2A4A" }),
      ],
      spacing: { before: 160, after: 40 }
    }),
    new Paragraph({
      children: [
        new TextRun({ text: meta, size: 19, color: "718096", italics: true }),
      ],
      indent: { left: 280 },
      spacing: { after: 40 }
    }),
    new Paragraph({
      children: [
        new TextRun({ text: desc, size: 21, color: "4A5568" }),
      ],
      indent: { left: 280 },
      spacing: { after: 40 }
    })
  ];
  if (result) {
    children.push(new Paragraph({
      children: [
        new TextRun({ text: result, size: 20, color: "3B7DD8", bold: true }),
      ],
      indent: { left: 280 },
      spacing: { after: 180 }
    }));
  }
  return children;
}

function skillRow(label, value) {
  return new Paragraph({
    children: [
      new TextRun({ text: "▸ ", color: "3B7DD8", size: 20 }),
      new TextRun({ text: label, bold: true, size: 21 }),
      new TextRun({ text: value, size: 21, color: "4A5568" }),
    ],
    spacing: { after: 60 }
  });
}

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Calibri", size: 22 }
      }
    }
  },
  sections: [{
    properties: {
      page: {
        margin: { top: 720, right: 860, bottom: 720, left: 860 }
      }
    },
    children: [
      // === HEADER ===
      new Paragraph({
        children: [
          new TextRun({ text: "SHI YUAN", bold: true, size: 56, color: "1B2A4A", font: "Georgia" })
        ],
        alignment: AlignmentType.CENTER,
        spacing: { after: 80 }
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "Senior Data Architect", size: 28, color: "3B7DD8", font: "Calibri" })
        ],
        alignment: AlignmentType.CENTER,
        spacing: { after: 160 }
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "📍 Shanghai, China   │   📱 +86 159 2183 0095   │   ✉️ robin202206@163.com", size: 20, color: "4A5568" }),
        ],
        alignment: AlignmentType.CENTER,
        spacing: { after: 80 }
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "💼 13+ Years of Experience   │   🌐 English: Professional Working Proficiency", size: 20, color: "4A5568" }),
        ],
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 }
      }),

      // Divider
      new Paragraph({
        border: { bottom: { color: "1B2A4A", space: 1, value: "single", size: 12 } },
        spacing: { after: 300 }
      }),

      // === SUMMARY ===
      sectionTitle("PROFESSIONAL SUMMARY"),
      new Paragraph({
        children: [
          new TextRun({
            text: "Seasoned Data Architect with 13+ years of experience designing and delivering enterprise-scale data platforms across Fortune 500 multinationals. Deep expertise in cloud-native architectures (GCP, Azure, Alibaba Cloud, AWS), big data ecosystems (Hadoop, Spark, Flink, HBase), and modern data stack (Snowflake, dbt, Delta Lake, ClickHouse). Proven track record in cross-border data migration, real-time data pipelines, LLM-powered intelligent operations, and data governance. International work experience with strong cross-cultural collaboration skills and English as a working language.",
            size: 22, color: "4A5568"
          })
        ],
        spacing: { after: 200 }
      }),

      // === SKILLS ===
      sectionTitle("CORE COMPETENCIES"),
      skillRow("Cloud Platforms: ", "GCP, Azure, Alibaba Cloud, AWS & native services"),
      skillRow("Big Data Ecosystem: ", "Hadoop, Hive, HBase, Spark, Flink, Kubernetes"),
      skillRow("Modern Data Stack: ", "Snowflake, dbt, Delta Lake, ClickHouse, Hudi"),
      skillRow("Data Modeling: ", "Dimensional modeling, DAMA governance methodology"),
      skillRow("Programming: ", "Python, Java, Shell scripting, advanced SQL"),
      skillRow("AI/ML: ", "LLM application development, MLOps end-to-end pipelines"),
      skillRow("Orchestration: ", "Airflow, Azkaban, DolphinScheduler, Cloud Build"),
      skillRow("Systems: ", "Linux (advanced), data governance platforms, DevOps"),

      // === EXPERIENCE ===
      sectionTitle("PROFESSIONAL EXPERIENCE"),

      // Baozun
      ...expHeader("Data Architect", "Shanghai Baozun E-Commerce Co., Ltd.", "Aug 2025 – Present"),
      bullet("Led enterprise bidding solution design, technical evaluation, and end-to-end data architecture delivery"),
      bullet("Managed data development teams — overseeing timelines, risk mitigation, and quality assurance"),
      bullet("Collaborated with global client teams on product upgrade roadmaps and platform modernization"),
      bullet("Designed cloud-native solutions across GCP, Alibaba Cloud, Azure, and AWS"),
      bullet("Built an intelligent data operations agent system using LangChain + Qwen/DeepSeek multi-agent architecture — achieved 80%+ auto-resolution rate, reducing incident response from hours to minutes", true),

      // eBay
      ...expHeader("Data Warehouse Engineer", "eBay Engineering Software (Shanghai) Co., Ltd. (AWF)", "Oct 2024 – Aug 2025"),
      bullet("Architected a GCP-based data lake for processing external user-intelligence and asset-protection data from third-party vendors and security platforms"),
      bullet("Built data collection pipelines from vendor APIs with regex-based preprocessing for unstructured data"),
      bullet("Developed structured data processing using Pandas with schema-formatted output to GCS"),
      bullet("Created unified Dataflow templates for analytics and ML model training support"),
      bullet("Designed and delivered Tableau dashboards; supported ML team model deployment", true),

      // JLL
      ...expHeader("Data Architect", "JLL (Jones Lang LaSalle) Shanghai", "Sep 2022 – Aug 2024"),
      bullet("Led China data center architecture design and executed cross-border data migration from Microsoft Azure (Global) to Alibaba Cloud"),
      bullet("Coordinated cross-departmental infrastructure migration and platform deployment"),
      bullet("Built and optimized scheduling platform (Airflow) and analytics environment (Zeppelin)"),
      bullet("Designed real-time data warehouse with dual batch/streaming pipeline using Flink CDC, Delta Lake, and Flink SQL"),
      bullet("Implemented cross-region data sync from Alibaba Cloud RDS to Azure SQL Server via DTS + Flink for global reporting dashboards", true),

      // StubHub
      ...expHeader("Data Architect", "StubHub (formerly eBay Inc.)", "Apr 2021 – Jul 2022"),
      bullet("Served as Infrastructure Architect responsible for pipeline development, ETL, and cloud-native infrastructure build-out"),
      bullet("Completed on-premise to GCP migration using dbt + BigQuery + Cloud Build + Airflow"),
      bullet("Executed GCP to Azure cloud migration leveraging Snowflake + dbt + Airflow"),
      bullet("Built end-to-end ETL pipelines and analytics dashboards"),
      bullet("Delivered knowledge transfer and internal training programs for cloud platform adoption", true),

      // Zhangmen
      ...expHeader("Data Warehouse Lead", "Shanghai Zhangmen Technology Co., Ltd. (Walmart Partner)", "Mar 2019 – Mar 2021"),
      bullet("Built real-time data center supporting high-throughput transaction processing using Kafka + Flink + HBase / ES / Redis"),
      bullet("Designed and implemented merchant fraud detection model using hybrid approach (Clustering + GBDT + Rules)"),
      bullet("Led Hadoop cluster migration across data centers under regulatory requirements"),
      bullet("Introduced DolphinScheduler with custom development for unified job scheduling and real-time monitoring"),
      bullet("Established data warehouse layered architecture standards, naming conventions, and code review processes", true),

      // Ping An
      ...expHeader("Data Engineer", "Ping An Puhui Enterprise Management Co., Ltd.", "Feb 2017 – Feb 2019"),
      bullet("Built financial big data platform from scratch on CDH, supporting real-time processing and anti-fraud applications"),
      bullet("Designed big data solutions integrating GoldenGate + Kafka + Redis + HBase"),
      bullet("Developed big data permission management platform and automated ETL synchronization tools"),
      bullet("Implemented batch scheduling using Azkaban; supported overseas business data expansion", true),

      // Zhongyi
      ...expHeader("Data Engineer", "Anhui Zhongyi Zhilv Information Technology Co., Ltd.", "Jul 2013 – Jan 2017"),
      bullet("Managed Apache Hadoop cluster setup, operations, and performance optimization"),
      bullet("Designed big data solutions and maintained database cluster systems"),
      bullet("Consolidated IT infrastructure resources and planned capacity allocation", true),

      // === PROJECTS ===
      sectionTitle("KEY PROJECTS"),

      ...projBlock(
        "Multi-Agent Intelligent Data Warehouse Operations System",
        "Shanghai Baozun · Data Architect · Dec 2025 – Apr 2026",
        "Designed and deployed a multi-agent system for enterprise data warehouse operations (10,000+ tables, 100+ users). Built on LangChain + Qwen/DeepSeek with specialized agents for routing, data querying, log analysis, code retrieval, and automated changes. Deeply integrated with metastore, Spark, ELK, and GitLab.",
        "✓ 80%+ auto-resolution rate · Response time: hours → minutes · Hundreds of team-hours saved monthly"
      ),
      ...projBlock(
        "Cross-Border Data Migration & China Data Center",
        "JLL · Data Architect · Aug 2022 – Sep 2024",
        "Architected China regional data center on Alibaba Cloud and executed full data migration from Microsoft Azure global instance. Redesigned data models, established development standards, and deployed DevOps practices."
      ),
      ...projBlock(
        "JLL Real-Time Data Warehouse",
        "JLL · Architect & Developer · Dec 2023 – Jun 2024",
        "Built real-time data warehouse with dual batch/streaming pipeline. Ingested click-stream logs and CDC data via Flume/Flink CDC, layered storage on Delta Lake, unified processing with Flink SQL."
      ),
      ...projBlock(
        "StubHub: On-Premise to GCP Migration",
        "StubHub · Senior Data Engineer · May 2021 – Oct 2021",
        "Led data migration strategy for StubHub's full system extraction from eBay infrastructure to GCP. Historical data (Oracle → GCS → BigQuery/Spanner), incremental sync (Oracle + GoldenGate + Kafka + Spanner), and DW migration (Airflow → BigQuery)."
      ),
      ...projBlock(
        "Real-Time Transaction Data Platform",
        "Zhangmen · Architect · Oct 2020 – Feb 2021",
        "Designed real-time merchant transaction system replacing Oracle ETL bottleneck. OGG-based CDC from Oracle redo logs → Kafka → Flink → multi-sink output (ES, HBase, Redis)."
      ),
      ...projBlock(
        "Merchant Fraud Detection Model",
        "Zhangmen · Data Engineer · Sep 2020 – Feb 2021",
        "Developed pre-transaction and in-transaction fraud warning system for bank card fraud using hybrid model approach: Clustering + GBDT + Rule-based engine."
      ),
      ...projBlock(
        "Unified Scheduling Platform",
        "Zhangmen · Developer · Jun 2019 – Jul 2019",
        "Introduced DolphinScheduler to replace 30-node cluster crontab chaos. Custom development for Jira integration and real-time monitoring with alerting."
      ),

      // === ADDITIONAL ===
      sectionTitle("ADDITIONAL INFORMATION"),
      skillRow("Languages: ", "Mandarin (Native) · English (Professional Working Proficiency)"),
      skillRow("International Experience: ", "eBay, StubHub, JLL (Fortune 500 multinationals)"),
      skillRow("Target Roles: ", "Data Architecture · Data Platform · AI Engineering"),
      skillRow("Availability: ", "Open to opportunities in Shanghai"),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("resume.docx", buffer);
  console.log("✅ Word简历已生成：resume.docx");
}).catch(err => {
  console.error("生成失败:", err);
});
