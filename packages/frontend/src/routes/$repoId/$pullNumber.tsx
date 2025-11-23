import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'

export const Route = createFileRoute('/$repoId/$pullNumber')({
  component: RouteComponent,
})

function RouteComponent() {
  const { repoId, pullNumber } = Route.useParams()

  const { isLoading, isError, data, error } = useQuery({
    queryKey: ['pullRequest', pullNumber],
    queryFn: async () => {
      const response = await fetch(
        `http://localhost:8000/github/repo/${repoId}/pull/${pullNumber}`,
      )
      const data = await response.json()
      return data
    },
  })

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div>Error: {error.message}</div>

  console.log(data)

  return <div>{pullNumber}</div>
}
