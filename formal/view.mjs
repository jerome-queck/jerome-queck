export const title = 'One publisher. Legacy upgrade and steady refresh.';
export const state = v => {
  if (v.phase[1] === 'published') return 'Snapshot published';
  if (v.phase[1] === 'failed') return v.remote[10] === 3 ? 'Legacy snapshot retained' : 'Complete snapshot retained';
  if (v.phase[1] === 'rejected') return 'Stale push rejected';
  if (v.phase[1] === 'copy') return `Copied ${v.progress[1]} of 15 payloads`;
  return v.remote[10] === 3 ? 'Legacy snapshot, 11 files' : 'Complete snapshot, 15 files';
};
export const step = (action, from) => {
  if (action === 'Fail' && from.phase[1] === 'copy') return null;
  return ({Ready: 'Collect and render', Copy: 'Copy next payload', Fail: 'Refresh fails', Push: 'Push snapshot'})[action] ?? action;
};
