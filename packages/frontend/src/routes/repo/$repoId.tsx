import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export const Route = createFileRoute('/repo/$repoId')({
  component: RouteComponent,
})

function RouteComponent() {
  const { repoId } = Route.useParams()

  const { isLoading, isError, data, error } = useQuery({
    queryKey: ['repo', repoId],
    queryFn: async () => {
      const response = await fetch(
        `http://localhost:8000/github/repo/${repoId}`,
      )
      if (!response.ok) throw new Error('Failed to fetch repo')
      return response.json()
    },
  })

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div>Error: {error.message}</div>

  return (
    <div className="w-full">
      <div className="flex flex-row gap-2 p-1">
        <Card className="w-full">
          <CardHeader>
            <CardTitle>Pull Requests</CardTitle>
          </CardHeader>
          <CardContent>{data.pulls.length}</CardContent>
        </Card>
        <Card className="w-full">
          <CardHeader>
            <CardTitle>Issues</CardTitle>
          </CardHeader>
          <CardContent>{data.issues.length}</CardContent>
        </Card>
      </div>
    </div>
  )
}
