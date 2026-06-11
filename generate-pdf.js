const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  // 读取HTML文件
  const html = fs.readFileSync('resume.html', 'utf-8');
  
  // 启动浏览器
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  // 设置HTML内容
  await page.setContent(html, { waitUntil: 'networkidle' });
  
  // 生成PDF
  await page.pdf({
    path: 'resume.pdf',
    format: 'A4',
    printBackground: true,
    margin: {
      top: '10mm',
      right: '10mm',
      bottom: '10mm',
      left: '10mm'
    }
  });
  
  await browser.close();
  console.log('PDF生成完成：resume.pdf');
})();
