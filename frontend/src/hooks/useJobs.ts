import { useState, useEffect, useCallback } from 'react'
import { api, initializeApi } from '../services/api'
import type { Job } from '../types'

export const useJobs = (): {
  jobs: Job[]
  cancelJob: (taskId: string) => Promise<void>
} => {
  const [jobs, setJobs] = useState<Job[]>([])

  const fetchJobs = useCallback(async () => {
    try {
      await initializeApi()
      const response = await api.get<Job[]>('/jobs')
      setJobs(response.data)
    } catch (error) {
      console.error('Failed to fetch jobs', error)
    }
  }, [])

  useEffect(() => {
    void fetchJobs()
    const interval = setInterval(() => {
      void fetchJobs()
    }, 1000)
    return () => {
      clearInterval(interval)
    }
  }, [fetchJobs])

  const cancelJob = async (taskId: string): Promise<void> => {
    try {
      await api.delete<unknown>(`/jobs/${taskId}`)
      void fetchJobs()
    } catch (error) {
      console.error('Failed to cancel job', error)
    }
  }

  return { jobs, cancelJob }
}
