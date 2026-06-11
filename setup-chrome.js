const https = require('https');
const fs = require('fs');
const path = require('path');
const AdmZip = require('adm-zip');

const CHROME_VERSION = '149.0.7827.22';
const CHROME_URL = `https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip`;
const CACHE_DIR = path.join(process.env.HOME || '/home/node', '.cache/puppeteer/chrome');
const ZIP_PATH = path.join(CACHE_DIR, 'chrome-linux64.zip');
const EXTRACT_DIR = path.join(CACHE_DIR, `linux-${CHROME_VERSION}`);

async function download(url, dest) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(dest);
    const request = https.get(url, (response) => {
      if (response.statusCode === 302 || response.statusCode === 301) {
        download(response.headers.location, dest).then(resolve).catch(reject);
        return;
      }
      const total = parseInt(response.headers['content-length'], 10);
      let downloaded = 0;
      response.on('data', (chunk) => {
        downloaded += chunk.length;
        if (total) {
          const pct = ((downloaded / total) * 100).toFixed(1);
          process.stdout.write(`\rDownloading: ${pct}% (${(downloaded/1024/1024).toFixed(1)}/${(total/1024/1024).toFixed(1)} MB)`);
        }
      });
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        console.log('\nDownload complete!');
        resolve();
      });
    });
    request.on('error', reject);
  });
}

async function main() {
  // Create cache dir
  fs.mkdirSync(CACHE_DIR, { recursive: true });
  
  // Download Chrome
  if (!fs.existsSync(ZIP_PATH) || fs.statSync(ZIP_PATH).size < 100000000) {
    console.log('Downloading Chrome for Testing...');
    await download(CHROME_URL, ZIP_PATH);
  } else {
    console.log('Chrome zip already exists');
  }
  
  // Extract
  console.log('Extracting...');
  fs.mkdirSync(EXTRACT_DIR, { recursive: true });
  const zip = new AdmZip(ZIP_PATH);
  zip.extractAllTo(EXTRACT_DIR, true);
  
  // Find chrome binary
  const chromePath = path.join(EXTRACT_DIR, 'chrome-linux64', 'chrome');
  if (fs.existsSync(chromePath)) {
    fs.chmodSync(chromePath, '755');
    console.log(`Chrome installed at: ${chromePath}`);
    console.log('SUCCESS');
  } else {
    console.log('Chrome binary not found after extraction');
    console.log('Contents:', fs.readdirSync(EXTRACT_DIR));
  }
}

main().catch(e => { console.error(e); process.exit(1); });
