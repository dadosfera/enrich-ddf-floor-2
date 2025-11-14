#!/usr/bin/env node
// scripts/add-node-options.js
// Add NODE_OPTIONS to package.json scripts

const fs = require('fs');
const path = process.argv[2] || 'package.json';

if (!fs.existsSync(path)) {
    console.log(`package.json not found: ${path}`);
    process.exit(0);
}

const packageJson = JSON.parse(fs.readFileSync(path, 'utf8'));

if (!packageJson.scripts) {
    console.log('No scripts section found');
    process.exit(0);
}

let modified = false;
const NODE_MEMORY = '2048';

// Scripts that need NODE_OPTIONS
const scriptsToUpdate = Object.keys(packageJson.scripts);

scriptsToUpdate.forEach(scriptName => {
    const script = packageJson.scripts[scriptName];

    // Skip if already has NODE_OPTIONS
    if (script.includes('NODE_OPTIONS')) {
        return;
    }

    // Skip if it's not a Node.js command
    if (!script.match(/\b(node|npm|vite|jest|tsc|webpack|next|nuxt|rollup|esbuild)\b/)) {
        return;
    }

    // Add NODE_OPTIONS
    packageJson.scripts[scriptName] = `NODE_OPTIONS=--max-old-space-size=${NODE_MEMORY} ${script}`;
    modified = true;
});

if (modified) {
    // Create backup
    fs.writeFileSync(`${path}.bak.${Date.now()}`, fs.readFileSync(path));

    // Write updated package.json
    fs.writeFileSync(path, JSON.stringify(packageJson, null, 2) + '\n');
    console.log(`✅ NODE_OPTIONS added to package.json (backup: ${path}.bak.*)`);
} else {
    console.log('✅ NODE_OPTIONS already present or not needed');
}
