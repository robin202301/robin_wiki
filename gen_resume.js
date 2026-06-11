const { Document, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType, Packer, convertInchesToTwip } = require("docx");
const fs = require("fs");

// 颜色定义
const NAVY = "1E3A5F";
const BLUE = "2C5282";
const GOLD = "D4AF37";
const GRAY = "7F8C8D";
const DARK = "2C3E50";
const LIGHT_GRAY = "34495E";

// 辅助函数
function sectionTitle(text) {
    return new Paragraph({
        children: [
            new TextRun({
                text: text,
                bold: true,
                size: 28,
                color: NAVY,
                font: "Arial"
            })
        ],
        border: {
            bottom: {
                color: GOLD,
                space: 4,
                value: "single",
                size: 6
            }
        },
        spacing: { before: 360, after: 240 }
    });
}

function bulletItem(text) {
    return new Paragraph({
        children: [
            new TextRun({ text: "■  ", size: 18, color: GOLD }),
            new TextRun({ text: text, size: 21, color: DARK, font: "Arial" })
        ],
        spacing: { after: 80 },
        indent: { left: convertInchesToTwip(0.3) }
    });
}

function jobHeader(title, company, period) {
    return [
        new Paragraph({
            children: [
                new TextRun({ text: title, bold: true, size: 24, color: NAVY, font: "Arial" })
            ],
            spacing: { after: 40 }
        }),
        new Paragraph({
            children: [
                new TextRun({ text: company, size: 21, color: BLUE, font: "Arial" }),
                new TextRun({ text: "    |    ", size: 21, color: GRAY }),
                new TextRun({ text: period, size: 21, color: GRAY, font: "Arial" })
            ],
            spacing: { after: 120 }
        })
    ];
}

function achievementCell(number, label) {
    return new TableCell({
        children: [
            new Paragraph({
                children: [new TextRun({ text: number, bold: true, size: 40, color: NAVY, font: "Arial" })],
                alignment: AlignmentType.CENTER,
                spacing: { after: 60 }
            }),
            new Paragraph({
                children: [new TextRun({ text: label, size: 19, color: GRAY, font: "Arial" })],
                alignment: AlignmentType.CENTER
            })
        ],
        width: { size: 3333, type: WidthType.DXA },
        borders: {
            top: { style: "none", size: 0 },
            bottom: { style: "none", size: 0 },
            left: { style: "none", size: 0 },
            right: { style: "none", size: 0 }
        }
    });
}

function projectBlock(name, role, desc) {
    return [
        new Paragraph({
            children: [
                new TextRun({ text: name, bold: true, size: 22, color: NAVY, font: "Arial" })
            ],
            spacing: { after: 40 }
        }),
        new Paragraph({
            children: [
                new TextRun({ text: role, size: 20, color: GRAY, italics: true, font: "Arial" })
            ],
            spacing: { after: 80 }
        }),
        new Paragraph({
            children: [
                new TextRun({ text: desc, size: 21, color: LIGHT_GRAY, font: "Arial" })
            ],
            spacing: { after: 200 },
            indent: { left: convertInchesToTwip(0.2) }
        })
    ];
}

function evalParagraph(title, content) {
    return new Paragraph({
        children: [
            new TextRun({ text: title, bold: true, size: 21, color: NAVY, font: "Arial" }),
            new TextRun({ text: content, size: 21, color: LIGHT_GRAY, font: "Arial" })
        ],
        spacing: { after: 120 }
    });
}

// 构建文档
const doc = new Document({
    creator: "Professional Resume",
    title: "Team Manager Resume",
    sections: [{
        properties: {
            page: {
                margin: {
                    top: convertInchesToTwip(0.8),
                    bottom: convertInchesToTwip(0.8),
                    left: convertInchesToTwip(1.0),
                    right: convertInchesToTwip(1.0)
                }
            }
        },
        children: [
            // ========== 头部：姓名 ==========
            new Paragraph({
                children: [
                    new TextRun({
                        text: "您 的 姓 名",
                        bold: true,
                        size: 52,
                        color: NAVY,
                        font: "Arial",
                        characterSpacing: 120
                    })
                ],
                spacing: { after: 80 }
            }),

            // 职位头衔
            new Paragraph({
                children: [
                    new TextRun({
                        text: "团队经理  |  银行信用卡业务管理",
                        size: 26,
                        color: GOLD,
                        font: "Arial",
                        characterSpacing: 40
                    })
                ],
                spacing: { after: 200 }
            }),

            // 头部金色分隔线
            new Paragraph({
                border: {
                    bottom: { color: GOLD, space: 1, value: "single", size: 12 }
                },
                spacing: { after: 280 }
            }),

            // 联系信息
            new Paragraph({
                children: [
                    new TextRun({ text: "138-XXXX-XXXX", size: 20, color: GRAY, font: "Arial" }),
                    new TextRun({ text: "   |   ", size: 20, color: GOLD }),
                    new TextRun({ text: "your.email@example.com", size: 20, color: GRAY, font: "Arial" }),
                    new TextRun({ text: "   |   ", size: 20, color: GOLD }),
                    new TextRun({ text: "上海市浦东新区", size: 20, color: GRAY, font: "Arial" }),
                    new TextRun({ text: "   |   ", size: 20, color: GOLD }),
                    new TextRun({ text: "1990年X月  |  已婚", size: 20, color: GRAY, font: "Arial" })
                ],
                spacing: { after: 360 }
            }),

            // ========== 职业概述 ==========
            sectionTitle("职业概述  PROFESSIONAL SUMMARY"),

            new Paragraph({
                children: [
                    new TextRun({
                        text: "资深银行信用卡业务管理专家，拥有8年以上银行金融风控及信用卡业务运营经验，具备大型团队统筹管理能力。独立管理150人以上业务团队，擅长团队精细化运营、业绩指标管控、人才梯队搭建、风险合规管理及业务产能优化。在交通银行信用卡中心任职期间，带领团队实现业绩持续增长，风险控制指标优良，团队人效提升显著，多次获得行内优秀管理奖项。精通银行信用卡业务全流程管理，熟悉监管政策与合规要求，具备出色的战略执行力与团队领导力。",
                        size: 21,
                        color: DARK,
                        font: "Arial"
                    })
                ],
                spacing: { after: 360 },
                indent: { left: convertInchesToTwip(0.1) }
            }),

            // ========== 核心技能 ==========
            sectionTitle("核心技能  CORE COMPETENCIES"),

            new Table({
                rows: [
                    new TableRow({
                        children: [
                            new TableCell({
                                children: [new Paragraph({ children: [new TextRun({ text: "■  大型团队统筹管理（150人+）", size: 21, color: DARK })], spacing: { after: 60 } })],
                                width: { size: 50, type: WidthType.PERCENTAGE },
                                borders: { top: { style: "none", size: 0 }, bottom: { style: "none", size: 0 }, left: { style: "none", size: 0 }, right: { style: "none", size: 0 } }
                            }),
                            new TableCell({
                                children: [new Paragraph({ children: [new TextRun({ text: "■  信用卡业务全流程运营", size: 21, color: DARK })], spacing: { after: 60 } })],
                                width: { size: 50, type: WidthType.PERCENTAGE },
                                borders: { top: { style: "none", size: 0 }, bottom: { style: "none", size: 0 }, left: { style: "none", size: 0 }, right: { style: "none", size: 0 } }
                            })
                        ]
                    }),
                    new TableRow({
                        children: [
                            new TableCell({
                                children: [new Paragraph({ children: [new TextRun({ text: "■  业绩指标拆解与达成管控", size: 21, color: DARK })], spacing: { after: 60 } })],
                                width: { size: 50, type: WidthType.PERCENTAGE },
                                borders: { top: { style: "none", size: 0 }, bottom: { style: "none", size: 0 }, left: { style: "none", size: 0 }, right: { style: "none", size: 0 } }
                            }),
                            new TableCell({
                                children: [new Paragraph({ children: [new TextRun({ text: "■  风险合规管理体系建设", size: 21, color: DARK })], spacing: { after: 60 } })],
                                width: { size: 50, type: WidthType.PERCENTAGE },
                                borders: { top: { style: "none", size: 0 }, bottom: { style: "none", size: 0 }, left: { style: "none", size: 0 }, right: { style: "none", size: 0 } }
                            })
                        ]
                    }),
                    new TableRow({
                        children: [
                            new TableCell({
                                children: [new Paragraph({ children: [new TextRun({ text: "■  人才梯队搭建与培养", size: 21, color: DARK })], spacing: { after: 60 } })],
                                width: { size: 50, type: WidthType.PERCENTAGE },
                                borders: { top: { style: "none", size: 0 }, bottom: { style: "none", size: 0 }, left: { style: "none", size: 0 }, right: { style: "none", size: 0 } }
                            }),
                            new TableCell({
                                children: [new Paragraph({ children: [new TextRun({ text: "■  业务产能优化与人效提升", size: 21, color: DARK })], spacing: { after: 60 } })],
                                width: { size: 50, type: WidthType.PERCENTAGE },
                                borders: { top: { style: "none", size: 0 }, bottom: { style: "none", size: 0 }, left: { style: "none", size: 0 }, right: { style: "none", size: 0 } }
                            })
                        ]
                    }),
                    new TableRow({
                        children: [
                            new TableCell({
                                children: [new Paragraph({ children: [new TextRun({ text: "■  客户体验管理与投诉处理", size: 21, color: DARK })], spacing: { after: 60 } })],
                                width: { size: 50, type: WidthType.PERCENTAGE },
                                borders: { top: { style: "none", size: 0 }, bottom: { style: "none", size: 0 }, left: { style: "none", size: 0 }, right: { style: "none", size: 0 } }
                            }),
                            new TableCell({
                                children: [new Paragraph({ children: [new TextRun({ text: "■  跨部门协作与资源整合", size: 21, color: DARK })], spacing: { after: 60 } })],
                                width: { size: 50, type: WidthType.PERCENTAGE },
                                borders: { top: { style: "none", size: 0 }, bottom: { style: "none", size: 0 }, left: { style: "none", size: 0 }, right: { style: "none", size: 0 } }
                            })
                        ]
                    })
                ],
                width: { size: 100, type: WidthType.PERCENTAGE }
            }),

            new Paragraph({ spacing: { after: 200 } }),

            // ========== 工作经历 ==========
            sectionTitle("工作经历  WORK EXPERIENCE"),

            // 工作1
            ...jobHeader("团队经理", "交通银行信用卡中心", "2020.06 - 至今"),
            bulletItem("独立管理150人以上信用卡业务团队，负责团队日常运营、业绩达成、人员管理及风险控制"),
            bulletItem("制定并执行团队年度业务规划，分解KPI指标至各业务单元，确保月度、季度、年度目标100%达成"),
            bulletItem("建立完善的团队管理体系，包括绩效考核、激励机制、培训体系及晋升通道，团队人效提升35%"),
            bulletItem("主导风险合规管理，建立事前预防、事中监控、事后复盘的全流程风控机制，不良率控制在行业优秀水平"),
            bulletItem("搭建三级人才梯队，培养储备主管12人，团队骨干流失率控制在8%以下，远低于行业平均水平"),
            bulletItem("优化业务流程，推行标准化作业体系，业务处理效率提升40%，客户满意度提升至98.5%"),
            bulletItem("负责团队合规培训与监管对接，确保业务操作符合银保监会及行内各项合规要求，零重大合规风险事件"),

            new Paragraph({ spacing: { after: 200 } }),

            // 工作2
            ...jobHeader("高级业务主管", "交通银行信用卡中心", "2018.03 - 2020.05"),
            bulletItem("负责50人业务团队日常管理，统筹信用卡营销推广、客户服务及风险管控工作"),
            bulletItem("制定团队业务策略，带领团队连续12个月超额完成业绩指标，季度业绩达成率120%+"),
            bulletItem("建立客户分层管理体系，针对高价值客户制定专属服务方案，客户留存率提升25%"),
            bulletItem("主导团队技能培训项目，设计系统化培训课程，团队成员业务考核通过率提升至95%"),
            bulletItem("协助部门经理进行团队管理，参与制定部门年度业务规划及管理制度优化"),

            new Paragraph({ spacing: { after: 200 } }),

            // 工作3
            ...jobHeader("客户经理", "交通银行XX分行", "2015.07 - 2018.02"),
            bulletItem("负责信用卡客户拓展与维护，完成个人业绩指标，连续24个月业绩排名分行前10%"),
            bulletItem("深入挖掘客户需求，提供综合金融解决方案，成功营销高端信用卡客户500+户"),
            bulletItem("严格执行风险管控要求，确保客户准入合规，个人管户不良率保持0.5%以下"),
            bulletItem("参与新员工带教工作，协助5名新员工快速成长并独立开展业务"),

            new Paragraph({ spacing: { after: 200 } }),

            // ========== 核心项目经历 ==========
            sectionTitle("核心项目经历  KEY PROJECTS"),

            ...projectBlock(
                "团队产能提升专项项目",
                "项目负责人 | 2023.01 - 2023.12",
                "针对团队产能瓶颈，主导实施\u201C效能倍增\u201D专项项目。通过优化业务流程、完善激励机制、强化技能培训、推行标杆管理等措施，实现团队人均产能提升45%，月度业务处理量突破历史峰值。项目成果获卡中心管理层高度认可，并在全中心推广复制。"
            ),

            ...projectBlock(
                "风险合规管理体系建设",
                "项目牵头人 | 2022.03 - 2022.09",
                "牵头建立团队风险合规管理体系，制定《团队合规操作手册》，建立三级风险预警机制，开展常态化合规培训20+场。项目实施后，团队合规操作规范率达100%，监管检查零问题，客户投诉率下降60%，风险控制指标位列卡中心前三。"
            ),

            ...projectBlock(
                "人才梯队建设工程",
                "项目负责人 | 2021.06 - 2021.12",
                "针对团队快速发展的人才需求，搭建\u201C雏鹰-飞鹰-精鹰\u201D三级人才培养体系。建立储备主管选拔机制，实施导师带教制度，开展管理技能培训项目。年度内成功培养储备主管12人，团队骨干流失率控制在8%以下，人才储备满足业务扩张需求。"
            ),

            // ========== 工作成果 ==========
            sectionTitle("工作成果  KEY ACHIEVEMENTS"),

            new Table({
                rows: [
                    new TableRow({
                        children: [
                            achievementCell("150+", "团队管理规模（人）"),
                            achievementCell("120%", "年度业绩达成率"),
                            achievementCell("35%", "团队人效提升")
                        ]
                    }),
                    new TableRow({
                        height: { value: 200 },
                        children: [
                            new Paragraph({ spacing: { after: 0 } }),
                            new Paragraph({ spacing: { after: 0 } }),
                            new Paragraph({ spacing: { after: 0 } })
                        ]
                    }),
                    new TableRow({
                        children: [
                            achievementCell("98.5%", "客户满意度"),
                            achievementCell("<8%", "骨干流失率"),
                            achievementCell("12人", "培养储备主管")
                        ]
                    })
                ],
                width: { size: 100, type: WidthType.PERCENTAGE }
            }),

            new Paragraph({ spacing: { after: 360 } }),

            // ========== 自我评价 ==========
            sectionTitle("自我评价  PERSONAL EVALUATION"),

            evalParagraph("管理理念：", "坚持以目标为导向、以结果论英雄的管理理念，注重团队文化建设与人文关怀，善于激发团队潜能，打造高绩效、高凝聚力、高执行力的精英团队。"),
            evalParagraph("专业能力：", "深耕银行信用卡业务多年，熟悉信用卡业务全流程及监管政策，具备扎实的风险管理功底和合规意识。在团队管理、业绩达成、风险控制等方面积累了丰富的实战经验。"),
            evalParagraph("职业素养：", "具备强烈的责任心和事业心，工作严谨细致，执行力强。善于沟通协调，具备优秀的跨部门协作能力。保持持续学习，紧跟行业发展趋势，不断提升专业素养和管理水平。"),
            evalParagraph("发展愿景：", "期望在银行信用卡业务管理领域持续深耕，发挥管理专长和专业优势，为银行创造更大价值，同时实现个人职业生涯的更高突破。")
        ]
    }]
});

// 输出
Packer.toBuffer(doc).then((buffer) => {
    fs.writeFileSync("/home/node/.openclaw/workspace/resume.docx", buffer);
    console.log("OK: resume.docx created successfully");
}).catch((err) => {
    console.error("Error:", err.message);
    console.error(err.stack);
});
