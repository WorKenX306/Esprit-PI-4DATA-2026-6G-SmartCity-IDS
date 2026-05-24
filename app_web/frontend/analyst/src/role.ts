export const ROLE_CONFIG = {
  appName: 'IOTinel Analyst Console',
  brandLine: 'Always watching. Always protecting.',
  role: 'security_analyst',
  roleLabel: 'Security Analyst',
  accent: '#1D9E75',
  homePath: '/dashboard',
  redirectMap: {
    security_analyst: 'https://iotinel-analyst-ui.onrender.com/dashboard',
    data_scientist: 'https://iotinel-scientist-ui.onrender.com/monitoring',
    administrator: 'https://iotinel-admin-ui.onrender.com/dashboard',
  },
  menu: [
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/live-detection', label: 'Live Detection' },
    { path: '/batch-analysis', label: 'Batch Analysis' },
    { path: '/model-comparison', label: 'Prediction History' },
    { path: '/swagger', label: 'Swagger' },
  ],
  enabledPages: ['dashboard', 'live-detection', 'batch-analysis', 'model-comparison', 'swagger'],
} as const;

export type SupportedRole = keyof typeof ROLE_CONFIG.redirectMap;
