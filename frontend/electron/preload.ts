import { contextBridge, ipcRenderer, webUtils } from 'electron'

contextBridge.exposeInMainWorld('electronAPI', {
  platform: process.platform,
  getApiUrl: () => ipcRenderer.invoke('get-api-url'),
  getBackendStatus: () => ipcRenderer.invoke('get-backend-status'),
  restartBackend: () => ipcRenderer.invoke('restart-backend'),
  selectFile: () => ipcRenderer.invoke('select-file'),
  getPathForFile: (file: File) => {
    const utils = webUtils as { getPathForFile?: (f: File) => string }
    return utils.getPathForFile?.(file)
  },
})
