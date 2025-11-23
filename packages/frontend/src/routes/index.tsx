import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'

export const Route = createFileRoute('/')({
  component: App,
})

function App() {
  const { isLoading, isError, data, error } = useQuery({
    queryKey: ['root-message'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8000/github/repos')
      if (!response.ok) throw new Error('failed to fetch root message')
      const result = await response.json()
      console.log('Repo data:', result)
      return result
    },
  })

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div>Error: {error.message}</div>

  return (
    <div className="text-center">
      <header className="min-h-screen flex flex-col items-center justify-center bg-[#282c34] text-white text-[calc(10px+2vmin)]">
        <div>
          {data && data.length > 0 ? (
            <ul>
              {data.map((repo: any) => (
                <li key={repo.id}>{repo.name}</li>
              ))}
            </ul>
          ) : (
            <p>No repositories found.</p>
          )}
        </div>
      </header>
    </div>
  )
}
