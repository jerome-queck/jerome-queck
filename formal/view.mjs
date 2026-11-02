export const title = 'Profile snapshot publication';
export const state = v => {
  if (v.phase[1] === 'published') return 'Snapshot published';
  if (v.phase[1] === 'failed') return 'Refresh failed';
  if (v.phase[1] === 'rejected') return 'Stale push rejected';
  if (v.phase[1] === 'copy') return `Copied ${v.progress[1]} of 11 payloads`;
  return 'Previous snapshot';
};
export const step = action => ({Ready: 'Collect and render', Copy: 'Copy next payload', Fail: 'Refresh fails', Push: 'Push snapshot'})[action] ?? action;
