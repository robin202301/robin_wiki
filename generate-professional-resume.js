const { Document, Paragraph, TextRun, AlignmentType, HeadingLevel, BorderStyle, TabStopPosition, TabStopType, PageBreak, LevelFormat } = require('docx');
const fs = require('fs');

// 配色方案
const colors = {
    primary: '1E3C72',      // 深蓝
    secondary: '2A5298',    // 亮蓝
    accent: '4FACFE',       // 天蓝
    text: '2D3748',         // 深灰
    lightText: '718096',    // 浅灰
    bg: 'F7FAFC',           // 背景灰
    white: 'FFFFFF',        // 白色
};

// 创建简历文档
const doc = new Document({
    styles: {
        default: {
            document: {
                run: {
                    font: 'Microsoft YaHei',
                    size: 21, // 10.5pt
                },
            },
        },
        paragraphStyles: [
            {
                id: 'Heading1',
                name: 'Heading 1',
                basedOn: 'Normal',
                next: 'Normal',
                quickFormat: true,
                run: {
                    size: 32,
                    bold: true,
                    color: colors.primary,
                    font: 'Microsoft YaHei',
                },
                paragraph: {
                    spacing: { before: 400, after: 200 },
                    outlineLevel: 0,
                },
            },
            {
                id: 'Heading2',
                name: 'Heading 2',
                basedOn: 'Normal',
                next: 'Normal',
                quickFormat: true,
                run: {
                    size: 26,
                    bold: true,
                    color: colors.secondary,
                    font: 'Microsoft YaHei',
                },
                paragraph: {
                    spacing: { before: 300, after: 150 },
                    outlineLevel: 1,
                },
            },
            {
                id: 'Heading3',
                name: 'Heading 3',
                basedOn: 'Normal',
                next: 'Normal',
                quickFormat: true,
                run: {
                    size: 24,
                    bold: true,
                    color: colors.text,
                    font: 'Microsoft YaHei',
                },
                paragraph: {
                    spacing: { before: 200, after: 100 },
                    outlineLevel: 2,
                },
            },
        ],
    },
    numbering: {
        config: [
            {
                reference: 'bullet-list',
                levels: [
                    {
                        level: 0,
                        format: LevelFormat.BULLET,
                        text: '•',
                        alignment: AlignmentType.LEFT,
                        style: {
                            paragraph: {
                                indent: { left: 720, hanging: 360 },
                            },
                        },
                    },
                ],
            },
        ],
    },
    sections: [
        {
            properties: {
                page: {
                    margin: {
                        top: 720,
                        right: 720,
                        bottom: 720,
                        left: 720,
                    },
                },
            },
            children: [
                // 姓名标题
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '[您的姓名]',
                            bold: true,
                            size: 48,
                            color: colors.primary,
                        }),
                    ],
                    alignment: AlignmentType.CENTER,
                    spacing: { after: 100 },
                }),

                // 职位头衔
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '电话销售团队经理',
                            size: 28,
                            color: colors.secondary,
                        }),
                    ],
                    alignment: AlignmentType.CENTER,
                    spacing: { after: 200 },
                }),

                // 联系信息
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '📱 [您的电话]  |  ✉️ [您的邮箱]  |  📍 上海  |  🎂 32岁',
                            size: 20,
                            color: colors.lightText,
                        }),
                    ],
                    alignment: AlignmentType.CENTER,
                    spacing: { after: 300 },
                }),

                // 分隔线
                new Paragraph({
                    children: [],
                    border: {
                        bottom: {
                            color: colors.secondary,
                            space: 1,
                            value: 'single',
                            size: 12,
                        },
                    },
                    spacing: { after: 300 },
                }),

                // 职业概述
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '💼 职业概述',
                            bold: true,
                            size: 28,
                            color: colors.primary,
                        }),
                    ],
                    spacing: { before: 200, after: 150 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({
                            text: '交通银行信用卡中心资深电销管理者，',
                            color: colors.text,
                        }),
                        new TextRun({
                            text: '9年',
                            bold: true,
                            color: colors.secondary,
                        }),
                        new TextRun({
                            text: '信用卡电话销售团队管理经验。从一线电销专员成长为管理',
                            color: colors.text,
                        }),
                        new TextRun({
                            text: '40+人',
                            bold: true,
                            color: colors.secondary,
                        }),
                        new TextRun({
                            text: '团队的资深经理，深谙信用卡电销业务全链条运作。擅长团队搭建、业绩突破、流程优化与风控管理，累计带领团队创造超过',
                            color: colors.text,
                        }),
                        new TextRun({
                            text: '15亿元',
                            bold: true,
                            color: colors.secondary,
                        }),
                        new TextRun({
                            text: '发卡业绩，客户满意度持续保持',
                            color: colors.text,
                        }),
                        new TextRun({
                            text: '95%',
                            bold: true,
                            color: colors.secondary,
                        }),
                        new TextRun({
                            text: '以上。',
                            color: colors.text,
                        }),
                    ],
                    spacing: { after: 300 },
                }),

                // 核心技能
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '⭐ 核心技能',
                            bold: true,
                            size: 28,
                            color: colors.primary,
                        }),
                    ],
                    spacing: { before: 200, after: 150 },
                }),

                // 技能表格
                new Paragraph({
                    children: [
                        new TextRun({ text: '• 团队管理：', bold: true, color: colors.text }),
                        new TextRun({ text: '40+人团队管理经验，擅长目标分解、过程管控、团队建设', color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 销售策略：', bold: true, color: colors.text }),
                        new TextRun({ text: '顾问式销售、SPIN提问法、异议处理、促成技巧', color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 数据分析：', bold: true, color: colors.text }),
                        new TextRun({ text: '熟练使用Excel、SQL进行业绩分析，通过数据发现问题并制定策略', color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 风控合规：', bold: true, color: colors.text }),
                        new TextRun({ text: '熟悉信用卡申请审核流程、反欺诈识别、合规要求', color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 300 },
                }),

                // 工作经历
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '💼 工作经历',
                            bold: true,
                            size: 28,
                            color: colors.primary,
                        }),
                    ],
                    spacing: { before: 200, after: 150 },
                }),

                // 职位1
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '电话销售团队经理',
                            bold: true,
                            size: 24,
                            color: colors.primary,
                        }),
                    ],
                    spacing: { after: 50 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({
                            text: '交通银行信用卡中心',
                            size: 22,
                            color: colors.secondary,
                        }),
                        new TextRun({
                            text: '    2020年 - 至今',
                            size: 20,
                            color: colors.lightText,
                        }),
                    ],
                    spacing: { after: 100 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({
                            text: '• 管理40人电销团队，下设4个小组，每组10人',
                            color: colors.text,
                        }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 2024年团队发卡量突破', color: colors.text }),
                        new TextRun({ text: '3.2万张', bold: true, color: colors.secondary }),
                        new TextRun({ text: '，完成率', color: colors.text }),
                        new TextRun({ text: '128%', bold: true, color: colors.secondary }),
                        new TextRun({ text: '，排名全国第3', color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 2023年团队业绩达', color: colors.text }),
                        new TextRun({ text: '5.8亿元', bold: true, color: colors.secondary }),
                        new TextRun({ text: '，超额完成KPI ', color: colors.text }),
                        new TextRun({ text: '35%', bold: true, color: colors.secondary }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 建立"师徒制"培养体系，新人3个月留存率从60%提升至', color: colors.text }),
                        new TextRun({ text: '85%', bold: true, color: colors.secondary }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 设计阶梯式激励方案，团队月均业绩波动率降低', color: colors.text }),
                        new TextRun({ text: '40%', bold: true, color: colors.secondary }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 200 },
                }),

                // 职位2
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '高级电销专员 / 组长',
                            bold: true,
                            size: 24,
                            color: colors.primary,
                        }),
                    ],
                    spacing: { after: 50 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({
                            text: '交通银行信用卡中心',
                            size: 22,
                            color: colors.secondary,
                        }),
                        new TextRun({
                            text: '    2017年 - 2020年',
                            size: 20,
                            color: colors.lightText,
                        }),
                    ],
                    spacing: { after: 100 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 连续', color: colors.text }),
                        new TextRun({ text: '18个月', bold: true, color: colors.secondary }),
                        new TextRun({ text: '个人发卡量排名第一，月均发卡', color: colors.text }),
                        new TextRun({ text: '180+张', bold: true, color: colors.secondary }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 2019年个人年度业绩突破', color: colors.text }),
                        new TextRun({ text: '2000万', bold: true, color: colors.secondary }),
                        new TextRun({ text: '，获"金牌销售"称号', color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 客户转化率从行业平均8%提升至', color: colors.text }),
                        new TextRun({ text: '18%', bold: true, color: colors.secondary }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 300 },
                }),

                // 项目经历
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '🚀 项目经历',
                            bold: true,
                            size: 28,
                            color: colors.primary,
                        }),
                    ],
                    spacing: { before: 200, after: 150 },
                }),

                // 项目1
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '电销团队数字化转型项目',
                            bold: true,
                            size: 22,
                            color: colors.primary,
                        }),
                        new TextRun({
                            text: '    2023年6月 - 2023年12月',
                            size: 20,
                            color: colors.lightText,
                        }),
                    ],
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({
                            text: '角色：业务负责人',
                            italics: true,
                            color: colors.lightText,
                            size: 20,
                        }),
                    ],
                    spacing: { after: 100 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '成果标签：', bold: true, color: colors.text }),
                        new TextRun({ text: ' 接通率↑35%  ', color: colors.secondary }),
                        new TextRun({ text: ' 产能↑22%  ', color: colors.secondary }),
                        new TextRun({ text: ' 成本↓15%  ', color: colors.secondary }),
                        new TextRun({ text: ' 创新奖', color: colors.secondary }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 200 },
                }),

                // 项目2
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '新人培养体系优化',
                            bold: true,
                            size: 22,
                            color: colors.primary,
                        }),
                        new TextRun({
                            text: '    2022年1月 - 2022年9月',
                            size: 20,
                            color: colors.lightText,
                        }),
                    ],
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({
                            text: '角色：项目负责人',
                            italics: true,
                            color: colors.lightText,
                            size: 20,
                        }),
                    ],
                    spacing: { after: 100 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '成果标签：', bold: true, color: colors.text }),
                        new TextRun({ text: ' 留存率↑25%  ', color: colors.secondary }),
                        new TextRun({ text: ' 首月产能↑40%  ', color: colors.secondary }),
                        new TextRun({ text: ' 培训成本↓25%  ', color: colors.secondary }),
                        new TextRun({ text: ' 全中心推广', color: colors.secondary }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 300 },
                }),

                // 教育背景
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '🎓 教育背景',
                            bold: true,
                            size: 28,
                            color: colors.primary,
                        }),
                    ],
                    spacing: { before: 200, after: 150 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '上海大学', bold: true, size: 24, color: colors.primary }),
                        new TextRun({ text: '  |  工商管理  |  本科  |  2011年 - 2015年', color: colors.text }),
                    ],
                    spacing: { after: 300 },
                }),

                // 荣誉奖项
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '🏆 荣誉奖项',
                            bold: true,
                            size: 28,
                            color: colors.primary,
                        }),
                    ],
                    spacing: { before: 200, after: 150 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 2024年 - 交行信用卡中心"优秀团队经理"', color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 2023年 - 全国电销团队业绩排名第3', color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 2022年 - 交行信用卡中心"管理创新奖"', color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 2020年 - "金牌团队经理"称号', color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 2019年 - 个人年度业绩冠军，"金牌销售"', color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 300 },
                }),

                // 自我评价
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '✨ 自我评价',
                            bold: true,
                            size: 28,
                            color: colors.primary,
                        }),
                    ],
                    spacing: { before: 200, after: 150 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 业务能力强：', bold: true, color: colors.text }),
                        new TextRun({ text: '9年深耕信用卡电销领域，从一线销售到团队管理，熟悉业务全链条，业绩持续优秀', color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 管理经验丰富：', bold: true, color: colors.text }),
                        new TextRun({ text: '管理40人团队，擅长目标分解、过程管控、团队建设，能带领团队持续超额完成KPI', color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 数据驱动：', bold: true, color: colors.text }),
                        new TextRun({ text: '善于通过数据分析发现问题、制定策略，用数据说话，推动业绩增长', color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '• 创新思维：', bold: true, color: colors.text }),
                        new TextRun({ text: '主动推动数字化转型，引入智能工具提升效率，获公司创新奖认可', color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 200 },
                }),

                // 附加信息
                new Paragraph({
                    border: {
                        top: {
                            color: colors.secondary,
                            space: 1,
                            value: 'single',
                            size: 6,
                        },
                    },
                    spacing: { before: 200, after: 100 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({
                            text: '到岗时间：1个月内  |  期望薪资：25-35K（可面议）  |  工作地点：上海优先',
                            size: 20,
                            color: colors.lightText,
                        }),
                    ],
                    alignment: AlignmentType.CENTER,
                    spacing: { after: 100 },
                }),
            ],
        },
    ],
});

// 生成Word文档
const Packer = require('docx').Packer;
Packer.toBuffer(doc).then((buffer) => {
    fs.writeFileSync('交行信用卡中心电销团队经理简历_精美版.docx', buffer);
    console.log('✅ 精美版简历已生成：交行信用卡中心电销团队经理简历_精美版.docx');
}).catch((err) => {
    console.error('生成失败：', err);
});
