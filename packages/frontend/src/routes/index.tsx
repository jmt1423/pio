import { createFileRoute, Link } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import { Button } from '@/components/ui/button'
import { ModeToggle } from '@/components/mode-toggle'

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
      <header className="min-h-screen flex flex-col items-center justify-center">
        <div className="fixed top-2 right-2">
          <ModeToggle />
        </div>
        <div>
          {data && data.length > 0 ? (
            <ul>
              {data.map((repo: any) => (
                <li key={repo.id}>
                  <Button variant={'link'}>
                    <Link
                      to={`/repo/$repoId`}
                      params={{ repoId: `${repo.full_name}` }}
                    >
                      {repo.full_name}
                    </Link>
                  </Button>
                </li>
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
