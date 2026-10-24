import fs from 'node:fs';
import path from 'node:path';
import { parse } from 'csv-parse/sync';
const root=path.resolve('..');
const csv=p=>parse(fs.readFileSync(path.join(root,p),'utf8'),{columns:true,skip_empty_lines:true});
const text=p=>fs.readFileSync(path.join(root,p),'utf8');
if (!fs.existsSync(path.join(root,'results/sepsis/metrics.csv'))) {
 fs.mkdirSync('public',{recursive:true});fs.copyFileSync('data/research.json','public/research.json');
 console.log('Using committed measured-results snapshot.');
} else {
const data={metrics:csv('results/sepsis/metrics.csv'),intervals:csv('results/sepsis/intervals.csv'),effects:csv('results/sepsis/paired_effects.csv'),math:text('MATHEMATICS.md'),methods:text('METHODS.md'),discussion:text('DISCUSSION.md'),report:text('results/sepsis/REPORT.md'),revision:fs.existsSync(path.join(root,'results/revision/summary.json'))?JSON.parse(text('results/revision/summary.json')):null};
fs.mkdirSync('public',{recursive:true});fs.writeFileSync('public/research.json',JSON.stringify(data));
console.log('Prepared measured results and mathematical documents.');

fs.mkdirSync('data',{recursive:true});fs.writeFileSync('data/research.json',JSON.stringify(data));
}
