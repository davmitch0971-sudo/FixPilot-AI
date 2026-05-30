const { spawn } = require('child_process');

function startGodheadArchitect() {
  console.log("Initializing Godhead Architect core...");
  const loop = spawn('node', ['run-loop.cjs'], { detached: true, stdio: 'inherit' });
  loop.on('close', (code) => {
    console.log(`Core process exited with code ${code}, restarting...`);
    startGodheadArchitect();
  });
}

startGodheadArchitect();
