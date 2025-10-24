const fs = require('fs');
const path = require('path');

const appPath = path.join(__dirname, '../app');
const backupPath = path.join(__dirname, '../app-example');

if (fs.existsSync(appPath)) {
  fs.renameSync(appPath, backupPath);
  console.log('/app moved to /app-example.');
}

fs.mkdirSync(appPath);
console.log('New /app directory created.');

fs.writeFileSync(path.join(appPath, 'index.tsx'), '');
fs.writeFileSync(path.join(appPath, '_layout.tsx'), '');
console.log('app/index.tsx created.');
console.log('app/_layout.tsx created.');