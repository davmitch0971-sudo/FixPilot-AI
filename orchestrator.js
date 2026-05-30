const { exec } = require('child_process');

const scripts = [
    'solution_saas_churn.py',
    'solution_security_vulnerabilities.py',
    'solution_slow_database_queries.py'
];

function runNext(index) {
    if (index >= scripts.length) {
        console.log("--- ALL AUDITS COMPLETE: INCOME STREAM ACTIVE ---");
        return;
    }
    
    console.log(`Executing Audit: ${scripts[index]}...`);
    exec(`python3 ${scripts[index]}`, (err, stdout, stderr) => {
        if (err) console.error(`Error: ${err}`);
        console.log(stdout);
        runNext(index + 1);
    });
}

runNext(0);
