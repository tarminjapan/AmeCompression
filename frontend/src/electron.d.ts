export interface BackendStatus {
  running: boolean
  healthy: boolean
  port: number
}

export interface IElectronAPI {
  platform: string
  getApiUrl: () => Promise<string>
  getBackendStatus: () => Promise<BackendStatus>
  restartBackend: () => Promise<boolean>
  selectFile: () => Promise<string | null>
  getPathForFile: (file: File) => string
}

declare global {
  interface Window {
    electronAPI?: IElectronAPI
  }

  interface File {
    path?: string
  }
}
