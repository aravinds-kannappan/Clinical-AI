import fs from 'node:fs';
import path from 'node:path';
import {parse} from 'csv-parse/sync';
const root=path.resolve('..');
const text=p=>fs.readFileSync(path.join(root,p),'utf8');
const csv=p=>parse(text(p),{columns:true,skip_empty_lines:true});
fs.mkdirSync('public',{recursive:true});
if(!fs.existsSync(path.join(root,'results/revision/summary.json'))){fs.copyFileSync('data/research.json','public/research.json');console.log('Using committed measured-results snapshot.');}
else {
 const data={paired:{discrimination:csv('results/consent-comparison/discrimination.csv'),policies:csv('results/consent-comparison/policies.csv'),summary:JSON.parse(text('results/consent-comparison/summary.json'))},summary:JSON.parse(text('results/revision/summary.json')),metrics:csv('results/revision/metrics.csv'),frontiers:csv('results/revision/frontiers.csv'),certificates:csv('results/revision/certificates.csv'),consent:csv('results/revision/consent.csv'),selected:csv('results/revision-audit/selected_policies.csv'),math:text('MATHEMATICS.md'),methods:text('METHODS.md'),discussion:text('DISCUSSION.md'),report:text('results/revision/REPORT.md')};
 fs.mkdirSync('data',{recursive:true});fs.writeFileSync('data/research.json',JSON.stringify(data));fs.writeFileSync('public/research.json',JSON.stringify(data));
 console.log('Prepared full-release results, consent analyses and mathematical documents.');
}
