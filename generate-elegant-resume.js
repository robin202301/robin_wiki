const { Document, Paragraph, TextRun, HeadingLevel, AlignmentType, BorderStyle, TabStopType, TabStopPosition } = require('docx');
const fs = require('fs');

// 暖色调配色方案（优雅风格）
const colors = {
    primary: '8B4513',      // 深棕色
    secondary: 'D4A574',    // 金棕色
    accent: 'A0522D',       // 赭色
    text: '2C2C2C',         // 深灰黑
    lightText: '888888',    // 浅灰
    bg: 'FAF6F0',           // 米白
    border: 'E8DDD0',       // 边框灰
};

// 创建优雅风格简历
const doc = new Document({
    styles: {
        default: {
            document: {
                run: {
                    font: 'Microsoft YaHei',
                    size: 21,
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
                    size: 36,
                    bold: true,
                    color: colors.primary,
                    font: 'SimSun',
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
                    size: 28,
                    bold: true,
                    color: colors.primary,
                    font: 'SimSun',
                },
                paragraph: {
                    spacing: { before: 360, after: 160 },
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
                    spacing: { before: 240, after: 120 },
                    outlineLevel: 2,
                },
            },
        ],
    },
    sections: [
        {
            properties: {
                page: {
                    margin: {
                        top: 1080,
                        right: 1080,
                        bottom: 1080,
                        left: 1080,
                    },
                },
            },
            children: [
                // 顶部装饰线
                new Paragraph({
                    children: [],
                    border: {
                        top: {
                            color: colors.secondary,
                            space: 1,
                            value: 'single',
                            size: 18,
                        },
                    },
                    spacing: { after: 400 },
                }),

                // 姓名
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '[您的姓名]',
                            bold: true,
                            size: 48,
                            color: colors.text,
                            font: 'SimSun',
                        }),
                    ],
                    alignment: AlignmentType.CENTER,
                    spacing: { after: 80 },
                }),

                // 副标题
                new Paragraph({
                    children: [
                        new TextRun({
                            text: '电话销售团队经理 · 9年资深管理',
                            size: 24,
                            color: colors.primary,
                            font: 'Microsoft YaHei',
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

                // 核心数据展示
                new Paragraph({
                    children: [
                        new TextRun({ text: '9年', bold: true, size: 32, color: colors.primary }),
                        new TextRun({ text: '深耕电销    ', size: 18, color: colors.lightText }),
                        new TextRun({ text: '40+', bold: true, size: 32, color: colors.primary }),
                        new TextRun({ text: '团队管理    ', size: 18, color: colors.lightText }),
                        new TextRun({ text: '15亿', bold: true, size: 32, color: colors.primary }),
                        new TextRun({ text: '累计业绩    ', size: 18, color: colors.lightText }),
                        new TextRun({ text: '95%', bold: true, size: 32, color: colors.primary }),
                        new TextRun({ text: '客户满意度', size: 18, color: colors.lightText }),
                    ],
                    alignment: AlignmentType.CENTER,
                    border: {
                        top: { color: colors.border, size: 6, style: BorderStyle.SINGLE, space: 8 },
                        bottom: { color: colors.border, size: 6, style: BorderStyle.SINGLE, space: 8 },
                    },
                    spacing: { before: 200, after: 300 },
                }),

                // 01 职业概述
                new Paragraph({
                    children: [
                        new TextRun({ text: '01', bold: true, size: 40, color: colors.secondary, font: 'SimSun' }),
                        new TextRun({ text: '  职业概述', bold: true, size: 28, color: colors.primary, font: 'SimSun' }),
                    ],
                    spacing: { before: 200, after: 150 },
                    border: {
                        bottom: { color: colors.secondary, size: 6, style: BorderStyle.SINGLE, space: 8 },
                    },
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
                            color: colors.primary,
                        }),
                        new TextRun({
                            text: '信用卡电话销售团队管理经验。从一线电销专员成长为管理',
                            color: colors.text,
                        }),
                        new TextRun({
                            text: '40+人',
                            bold: true,
                            color: colors.primary,
                        }),
                        new TextRun({
                            text: '团队的资深经理，深谙信用卡电销业务全链条运作。擅长团队搭建、业绩突破、流程优化与风控管理，累计带领团队创造超过',
                            color: colors.text,
                        }),
                        new TextRun({
                            text: '15亿元',
                            bold: true,
                            color: colors.primary,
                        }),
                        new TextRun({
                            text: '发卡业绩，客户满意度持续保持',
                            color: colors.text,
                        }),
                        new TextRun({
                            text: '95%',
                            bold: true,
                            color: colors.primary,
                        }),
                        new TextRun({
                            text: '以上。',
                            color: colors.text,
                        }),
                    ],
                    indent: { left: 200, right: 200 },
                    shading: { type: 'clear', color: 'auto', fill: colors.bg },
                    border: {
                        left: { color: colors.secondary, size: 12, style: BorderStyle.SINGLE },
                    },
                    spacing: { before: 100, after: 300 },
                }),

                // 02 职业履历
                new Paragraph({
                    children: [
                        new TextRun({ text: '02', bold: true, size: 40, color: colors.secondary, font: 'SimSun' }),
                        new TextRun({ text: '  职业履历', bold: true, size: 28, color: colors.primary, font: 'SimSun' }),
                    ],
                    spacing: { before: 200, after: 150 },
                    border: {
                        bottom: { color: colors.secondary, size: 6, style: BorderStyle.SINGLE, space: 8 },
                    },
                }),

                // 职位1
                new Paragraph({
                    children: [
                        new TextRun({ text: '电话销售团队经理', bold: true, size: 24, color: colors.text }),
                        new TextRun({ text: '    2020 — 至今', size: 20, color: colors.primary }),
                    ],
                    spacing: { after: 60 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '交通银行信用卡中心 · 上海', italics: true, size: 20, color: colors.lightText }),
                    ],
                    spacing: { after: 100 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '◆  管理', size: 20, color: colors.secondary }),
                        new TextRun({ text: ' 40人 ', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '电销团队，下设4个小组，建立"师徒制"培养体系', size: 20, color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '◆  2024年发卡量 ', size: 20, color: colors.secondary }),
                        new TextRun({ text: '3.2万张', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '，完成率 ', size: 20, color: colors.secondary }),
                        new TextRun({ text: '128%', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '，全国排名第3', size: 20, color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '◆  2023年业绩达 ', size: 20, color: colors.secondary }),
                        new TextRun({ text: '5.8亿元', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '，超额KPI 35%，连续3年人均产能前20%', size: 20, color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '◆  新人留存率从60%提升至 ', size: 20, color: colors.secondary }),
                        new TextRun({ text: '85%', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '，业绩波动率降低 ', size: 20, color: colors.secondary }),
                        new TextRun({ text: '40%', bold: true, color: colors.primary, size: 20 }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 200 },
                }),

                // 职位2
                new Paragraph({
                    children: [
                        new TextRun({ text: '高级电销专员 / 组长', bold: true, size: 24, color: colors.text }),
                        new TextRun({ text: '    2017 — 2020', size: 20, color: colors.primary }),
                    ],
                    spacing: { after: 60 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '交通银行信用卡中心 · 上海', italics: true, size: 20, color: colors.lightText }),
                    ],
                    spacing: { after: 100 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '◆  连续', size: 20, color: colors.secondary }),
                        new TextRun({ text: ' 18个月 ', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '发卡量排名第一，月均发卡 ', size: 20, color: colors.secondary }),
                        new TextRun({ text: '180+张', bold: true, color: colors.primary, size: 20 }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '◆  2019年年度业绩突破 ', size: 20, color: colors.secondary }),
                        new TextRun({ text: '2000万', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '，获"金牌销售"称号', size: 20, color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '◆  客户转化率从行业平均8%提升至 ', size: 20, color: colors.secondary }),
                        new TextRun({ text: '18%', bold: true, color: colors.primary, size: 20 }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 300 },
                }),

                // 03 代表项目
                new Paragraph({
                    children: [
                        new TextRun({ text: '03', bold: true, size: 40, color: colors.secondary, font: 'SimSun' }),
                        new TextRun({ text: '  代表项目', bold: true, size: 28, color: colors.primary, font: 'SimSun' }),
                    ],
                    spacing: { before: 200, after: 150 },
                    border: {
                        bottom: { color: colors.secondary, size: 6, style: BorderStyle.SINGLE, space: 8 },
                    },
                }),

                // 项目1
                new Paragraph({
                    children: [
                        new TextRun({ text: '电销数字化转型', bold: true, size: 22, color: colors.text }),
                        new TextRun({ text: '    2023.06 — 2023.12 · 业务负责人', size: 18, color: colors.lightText }),
                    ],
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '主导智能外呼系统试点，设计人机协作流程，优化差异化话术策略', size: 20, color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 100 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '成果：', bold: true, size: 20, color: colors.primary }),
                        new TextRun({ text: ' 接通率↑35%  ', color: colors.accent, size: 18 }),
                        new TextRun({ text: ' 产能↑22%  ', color: colors.accent, size: 18 }),
                        new TextRun({ text: ' 成本↓15%  ', color: colors.accent, size: 18 }),
                        new TextRun({ text: ' 创新奖', color: colors.accent, size: 18 }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 200 },
                }),

                // 项目2
                new Paragraph({
                    children: [
                        new TextRun({ text: '新人培养体系优化', bold: true, size: 22, color: colors.text }),
                        new TextRun({ text: '    2022.01 — 2022.09 · 项目负责人', size: 18, color: colors.lightText }),
                    ],
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '重建培训体系，1对1师徒带教3个月，阶段性考核+缓冲期', size: 20, color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 100 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '成果：', bold: true, size: 20, color: colors.primary }),
                        new TextRun({ text: ' 留存率↑25%  ', color: colors.accent, size: 18 }),
                        new TextRun({ text: ' 首月产能↑40%  ', color: colors.accent, size: 18 }),
                        new TextRun({ text: ' 培训成本↓25%  ', color: colors.accent, size: 18 }),
                        new TextRun({ text: ' 全中心推广', color: colors.accent, size: 18 }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 300 },
                }),

                // 04 核心能力
                new Paragraph({
                    children: [
                        new TextRun({ text: '04', bold: true, size: 40, color: colors.secondary, font: 'SimSun' }),
                        new TextRun({ text: '  核心能力', bold: true, size: 28, color: colors.primary, font: 'SimSun' }),
                    ],
                    spacing: { before: 200, after: 150 },
                    border: {
                        bottom: { color: colors.secondary, size: 6, style: BorderStyle.SINGLE, space: 8 },
                    },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '◆  团队搭建与管理', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '    ◆  销售策略与执行', bold: true, color: colors.primary, size: 20 }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '◆  绩效激励设计', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '    ◆  数据分析（Excel/SQL）', bold: true, color: colors.primary, size: 20 }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '◆  风控合规管理', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '    ◆  跨部门协同', bold: true, color: colors.primary, size: 20 }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 80 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '◆  话术优化与迭代', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '    ◆  培训体系搭建', bold: true, color: colors.primary, size: 20 }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 300 },
                }),

                // 05 荣誉奖项
                new Paragraph({
                    children: [
                        new TextRun({ text: '05', bold: true, size: 40, color: colors.secondary, font: 'SimSun' }),
                        new TextRun({ text: '  荣誉奖项', bold: true, size: 28, color: colors.primary, font: 'SimSun' }),
                    ],
                    spacing: { before: 200, after: 150 },
                    border: {
                        bottom: { color: colors.secondary, size: 6, style: BorderStyle.SINGLE, space: 8 },
                    },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '2024  ', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '交行信用卡中心"优秀团队经理"    ', size: 20, color: colors.text }),
                        new TextRun({ text: '2023  ', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '全国电销团队业绩排名第3', size: 20, color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 100 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '2022  ', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '交行信用卡中心"管理创新奖"    ', size: 20, color: colors.text }),
                        new TextRun({ text: '2020  ', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '"金牌团队经理"称号', size: 20, color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 100 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '2019  ', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '个人年度业绩冠军 · 金牌销售    ', size: 20, color: colors.text }),
                        new TextRun({ text: '2018  ', bold: true, color: colors.primary, size: 20 }),
                        new TextRun({ text: '连续4季度"月度销售之星"', size: 20, color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 300 },
                }),

                // 06 教育背景
                new Paragraph({
                    children: [
                        new TextRun({ text: '06', bold: true, size: 40, color: colors.secondary, font: 'SimSun' }),
                        new TextRun({ text: '  教育背景', bold: true, size: 28, color: colors.primary, font: 'SimSun' }),
                    ],
                    spacing: { before: 200, after: 150 },
                    border: {
                        bottom: { color: colors.secondary, size: 6, style: BorderStyle.SINGLE, space: 8 },
                    },
                }),

                new Paragraph({
                    children: [
                        new TextRun({ text: '🎓  上海大学', bold: true, size: 24, color: colors.primary }),
                        new TextRun({ text: '  ·  工商管理  ·  本科  ·  2011年 — 2015年', size: 20, color: colors.text }),
                    ],
                    indent: { left: 360 },
                    spacing: { after: 300 },
                }),

                // 底部信息
                new Paragraph({
                    children: [],
                    border: {
                        bottom: { color: colors.border, size: 6, style: BorderStyle.SINGLE, space: 8 },
                    },
                    spacing: { after: 200 },
                }),

                new Paragraph({
                    children: [
                        new TextRun({
                            text: '到岗时间：1个月内  |  期望薪资：25-35K（可面议）  |  工作地点：上海优先',
                            size: 18,
                            color: colors.lightText,
                        }),
                    ],
                    alignment: AlignmentType.CENTER,
                    spacing: { after: 200 },
                }),

                // 底部装饰线
                new Paragraph({
                    children: [],
                    border: {
                        bottom: { color: colors.secondary, size: 18, style: BorderStyle.SINGLE, space: 1 },
                    },
                }),
            ],
        },
    ],
});

// 生成Word文档
const Packer = require('docx').Packer;
Packer.toBuffer(doc).then((buffer) => {
    fs.writeFileSync('交行信用卡中心电销团队经理简历_优雅风格.docx', buffer);
    console.log('✅ 优雅风格简历已生成：交行信用卡中心电销团队经理简历_优雅风格.docx');
}).catch((err) => {
    console.error('生成失败：', err);
});
