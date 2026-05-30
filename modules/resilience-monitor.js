export class ResilienceMonitor { 
  constructor(opts = {}) { 
    this.opts = opts; 
    this.registry = new Map(); 
  } 
  register(name, config) { 
    this.registry.set(name, config); 
    console.log('[ResilienceMonitor] Registered:', name); 
  }
  getStatus() {
    return Object.fromEntries(this.registry);
  }
  start() { console.log('[ResilienceMonitor] Started'); } 
}
export const slackAlerter = (url) => (msg) => console.log('Slack:', msg);
export const STATUS = { OK: 'OK', ERROR: 'ERROR' };
