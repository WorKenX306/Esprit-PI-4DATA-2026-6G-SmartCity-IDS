export const ROLE_CONFIG = {
  appName: 'IOTinel Scientist Console',
  brandLine: 'Always watching. Always protecting.',
  role: 'data_scientist',
  roleLabel: 'Data Scientist',
  accent: '#185FA5',
  homePath: '/monitoring',
  redirectMap: {
    security_analyst: 'https://iotinel-analyst-ui.onrender.com/dashboard',
    data_scientist: 'https://iotinel-scientist-ui.onrender.com/monitoring',
    administrator: 'https://iotinel-admin-ui.onrender.com/dashboard',
  },
  menu: [
    { path: '/monitoring', label: 'Monitoring' },
    { path: '/model-comparison', label: 'Model Comparison' },
    { path: '/training', label: 'Training' },
    { path: '/drift-metrics', label: 'Drift Metrics' },
    { path: '/shap-explanations', label: 'SHAP Explanations' },
    { path: '/swagger', label: 'Swagger' },
  ],
  enabledPages: ['monitoring', 'model-comparison', 'training', 'drift-metrics', 'shap-explanations', 'swagger'],
} as const;

export type SupportedRole = keyof typeof ROLE_CONFIG.redirectMap;
